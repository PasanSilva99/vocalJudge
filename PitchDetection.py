import crepe
import librosa
import numpy as np
import resampy
import soundfile as sf
import matplotlib
import matplotlib.pyplot as plt
from scipy.io import wavfile


def GetPitch(file):
    # Load in librosa's example audio file at its native sampling rate
    x, sr_orig = librosa.load(file)

    # x is now a 1-d numpy array, with `sr_orig` audio samples per second

    # We can resample this to any sampling rate we like, say 16000 Hz
    y_low = resampy.resample(x, sr_orig, 16000)

    sf.write("Resample.wav", y_low, 16000, 'PCM_24')

    sr, audio = wavfile.read('Resample.wav')
    return crepe.predict(audio, sr, viterbi=True)


time, frequency, confidence, activation = GetPitch('T2Vocal.wav')

for t, f, c in zip(time, frequency, confidence):
    print(t, ",", f, ",", c, "\n")

plt.plot(time, frequency)
plt.show()

itime, ifrequency, iconfidence, iactivation = GetPitch('T2Instrumental.wav')

for it, fi, ic in zip(itime, ifrequency, iconfidence):
    print(it, ",", fi, ",", ic, "\n")

plt.plot(itime, ifrequency)
plt.show()
