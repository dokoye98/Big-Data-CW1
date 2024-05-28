from pytube import YouTube
import time
import threading
import logging


vids = []
with open('video_url.txt','r') as file:
    for line in file:
        vids.append(line.strip())



def serial(urls):
    for url in urls:
        yt = YouTube(url)
        stream = yt.streams.get_audio_only()
        print(f"Downloading video: {yt.title}")
        stream.download(output_path="video_output")
        print(f"Download completed: {yt.title}")


if __name__ =='__main__':
    serialTime = time.time()
    serial(vids)
    endStime = time.time()
    timetaken = endStime - serialTime
    print(f"Time taken ={timetaken}")
