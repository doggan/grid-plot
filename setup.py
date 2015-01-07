from setuptools import setup

version = '0.0.0'

setup(
    name = 'grid-plot',
    version = version,
    description = 'Plots data onto a grid.',
    url = 'http://github.com/doggan/grid-plot',
    license = 'MIT',
    author='Shyam Guthikonda',

    packages = ['grid_plot'],
    # install_requires = ['...'],
    entry_points="""
    [console_scripts]
    grid-plot = grid_plot.command_line:main
    """
)
