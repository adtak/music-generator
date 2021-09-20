from pathlib import Path
from pprint import pprint
from music21 import chord, converter, instrument, note
from typing import Dict, List, Tuple


def load_midi_from_dir(midi_dir_parh: Path) -> Tuple[List[List[str]], List[List[str]]]:
    notes = []
    durations = []
    for file in midi_dir_parh.glob('*.mid'):
        score = instrument.partitionByInstrument(converter.parse(file).chordify())
        n, d = get_notes_and_durations(score)
        notes.append(n)
        durations.append(d)
    print(f"Load {len(notes)} MIDI files.")
    return (notes, durations)


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


def create_lookup_dict(elements: List[List[str]]) -> Tuple[Dict[str, int], Dict[int, str]]:
    unique_elements = set()
    for element in elements:
        unique_elements |= set(element)
    unique_elements = sorted(unique_elements)
    return (
        {e: i for i, e in enumerate(unique_elements)},
        {i: e for i, e in enumerate(unique_elements)},
    )


def create_dataset():
    pass


if __name__ == '__main__':
    notes, durations = load_midi_from_dir(Path('resources'))
    notes_to_int, int_to_notes = create_lookup_dict(notes)
    durations_to_int, int_to_durations = create_lookup_dict(durations)

    pprint(notes_to_int)
    pprint(durations_to_int)
