import os
import sys
import random
import midi


data = []
titles = []


"""
 Recursively parses all MIDI files found in the given directory or any of its
 child directories
"""
def parse_data_in_dir(direc):
    if os.path.isdir(direc):
        print('Looking in {}...'.format(direc))
        for filename in os.listdir(direc):
            abs_filename = direc + '/' + filename
            if os.path.isdir(abs_filename):
                parse_data_in_dir(abs_filename)
            elif os.path.isfile(abs_filename):
                if abs_filename.endswith('.mid'):
                    print('Parsing MIDI file {}'.format(filename))
                    data.append(midi.read_midifile(abs_filename))
                    titles.append(filename)
                    # print(midi.read_midifile(abs_filename))


"""
 Generates and returns a random melody as a MIDI pattern, based on the given end
 tick, the maximum number of notes to play in the melody, the minimum initial
 pitch, the maximum initial pitch, the range of pitches to play, and whether or
 not to force the melody to stop at the given end tick.
"""
def generate_random_melody(end_tick, max_notes, min_init_pitch, max_init_pitch,
        pitch_range, force_stop):
    pattern = midi.Pattern()
    track = midi.Track()
    pattern.append(track)
    curr_tick = 0
    curr_note = 0
    curr_pitch = 0
    last_pitch = -1
    while curr_tick < end_tick and curr_note < max_notes:
        if last_pitch < 0:
            curr_pitch = random.randint(min_init_pitch, max_init_pitch)
        else:
            curr_pitch = last_pitch + random.randint((pitch_range / 2) * -1,
                    pitch_range / 2)
        on = midi.NoteOnEvent(tick=curr_tick, velocity=100, pitch=curr_pitch)
        track.append(on)
        last_for = end_tick / max_notes + random.randint(max_notes * -1, max_notes)
        curr_tick += last_for
        if curr_tick > end_tick and force_stop:
            curr_tick = end_tick
        off = midi.NoteOffEvent(tick=curr_tick, pitch=curr_pitch)
        track.append(off)
        last_pitch = curr_pitch
        curr_note += 1
    eot = midi.EndOfTrackEvent(tick=curr_tick)
    track.append(eot)
    return pattern


"""
Returns the average pitch among all notes in the song at song_index in the
MIDI data array
"""
def get_average_pitch(song_index):
    num_pitches = 0
    average_pitch = 0.0
    for track in data[song_index]:
        for event in track:
            if isinstance(event, midi.NoteOnEvent):
                average_pitch += event.get_pitch()
                num_pitches += 1
    average_pitch /= num_pitches
    return average_pitch


"""
Returns the index of the track with the given track_name in the song at
song_index in the MIDI data array, or -1 if it doesn't exist
"""
def get_track_index(song_index, track_name):
    for i in range(len(data[song_index])):
        for event in data[song_index][i]:
            if isinstance(event, midi.TrackNameEvent):
                if event.text == track_name:
                    return i
    return -1


# Parse all given data folders
for i in range(1, len(sys.argv)):
    parse_data_in_dir(sys.argv[1])

if len(data) > 0:
    print('Parsed {} MIDI files'.format(len(data)))

pattern = midi.Pattern()

# left = midi.Track() # Piano left
# pattern.append(left)

right = midi.Track() # Piano right
pattern.append(right)

# Randomly choose a starting song until valid left/right tracks are found in it
# Optimally, each song in the parsed data should have a left/right track
left_index = -1
right_index = -1
start_song_index = -1
last_pitch = -1

# Generate 25 random sections from the parsed pieces
for i in range(0, 25):
    # left_index = -1
    right_index = -1
    next_song_index = -1
    # while left_index == -1 or right_index == -1:
    while right_index == -1:
        next_song_index = random.randint(0, len(data) - 1)
       # left_index = get_track_index(next_song_index, 'Piano left')
        right_index = get_track_index(next_song_index, 'Piano right')
    next_song = data[next_song_index]
    num_events_to_add = random.randint(20, 50)
    if last_pitch < 0:
        print('Adding {} events from {}'.format(num_events_to_add, titles[next_song_index]))
        for j in range(0, num_events_to_add):
           # left.append(next_song[left_index][j])
            right.append(next_song[right_index][j])
        last_pitch = right[len(right) - 1].get_pitch()
    else:
        event_index = 0
        while isinstance(next_song[right_index][event_index], midi.NoteEvent) and next_song[right_index][event_index].get_pitch() != last_pitch:
            event_index += 1
            if event_index >= len(next_song[right_index]):
                # left_index = -1
                right_index = -1
                # while left_index == -1 or right_index == -1:
                while right_index == -1:
                    next_song_index = random.randint(0, len(data) - 1)
                   # left_index = get_track_index(next_song_index, 'Piano left')
                    right_index = get_track_index(next_song_index, 'Piano right')
                next_song = data[next_song_index]
                event_index = 0
                print('Didn\'t find the last pitch, new track is {}'.format(titles[next_song_index]))
        print('Adding {} events from {}'.format(num_events_to_add, titles[next_song_index]))
        for j in range(event_index, event_index + num_events_to_add):
            # left.append(next_song[left_index][j])
            right.append(next_song[right_index][j])
    


midi.write_midifile('output.mid', pattern)




"""
pattern = generate_random_melody(500, 10, 50, 70, 6, False)
midi.write_midifile("output.mid", pattern)
"""


"""
pattern = midi.Pattern()
track = midi.Track()
pattern.append(track)
on = midi.NoteOnEvent(tick=0, velocity=20, pitch=midi.G_3)
track.append(on)
off = midi.NoteOffEvent(tick=10000, pitch=midi.G_3)
track.append(off)
eot = midi.EndOfTrackEvent(tick=10000)
track.append(eot)
print pattern

midi.write_midifile("output.mid", pattern)
"""

