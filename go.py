#!/usr/bin/python

import re
import sys
import math
import glob
import xlrd

def meandev(lst):
    mean = sum(lst)/len(lst)
    dev = math.sqrt(sum([(i-mean)**2 for i in lst])/len(lst))

    return mean, dev

def toBlock(filename):
    try: 
        xlrd.open_workbook(filename)
        return toBlock_xls(filename)
    except:
        return toBlock_txt(filename)

def toBlock_txt(filename):
    """ open source data file and convert it to python lists """
    blocks = []
    block = []
    
    for line in open(filename).readlines()[3:-3]:
        spline =  line.split("\t")
        if not re.search("[0-9]", line):
            if block != []:
                blocks.append(block)
                block = []
        else:
            for i in spline[2:-2]:
                if re.search("[0-9]", i):
                    block.append(float("".join([chr(j) for j in map(ord, i) if j > 0])))

    return blocks

def toBlock_xls(filename):
    blocks = []
    block = []

    wb = xlrd.open_workbook(filename)
    table = wb.sheets()[0]

    for rownum in range(3, table.nrows-3):
        num_line = False
        for n in table.row_values(rownum)[2:-2]:
            if isinstance(n, float):
                num_line = True
                block.append(n)
        if not num_line:
            if block != []:
                blocks.append(block)
                block = []

    return blocks


def writeResult(outfilename, blocks, data_per_group):
    """ write result to files """
    allfile = open("".join(["res_", outfilename, ".xls"]), "w")
    meandevfile = open("".join(["res_", outfilename, "_meandev.xls"]), "w")

    # write titles
    i = 0
    for letter in range(len(blocks[0])/12):
        for number in range(12):
            i += 1
            allfile.write("".join([chr(ord('A') + letter), str(number+1), '\t']))
            if (i % data_per_group == 0):
                allfile.write("\t")
            if ((i-1) % data_per_group == 0):
                meandevfile.write("".join([chr(ord('A') + letter), str(number+1), '\t']))
            else:
                meandevfile.write("\t")
    allfile.write("\n")
    meandevfile.write("\n")


    for block in blocks:
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
        allfile.write("\n")
        meandevfile.write("\n")

            
def main():
    infilenames = []
    if len(sys.argv) < 2:
        for i in glob.glob("*.xls"):
            if "res_" not in i:
                infilenames.append(i)
    else:
        infilenames = sys.argv[1:]

    for infilename in infilenames:
        print "Processing %s ..." % infilename
        blocks = toBlock(infilename)
        prefix = infilename.split('.')[0]
        writeResult(prefix, blocks, 3)

main()
