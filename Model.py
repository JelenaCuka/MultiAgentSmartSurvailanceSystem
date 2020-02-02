class Model:
   __instance = None
   @staticmethod
   def getInstance():
      if Model.__instance == None:
         Model()
      return Model.__instance

   def __init__(self):
      if Model.__instance != None:
         raise Exception("This class is a singleton!")
      else:
         Model.__instance = self
      self.set_name('ssd_mobilenet_v2_coco_2018_03_29')
      #self.set_name('faster_rcnn_inception_v2_coco_2018_01_28')

   def get_name(self):
       return self.__name
   def set_name(self, name):
       self.__name = name

