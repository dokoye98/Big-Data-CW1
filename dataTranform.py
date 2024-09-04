from pathlib import Path
import moviepy.editor as mp
import os
import speech_recognition as sr
import threading
import time
failedList = []
passedList = []
def vidToWav():
    vidFolder = "par_vids"
    Path("wavFolder").mkdir(parents=True,exist_ok=True)
    videos = []
    for vid in os.listdir(vidFolder):
        if vid.endswith('.mp4'):
            videos.append(vid) 

    for vid in videos:
        audio_path = os.path.join("wavFolder",f"{Path(vid).stem}.wav")
        video_path = os.path.join(vidFolder,vid)
        try:
           clips = mp.VideoFileClip(video_path)
           clips.audio.write_audiofile(audio_path)
           print(f"Succesful mp4 to wav: {audio_path}")
        except Exception as e:
           print(f"Unsuccesful mp4 to wav: {audio_path}")
        finally:
            if 'clips' in locals():
                clips.reader.close()
                clips.audio.reader.close_proc()


def wavTranscription(wavFile):
    wavFolder = "wavFolder"
    recognizer = sr.Recognizer()
    wavPath = os.path.join(wavFolder,wavFile)
    textPath = os.path.join("textFolder",f"{Path(wavFile).stem}.txt")
    try:
        with sr.AudioFile(wavPath) as source:
            audio = recognizer.record(source)
            text = recognizer.recognize_google(audio)
            with open(textPath, "w") as textFile:
                textFile.write(text)
            print(f"Successful transcription of: {wavPath}")
            passedList.append(wavPath)
    except Exception as e:
        failedList.append(wavPath)


def threadedTranscription():
    Path("textFolder").mkdir(exist_ok=True,parents=True)
    wavFolder = "wavFolder"
    wavFiles = []
    for wavFile in os.listdir(wavFolder):
        if wavFile.endswith(".wav"):
            wavFiles.append(wavFile)
    threads = []
    for wavFile in wavFiles:
        thread = threading.Thread(target=wavTranscription,args=(wavFile,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()
   


#vidToWav()

threadedTranscription()
print(len(failedList))
print(len(passedList))



