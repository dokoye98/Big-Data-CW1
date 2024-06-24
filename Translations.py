from deep_translator import GoogleTranslator
import os
from pathlib import Path
import threading
import time


def textTranslation(textFile, inputLocation, outputDestination):
    inputPath = os.path.join(inputLocation, textFile)
    outputPath = os.path.join(outputDestination, f"{Path(textFile).stem}_translated.txt")
    
    try:
        translate =  GoogleTranslator(source='auto', target='pt')
        with open(inputPath, "r") as file:
            text = file.read()
            translated_text =translate.translate(text)
        with open(outputPath, "w") as translated:
            translated.write(f"Title: {textFile}\n")
            translated.write(translated_text)
        print(f"Finished translating: {textFile}")
    except Exception as e:
        print(f"Failed translation of: {textFile}")
        

def threadedTranslation():
    threads = []
    texts = []
    Path("parTranslate").mkdir(exist_ok=True, parents=True)
    for text in os.listdir("parText"):
        if text.endswith(".txt"):
            texts.append(text)
    for text in texts:
        thread = threading.Thread(target=textTranslation, args=(text, "parText", "parTranslate"))
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()

def serialTranslation():
    
    Path("serTranslation").mkdir(exist_ok=True,parents=True)
    textFiles = []
    output = "serTranslation"
    input = "serText"
    for txt in os.listdir("serText"):
        if txt.endswith(".txt"):
            textFiles.append(txt)
    for txt in textFiles:
        textTranslation(txt,input,output)

def translationRunner():
    print("\nSerial")
    serialStartTime = time.perf_counter()
    serialTranslation()
    serialEndTime = time.perf_counter()
    sTimeTaken = serialEndTime - serialStartTime
    print("\nThread") 
    threadedStartTime = time.perf_counter()
    threadedTranslation()
    threadedEndTime = time.perf_counter()
    tTimeTaken = threadedEndTime - threadedStartTime
    print(f"Threaded Time: {tTimeTaken} ")
    print(f"Serial Time: {sTimeTaken} ")