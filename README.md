grid-plot
===========
```grid-plot``` is a simple utility for plotting and visualizing data on a 2D grid.

<p align="center">
<img src="https://raw.github.com/doggan/grid-plot/screenshots/grid_00.png"/>
</p>

## Installation
``` bash
pip install -e git://github.com/doggan/grid-plot.git#egg=grid-plot
```

or

``` bash
git clone git://github.com/doggan/grid-plot.git
cd grid-plot
python setup.py install
```

## Usage
``` bash
$ grid-plot --help
usage: grid-plot [-h] infile outfile

positional arguments:
infile      the input data file
outfile     the output file

optional arguments:
-h, --help  show this help message and exit
```

### Example
``` bash
$ grid-plot ./examples/01.txt example_01.png
Processing [./examples/01.txt]...
Successfully created image [example_01.png].
Elapsed time: 0.1(s)
```

## Data File Description
TODO
