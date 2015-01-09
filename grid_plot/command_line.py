import argparse
from time import time
import grid_plot

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("infile", help="the input data file")
    args = parser.parse_args()

    inFileName = args.infile

    startTime = time()
    print "Processing [%s]..." % inFileName

    # Processing.
    grid_plot.processFile(inFileName)

    endTime = time()
    totalTime = endTime - startTime
    print "Elapsed time: %.1f(s)" % totalTime

if __name__ == "__main__":
    main()
