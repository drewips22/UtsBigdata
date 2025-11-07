#!/usr/bin/env python3
import sys
from itertools import groupby
for key, group in groupby(sys.stdin, key=lambda x: x.split('\t', 1)[0]):
    try:
        total = sum(int(line.split('\t', 1)[1].strip()) for line in group)
        print(f"{key}\t{total}")
    except ValueError:
        pass
