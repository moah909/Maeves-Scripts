#!/usr/bin/env python3
import csv
import sys

if (len(sys.argv) != 3) or ("-h" in sys.argv) or ("--help" in sys.argv):
    print("Usage: {} <input file> <output file>\nGenerates a list of unique positions in <input file> and outputs them in <output file>".format(sys.argv[0]))
    exit()

positions = set()

with open(sys.argv[1]) as csvfile:
    filereader = csv.reader(csvfile)
    for row in filereader:
        positions.add(row[2])

with open(sys.argv[2], 'a+', newline='') as csvfile:
    writer = csv.writer(csvfile)
    for x in positions:
        writer.writerow([x,""])
