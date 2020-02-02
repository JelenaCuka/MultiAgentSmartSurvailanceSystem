from SpectatorAgent import SpectatorAgent

if __name__ == "__main__":
    od = SpectatorAgent("aeae100@jix.im", "100dva")
    od.postaviPrimatela("agent003@jix.im")
    od.setVideoSource("input_videos/1.mp4")
    od.start()
    od.Detect()