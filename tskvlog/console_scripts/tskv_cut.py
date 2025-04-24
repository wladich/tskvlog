#!/usr/bin/env python3
import argparse
import sys
from contextlib import suppress

from tskvlog import get_field_values


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("file", type=argparse.FileType(), nargs="?", default=sys.stdin)
    parser.add_argument("-f", "--fields", required=True)
    parser.add_argument("-n", "--nokeys", action="store_true", default=False)
    parser.add_argument("-i", "--ignore-missing", action="store_true", default=False)
    conf = parser.parse_args()
    field_names = conf.fields.split(",")
    nokeys = conf.nokeys
    ignore_missing = conf.ignore_missing
    with suppress(BrokenPipeError):
        for line in conf.file:
            values = get_field_values(line.rstrip(), field_names)
            if None in values:
                if ignore_missing:
                    continue
                missing_index = values.index(None)
                sys.exit('Field "%s" missing in record' % field_names[missing_index])
            if nokeys:
                s = "    ".join(values)  # type: ignore[arg-type]
            else:
                s = "    ".join(
                    f"{key}={value}" for key, value in zip(field_names, values)
                )
            print(s)


if __name__ == "__main__":
    main()
