from pytube import YouTube
import time
import threading
import logging as lg


lg.basicConfig(filename='thread_download_log.txt',level=lg.INFO,
             format='Timestamp: %(asctime)s, URL: %(message)s, Download: %(status)s')

mut = threading.Lock()
vids = []
with open('video_url.txt','r') as file:
    for line in file:
        vids.append(line.strip())

def download(url):
    try:

        yt = YouTube(url)
        stream = yt.streams.get_highest_resolution()
        print(f"Downloading vid:{yt.title}")
        stream.download(output_path="par_vids")
        print(f"complete: {yt.title}")
        print(x)
        x+=1
        with mut:
            lg.info(f"{url}",extra={"status":"True"})
    except Exception as e:
        print(f"Error {e}")
        with mut:
            lg.error(f"{url}",extra={"status":"False"})


def threaded(urls):
    threads = []
    for url in urls:
        thread = threading.Thread(target=download,args=(url,))
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()

def serial(urls):
    for url in urls:
        yt = YouTube(url)
        stream = yt.streams.get_highest_resolution()
        print(f"Downloading video: {yt.title}")
        stream.download(output_path="ser_vids")
        print(f"Download completed: {yt.title}")


if __name__ =='__main__':
    sSTime = time.perf_counter()
    serial(vids)
    eSTime = time.perf_counter()
    sTimetaken = eSTime - sSTime
    pSTime = time.perf_counter()
    threaded(vids)
    pETime = time.perf_counter()
    ptimetake = pETime - pSTime
  
    print(f"parallel time taken: {ptimetake}")
    print(f"serial time taken: {sTimetaken}")

