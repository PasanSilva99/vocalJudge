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
    d_major = ["D", "F#", "A"]
    # Eb major – Eb G Bb
    Eb_major = ["Eb", "G", "Bb"]
    # E major – E G# B
    E_major = ["E", "G#", "B"]
    # F major – F A C
    F_major = ["F", "A", "C"]
    # F# major – F# A# C#
    Fs_major = ["F#", "A#", "C#"]
    # G major – G B D
    G_major = ["G", "B", "D"]
    # Ab major – Ab C Eb
    Ab_major = ["Ab", "C", "Eb"]
    # A major – A C# E
    A_major = ["A", "C#", "E"]
    # Bb major – Bb D F
    Bb_major = ["Bb", "D", "F"]
    # B major – B D# F#
    B_major = ["B", "D#", "F#"]
    # C minor (Cm). C - Eb - G

    C_minor = ["B", "D#", "F#"]
    # C# minor (C#m). C# - E - G#
    cs_minor = ["B", "D#", "F#"]
    # D minor (Dm). D - F -A
    d_minor = ["D", "F", "A"]
    # Eb minor (Ebm). Eb - Gb - Bb
    Eb_minor = ["Eb", "Gb", "Bb"]
    # E minor (Em). E - G - B
    E_minor = ["E", "G", "B"]
    # F minor (Fm). F - Ab - C
    F_minor = ["F", "Ab", "C"]
    # F# minor (F#m). F# - A - C#
    Fs_minor = ["F#", "A", "C#"]
    # G minor (Gm). G - Bb - D
    G_minor = ["G", "Bb", "D"]
    # Ab minor (Abm). Ab - Cb - Eb
    Ab_minor = ["Ab", "Cb", "Eb"]
    # A minor (Am). A - C - E
    A_minor = ["Ab", "Cb", "Eb"]
    # Bb minor (Bbm). Bb - Db - F
    Bb_minor = ["Bb", "Db", "F"]
    # B minor (Bm). B - D - F#
    B_minor = ["B", "D", "F#"]

    # C diminished (Cdim). C - Eb - Gb
    C_dim = ["C", "Eb", "Gb"]
    # C# diminished (C#dim). C# - E - G
    Cs_dim = ["C#", "E", "G"]
    # D diminished (Ddim). D - F - Ab
    D_dim = ["D", "F", "Ab"]
    # D# diminished (D#dim). D# - F# - A
    Ds_dim = ["D#", "F#", "A"]
    # E diminished (Edim). E - G - Bb
    E_dim = ["E", "G", "Bb"]
    # F diminished (Fdim). F - Ab - Cb
    F_dim = ["F", "Ab", "Cb"]
    # F# diminished (F#dim). F# - A - C
    Fs_dim = ["F#", "A", "C"]
    # G diminished (Gdim). G - Bb - Db
    G_dim = ["G", "Bb", "Db"]
    # G# diminished (G#dim). G# - B - D
    Gs_dim = ["G#", "B", "D"]
    # A diminished (Adim). A - C - Eb
    A_dim = ["A", "C", "Eb"]
    # A# diminished (A#dim). A# - C# - E
    As_dim = ["A#", "C#", "E"]
    # B diminished (Bdim). B - D - F
    B_dim = ["B", "D", "F"]

    # C augmented (Caug). C - E - G#
    C_aug = ["C", "E", "G#"]
    # C# augmented (C#aug). C# - E# - G##
    Cs_aug = ["C#", "E#", "G#"]
    # D augmented (Daug). D - F# - A#
    D_aug = ["D", "F#", "A#"]
    # D# augmented (D#aug). D# - F## - A##
    Ds_aug = ["D#", "F#", "A#"]
    # E augmented (Eaug). E - G# - B#
    E_aug = ["E#", "G#", "B#"]
    # F augmented (Faug). F - A - C#
    F_aug = ["F", "A", "C#"]
    # F# augmented (F#aug). F# - A# - C##
    Fs_aug = ["F#", "A#", "C#"]
    # G augmented (Gaug). G - B - D#
    G_aug = ["G", "B", "D#"]
    # G# augmented (G#aug). G# - B# - D##
    Gs_aug = ["G#", "B#", "D#"]
    # A augmented (Aaug). A - C# - E#
    A_aug = ["A", "C#", "E#"]
    # A# augmented (A#aug). A# - C## - E##
    As_aug = ["A#", "C#", "E#"]
    # B augmented (Baug). B - D# - F## 
    B_aug = ["B", "D#", "F#"]

    stadard_chords = [c_majour, cs_majour, d_major, Eb_major, E_major, F_major, Fs_major,
                      G_major, Ab_major, A_major, Bb_major, B_major,
                      C_minor, cs_minor, d_minor, Eb_minor, E_minor, F_minor, Fs_minor,
                      G_minor, Ab_minor, A_minor, Bb_minor, B_minor,
                      C_dim, Cs_dim, D_dim, Ds_dim, E_dim, F_dim, Fs_dim, G_dim, Gs_dim,
                      A_dim, As_dim, B_dim,
                      C_aug, Cs_aug, D_aug, Ds_aug, E_aug, F_aug, Fs_aug, G_aug, Gs_aug,
                      A_aug, As_aug, B_aug]

    for chord in stadard_chords:
        if chord1 in chord and chord2 in chord:
            print("Matching chord")
            return True

    return False


def GetPitch(file):
    # Load in librosa's example audio file at its native sampling rate
    x, sr_orig = librosa.load(file)

    # x is now a 1-d numpy array, with `sr_orig` audio samples per second

    # We can resample this to any sampling rate we like, say 16000 Hz
    y_low = resampy.resample(x, sr_orig, 16000)

    sf.write("Resample.wav", y_low, 16000, 'PCM_24')

    sr, audio = wavfile.read('Resample.wav')
    return crepe.predict(audio, sr, viterbi=True, step_size=500)


print("Detecting pitch for Vocal Track")
time, frequency, confidence, activation = GetPitch('T2Vocal.wav')

print("Detecting pitch for Instrumental Track")
itime, ifrequency, iconfidence, iactivation = GetPitch('T2Instrumental.wav')
print("Pitch Detection Complete")


def SavePlots(i_time, i_frequency, _time, _frequency):
    print("Plotting detected data")
    plt.plot(i_time, i_frequency, label="Instruments")
    plt.plot(_time, _frequency, label="Vocals")
    plt.show()
    plt.plot(i_time, i_frequency, label="Instruments")
    plt.plot(_time, _frequency, label="Vocals")
    plt.savefig('DetectedPitchComparison.png')

    plt.clf()
    plt.cla()

    plt.plot(i_time, i_frequency, label="Instruments")
    plt.show()
    plt.plot(i_time, i_frequency, label="Instruments")
    plt.savefig('DetectedPitchInstrumental.png')

    plt.clf()
    plt.cla()

    plt.plot(_time, _frequency, label="Vocals")
    plt.show()
    plt.plot(_time, _frequency, label="Vocals")
    plt.savefig('DetectedPitchVocals.png')
    print("Plot Data Saved")


SavePlots(itime, ifrequency, time, frequency)

print("Beginning Comparison")


def Filter(freq):
    return np.where(freq < 60, 0, freq)


# Get the silences
filteredFreq = Filter(frequency)
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


def GetNotation(freq):
    Notation = []

    for v in freq:
        if v > 0:
            Notation.append(notation(v))
        else:
            Notation.append("Silence")

    return Notation


def GetMidiNotation(freq):
    MidiNotes = []
    for v in freq:
        if v > 0:
            MidiNotes.append(midiNote(v))
        else:
            MidiNotes.append(0)
    return MidiNotes


pitchNotation = GetNotation(filteredFreq)
instrumentalNotation = GetNotation(ifrequency)
midiNotation = GetMidiNotation(filteredFreq)

for t, If, ff, pn, ipn, mn in zip(time, ifrequency, filteredFreq, pitchNotation, instrumentalNotation, midiNotation):
    print(t, ",", If, ",", ff, ",", pn, ",", ipn, ",", mn, "\n")


def GetTheDifference(t, insfreq, vocfreq_raw, pitchNotation, instrumentalNotation):
    vocfreq = Filter(vocfreq_raw)
    diff_matching_notes = []
    diff = []
    matching_chords = []
    pitch_outs = []
    print("Musical Notation Comparison")
    for iF, fF, pN, iN in zip(insfreq, vocfreq, pitchNotation, instrumentalNotation):

        if iF - fF != 0:
            if pN == iN:
                print("Matching Notes: ", iF - fF)
                diff_matching_notes.append(iF - fF)
                diff.append(iF - fF)
            else:
                if checkMatchingChords(pN, iN):
                    print("Matching Chord: ", pN, midiNote(fF), iN, midiNote(iF))
                    matching_chords.append([pN, iN])
                else:
                    print("Pitch-out: ", pN, midiNote(fF), iN, midiNote(iF))
                    pitch_outs.append([pN, iN])
        else:
            print("Perfect Match: ", fF)
    return diff


Grading = GetTheDifference(time, ifrequency, filteredFreq, pitchNotation, instrumentalNotation)

avgGrade = sum(Grading) / len(Grading)

print("Average Grading For Matching Notes:", (100 - avgGrade), "%")
