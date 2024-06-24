from Reader import url_reader
import time
from Downloaded import downloadRunner
from AudioExtraction import audioRunner
from Transcrption import transcritpRunner
from EmotionExtraction import emotionRunner
from TextAnalysis import textAnalysisRunner
from Translations import translationRunner



def main():

    bigStartTime = time.perf_counter()
    print("Download Starting\n")
    downloadRunner()
    print("\nAudio extraction Starting\n")
    audioRunner()
    print("\ntranscription Starting\n")
    transcritpRunner()
    print("\ntranslation Starting\n")
    translationRunner()
    print("\nfeeling checks Starting\n")
    emotionRunner()
    print("\nAnalysis Starting\n")
    textAnalysisRunner()
    print("\ntranslation Starting\n")
    translationRunner()
    bigEndTime = time.perf_counter()
    runtime = bigEndTime -bigStartTime
    print(f"Runtime = {runtime}")
    
#Runtime without transcription is 2-3 minutes
#with it its 19-20 minutes  (before refactor)
#after refactor 10 - 11minutes 

if __name__=='__main__':
   main()