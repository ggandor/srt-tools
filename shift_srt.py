#!/usr/bin/env python3

import argparse
import re
import sys
from math import floor
from typing import Match


MSECS_PER_SEC : int = 1000
MSECS_PER_MIN : int = 1000 * 60
MSECS_PER_HOUR : int = 1000 * 60 * 60
SECS_PER_MIN : int = 60
MINS_PER_HOUR : int = 60


def timecode_to_msecs(timecode: Match) -> int:
    hours, mins, secs, msecs = map(int, timecode.groups())
    return (hours * MSECS_PER_HOUR +
            mins * MSECS_PER_MIN +
            secs * MSECS_PER_SEC +
            msecs)


def msecs_to_timecode(arg_msecs: int) -> str:
    if arg_msecs < 0:
        raise ValueError
    hours = str(arg_msecs // MSECS_PER_HOUR).zfill(2)
    mins = str((arg_msecs // MSECS_PER_MIN) % MINS_PER_HOUR).zfill(2)
    secs = str((arg_msecs // MSECS_PER_SEC) % SECS_PER_MIN).zfill(2)
    msecs = str(arg_msecs % MSECS_PER_SEC).zfill(3)
    return f"{hours}:{mins}:{secs},{msecs}"


def get_shifted_timecode(timecode: Match, timeshift: int) -> str:
    return msecs_to_timecode(timecode_to_msecs(timecode) + timeshift)


def get_shifted_srt(text: str, timeshift: int) -> str:
    timecode_pattern = r'(\d{2}):(\d{2}):(\d{2}),(\d{3})'
    return re.sub(timecode_pattern,
            lambda match: get_shifted_timecode(match, timeshift),
            text)


def main():
    if sys.argv[1:]:
        ap = argparse.ArgumentParser(
                description='Minimalist subtitle synchroniser utility.')
        ap.add_argument('file',
                help="source file")
        ap.add_argument('timeshift',
                type=int,
                help="timeshift in milliseconds")
        ap.add_argument("-o", "--output",
                required=False,
                help="output file (if not given, overwrites the original)")
        args = ap.parse_args()
        src_path = args.file
        timeshift = args.timeshift
        out_path = args.output if args.output else src_path
    else:  # ask for input
        src_path = input('source file: ')
        timeshift = int(input('timeshift in milliseconds: '))
        out_path = (input('output file (hit Enter to overwrite the original): ')
                or src_path)
    try:
        with open(src_path) as src, open(out_path, 'w') as out:
            text = src.read()
            shifted_srt = get_shifted_srt(text, timeshift)
            out.write(shifted_srt)
    except ValueError:
        print("Error: the given time shift would result in negative timecode values.")


if __name__ == "__main__":
    main()

