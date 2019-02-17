from music21 import chord, harmony, interval
import json

def transpose(ch, key):
  # transpose the given chord (wrt given key) to the C major scale
  return ch.transpose(interval.Interval(-key.normalOrder[0]))

def tomusic21(ch):
  # flatten human-written chords into music21 chord objects
  return [chord.Chord(harmony.ChordSymbol(c)) for c in ch]

def flatten(ch):
  # flatten music21 chords into normal order vectors
  return [c.normalOrder for c in ch]

def transpose_chs(chs, key):
  # make into actual chords, and transpose each wrt the song's key
  key = chord.Chord(harmony.ChordSymbol(key))
  return [transpose(c, key) for c in chs]

def sanitize_chord(ch):
    reps = {
        '\\': '',
        'b': '-',
        '-5': 'b5',
        '-9': 'b9',
        '(maj7)': 'M7',
        '(+5)': 'add5',
        '+5': 'add5',
        '/9': 'add9',
        'maj9': 'add9',
        'sus2': 'add2',
        'add4add9':'add4',
        'Maj7':'M7',
        '/G#':'b9',
        '(2)':'add2',
    }
    for k, v in reps.items():
        ch = ch.replace(k, v)
    return ch

def preprocess(fname,out_file):
    count = 0
    songs = ''
    with open(fname, 'r') as f:
        j = json.loads(f.read())
        for song in j:
            chs = [sanitize_chord(c) for c in song['chords']]
            chs = tomusic21(chs)
#             print(chs)
#             print(song['tonality_name'])
            chs = transpose_chs(chs,sanitize_chord(song['tonality_name']))
#             print(chs)
            chs = flatten(chs) #List of chords in a song 
            procs = [' '.join([str(n) for n in ch]) for ch in chs]
            procs = ' - '.join(procs)
            songs = songs + procs + ' . '
            count += 1
            print(count)
#             print("{} - {}".format(song['chords'], transpose_chs(chs, song['tonality_name'])))
    g = open(out_file,'w')
    g.write(songs)
    g.close()