import operator
import midi
import re
import mido
from mido import MidiFile

from parse import *
#test = midi.read_midifile("test.mid") #mary.mid
#print test

#on = midi.NoteOnEvent(tick=0, channel=0, data=[43,20])
#print on.data
#prints 43,20

#print on.pitch
#prints 43

#print on.velocity
#prints 20

#off = midi.NoteOffEvent(tick=0, channel=0, data=[60,64])
#print off.pitch
#prints 60


#print re.findall("NoteOnEvent", test(midi.Track))#parse 

#Hello = str(test)
#print Hello
#ParsedMessage = parse("data", Hello)
#print ParsedMessage
#print tracks in midi.Pattern()
#test = midi.FileReader("test.mid")
#print test

mid = MidiFile('test.mid')
for message in MidiFile('silent_night_easy.mid').play():
	if message.type == 'note_on':
		print message
	elif message.type == 'note_off':
		print message	

#msg = mido.Message(message)
	#print msg
	#if msg == note_on #channel=0 note=71 velocity=100 time=0.0166666666667
	#print True
	#else msg == note_off:
	#print False

#for i, track in enumerate(mid.tracks):
#	print('Track {}: {}'.format(i, track.name))
#	for message in track:
#		if message = note_on
#		print(message)











#####Test2 = test(midi.NoteOnEvent())	#test = midi.Track(pattern)
#print test
#sorted_x = sorted(test, key=operator.attrgetter('NoteOnEvent'))
#x.sort(test('NoteOnEvent'))
#var1 = test(pitch)


#test = midi.Track()
#print test
#midi.Track(\
#  [])

#test1 = midi.NoteOnEvent(pattern)
#print test1

#class NoteEvent(NoteEvent)
#Found this.

#for NoteOnEvent in midi.Track(pattern)
	#print pitch

#if midi.Track(pattern) == NoteOnEvent
	#print NoteOnEvent
#else if midi.Track(pattern) = NoteOffEvent
	#print NoteOffEvent
#else midi.Track(pattern) = EndOfTrackEvent
	#print EndOfTrackEvent


#if  Pattern == NoteOnEvent
	#Note1 = midi.NoteOnEvent
	#print NoteOnEvent

#if else NoteOffEvent = True
	#print NoteOffEvent

#else EndOfTrackEvent = True
	#stop program
