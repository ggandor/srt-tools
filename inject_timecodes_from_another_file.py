#!/usr/bin/env python3

import argparse
import re
import sys
from typing import List


# TODO extract into utils module
def yes_no_prompt(prompt_msg: str) -> bool:
    return input(prompt_msg + " [Y/n] ") in ["Y", "y", ""]


# TODO extract into utils module
def is_timecode_line(line: str) -> bool:
    timecode_line_pattern = re.compile(
            "\d\d:\d\d:\d\d,\d\d\d --> \d\d:\d\d:\d\d,\d\d\d\s*")
    return timecode_line_pattern.match(line)


def inject_timecodes(source: List[str], target: List[str]) -> bool:
    timecode_lines_source = [line for line in source if is_timecode_line(line)]
    timecode_lines_target = [line for line in target if is_timecode_line(line)]
    num_of_timecode_lines_in_source = len(timecode_lines_source)
    num_of_timecode_lines_in_target = len(timecode_lines_target)
    msg = "The source and target file don't seem to have the same number of text groups. Continue and replace as many timecode lines in the target file as possible?"
    if (num_of_timecode_lines_in_source != num_of_timecode_lines_in_target
            and not yes_no_prompt(msg)):
        return False
    j = 0
    for i in range(len(target)):
        if is_timecode_line(target[i]):
            target[i] = timecode_lines_source[j]
            j += 1
            if j >= num_of_timecode_lines_in_source:
                break
    return True


def main():
    if sys.argv[1:]:
        ap = argparse.ArgumentParser(
                description="Inject timecodes from one srt file to another")
        ap.add_argument("-s", "--source",
                help="source file")
        ap.add_argument("-t", "--target",
                help="target file")
        ap.add_argument("-o", "--output",
                required=False,
                help="output file (if not given, overwrites the original)")
        args = ap.parse_args()
        source_path = args.source
        target_path = args.target
        out_path = args.output if args.output else source_path
    else:  # ask for input
        source_path = input('source file: ')
        target_path = input('target file: ')
        out_path = (input('output file (hit Enter to overwrite the original): ')
                or source_path)

    with open(source_path) as source:
        source_lines = source.readlines()
    with open(target_path) as target:
        target_lines = target.readlines()
    if inject_timecodes(source_lines, target_lines):
        with open(out_path, 'w') as out:
            out.writelines(target_lines)


if __name__ == "__main__":
    main()
