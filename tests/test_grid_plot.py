import unittest
from grid_plot import grid_plot

infilePath = "./examples/01.txt"

class TestSettingsFile(unittest.TestCase):
    # Parse should fail when an invalid file is specified.
    def test_file_parse_failure(self):
        rootValue = grid_plot.parseFile("foo.txt")
        self.assertIsNone(rootValue)

    # Parse should succeed when a valid file is specified.
    def test_file_parse(self):
        rootValue = grid_plot.parseFile(infilePath)
        self.assertIsNotNone(rootValue)

    # Parsed dictionary object should have valid keys.
    def test_file_format(self):
        rootValue = grid_plot.parseFile(infilePath)
        gridDesc = grid_plot.createGridDesc(rootValue)

        self.assertIn("gridMajorLineInterval", gridDesc)
        self.assertIn("gridMajorLineThickness", gridDesc)
        self.assertIn("cellSizeInPixels", gridDesc)
        self.assertIn("gridOrigin", gridDesc)
        self.assertIn("gridOriginInPixels", gridDesc)
        self.assertIn("gridSize", gridDesc)
        self.assertIn("gridSizeInPixels", gridDesc)
        self.assertIn("imageSizeInPixels", gridDesc)
