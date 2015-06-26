import csv
import sys

## Print the obs ids from a csv file produced by the NGAS webpage

file = sys.argv[1]

out = open(file+'.txt','w')

with open(file, 'rb') as f:
    reader = csv.reader(f)
    for row in reader:
        out.write(row[0])
        out.write('\n')

out.close()
