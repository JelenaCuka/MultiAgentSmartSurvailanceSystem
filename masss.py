from SpectatorAgent import SpectatorAgent

class SampleApp:
    def __init__(self):
        self.od = SpectatorAgent("aeae100@jix.im", "100dva")
        self.od.postaviPrimatela("agent003@jix.im")
        self.od.setVideoSource("input_videos/1.mp4")
        self.od.start()
        self.od.Detect()

        self.od2 = SpectatorAgent("agent000@jix.im", "agent000??")
        self.od2.postaviPrimatela("agent003@jix.im")
        self.od2.setVideoSource("input_videos/2.mp4")
        self.od2.start()
        self.od2.Detect()

        self.od3 = SpectatorAgent("agent002@jix.im", "agent002??")
        self.od3.postaviPrimatela("agent003@jix.im")
        self.od3.setVideoSource("input_videos/3.mp4")
        self.od3.start()
        self.od3.Detect()


if __name__ == "__main__":
    app = SampleApp()

