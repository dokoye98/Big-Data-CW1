import spacy,nltk
from nrclex import NRCLex
nlp = spacy.load('en_core_web_sm')
import os
from pathlib import Path
import threading
import time



def setUp():
    ##limit function calls when running unrelated methods 
    nltk.download('punkt')
def emotionExtract(textFile, inputLocation,outputDestination):
    inputPath = os.path.join(inputLocation, textFile)
    outputPath = os.path.join(outputDestination, f"{Path(textFile).stem}_translated.txt")
    try:
        ##encoding for ust to be careful
        with open(inputPath,"r",encoding="utf-8") as file:
            text = file.read()
        emotion = NRCLex(text)
        with open(outputPath,"w",encoding="utf-8") as feelings:
            feelings.write(f"Feelings for {textFile}\n")
            ##instead of writing emotions.affect_frequencies iterate for readability 
            for emotions, freq in emotion.affect_frequencies.items():
                feelings.write(f"{emotions}: {freq}\n")
        print(f"Feeling extraction for {textFile} complete")
    except Exception as e:
        print(f"Failed emotion exctaction of {textFile} cause of {e}")


def threadedEmotions():
    Path("parEmotion").mkdir(exist_ok=True,parents=True)
    setUp()
    textFiles = []
    
    for txt in os.listdir("parText"):
        if txt.endswith(".txt"):
            textFiles.append(txt)
    threads = []
    for txt in textFiles:
        thread = threading.Thread(target=emotionExtract, args=(txt,"parText","parEmotion"))
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()

def serialEmotions():
    Path("serEmotions").mkdir(exist_ok=True, parents=True)
    setUp()
    textFiles = []
    for txt in os.listdir("serText"):
        if txt.endswith(".txt"):
            textFiles.append(txt)
    for txt in textFiles:
        emotionExtract(txt,"serText","serEmotions")

def emotionRunner():
    print("Threaded")
    threadedStartTime = time.perf_counter()
    threadedEmotions()
    threadedEndTime = time.perf_counter()
    tTimeTaken = threadedEndTime - threadedStartTime
    print("Serial")
    serialSTime = time.perf_counter()
    serialEmotions()
    serialEndTime = time.perf_counter()
    sTimeTaken = serialEndTime - serialSTime
    print(f"Serial Extraction Time: {sTimeTaken}")
    print(f"Thread time: {tTimeTaken}")