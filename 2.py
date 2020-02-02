from SpectatorAgent import SpectatorAgent

if __name__ == "__main__":
    od = SpectatorAgent("agent000@jix.im", "agent000??")
    od.postaviPrimatela("agent003@jix.im")
    od.setVideoSource("input_videos/2.mp4")
    od.start()
    od.Detect()