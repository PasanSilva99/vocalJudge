import crepe
import librosa
import numpy as np
import resampy
import soundfile as sf
import matplotlib
import matplotlib.pyplot as plt
from scipy.io import wavfile
from math import log2, pow

def checkMatchingChords(chord1, chord2):
    # C major – C E G
    c_majour = ["C", "E", "G"]
    # C# major – C# E# G#
    cs_majour = ["C#", "E#", "G#"]
    # D major – D F# A
    major = ["D", "F#", "A"]
    # Eb major – Eb G Bb
    major = ["Eb", "G", "Bb"]
    # E major – E G# B
    major = ["E", "G#", "B"]
    # F major – F A C
    major = ["F", "A", "C"]
    # F# major – F# A# C#
    major = ["F#", "A#", "C#"]
    # G major – G B D
    major = ["G", "B", "D"]
    # Ab major – Ab C Eb
    major = ["Ab", "C", "Eb"]
    # A major – A C# E
    major = ["A", "C#", "E"]
    # Bb major – Bb D F
    major = ["Bb", "D", "F"]
    # B major – B D# F#
    major = ["B", "D#", "F#"]


def GetPitch(file):
    # Load in librosa's example audio file at its native sampling rate
    x, sr_orig = librosa.load(file)

    # x is now a 1-d numpy array, with `sr_orig` audio samples per second

    # We can resample this to any sampling rate we like, say 16000 Hz
    y_low = resampy.resample(x, sr_orig, 16000)

    sf.write("Resample.wav", y_low, 16000, 'PCM_24')

    sr, audio = wavfile.read('Resample.wav')
    return crepe.predict(audio, sr, viterbi=True)


print("Detecting pitch for Vocal Track")
time, frequency, confidence, activation = GetPitch('T2Vocal.wav')

print("Detecting pitch for Instrumental Track")
itime, ifrequency, iconfidence, iactivation = GetPitch('T2Instrumental.wav')
print("Pitch Detection Complete")

print("Plotting detected data")
plt.plot(itime, ifrequency, label="Instruments")
plt.plot(time, frequency, label="Vocals")
plt.show()
plt.plot(itime, ifrequency, label="Instruments")
plt.plot(time, frequency, label="Vocals")
plt.savefig('DetectedPitchComparison.png')

plt.clf()
plt.cla()

plt.plot(itime, ifrequency, label="Instruments")
plt.show()
plt.plot(itime, ifrequency, label="Instruments")
plt.savefig('DetectedPitchInstrumental.png')

plt.clf()
plt.cla()

plt.plot(time, frequency, label="Vocals")
plt.show()
plt.plot(time, frequency, label="Vocals")
plt.savefig('DetectedPitchVocals.png')
print("Plot Data Saved")

print("Beginning Comparison")

# Get the silences
filteredFreq = np.where(frequency < 60, 0, frequency)
# Testcase
for t, If, Vf, ff in zip(time, ifrequency, frequency, filteredFreq):
    print(t, ",", If, ",", Vf, ",", ff, "\n")

plt.plot(itime, ifrequency, label="Instruments")
plt.plot(time, filteredFreq, label="FilteredVocals")
plt.show()
plt.plot(itime, ifrequency, label="Instruments")
plt.plot(time, filteredFreq, label="FilteredVocals")
plt.savefig('DetectedPitchVocals.png')
print("Plot Data Saved")

A4 = 440
C0 = A4 * pow(2, -4.75)
name = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]


def notation(freq):
    h = round(12 * log2(freq / C0))
    octave = h // 12
    n = h % 12
    return name[n] + str(octave) + " " + str(h)


def midiNote(Freq):
    return 12 * (log2(Freq / 440.00)) + 69


pitchNotation = []
instrumentalNotation = []
midiNotation = []

for fr in filteredFreq:
    if fr > 0:
        pitchNotation.append(notation(fr))
    else:
        pitchNotation.append("Silence")

for fr in ifrequency:
    if fr > 0:
        instrumentalNotation.append(notation(fr))
    else:
        instrumentalNotation.append("Silence")

for frq in filteredFreq:
    if frq > 0:
        midiNotation.append(midiNote(frq))
    else:
        midiNotation.append(0)

for t, If, ff, pn, ipn, mn in zip(time, ifrequency, filteredFreq, pitchNotation, instrumentalNotation, midiNotation):
    print(t, ",", If, ",", ff, ",", pn, ",", ipn, ",", mn, "\n")


def GetTheDifference(t, insfreq, filfreq, pitchNotation, instrumentalNotation):
    diff_matching_notes = []
    diff = []
    print("Musical Notation Comparison")
    for iF, fF, pN, iN in zip(insfreq, filfreq, pitchNotation, instrumentalNotation):

        if iF - fF is not 0:
            if pN == iN:
                print("Matching Notes: ", iF - fF)
                diff_matching_notes.append(iF-fF)
                diff.append(iF-fF)

    return diff


Grading = GetTheDifference(time, ifrequency, filteredFreq, pitchNotation, instrumentalNotation)

avgGrade = sum(Grading)/ len(Grading)

print("Average Grading For Matching Notes:", (100-avgGrade), "%")