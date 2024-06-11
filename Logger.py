import logging as lg
import threading


mut = threading.Lock()

lg.basicConfig(filename='download_log.txt',level=lg.INFO,
               format='Timestamp: %(asctime)s, URL: %(url)s, Downloaded: %(download_status)s')

def log_download(url,status):
    with mut:
        lg.info('', extra={'url': url, 'download_status': status})