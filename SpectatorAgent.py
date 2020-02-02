from Model import Model
import numpy as np
import tensorflow as tf
import cv2
from PIL import ImageFont
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as vis_util
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour, OneShotBehaviour
import spade,datetime,time
from datetime import timedelta
from datetime import datetime
def SENDING_MESSAGE_INTERVAL():
    return 20#seconds, current value 20 -> every 30 seconds sends Number of People to ListenerAgent
CONST_SENDING_MESSAGE_INTERVAL = SENDING_MESSAGE_INTERVAL()

class SpectatorAgent(Agent):
    def resetCounters(self):
        self.detectionCounter = 0
        self.sumOfPositiveDetections = 0

    def setVideoSource(self,video):
        if video == "":
            self.videoSource = 0
            self.set("cameraOff",False)
        else:
            self.videoSource = video
            self.set("cameraOff", True)

    def getAverageNumberOfDetections(self):
        if self.detectionCounter == 0 or self.sumOfPositiveDetections == 0:
            averageNumberOfDetections = 0
        else:
            averageNumberOfDetections = self.sumOfPositiveDetections / self.detectionCounter
        self.resetCounters()
        return averageNumberOfDetections

    def loadModel(self):
        self.detection_graph = tf.Graph()
        with self.detection_graph.as_default():
            od_graph_def = tf.compat.v1.GraphDef()
            print(self.PATH_TO_CKPT)
            with tf.io.gfile.GFile(self.PATH_TO_CKPT, 'rb') as fid:
                serialized_graph = fid.read()
                od_graph_def.ParseFromString(serialized_graph)
                tf.import_graph_def(od_graph_def, name='')

    def loadLabelMap(self):
        self.label_map = label_map_util.load_labelmap( self.PATH_TO_LABELS)
        self.categories = label_map_util.convert_label_map_to_categories(
            self.label_map, max_num_classes=self.NUM_CLASSES, use_display_name=True)
        self.category_index = label_map_util.create_category_index(self.categories)

    def configureModel(self):
        self.loadModel()
        self.loadLabelMap()

    def model_setup(self):
        self.MODEL_NAME = self.model.get_name()
        self.PATH_TO_CKPT = 'models/'+ self.MODEL_NAME + '/frozen_inference_graph.pb'  #
        self.MODEL_FILE = self.MODEL_NAME + '.tar.gz'
        self.NUM_CLASSES = 90
        self.PATH_TO_LABELS = 'models/'+ self.MODEL_NAME + '/mscoco_complete_label_map.pbtxt'
        self.configureModel()

    def filter_boxes_by_categories_and_score(self,min_score, boxes, scores, classes, categories):
        """Return boxes with a confidence >= `min_score`"""
        n = len(classes)
        idxs = []
        for i in range(n):
            if classes[i] in categories and scores[i] >= min_score:
                idxs.append(i)

        filtered_boxes = boxes[idxs, ...]
        filtered_scores = scores[idxs, ...]
        filtered_classes = classes[idxs, ...]
        return filtered_boxes, filtered_scores, filtered_classes

    class detectOcjectsFromCamera(OneShotBehaviour):#CyclicBehaviour
        async def on_start(self):
            print("-----------------started detector-="+self.agent.name)
            self.agent.model_setup()
            if self.agent.videoSource != None :
                self.cap = cv2.VideoCapture(self.agent.videoSource)
            else:
                self.cap = cv2.VideoCapture(0)
            msg = spade.message.Message(
                to=self.get("primateljAdresa"),
                body="Detection Started >"+self.agent.name,
                metadata={"ontology": "MASSS"})
            await self.send(msg)
            print(f"[{self.agent.name}]: Poslana poruka: {msg.body}")
            self.startTime = datetime.now() + timedelta(days=0, seconds=0, microseconds=0)
            self.wantedInterval = timedelta(days=0, seconds=1*CONST_SENDING_MESSAGE_INTERVAL, microseconds=0)
            self.frame_counter = 0

        async def run(self):
            with self.agent.detection_graph.as_default():
                with tf.compat.v1.Session(graph=self.agent.detection_graph) as sess:
                    while True:
                        # Read frame from camera
                        ret, image_np = self.cap.read()

                        #reset video on end
                        self.frame_counter += 1
                        # If the last frame is reached, reset the capture and the frame_counter
                        if self.get("cameraOff"):
                            if self.frame_counter == self.cap.get(cv2.CAP_PROP_FRAME_COUNT):
                                self.frame_counter = 0  # Or whatever as long as it is the same as next line
                                self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

                        # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
                        image_np_expanded = np.expand_dims(image_np, axis=0)
                        # Extract image tensor
                        image_tensor = self.agent.detection_graph.get_tensor_by_name('image_tensor:0')
                        # Extract detection boxes
                        boxes = self.agent.detection_graph.get_tensor_by_name('detection_boxes:0')
                        # Extract detection scores
                        scores = self.agent.detection_graph.get_tensor_by_name('detection_scores:0')
                        # Extract detection classes
                        classes = self.agent.detection_graph.get_tensor_by_name('detection_classes:0')
                        # Extract number of detections
                        num_detections = self.agent.detection_graph.get_tensor_by_name(
                            'num_detections:0')

                        # Actual detection.
                        (boxes, scores, classes, num_detections) = sess.run(
                            [boxes, scores, classes, num_detections],
                            feed_dict={image_tensor: image_np_expanded})
                        # Visualization of the results of a detection.
                        boxes = np.squeeze(boxes)
                        scores = np.squeeze(scores)
                        classes = np.squeeze(classes)
                        #apply filter to results - selecting only class person with id 1
                        (boxes, scores, classes) = self.agent.filter_boxes_by_categories_and_score(0.2, boxes, scores, classes, [1])#person id is 1
                        numberOfDetectedObjects = np.squeeze(scores).size

                        if numberOfDetectedObjects > 0:
                            self.agent.detectionCounter = self.agent.detectionCounter + 1
                            self.agent.sumOfPositiveDetections = self.agent.sumOfPositiveDetections + numberOfDetectedObjects

                        self.timeNow = datetime.now() + timedelta(days=0, seconds=0, microseconds=0)
                        if self.timeNow - self.startTime >= self.wantedInterval :

                            msg = spade.message.Message(
                                to=self.get("primateljAdresa"),
                                body=str(self.agent.getAverageNumberOfDetections()),  # check
                                metadata={"ontology": "MASSS"})
                            await self.send(msg)
                            print(self.agent.name + " Message sent:  " + msg.body)
                            self.startTime = datetime.now() + timedelta(days=0, seconds=0, microseconds=0)

                        vis_util.visualize_boxes_and_labels_on_image_array(
                            image_np,
                            boxes,
                            classes.astype(np.int32),
                            scores,
                            self.agent.category_index,
                            use_normalized_coordinates=True,
                            line_thickness=8)

                        cv2.imshow('Camera detection -' + self.agent.name, cv2.resize(image_np, (800, 600)))

                        if cv2.waitKey(25) & 0xFF == ord('q'):
                            cv2.destroyAllWindows()
                            self.agent.stop()
                            self.kill()
                            break


        async def on_end(self):
            print(f"[{self.agent.name}]: Detect behaviour stop.")


    def postaviPrimatela(self,primateljAdresa):
        self.set("primateljAdresa",primateljAdresa)

    def Detect(self):
        self.add_behaviour(self.detectOcjectsFromCamera(), spade.template.Template(
            metadata={"ontology": "MASSS"}
        ))
        self.detectOcjectsFromCamera()

    async def setup(self):
        print("Agent "+self.name+" starting")
        ImageFont.truetype('Arial.ttf', 30)
        self.model = Model.getInstance()
        self.model_setup()
        self.detectionCounter = 0
        self.sumOfPositiveDetections = 0

