#!/usr/bin/env python3

import sys
import argparse

# Local
import music
from mode import *


_banner = sys.argv[0].split('/')[-1].split('.')[0] + ''' [options] [root]?
    -h, --help                this
    -l, --list                list known modes
    -t, --triads              show triads aside scale notes
    -T, --tetrades            show tetrades aside scale notes
    -m, --mode     [mode]     set the musical [mode] (default: ionian)
    -c, --chords   [n1,n2..]  build chords from arbitrary scales
    -i, --id       [n1,n2..]  identify the mode of a scale
'''


def parse_args():
    parser = argparse.ArgumentParser(usage = _banner, add_help = False)

    parser.add_argument('-h', '--help', action = 'store_true')
    parser.add_argument('-l', '--list', action = 'store_true')
    parser.add_argument('-t', '--triads', action = 'store_true')
    parser.add_argument('-T', '--tetrades', action = 'store_true')

    parser.add_argument('-m', '--mode', type = str, default = ionian.name)
    parser.add_argument('-c', '--chords', type = str, default = '')
    parser.add_argument('-i', '--id', type = str, default = '')

    parser.add_argument('root', type = str, default = '', nargs = '?')

    args = parser.parse_args()

    if len(sys.argv) < 2:
        print(_banner, end = '')
        sys.exit(0)

    if args.help:
        print(_banner, end = '')
        sys.exit(0)

    if args.triads and args.tetrades:
        raise ValueError('Option -T makes no sense with -t')

    args.mode = Mode.get_mode(args.mode)

    if not args.mode:
        raise ValueError(f"No such mode")

    if args.chords and args.id:
        raise ValueError('Option -c makes no sense with -i')

    if args.chords:
        args.chords = [n.strip().capitalize() for n in args.chords.split(' ')]

        if False in [music.is_note(n) for n in args.chords]:
            raise ValueError(f"Invalid scale: {' '.join(args.chords)}")

    if args.id:
        args.id = [n.strip().capitalize() for n in args.id.split(' ')]

        if False in [music.is_note(n) for n in args.id]:
            raise ValueError(f"Invalid scale: {' '.join(args.id)}")

    if args.root:
        args.root = args.root.strip().capitalize()

        if args.chords or args.id:
            raise ValueError('[root] makes no sense with options -b and -i')

        if not music.is_note(args.root):
            raise ValueError(f"Invalid note: '{args.root}'")

    return args


def main(args):
    if args.list:
        print('\n'.join(m.name for m in modes))
        return 0

    if args.chords:
        m = Mode('', music.build_intervals(args.chords))
        c = m.get_triads() if args.triads else m.get_tetrades()

        print(' '.join(''.join(z) for z in zip(m.get_roman_intervals(), c)))
        return 0

    if args.id:
        intervals = music.build_intervals(args.id)

        if (m := next((m for m in modes if list(m.intervals) == intervals), None)):
            print(m.name)
        else:
            print('Unknown mode')

        return 0

    chords = args.mode.get_triads() if args.triads else args.mode.get_tetrades()

    if args.root:
        scale = args.mode.build_scale(args.root)
    else:
        scale = args.mode.get_roman_intervals()

    if args.triads or args.tetrades:
        print(' '.join(''.join(z) for z in zip(scale, chords)))

    else:
        print(' '.join(scale))


if __name__ == '__main__':
    try:
        args = parse_args()

    except Exception as x:
        print(f'\x1b[90m[\x1b[91m!\x1b[90m] {type(x).__name__}\x1b[0m: {x}')
        sys.exit(1)

    try:
        sys.exit(main(args))

    except Exception as x:
        print(f'\x1b[90m[\x1b[91m!\x1b[90m] {type(x).__name__}\x1b[0m: {x}')
        sys.exit(2)
