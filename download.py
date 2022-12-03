from pytube import YouTube

youtube_video_url = "https://www.youtube.com/watch?v=yYUIt6FtIB4"
youtube_video = YouTube(youtube_video_url)

streams = youtube_video.streams.filter(only_audio=True)
stream = streams.first()

stream.download(filename='fed_meeting.mp4')