import librosa
file = open("log.txt", "a")
file.write("Tempo Analysis" + "\n")
file.close()


def DetectTempo(music_track):
    file = open("log.txt", "a")
    file.write("Tempo Analysis for " + str(music_track) + "\n")
    file.close()
    x, sr = librosa.load(music_track)
    tempo, beat_times = librosa.beat.beat_track(x, sr=sr, start_bpm=60, units='time')
    print(tempo)
    return tempo


print("Vocal track")
tempo = DetectTempo("Vocals.wav")
print("Instrumental track")
vtempo = DetectTempo("Instrumentals.wav")
tempo_difference = tempo - vtempo
tempo_grading = -1
print("Tempo Difference: ", tempo_difference)

if -100 <= tempo_difference <= 100:
    if tempo_difference < 0:
        tempo_difference = tempo_difference * (-1)
    tempo_grading = 100 - tempo_difference

print("Grade on Tempo Balancing : ", tempo_grading, "%")

file = open("TempoGrade.txt", "a")
file.write(str(vtempo)+ "\n")
file.write(str(tempo) + "\n")
file.write(str(tempo_grading) + "\n")
file.close()
