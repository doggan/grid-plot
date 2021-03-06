import math
import json
import os
import errno

# PIL
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

"""
Struct-like object for grouping together data
Reference: http://code.activestate.com/recipes/52308/
"""
class Bunch(dict):
    def __init__(self, **kwds):
        dict.__init__(self, kwds)
        self.__dict__ = self

def processLayer(baseImg, gridDesc, layerValue):
    color = layerValue["color"]
    if not isinstance(color, list):
        print "Invalid color \"%s\". Color must be of the form [R,G,B,A]. Example: [255,0,0,255]. Skipping this layer." % str(color)
        return

    color = tuple(color)
    cells = layerValue["cells"]

    gridOrigin = gridDesc.gridOrigin
    gridOriginInPixels = gridDesc.gridOriginInPixels
    gridSize = gridDesc.gridSize
    cellSizeInPixels = gridDesc.cellSizeInPixels

    # Create new image for drawing this layer.
    img2 = Image.new("RGBA", gridDesc.imageSizeInPixels)
    draw2 = ImageDraw.Draw(img2)

    # Draw all cells in this layer.
    for cell in cells:
        # Convert to relative coordinates.
        cellCoord = (cell[0] - gridOrigin[0], cell[1] - gridOrigin[1])

        if cellCoord[0] < 0 or cellCoord[0] >= gridSize[0] or\
           cellCoord[1] < 0 or cellCoord[1] >= gridSize[1]:
            print "Invalid cell coordinate: [%s,%s]. Skipping." % (cell[0], cell[1])
            continue

        cellMinPos =\
            (gridOriginInPixels[0] + cellCoord[0] * cellSizeInPixels[0],\
             gridOriginInPixels[1] + cellCoord[1] * cellSizeInPixels[1])
        cellMaxPos =\
            (cellMinPos[0] + cellSizeInPixels[0],\
             cellMinPos[1] + cellSizeInPixels[1])

        draw2.rectangle(cellMinPos + cellMaxPos, fill=color)

    # Merge images (alpha-compositing).
    r,g,b,a = img2.split()
    img2 = Image.merge("RGB", (r,g,b))    # Retrieve the RGB bands of the top image.
    mask = Image.merge("L", (a,))        # Retrieve the alpha band of the top image to use as a mask.
    baseImg.paste(img2, (0,0), mask)    # Paste top layer into base layer using mask for interpolation.

def drawGrid(draw, gridDesc):
    cellSizeInPixels = gridDesc.cellSizeInPixels
    gridSize = gridDesc.gridSize
    gridSizeInPixels = gridDesc.gridSizeInPixels
    gridOriginInPixels = gridDesc.gridOriginInPixels

    # Vertical lines.
    for x in range(gridSize[0] + 1):
        fromPos = (x * cellSizeInPixels[0] + gridOriginInPixels[0], gridOriginInPixels[1])
        toPos = (fromPos[0], fromPos[1] + gridSizeInPixels[1])

        # Line width calculation ("major" lines and first/last line of the grid).
        width = gridDesc.gridMajorLineThickness\
            if (x % gridDesc.gridMajorLineInterval == 0)\
            or x == gridSize[0]\
            else 1

        draw.line(fromPos + toPos, fill="black", width=width)

    # Horizontal lines.
    for y in range(gridSize[1] + 1):
        fromPos = (gridOriginInPixels[0], gridOriginInPixels[1] + y * cellSizeInPixels[1])
        toPos = (fromPos[0] + gridSizeInPixels[0], fromPos[1])

        # Line width calculation ("major" lines and first/last line of the grid).
        width = gridDesc.gridMajorLineThickness\
            if (y % gridDesc.gridMajorLineInterval == 0)\
            or y == gridSize[1]\
            else 1

        draw.line(fromPos + toPos, fill="black", width=width)

# Finds the biggest size font that will fit inside a single cell.
def getFont(gridDesc):
    cellSizeInPixels = gridDesc.cellSizeInPixels
    currentFontSize = 4

    font = None
    prevFont = None

    while True:
        #todo: need to get correct font even on windows...
        fontName = "/Library/Fonts/Arial.ttf"
        try:
            font = ImageFont.truetype(fontName, currentFontSize)

            # Initialize if necessary.
            if not prevFont:
                prevFont = font
        except IOError:
            print "Unable to load font [%s]. Skipping grid coordinate rendering." % fontName
            return None

        requiredFontSize = font.getsize("000")    # todo

        # If we can still make the font bigger, keep going.
        if requiredFontSize[0] < cellSizeInPixels[0] and\
           requiredFontSize[1] < cellSizeInPixels[1]:
            currentFontSize *= 2
            prevFont = font
        # This font doesn't fit. Revert to using previous size.
        else:
            return prevFont

    return None

def drawGridCoordinates(draw, gridDesc):
    # Get font for rendering grid coordinates.
    font = getFont(gridDesc)
    if not font:
        return

    cellSizeInPixels = gridDesc.cellSizeInPixels
    gridSize = gridDesc.gridSize
    gridSizeInPixels = gridDesc.gridSizeInPixels
    gridOrigin = gridDesc.gridOrigin

    # Prevents text from running into thick border along edges of grid.
    padding = math.ceil(gridDesc.gridMajorLineThickness / 2.0 + 1)

    # Top/Bottom
    posBotY = gridSizeInPixels[1] + cellSizeInPixels[1] + padding
    for x in range(gridSize[0]):
        coordStr = str(gridOrigin[0] + x)
        fontSize = font.getsize(coordStr)

        offsetX = cellSizeInPixels[0]
        offsetX += (cellSizeInPixels[0] - fontSize[0]) / 2

        posTopY = cellSizeInPixels[1] - fontSize[1] - padding
        pos = (x * cellSizeInPixels[0] + offsetX, posTopY)
        draw.text(pos, str(coordStr), font = font, fill = "black")

        pos = (pos[0], posBotY)
        draw.text(pos, str(coordStr), font = font, fill = "black")

    # Left/Right
    posRightX = gridSizeInPixels[0] + cellSizeInPixels[0] + padding
    for y in range(gridSize[1]):
        coordStr = str(gridOrigin[1] + y)
        fontSize = font.getsize(coordStr)

        offsetY = cellSizeInPixels[1]
        offsetY += (cellSizeInPixels[1] - fontSize[1]) / 2

        posLeftX = cellSizeInPixels[0] - fontSize[0] - padding
        pos = (posLeftX, y * cellSizeInPixels[1] + offsetY)
        draw.text(pos, str(coordStr), font = font, fill = "black")

        pos = (posRightX, pos[1])
        draw.text(pos, str(coordStr), font = font, fill = "black")

# Parse settings and create description struct used for grid creation.
def createGridDesc(rootValue):
    # The interval at which major lines will be drawn.
    gridMajorLineInterval = 5
    if "majorLineInterval" in rootValue:
        gridMajorLineInterval = rootValue["majorLineInterval"]
    # The thickness of all major lines
    gridMajorLineThickness = 3
    if "majorLineThickness" in rootValue:
        gridMajorLineThickness = rootValue["majorLineThickness"]

    cellSizeInPixels = tuple(rootValue["cellSizeInPixels"])

    coordValue = rootValue["coordinates"]
    startCoords = coordValue[0]
    endCoords = coordValue[1]
    colCount = endCoords[0] - startCoords[0] + 1
    rowCount = endCoords[1] - startCoords[1] + 1

    if colCount <= 0 or rowCount <= 0:
        raise ValueError("Invalid grid size: [%sx%s]. Check coordinates." % (colCount, rowCount))

    # Calculate the grid size (add 1 for border at far edges).
    gridSizeInPixels =\
        (cellSizeInPixels[0] * colCount + 1,\
         cellSizeInPixels[1] * rowCount + 1)
    # Entire image size - add 1 cell width border on each side.
    imageSizeInPixels =\
        (gridSizeInPixels[0] + cellSizeInPixels[0] * 2,\
         gridSizeInPixels[1] + cellSizeInPixels[1] * 2)

    return Bunch(\
        gridMajorLineInterval = gridMajorLineInterval,\
        gridMajorLineThickness = gridMajorLineThickness,\
        cellSizeInPixels = cellSizeInPixels,\
        gridOrigin = startCoords,\
        gridOriginInPixels = cellSizeInPixels,\
        gridSize = (colCount, rowCount),\
        gridSizeInPixels = gridSizeInPixels,\
        imageSizeInPixels = imageSizeInPixels)

# Open and parse the input date file.
def parseFile(filePath):
    inFile = None
    rootValue = None

    try:
        inFile = open(filePath, "r")
        rootValue = json.load(inFile)
        inFile.close()
    except IOError:
        print "Unable to open file [%s]." % filePath
        return None
    except ValueError:
        print "Unable to parse input file [%s]. Invalid JSON format." % filePath
        return None

    return rootValue

def mkdir_p(path):
    path = os.path.dirname(path)

    # Path is within a directory.
    if not path:
        return

    # Attempt to create the directory.
    try:
        os.makedirs(path)
    except OSError as e:
        if e.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

def generateGrid(infilePath, outfilePath):
    # Process input file.
    rootValue = parseFile(infilePath)
    if not rootValue:
        return

    # Parse grid description settings.
    try:
        gridDesc = createGridDesc(rootValue)
    except KeyError as e:
        print "Unable to parse input data file. Key [%s] does not exist." % e
        return
    except ValueError as e:
        print e
        return

    # Image creation.
    img = Image.new("RGBA", gridDesc.imageSizeInPixels, color="white")
    draw = ImageDraw.Draw(img)

    # Set up background image if specified.
    backgroundImageFileName = rootValue.get("backgroundImage")
    if backgroundImageFileName:
        try:
            bgImg = Image.open(backgroundImageFileName, "r")
            # Resize to fit within grid boundaries.
            bgImg = bgImg.resize(gridDesc.gridSizeInPixels)
            # Paste into base image.
            img.paste(bgImg, gridDesc.gridOriginInPixels)
        except IOError:
            print "Unable to open backgroundImage [%s]." % backgroundImageFileName

    # Process each layer from bottom to top.
    layersValue = rootValue["layers"]
    for layerValue in layersValue:
        processLayer(img, gridDesc, layerValue)

    # Draw the grid overlay.
    drawGrid(draw, gridDesc)
    drawGridCoordinates(draw, gridDesc)

    # Save image.
    # Attempt directory structure creation if necessary.
    try:
        mkdir_p(outfilePath)
        img.save(outfilePath, "PNG")
        print "Successfully created image [%s]." % outfilePath
    except IOError as e:
        print e
        print "Unable to create image [%s]." % outfilePath
        print "Please verify outfile path."
