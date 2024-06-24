from pathlib import Path
import moviepy.editor as mp
import os
import threading
import multiprocessing
import time
from concurrent.futures import ThreadPoolExecutor
import asyncio
import pandas as pd



def vidtoWav(videoFile,vidLocation,wavDestinaiton):
    #generates the filepath for the video
    videoPath = os.path.join(vidLocation,videoFile)
    #stem allows for data transformation save
    audioPath = os.path.join(wavDestinaiton,f"{Path(videoFile).stem}.wav")
    print(f"Beginning extraction of: {videoPath}")
   
    try:
        videoClip = mp.VideoFileClip(videoPath)
        videoClip.audio.write_audiofile(audioPath)
        print(f"Extraction complete for: {videoFile}")
    except Exception as e:
        print(f"Failed extraction of: {videoClip}")
   
def serialExtract():
    Path("serAudio").mkdir(parents=True, exist_ok=True)
    vidFolder = "serVids"
    videos = [vid for vid in os.listdir(vidFolder) if vid.endswith(".mp4")]
    for v in videos:
        vidtoWav(v,"serVids","serAudio")



def multiprocessingExtract():
    videos =[]
    Path("mulAudio").mkdir(parents=True,exist_ok=True)
    for vid in os.listdir("parVids"):
        if vid.endswith(".mp4"):
            videos.append(vid)
    coreCount = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(processes=coreCount)
    jobs = []
    for vid in videos:
        jobs.append((vid,"parVids","mulAudio"))
    pool.starmap(vidtoWav,jobs)
    pool.close()
    pool.join()


async def concurrentWrapper(videoFile, vidLocation, wavDestination, loop, executor):
    await loop.run_in_executor(executor, vidtoWav, videoFile, vidLocation, wavDestination)

async def concurrentExtraction(videoFiles, vidLocation, wavDestination):
    Path(wavDestination).mkdir(exist_ok=True, parents=True)
    loop = asyncio.get_running_loop()
    executor = ThreadPoolExecutor()
    jobs = []
    for videoFile in videoFiles:
        job = concurrentWrapper(videoFile, vidLocation, wavDestination, loop, executor)
        jobs.append(job)
    await asyncio.gather(*jobs)

def conRunner():
    vidFolder = "parVids"
    wavDestination = "conAudio"
    videoFiles = []
    for vid in os.listdir(vidFolder):
        if vid.endswith(".mp4"):
            videoFiles.append(vid)
    asyncio.run(concurrentExtraction(videoFiles, vidFolder, wavDestination))

def threadExtraction():
    Path("threadAudio").mkdir(exist_ok=True,parents=True)
    vidFolder = "parVids"
    wavDestination = "threadAudio"
    videoFiles = []
    for vid in os.listdir(vidFolder):
        if vid.endswith(".mp4"):
            videoFiles.append(vid)
    threads = []
    for vid in videoFiles:
        thread = threading.Thread(target=vidtoWav, args=(vid,vidFolder,wavDestination))
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()


def audioRunner():
    times = {
        "Serial":0,
        "Multi":0,
        "Threads":0,
        "Concurrent":0,

    }
    print("\nMultiprocessing ")
    mStartTime = time.perf_counter()
    multiprocessingExtract()
    mEndTime = time.perf_counter()
    mTimeTaken = mEndTime - mStartTime
    print("\nSerial")
    sStartTime = time.perf_counter()
    serialExtract()
    sEndTime = time.perf_counter()
    sTimeTaken = sEndTime - sStartTime
    print("\Concurrent ")
    cStartTime = time.perf_counter()
    conRunner()
    cEndTime = time.perf_counter()
    cTimeTaken = cEndTime - cStartTime
    print("\Threads ")
    tStartTime = time.perf_counter()
    threadExtraction()
    tEndTime = time.perf_counter()
    tTimeTaken = tEndTime - tStartTime
   
    times["Serial"] = sTimeTaken
    times["Multi"] = mTimeTaken
    times["Concurrent"] = cTimeTaken
    times["Threads"] = tTimeTaken
    
    df = pd.DataFrame(list(times.items()),columns=["Type","Time"])
    dfSorted = df.sort_values(by="Time",ascending=True)
    print("\n\n")
    print(dfSorted)
if __name__ == '__main__':   
    audioRunner()