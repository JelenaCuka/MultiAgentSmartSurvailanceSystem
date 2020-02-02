from spade.agent import Agent
from spade.behaviour import CyclicBehaviour, OneShotBehaviour
import numpy as np
import spade,datetime,time
from datetime import timedelta
from datetime import datetime
import facebook
import FBToken
def POSTINTERVAL():
    return 30#seconds, current value 120 -> every 2 minutes posts to Facebook
CONST_POSTINTERVAL = POSTINTERVAL()
class ListenerAgent(Agent):

    def startListening(self):
        igraTemplate = spade.template.Template(
            metadata={"ontology": "MASSS"}
        )
        listenBehaviour = self.ListenInbox()
        self.add_behaviour(listenBehaviour, igraTemplate)

    def FormatBehaviour(self):
        self.add_behaviour(self.FormatMessage(), spade.template.Template(
            metadata={"ontology": "MASSS"}
        ))

    def PostBehaviour(self):
        self.add_behaviour(self.PostToFacebook(), spade.template.Template(
            metadata={"ontology": "MASSS"}
        ))

    class FormatMessage(OneShotBehaviour):
        async def on_start(self):
            self.messagesTemplate = ["10% discount next 3 hours (ps lots of free samples) (<10 people)",
                          "If I had to describe atmosfere right now, I would say Relax and Chill (>=10,<20 people)",
                          "Wow , it's a bit crowded atmosphere at the moment, it might be thanks to huge number of our loyal customers, you are the best, thanks! (>=20 people)"]
        async def run(self):
            print(f"formating message based on number of objects in system")

            if(self.get("sumCount") < 10 ):
                self.set("messageToPost", self.messagesTemplate[0] + "\n\n Number of people in system: "+str(int(round(self.get("sumCount"))))+ "\n" )
            if (self.get("sumCount") >= 10 ) and ( self.get("sumCount") < 20) :
                self.set("messageToPost", self.messagesTemplate[1] + "\n\n Number of people in system: "+str(int(round(self.get("sumCount"))))+  "\n" )
            if(self.get("sumCount") >= 20 ):
                self.set("messageToPost", self.messagesTemplate[2] + "\n\n Number of people in system: "+str(int(round(self.get("sumCount"))))+ "\n" )
            self.agent.PostBehaviour()


    class PostToFacebook(OneShotBehaviour):
        async def run(self):
            print("posting to facebook =>" + self.get("messageToPost") )
            graph = facebook.GraphAPI(access_token=FBToken.Access_Token, version="2.12")
            graph.put_object(
                parent_object=FBToken.PageId,
                connection_name="feed",
                message= self.get("messageToPost")+"\n\n " + datetime.now().strftime("%A, %d. %B %Y. (%H:%M:%S)")+"\n\n MAS MAS Team")
               #link="https://www.foi.unizg.hr/")


    class ListenInbox(CyclicBehaviour):
        async def on_start(self):
            print("listening start")
            self.agentIme = self.get("agentIme")
            self.objectCounterSum = 0
            self.startTime = datetime.now() + timedelta(days=0, seconds=0, microseconds=0)
            self.wantedInterval = timedelta(days=0, seconds=1*CONST_POSTINTERVAL, microseconds=0)
            self.ZeroMessagesReceived = True

        async def run(self):
            time.sleep(1)
            print("listening...")
            msg = await self.receive(timeout=10)
            if msg:
                print(f"[{self.agent.name}]: Received message: {msg.body}")
                try:
                    valueToAdd = float(np.float64(msg.body))
                    self.objectCounterSum = self.objectCounterSum + valueToAdd
                    self.ZeroMessagesReceived = False
                except:
                    print("Casting error")

            print("new Sum = " + str(self.objectCounterSum))

            # svakih 60 sekundi aka 60 minuta
            self.timeNow = datetime.now() + timedelta(days=0, seconds=0, microseconds=0)
            if self.timeNow - self.startTime >= self.wantedInterval:
                self.set("sumCount", self.objectCounterSum)
                self.objectCounterSum = 0
                self.startTime = datetime.now() + timedelta(days=0, seconds=0, microseconds=0)
                if self.ZeroMessagesReceived == False:
                    self.agent.FormatBehaviour()
                self.ZeroMessagesReceived = True

        async def on_end(self):
            print("listening behaviour end")

    async def setup(self):
        print("ListenerAgent:" + self.name + " Agent Starting!")
        self.set("agentIme", self.name)

if __name__ == '__main__':
    listener = ListenerAgent("agent003@jix.im", "agent003??")
    listener.start()
    listener.startListening()