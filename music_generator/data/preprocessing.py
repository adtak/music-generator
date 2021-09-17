from pathlib import Path
from music21 import chord, converter, instrument, note
from typing import List


def load_midi_from_dir(midi_dir_parh: Path) -> List[List[str]]:
    notes = []
    durations = []
    for file in midi_dir_parh.glob('*.mid'):
        score = instrument.partitionByInstrument(converter.parse(file).chordify())
        n, d = get_notes_and_durations(score)
        notes.append(n)
        durations.append(d)
    print(f"Load {len(notes)} MIDI files.")


def get_notes_and_durations(score) -> List[str]:
    notes = []
    durations = []
    for element in score.flat:
        if isinstance(element, chord.Chord):
            notes.append('.'.join(p.nameWithOctave for p in element.pitches))
            durations.append(element.duration.quarterLength)
        elif isinstance(element, note.Note):
            if element.isRest:
                notes.append(element.name)
                durations.append(element.duration.quarterLength)
            else:
                notes.append(element.nameWithOctave)
                durations.append(element.duration.quarterLength)
    return notes, durations


if __name__ == '__main__':
    load_midi_from_dir(Path('resources'))
