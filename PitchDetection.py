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


# print("Detecting pitch for Vocal Track")
time, frequency, confidence, activation = GetPitch('Instrumentals.wav')

# print("Detecting pitch for Instrumental Track")
itime, ifrequency, iconfidence, iactivation = GetPitch('Vocals.wav')


# print("Pitch Detection Complete")


def SavePlots(i_time, i_frequency, _time, _frequency):
    px = 1 / plt.rcParams['figure.dpi']  # pixel in inches

    # Lets set the Style of the Plot
    COLOR = 'white'
    plt.rcParams['text.color'] = COLOR
    plt.rcParams['axes.labelcolor'] = COLOR
    plt.rcParams['xtick.color'] = COLOR
    plt.rcParams['ytick.color'] = COLOR

    plt.rcParams['axes.facecolor'] = 'black'
    plt.rcParams['figure.facecolor'] = 'black'

    # print("Plotting detected data")

    # Instrumentals Track
    plt.figure(figsize=(600 * px, 200 * px))
    plt.plot(i_time, i_frequency, label="Instruments", color='#9E2AFE')
    plt.savefig('InstrumentalTrack.png')

    plt.clf()
    plt.cla()

    # Vocals Track
    plt.figure(figsize=(600 * px, 200 * px))
    plt.plot(_time, _frequency, label="Vocals", color='#4B74EC')
    plt.savefig('VocalTrack.png')

    plt.clf()
    plt.cla()

    # Comparison
    plt.figure(figsize=(1200 * px, 200 * px))
    plt.plot(i_time, i_frequency, label="Instruments", color='#9E2AFE')
    plt.plot(_time, _frequency, label="Vocals", color='#4B74EC')
    plt.savefig('PitchComparison.png')

    plt.clf()
    plt.cla()

    # print("Plot Data Saved")


SavePlots(itime, ifrequency, time, frequency)


# print("Beginning Comparison")


def Filter(freq):
    return np.where(freq < 60, 0, freq)  # bound rate


# Get the silences
filteredFreq = Filter(frequency)
# Testcase
for t, If, Vf, ff in zip(time, ifrequency, frequency, filteredFreq):
    outst = t, ",", If, ",", Vf, ",", ff, "\n"
    # print(outst)

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
    oust = t, ",", If, ",", ff, ",", pn, ",", ipn, ",", mn, "\n"
    # print(oust)


def GetTheDifference(t, insfreq, vocfreq_raw, pitchNotation, instrumentalNotation):
    vocfreq = Filter(vocfreq_raw)
    diff_matching_notes = []
    diff = []
    matching_chords = []
    diff_matching_chords = []
    diff_pitch_out = []
    pitch_outs = []
    perfectMatches = []
    rangeouts = []

    # print("Musical Notation Comparison")
    for iF, fF, pN, iN in zip(insfreq, vocfreq, pitchNotation, instrumentalNotation):

        if iF - fF != 0 and fF != 0:  # Skipp all frequancies which is silance or the grading will have negative impact
            if pN == iN:
                # Exact Note
                # print("Matching Notes: ", iF - fF)
                diff_matching_notes.append(abs(iF - fF))
                diff.append(abs(iF - fF))
            else:
                if checkMatchingChords(pN, iN):
                    # pitch was out of range but it is a musical chord
                    # print("Matching Chord: ", pN, midiNote(fF), iN, midiNote(iF))
                    matching_chords.append([pN, iN])
                    diff_matching_chords.append(abs(midiNote(fF) - midiNote(iF)))
                else:
                    try:
                        # Pitch was out of range
                        # print("Pitch-out: ", pN, midiNote(fF), iN, midiNote(iF))
                        pitch_outs.append([pN, iN])
                        diff_pitch_out.append(abs(midiNote(fF) - midiNote(iF)))
                    except Exception as e:
                        # Some error on pitch
                        # print("Ranged out")
                        # diff_pitch_out.append(abs(iF - fF))
                        rangeouts.append(1)

        else:
            # Pitch Matched Perfectly
            perfectMatches.append(1)

    totalPitchOuts = 0
    totalMatchedNotes = 0
    totalMatchingChords = 0
    totalPerfectMatches = 0
    ## Silences are filtered from the above statements
    # so there is no need to grade silences. that can be instrumentals only
    if len(diff_pitch_out) != 0:
        totalPitchOuts = len(diff_pitch_out) / len(vocfreq)
    if len(diff_matching_notes) != 0:
        totalMatchedNotes = sum(diff_matching_notes) / len(diff_matching_notes)
    if len(diff_matching_chords) != 0:
        totalMatchingChords = sum(diff_matching_chords) / len(diff_matching_chords)
    if len(perfectMatches) != 0:
        totalPerfectMatches = sum(perfectMatches) / len(perfectMatches)

    gradeFile = open("PitchGrade.txt", "a")
    gradeFile.write(str(totalPitchOuts) + "%" + "\n")
    gradeFile.write(str(totalMatchedNotes) + "%" + "\n")
    gradeFile.write(str(totalMatchingChords) + "%" + "\n")
    gradeFile.write(str(totalPerfectMatches) + "%" + "\n")
    gradeFile.close()

    file = open("log.txt", "a")
    file.write("Pitch Analysis" + "\n")

    print("Perfect Matches AVG: ", totalPerfectMatches)  # The deference
    file.write("Perfect Matches AVG: " + str(totalPerfectMatches) + "\n")
    print("Matched Notes AVG: ", totalMatchedNotes)
    file.write("Matched Notes AVG: " + str(totalMatchedNotes) + "\n")
    print("Matching Chords AVG: ", totalMatchingChords)
    file.write("Matching Chords AVG: " + str(totalMatchingChords) + "\n")
    print("Pitchouts AVG: ", totalPitchOuts)
    file.write("Pitchouts AVG: " + str(totalPitchOuts) + "\n")

    print("Perfect match Grade : ", ((10 - totalPerfectMatches) if 0 < totalPerfectMatches <= 10 else 0))
    print("Matched Note Grade : ", ((10 - totalMatchedNotes) if 0 < totalMatchedNotes <= 10 else 0))
    print("Matching Chord Grade : ", ((10 - totalMatchingChords) if 0 < totalMatchingChords <= 10 else 0))
    print("Pitchout Grade : ", (totalPitchOuts if 0 < totalPitchOuts < 10 else 10))
    file.close()
    # lets get the positive score  (if the avd of each value is > 10 that means there is a problem or that is a silence or noice)
    positiveScore = ((10 - totalPerfectMatches) if 0 < totalPerfectMatches <= 10 else 0) + (
        (10 - totalMatchedNotes) if 0 < totalMatchedNotes <= 10 else 0) + (
                        (10 - totalMatchingChords) if 0 < totalMatchingChords <= 10 else 0) - (
                        totalPitchOuts if 0 < totalPitchOuts < 10 else 10)
    multiplier = 0  # This is to to get a equal mark for each section
    # if the user sand without perfect matches but it matched the actual musical notes -
    # if the user sang without chords,
    # likewise, this will determine the multipler for singers sections
    if totalPerfectMatches > 0:
        multiplier += 1
    if totalMatchedNotes > 0:
        multiplier += 1
    if totalMatchingChords > 0:
        multiplier += 1
    if multiplier > 3:
        multiplier = 3
    if multiplier == 0:
        multiplier = 1
    #print("Mul : ", multiplier)
    grade = positiveScore / (
                10 * multiplier) * 100  # Total is 300 as 100 for Perfect Matches, 100 for Exact note matches, 100 for matching chrords
    return grade


# Lets get the grading for the input data
Grading = GetTheDifference(time, ifrequency, filteredFreq, pitchNotation, instrumentalNotation)

print("Average Grading:", Grading, "%")
file = open("log.txt", "a")
file.write("Average Grading:" + str(Grading) + "%" + "\n")
file.close()

file = open("PitchGrade.txt", "a")
file.write(str(Grading) + "%" + "\n")
file.close()
