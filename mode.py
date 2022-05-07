import music


class Mode(object):
    def __init__(self, name: str, intervals: tuple):
        self.name = name
        self.intervals = intervals

        # Prevent mode loading overhead
        self._triads = None
        self._tetrades = None
        self._roman_intervals = None

    # Get the mode whose name best matches a stirng
    @classmethod
    def get_mode(cls, name: str):
        best = 0
        mode = None
        name = name.lower()

        for m in modes:
            score = 0
            mode_name = m.name.lower()

            for i in range(min(len(mode_name), len(name))):
                if mode_name[i] != name[i]:
                    break

                score += 1

            if score > best:
                mode = m

        return mode

    def get_triads(self) -> tuple:
        if self._triads:
            return self._triads

        self._triads = music.build_triads(self.intervals)
        return self._triads

    def get_tetrades(self) -> tuple:
        if self._tetrades:
            return self._tetrades

        self._tetrades = music.build_tetrades(self.intervals)
        return self._tetrades

    def get_roman_intervals(self) -> tuple:
        if self._roman_intervals:
            return self._roman_intervals

        self._roman_intervals = music.romanize(self.intervals)
        return self._roman_intervals

    # Build a scale in this mode
    def build_scale(self, root: str) -> list:
        return music.build_scale(root, self.intervals)


# Modes of Ionian
ionian     = Mode('Ionian',     (2, 2, 1, 2, 2, 2, 1))
dorian     = Mode('Dorian',     (2, 1, 2, 2, 2, 1, 2))
phrygian   = Mode('Phrygian',   (1, 2, 2, 2, 1, 2, 2))
lydian     = Mode('Lydian',     (2, 2, 2, 1, 2, 2, 1))
mixolydian = Mode('Mixolydian', (2, 2, 1, 2, 2, 1, 2))
aeolian    = Mode('Aeolian',    (2, 1, 2, 2, 1, 2, 2))
locrian    = Mode('Locrian',    (1, 2, 2, 1, 2, 2, 2))

# Other modes
ionian_b3   = Mode('Ionian b3 (Melodic Minor)',       (2, 1, 2, 2, 2, 2, 1))
aeolian_s7  = Mode('Aeolian #7 (Harmonic Minor)',     (2, 1, 2, 2, 1, 3, 1))
lydian_b7   = Mode('Lydian b7 (Lydian Dominant)',     (2, 2, 2, 1, 2, 1, 2))
phrygian_s3 = Mode('Phrygian #3 (Phrygian Dominant)', (1, 3, 1, 2, 1, 2, 2))

# # Make modes accessible iteratively
modes = [
    ionian, dorian, phrygian, lydian, mixolydian, aeolian, locrian, ionian_b3,
    aeolian_s7, lydian_b7, phrygian_s3
]
