import csv
import sys

mapping = {}

if (len(sys.argv) != 1) and (len(sys.argv) != 4) or ("-h" in sys.argv) or ("--help" in sys.argv):
    print("Usage: {} <input file> <position mappings> <output file>\nReplaces positions in <input file> with mappings from <positions mappings> and outputs them in <output file>".format(sys.argv[0]))
    exit()

if (len(sys.argv) == 1):
    sys.argv = [0,input("Input File: "),input("Position Mapping: "),input("Output File: ")]

positions = set()

with open(sys.argv[1]) as datafile, open(sys.argv[2]) as mappingfile, open(sys.argv[3], 'w')as outputfile:
    datareader = csv.reader(datafile)
    writer = csv.writer(outputfile)
    posmap = csv.reader(mappingfile)
    # posmapw = csv.writer(mappingfile)
    mapping = {rows[0]:rows[1] for rows in posmap}

    for row in datareader:
        try:
            if mapping[row[2]] == "--":
                continue
        except KeyError:
            print("Missing mapping for: {}".format(repr(row[2])))
            positions.add(row[2])
            continue

        if mapping[row[2]] != "=":
            row[2] = mapping[row[2]]
        writer.writerow(row)

    # for x in positions:
    #     posmapw.writerow([x,""])
