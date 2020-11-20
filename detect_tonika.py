import tonika_detector as td
import mido

mid = mido.MidiFile('test.mid')

for i, track in enumerate(mid.tracks):
    notes = [msg.note for msg in track if type(msg) == mido.messages.messages.Message]
    tonika = td.detect_tonika(notes)
    print(f'Track {i}: {tonika}')
