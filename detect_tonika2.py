import tonika_detector as td
import mido

ok = 0
total = 0

for line in open('markup/markup.tsv'):
    fn, label = line.strip().split('\t')

    mid = mido.MidiFile(f'markup/midi/{fn}')
    notes = [msg.note for msg in mid.tracks[0] if type(msg) == mido.messages.messages.Message]
    tonika = td.detect_tonika(notes)
    print(f'{fn}\t{label}\t{tonika}')
    if label == tonika: ok += 1
    total += 1

print(f'{ok}/{total}={ok/total} right guesses')