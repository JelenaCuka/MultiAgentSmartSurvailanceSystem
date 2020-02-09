# MultiAgentSmartSurvailanceSystem

MultiAgentSmartSurvailanceSystem
------------------------------------------------------------------------------------------------------------------------------

This system includes agents who track and detect objects (people,person) on camera/video input. 
After detection they also count number of detected objects and in defined time intervals they send average count info to ListenerAgent. 
ListenerAgents listens messages from all SpectatorAgents in System. In defined time intervals Agent Formats message and posts message to Facebook page. Content of message is result of total number of detected objects in system (sum of information from all agents in system).

------------------------------------------------------------------------------------------------------------------------------
Architecture

![arh1](https://user-images.githubusercontent.com/26230313/73700647-64c14980-46e7-11ea-8819-a1b09a42df42.png)

![arh2](https://user-images.githubusercontent.com/26230313/73700651-6be85780-46e7-11ea-83b6-7182a3113d03.png)

![arh3_2](https://user-images.githubusercontent.com/26230313/73700663-76a2ec80-46e7-11ea-8a1b-6a58978b29f9.png)

------------------------------------------------------------------------------------------------------------------------------
SpectatorAgents

![spectatorsLog](https://user-images.githubusercontent.com/26230313/73700511-0ac08400-46e7-11ea-94e4-bc817cb6578f.png)

SpectatorAgents detections visualizations

![spectators](https://user-images.githubusercontent.com/26230313/73700523-14e28280-46e7-11ea-98dd-9f100db35d98.png)
-----------------------------------------------------------------------------------------------------------------------------
ListenerAgent
![ListenerLog](https://user-images.githubusercontent.com/26230313/73700447-dd73d600-46e6-11ea-9cc4-f27918604b52.png)

![ListenerFBObjaveSve](https://user-images.githubusercontent.com/26230313/73700402-c2a16180-46e6-11ea-9013-fb13cfe3c115.png)
-----------------------------------------------------------------------------------------------------------------------------
-
-main classes are ListenerAgent and SpectatorAgent

-file FBToken is not uploaded
-and also videos are not uploaded (bcz size)
-used trained models of neural networks are not uploaded
-also several dependencies need to be installed to use system spade, tensorflow, opencv, facebook-sdk,..

-following files represent different running versions (different videos):

--------------------------------------------------------------------------------------

-masss2.py,masss3.py,masss4.py,-start 3 agents with MOT challenge videos

-masss5.py, -camera

-masss.py, -camera -videos with bad detections

-1.py,2.py,3.py -start single agent

-----------------------------------------------------------------------------------------------------------------------------


