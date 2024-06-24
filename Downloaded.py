from pytube import YouTube
from Logger import log_download as log
import threading 
import Reader
import time

def download(url,proType,outputLocation):
    try:
        yt = YouTube(url)
        stream = yt.streams.get_highest_resolution()
        print(f"Downloading vid:{yt.title}")
        stream.download(output_path=outputLocation)
        print(f"complete: {yt.title}")
        log(url,'True',proType)
    except Exception as e:
        print(f"Error {e}")
        log(url,'False',proType)


def parallel(urls):
    semaphore = threading.Semaphore(12)
    threads = []
    def wrapper(url,proType,outputLocation):
        with semaphore:
            download(url,proType,outputLocation)
    for url in urls:
        thread = threading.Thread(target=wrapper,args=(url,"Parallel","parVids"))
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()




def serial(urls):
    
       for url in urls:
            download(url,"Serial","serVids")

def downloadRunner():
    urls = Reader.url_reader()
    print("Threads ")
    tStartTime = time.perf_counter()
    parallel(urls)
    tEndTime = time.perf_counter()
    tTimeTaken = tEndTime - tStartTime
    print("\nSerial")
    sStartTime = time.perf_counter()
    serial(urls)
    sEndTime = time.perf_counter()
    sTimeTaken = sEndTime - sStartTime
    print(f"The serial time is: {sTimeTaken}")
    print(f"\nThe parallel time taken is: {tTimeTaken}")
