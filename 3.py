from SpectatorAgent import SpectatorAgent

if __name__ == "__main__":
    od = SpectatorAgent("agent002@jix.im", "agent002??")
    od.postaviPrimatela("agent003@jix.im")
    od.setVideoSource("input_videos/3.mp4")
    od.start()
    od.Detect()