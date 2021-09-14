from pathlib import Path
from music21 import chord, converter, instrument, note
from typing import List


def get_notes(midi_dir_parh: Path) -> List[str]:
    all_notes = []
    for file in midi_dir_parh.glob('*.mid'):
        notes = []
        score = instrument.partitionByInstrument(converter.parse(file))
        for element in score.parts[0].recurse():
            if isinstance(element, chord.Chord):
                notes.append('-'.join(str(i) for i in element.normalOrder))
            elif isinstance(element, note.Note):
                notes.append(str(element.pitch))
        all_notes.append(notes)
        print(f'{file.name} has {len(notes)} notes.')


if __name__ == '__main__':
    get_notes(Path('resources'))
