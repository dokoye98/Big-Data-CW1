from Reader import url_reader
import time
from Downloaded import serial, parallel


def main():
    urls = url_reader()
    serialStartTime = time.time()
    serial(urls)
    serialEndTime = time.time()
    sTimetaken = serialEndTime - serialStartTime
    parallelStartTime = time.time()
    parallel(urls)
    parallelEndTime = time.time()
    ptimetake = parallelEndTime - parallelStartTime

    print(f"Serial download time: {sTimetaken}")
    print(f"Parellel time take: {ptimetake}")
    

if __name__=='__main__':
   main()