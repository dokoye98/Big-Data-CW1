from textblob import TextBlob
import os
from pathlib import Path
import threading
import time

def textSentiment(textFile, outputDestination, inputLocation):
    inputPath = os.path.join(inputLocation, textFile)
    outputPath = os.path.join(outputDestination, f"{Path(textFile).stem}_analysed.txt")
    try:
        with open(inputPath, "r") as file:
            text = file.read()
        blob = TextBlob(text)
        senti = blob.sentiment
        pola = senti.polarity
        subject = senti.subjectivity

        with open(outputPath, "w") as analysed:
            analysed.write(f"Text: {text}\n")
            analysed.write(f"Polarity: {pola}\n")
            analysed.write(f"Sentiment: {senti}\n")
            analysed.write(f"Subjectivity: {subject}\n")
        print(f"Finished analysis of: {textFile}")
    except Exception as e:
        print(f"Failed analysis of: {textFile}")

def serialAnalysis():
    Path("serAnalysis").mkdir(exist_ok=True,parents=True)
    for txt in os.listdir("serText"):
        if txt.endswith(".txt"):
            textSentiment(txt,"serAnalysis","serText")

def threadedAnalysis():
    Path("parAnalysis").mkdir(exist_ok=True, parents=True)
    textFolder = "parText"
    outputFolder = "parAnalysis"
    textFiles = []
    for txt in os.listdir(textFolder):
        if txt.endswith(".txt"):
            textFiles.append(txt)
    threads = []
    for textFile in textFiles:
        thread = threading.Thread(target=textSentiment, args=(textFile, outputFolder, textFolder))
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()

def textAnalysisRunner():
    print("\nSerial")
    serialStartTime = time.perf_counter()
    serialAnalysis()
    serialEndTime = time.perf_counter()
    sTimeTaken = serialEndTime - serialStartTime
    print("\nThread") 
    threadedStartTime = time.perf_counter()
    threadedAnalysis()
    threadedEndTime = time.perf_counter()
    tTimeTaken = threadedEndTime - threadedStartTime
    print(f"Threaded Analysis Time: {tTimeTaken} ")
    print(f"Serial Analysis Time: {sTimeTaken} ")
    
