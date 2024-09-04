import os
import speech_recognition as sr
from pathlib import Path
import multiprocessing 
import time


def wavTranscription(wavFile, textDestination,wavDestination):
    recognizer = sr.Recognizer()
    wavPath = os.path.join(wavDestination,wavFile)
    textPath = os.path.join(textDestination,f"{Path(wavFile).stem}.txt")
    try:
       
        with sr.AudioFile(wavPath) as source:
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.record(source )
            #instead of google use whisper no need to import it 
            text = recognizer.recognize_whisper(audio)
            #print(text)

            with open(textPath, "w",encoding="utf-8") as textFile:
                textFile.write(text)
            print(f"Successful transcription of: {wavFile}")
            
    except Exception as e:
        print(f"Failed transcription: {wavFile} because of {e}")


def processParameters(wavFile,textDestination,wavDestination):
    wavTranscription(wavFile, textDestination, wavDestination)


def multiprocessingTranscription():
    Path("parText").mkdir(exist_ok=True, parents=True)
    wavFolder = "mulAudio"
    outputFolder = "parText"
    wavFiles = [wav for wav in os.listdir(wavFolder) if wav.endswith(".wav")]
    ##List comprehension be used to reduce loops hopefully reducing runtime
    ##reduction of overhead(reducing processes ) in this case instead of creating pool variable and assigning actions just perform
    ## creation and action at the same time
    coreCount = min(len(wavFiles),multiprocessing.cpu_count())#automatically controls num of process = num of audio files
    with multiprocessing.Pool(processes=coreCount) as pool:
        jobs = [(wavFile, outputFolder,wavFolder) for wavFile in wavFiles]
        pool.starmap(processParameters,jobs)
    


def serialTranscription():
    Path("serText").mkdir(exist_ok=True,parents=True)
    wavFolder = "serAudio"
    wavFiles =[wav for wav in os.listdir(wavFolder) if wav.endswith(".wav")]
    
    for wav in wavFiles:
        wavTranscription(wav,"serText","serAudio")



def transcritpRunner():
    print("Multiprocessing transcription")
    multiprocessingStartTime = time.perf_counter()
    multiprocessingTranscription()
    multiprocessingEndTime = time.perf_counter()
    mTimeTaken = multiprocessingEndTime - multiprocessingStartTime
    print("Serial transcription")
    sStartTime = time.perf_counter()
    serialTranscription()
    sEndTime = time.perf_counter()
    sTimeTaken = sEndTime - sStartTime
    print(f"Serial Transcription Time: {sTimeTaken} ")
    print(f"Multiprocessing Transcription Time: {mTimeTaken}")

  
