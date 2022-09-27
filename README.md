# Summary
## Shulu Chen @ GWU

Fork from the BlueSky Air Traffic Simulator developed by TU Delft. The original ReadMe can be seen below.

In this work, we built the NYC structured airspace by helicopter route and replaced the vertiport data.

We designed a trajectory generator in bluesky/scenario/generate_trj.py to generate all of required operations in BlueSky.

A video demo can be found [here](https://youtu.be/vRyiNrF8ic4).

# Installation

To run the case study please run the following steps:

For windows:
1. Download NYC branch of this repository.
   git clone -b NYC https://github.com/Shulu-Chen/bluesky.git
2. Create a python 3.6 environment (python 3.7 not work).
3. Install all these packages: ‘pyqt5’, ’pyqtwebengine’, ’numpy’, ’scipy’, ’matplotlib’, ’pandas’, ’msgpack’, ’zmq’, ’pygame’, ‘pyopengl’, ‘rtree’.
4. Run BlueSky.py to see if you install it successfully.
5. Run generate_trj.py to generate a new operation list called NYC_test.scn.
6. In BlueSky GUI, click “file->open” and choose NYC_test.scn, then you can play with that.

For MAC:

All steps are the same, you still need to restart your computer. Additionally, MAC may not support PyOpenGL. You can fix this issue by editing PyOpenGL file OpenGL/platform/ctypesloader.py, and changing the line
```
fullName = util.find_library( name )
```
to
```
fullName = '/System/Library/Frameworks/OpenGL.framework/OpenGL'
```
# Features of trajectory generator

1. Run scenario/deconflication_trj.py to generate the flight plan.
2. The UAV will depart randomly in any ORIG by Poisson dist.
3. The generator will fulfill all necessary waypoints the UAV need.
4. For confliction detection, currently we set the buffer radius as 100 meter.
5. The architecture of our current setting:
![image](https://github.com/Shulu-Chen/bluesky/blob/NYC/ARC.png)


------------------------------------------------------------------------------------------------------------------------------



# BlueSky - The Open Air Traffic Simulator

[![Open in Visual Studio Code](https://img.shields.io/static/v1?logo=visualstudiocode&label=&message=Open%20in%20Visual%20Studio%20Code&labelColor=2c2c32&color=007acc&logoColor=007acc)](https://open.vscode.dev/TUDelft-CNS-ATM/bluesky)
[![GitHub release](https://img.shields.io/github/release/TUDelft-CNS-ATM/bluesky.svg)](https://GitHub.com/TUDelft-CNS-ATM/bluesky/releases/)
![GitHub all releases](https://img.shields.io/github/downloads/TUDelft-CNS-ATM/bluesky/total?style=social)

[![PyPI version shields.io](https://img.shields.io/pypi/v/bluesky-simulator.svg)](https://pypi.python.org/pypi/bluesky-simulator/)
![PyPI - Downloads](https://img.shields.io/pypi/dm/bluesky-simulator?style=plastic)
[![PyPI license](https://img.shields.io/pypi/l/bluesky-simulator?style=plastic)](https://pypi.python.org/pypi/bluesky-simulator/)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/bluesky-simulator?style=plastic)](https://pypi.python.org/pypi/bluesky-simulator/)

BlueSky is meant as a tool to perform research on Air Traffic Management and Air Traffic Flows, and is distributed under the GNU General Public License v3.

The goal of BlueSky is to provide everybody who wants to visualize, analyze or simulate air
traffic with a tool to do so without any restrictions, licenses or limitations. It can be copied,
modified, cited, etc. without any limitations.

**Citation info:** J. M. Hoekstra and J. Ellerbroek, "[BlueSky ATC Simulator Project: an Open Data and Open Source Approach](https://www.researchgate.net/publication/304490055_BlueSky_ATC_Simulator_Project_an_Open_Data_and_Open_Source_Approach)", Proceedings of the seventh International Conference for Research on Air Transport (ICRAT), 2016.

## BlueSky Releases
BlueSky is also available as a pip package, for which periodically version releases are made. You can find the latest release here:
https://github.com/TUDelft-CNS-ATM/bluesky/releases
The BlueSky pip package is installed with the following command:

    pip install bluesky-simulator[full]

Using ZSH? Add quotes around the package name: `"bluesky-simulator[full]"`. For more installation instructions go to the Wiki.

## BlueSky Wiki
Installation and user guides are accessible at:
https://github.com/TUDelft-CNS-ATM/bluesky/wiki

## Some features of BlueSky:
- Written in the freely available, ultra-simple-hence-easy-to-learn, multi-platform language
Python 3 (using numpy and either pygame or Qt+OpenGL for visualisation) with source
- Extensible by means of self-contained [plugins](https://github.com/TUDelft-CNS-ATM/bluesky/wiki/plugin)
- Contains open source data on navaids, performance data of aircraft and geography
- Global coverage navaid and airport data
- Contains simulations of aircraft performance, flight management system (LNAV, VNAV under construction),
autopilot, conflict detection and resolution and airborne separation assurance systems
- Compatible with BADA 3.x data
- Compatible wth NLR Traffic Manager TMX as used by NLR and NASA LaRC
- Traffic is controlled via user inputs in a console window or by playing scenario files (.SCN)
containing the same commands with a time stamp before the command ("HH:MM:SS.hh>")
- Mouse clicks in traffic window are use in console for lat/lon/heading and position inputs

## Contributions
BlueSky can be considered 'perpetual beta'. We would like to encourage anyone with a strong interest in
ATM and/or Python to join us. Please feel free to comment, criticise, and contribute to this project. Please send suggestions, proposed changes or contributions through GitHub pull requests, preferably after debugging it and optimising it for run-time performance.
