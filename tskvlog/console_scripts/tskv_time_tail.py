#!/usr/bin/env python3
import argparse
import sys
import time
from contextlib import suppress

from tskvlog import MissingFieldError, iterate_tskv_lines_within_time_range


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("files", nargs="+")
    parser.add_argument("-f", "--time-field", required=False, default="msec")
    parser.add_argument("-a", "--max-age", type=int, required=True)
    conf = parser.parse_args()

    now = time.time()
    with suppress(BrokenPipeError):
        for filename in reversed(conf.files):
            try:
                for line in iterate_tskv_lines_within_time_range(
                    filename,
                    conf.time_field,
                    since=now - conf.max_age,
                    until=None,
                ):
                    print(line)
            except MissingFieldError as exc:
                sys.exit(str(exc))


if __name__ == "__main__":
    main()
