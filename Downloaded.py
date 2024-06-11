from pytube import YouTube
from Logger import log_download as log
import threading 


def download(url):
    try:
        yt = YouTube(url)
        stream = yt.streams.get_highest_resolution()
        print(f"Downloading vid:{yt.title}")
        stream.download(output_path="par_vids")
        print(f"complete: {yt.title}")
        log(url,'True')
    except Exception as e:
        print(f"Error {e}")
        log(url,'False')


def parallel(urls):
    semaphore = threading.Semaphore(8)
    threads = []
    def wrapper(url):
        with semaphore:
            download(url)
    for url in urls:
        thread = threading.Thread(target=wrapper,args=(url,))
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