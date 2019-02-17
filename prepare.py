from music21 import chord, harmony, interval #Chord/Music Theory parsing
from music21 import midi, volume, stream #Music Generation
import json,time

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
    return;

def better_preprocess(fname, outfname):
    import sys
    from functools import reduce
    
    print('Better preprocessing dataset...')
    print('--------------------------------')
    
    count = 0
    final = []
    
    with open(fname, 'r') as f:
        j = json.loads(f.read())
        
        for song in j[count:]:
            chs = [sanitize_chord(c) for c in song['chords']]
            chs = tomusic21(chs)
            key = sanitize_chord(song['tonality_name'])
            if key == '':
                continue
                
            chs = transpose_chs(chs, key)
            chs = flatten(chs)
            # separate chords with '12' integer
            chs = reduce(lambda a, b: a+[12]+b, chs)
            final.append(chs)
            if count % 50 == 0:
                sys.stdout.write('{}... '.format(count))
            count += 1
    
    print('--------------------------------')
    
    # separate songs with '13' integer
    final = reduce(lambda a, b: a+[13]+b, final)
    
    with open(outfname, 'w') as f:
        json.dump(final, f)
    return;

def chord_cleaned(chords):
    import sys
    from functools import reduce

    chs = [sanitize_chord(c) for c in chords.split()]
    chs = tomusic21(chs)
    key = 'C'
   
    chs = transpose_chs(chs, key)
    chs = flatten(chs)
    # separate chords with '12' integer
    chs = reduce(lambda a, b: a+[12]+b, chs)
    return chs

#Helper functions for sanity checks of improperly formatted songs
def count_none(fn):
    count = 0 
    with open(fn,'r') as f:
        j = json.loads(f.read())
        for song in j:
            if(song['tonality_name'] == ''):
                count += 1
    return count

def find_song(fname, num):
    with open(fname,'r') as f:
        j = json.loads(f.read())
        raw = j[num]
        chs = [sanitize_chord(c) for c in raw['chords']]
        chs = tomusic21(chs)
#         print(chs)
        return chs, raw['tonality_name']
        
def write_song(chords, off = 0.0):
    #mod_chs = [chord.Chord(ch) for ch in chords]
    from music21 import chord, harmony, interval #Chord/Music Theory parsing
    from music21 import midi, volume, stream #Music Generation

    print(chords)
    # chords = [int(c) for c in chords]
    mod_chs = []
    for ch in chords:
        print(ch)
        try:
            mod_chs.append(chord.Chord(ch))
        except:
            print("failed...")
            pass

    for note in mod_chs:
        note.volume = volume.Volume(velocity=90)
        note.volume.velocityIsRelative = False
        note.offset = off 
        off += 1.2

    s = stream.Stream(mod_chs)
    print("Moving chords to stream, memory alloc {}".format(s))
    mf = midi.translate.streamToMidiFile(s)

    #fname = '{}.midi'.format(time.strftime("%Y%m%d-%H%M%S"))
    fname = "output.midi"
    mf.open(fname,'wb')
    mf.write()
    mf.close()
    print('done writing midi file')

    return fname

if __name__ == '__main__':
    # preprocess('json_songs.json', 'test')
    # better_preprocess('json_songs.json', 'clean_dataset.json')
    # find_song('json_songs.json',201)

    #test run
    chords = [[0, 4, 7], [7, 11, 2], [0, 4, 7], [0, 4, 7], [2, 5, 9], [7, 11, 2], [9, 0, 4], [7, 11, 2], [5, 9, 0], [0, 4, 7], [5, 9, 0], [7, 9, 2], [2, 5, 9], [0, 4, 7], [7, 11, 2], [0, 4, 7], [0, 4, 7]]

    write_song(chords)