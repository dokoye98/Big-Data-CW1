import speech_recognition as sr

Rec = sr.Recognizer()

with sr.AudioFile('2-Minute Neuroscience Autism.wav') as source:
    
    audio = Rec.record(source)
    text = Rec.recognize_google(audio)
print(text)
