#!/usr/bin/python

import re
import sys
import math

def meandev(lst):
    mean = sum(lst)/len(lst)
    dev = math.sqrt(sum([(i-mean)**2 for i in lst])/len(lst))

    return mean, dev


def toBlock(filename):
    """ open source data file and convert it to python lists """
    blocks = []
    block = []
    
    for line in open(filename).readlines()[3:-3]:
        spline =  line.split("\t")
        if len(spline) == 1:
            blocks.append(block)
            block = []
        else:
            for i in spline[2:-2]:
                if re.search("[0-9]", i):
                    block.append(float("".join([chr(j) for j in map(ord, i) if j > 0])))

    return blocks

def writeResult(outfilename, blocks, data_per_group, group_per_line):
    """ write result to files """
    allfile = open("".join([outfilename, "_all.xls"]), "w")
    meandevfile = open("".join([outfilename, "_meandev.xls"]), "w")

    while group_per_line:
        for block in blocks:
            ngroup = 0
            i = 0
            thl = []
            for n in block:
                thl.append(n)
                allfile.write("%f\t" % n)
                i += 1
                if (i % data_per_group == 0):
                    allfile.write("\t")
                    m, d = meandev(thl)
                    meandevfile.write("%f\t" % m)
                    meandevfile.write("%f" % d)
                    meandevfile.write("\t\t")
                    thl = []
                    ngroup += 1
                    if ngroup >= group_per_line:
                        allfile.write("\n")
                        meandevfile.write("\n")
                        break
        allfile.write("\n")
        meandevfile.write("\n")

        for n,block in enumerate(blocks):
            blocks[n] = block[data_per_group * group_per_line:]

        if len(blocks[0])/data_per_group < group_per_line:
            group_per_line = len(blocks[0])/data_per_group

            
def main():
    if len(sys.argv) < 2:
        print "Usage: %s <filename>" % (sys.argv[0])
        sys.exit(1)
    for infilename in sys.argv[1:]:
        blocks = toBlock(infilename)
        prefix = infilename.split('.')[0]
        writeResult(prefix, blocks, 3, 3)

main()
