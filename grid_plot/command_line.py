import argparse
from time import time
import grid_plot

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("infile", help = "the input data file")
    parser.add_argument("outfile", help = "the output file")
    args = parser.parse_args()

    infilePath = args.infile
    outfilePath = args.outfile

    startTime = time()
    print "Processing [%s]..." % infilePath

    # Processing.
    grid_plot.processFile(infilePath, outfilePath)

    endTime = time()
    totalTime = endTime - startTime
    print "Elapsed time: %.1f(s)" % totalTime

if __name__ == "__main__":
    main()
