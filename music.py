# Notes represented in flats and sharps
_notes = {
    'flat':('C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B'),
    'sharp':('C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'),

    # Default accidental scheme
    'default':('C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B'),

    # Translate all notes names into the default (also used to validate notes)
    'all_default':{
        'C': 'C', 'C#': 'Db', 'Db': 'Db', 'D': 'D', 'D#': 'Eb', 'Eb': 'Eb',
        'E': 'E', 'F': 'F', 'F#': 'Gb', 'Gb': 'Gb', 'G': 'G', 'G#': 'Ab',
        'Ab': 'Ab', 'A': 'A', 'A#': 'Bb', 'Bb': 'Bb', 'B': 'B'
    },
}

# Semitones in each interval represented in flats and sharps
_intervals = {
    'flat':{
        1: 'bII', 2: 'II', 3: 'bIII', 4: 'III', 5: 'IV', 6: 'bV', 7: 'V',
        8: 'bVI', 9: 'VI', 10: 'bVII', 11: 'VII'
    },

    'sharp':{
        1: '#I', 2: 'II', 3: '#II', 4: 'III', 5: 'IV', 6: '#IV', 7: 'V',
        8: '#V', 9: 'VI', 10: '#VI', 11: 'VII'
    },

    # Default accidental scheme
    'default':{
        1: 'bII', 2: 'II', 3: 'bIII', 4: 'III', 5: 'IV', 6: 'bV', 7: 'V',
        8: 'bVI', 9: 'VI', 10: 'bVII', 11: 'VII'
    }
}

# Chord types identified by the product of it's intervals, in semitones, from I
# Add: 9, min9, 7(9), 7M(9) ...
_chords = {
    18: 'dim', 21: 'min', 28: 'maj', 32: 'maj(#5)', 162: 'dim7',
    180: 'min7(b5)', 210:'min7', 231:'min(M7)', 280:'7', 308:'maj7',
    352:'maj7(#5)'
}


# Identify if a string represents a valid note
is_note = lambda s: s.capitalize() in _notes['all_default']


# Build a list triads from a list of intervals
def build_triads(intervals: list) -> list:
    triads = []

    try:
        for i in range(len(intervals)):
            # The relative scale's I chord
            r = intervals[i:] + intervals[:i]
            triads.append(_chords[sum(r[:2]) * sum(r[:4])])

    except KeyError:
        raise RuntimeError("Given intervals produce triads currently unknown")

    return triads


# Build a list of tetrads from a list of intervals
def build_tetrads(intervals: list) -> list:
    tetrads = []

    try:
        for i in range(len(intervals)):
            # The relative scale's I chord
            r = intervals[i:] + intervals[:i]
            tetrads.append(_chords[sum(r[:2]) * sum(r[:4]) * sum(r[:6])])

    except KeyError:
        raise RuntimeError("Given intervals produce tetrads currently unknown")

    return tetrads


# Build a list of intervals from a list of notes
def build_intervals(scale: list) -> list:
    intervals = []

    # Rebuild the scale to internal standards
    scale = [_notes['all_default'][n.capitalize()] for n in scale]
    alpha = (_notes['default'] * 2)[_notes['default'].index(scale[0]):]

    for i in range(len(scale) - 1):
        intervals.append(alpha.index(scale[i + 1]) - alpha.index(scale[i]))

    # The interval between last and first degrees
    intervals.append(alpha[1:].index(scale[0]) - alpha.index(scale[-1]) + 1)

    return intervals


# Build a list of notes from a list of intervals and a root
def build_scale(root: str, intervals: list) -> list:
    scale = []
    alpha = _notes['default']

    scale.append(root)
    scale.append(alpha[(alpha.index(root) + intervals[0]) % len(alpha)])

    for i in range(2, 7):
        scale.append(alpha[(alpha.index(root) + sum(intervals[:i])) % len(alpha)])

    return scale


# Return roman notation of numeric intervals
def romanize(intervals: list) -> list:
    roman_intervals = ['I']

    for i in range(1, len(intervals)):
        roman_intervals.append(_intervals['default'][sum(intervals[:i])])

    return roman_intervals
