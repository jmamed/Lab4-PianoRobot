#https://github.com/olemb/mido
#http://mido.readthedocs.io/en/latest/intro.html




from mido import MidiFile
import mido
output = mido.open_output()
output.send(mido.Message('note_on', note = 60, velocity=64))


with input as mido.open_input('SH-201'):
	for message in input:
		print(message)

from mido import MidiFile
for message in MidiFile('song.mid').play():
	output.send(message)
p = mido.Parser()
p.feed([0x90, 0x40])
p.feed_byte(0x60)

p.pending()
for message in p:
	print(message)

#note_on channel=0 note=64 velocity=96 time=0

for message in MidiFile('song.mid').play():
	port.send(message)

from mido import Message
msg = Message('note_on', note=60)
msg

inport = mido.opne_input()
msg = inport.receive()

#To iterate through all incoming messages:
for msg in inport:


#!/usr/bin/env python

"""
#Open a MIDI file and print every message in every track.
#Support for MIDI files is still experimental.
"""

import sys
from mido import MidiFile

if __name__ == '__main__':
    filename = sys.argv[1]

    midi_file = MidiFile(filename)

    for i, track in enumerate(midi_file.tracks):
        sys.stdout.write('=== Track {}\n'.format(i))
        for message in track:
            sys.stdout.write('  {!r}\n'.format(message))

#!/usr/bin/env python
"""                                                                            
Play MIDI file on output port.
Run with (for example):
    ./play_midi_file.py 'SH-201 MIDI 1' 'test.mid'
"""

import sys
import mido
from mido import MidiFile

filename = sys.argv[1]
if len(sys.argv) == 3:
    portname = sys.argv[2]
else:
    portname = None

with mido.open_output(portname) as output:
    try:
        for message in MidiFile(filename).play():
            print(message)
            output.send(message)

    except KeyboardInterrupt:
        print()
        output.reset()


def decode(self, message, data):
	#interpret the data bytes and assign them to attributes
	(message.r, message.g, message.b) = data
