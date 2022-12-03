import sounddevice as sd
import wavio as wv
import whisper
import multiprocessing
import os
import redis

r = redis.Redis(host='localhost', port=6379, db=0)

def record():
    freq = 44100
    duration = 5

    print('Recording')
    
    while True:
        # Start recorder with the given values of duration and sample frequency
        # PTL Note: I had to change the channels value in the original code to fix a bug
        recording = sd.rec(int(duration * freq), samplerate=freq, channels=1)

        # Record audio for the given number of seconds
        sd.wait()

        # Convert the NumPy array to audio file
        wv.write("recording0.wav", recording, freq, sampwidth=2)

def transcribe(model):

    while True:
        audio = whisper.load_audio("recording0.wav")
        audio = whisper.pad_or_trim(audio)
        
        mel = whisper.log_mel_spectrogram(audio).to(model.device)
        options = whisper.DecodingOptions(language= 'en', fp16=False)
        result = whisper.decode(model, mel, options)
        if result.text != '.':
            print(result)
            r.publish('textanalyzer', result.text)


def loadfile(directory):
    content = {}

    for file in os.scandir(directory):
        with open(file) as f:
            filename = os.path.split(file)[1]
            contents = f.read()
            content[filename] = contents
    return content

if __name__=="__main__":

    model = whisper.load_model("base")

    to_mic, to_whisper = multiprocessing.Pipe()

    mic = multiprocessing.Process(target=record)
    whisp = multiprocessing.Process(target=transcribe, args = (model,))
    
    mic.start()
    whisp.start()

    mic.join()
    whisp.join()

