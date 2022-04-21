import librosa


def DetectTempo(music_track):
    x, sr = librosa.load('T2Instrumental.wav')
    tempo, beat_times = librosa.beat.beat_track(x, sr=sr, start_bpm=60, units='time')

    print("Instrumental track")
    print(tempo)
    return tempo


tempo = DetectTempo("T1Instrumental.wav")
vtempo = DetectTempo("T1Vocal.wav")
tempo_difference = tempo - vtempo
tempo_grading = -1
print("Tempo Difference: ", tempo_difference)

if -100 <= tempo_difference <= 100:
    if tempo_difference < 0:
        tempo_difference = tempo_difference * (-1)
    tempo_grading = 100 - tempo_difference

print("Grade on Tempo Balancing : ", tempo_grading, "%")
