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
The input description file is JSON, and must follow the format below:
```
{
    "_comment": "The size of a single cell in pixels.",
    "cellSizeInPixels":[64,64],

    "_comment": "The start [x, y] and end [x, y] coordinates of the grid.",
    "coordinates":[
        [0,0],
        [4,4]
    ],

    "_comment": "Layers contain the actual cell data to be plotted on the grid. Multiple layers can exist, and are specified from low priority to high priority. High priority layers will be rendered on top of lower priority layers.",
    "layers":[
        {
            "_comment": "The color of the layer specified as an [R,G,B,A] value.",
            "color":[255,0,0,255],

            "_comment": "The cell data (points) to be plotted on the grid for this layer.",
            "cells":[
                [0,0],[1,0],[2,0],
                [1,1],[2,1],
                [2,2]
            ]
        },
        {
            "color":[0,0,255,255],
            "cells":[
                [2,2]
            ]
        }
    ],

    "_comment": "(Optional) The interval at which major lines will be drawn.",
    "majorLineInterval":5,

    "_comment": "(Optional) The thickness of drawn major lines.",
    "majorLineThickness":3,

    "_comment": "(Optional) Supply an image to be used as the background for the output grid. Must be a valid image path.",
    "backgroundImage":"path/to/image.png"
}
```
