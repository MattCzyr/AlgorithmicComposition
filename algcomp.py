import os
import sys
import random
import midi


data = []


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
        on = midi.NoteOnEvent(tick=curr_tick, velocity=20, pitch=curr_pitch)
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


# Parse all given data folders
for i in range(1, len(sys.argv)):
    parse_data_in_dir(sys.argv[1])

print('Parsed {} MIDI files'.format(len(data)))




pattern = generate_random_melody(10000, 10, 50, 70, 6, False)
midi.write_midifile("output.mid", pattern)




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

