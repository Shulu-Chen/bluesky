# Summary
## Shulu Chen @ GWU

Fork of the BlueSky Air Traffic Simulator developed by TU Delft. The original ReadMe can be seen below.

In this work, we built the NYC structured airspace by helicopter route and replaced the vertiport data.

We designed a trajectory generator in bluesky/scenario/generate_trj.py to generate all of required operations in BlueSky.

A video demo can be found [here](https://youtu.be/vRyiNrF8ic4).

# Installation

To run the case study please run the following steps:

1. Download NYC branch of this repository.
   git clone -b NYC https://github.com/Shulu-Chen/bluesky.git
2. Create a python 3.6 environment (python 3.7 not work).
3. Install all these packages: ‘pyqt5’, ’pyqtwebengine’, ’numpy’, ’scipy’, ’matplotlit’, ’pandas’, ’msgpack’, ’zmq’, ’pygame’, ‘pyopengl’, ‘rtree’.
4. Run BlueSky.py to see if you install it successfully.
5. Run generate_trj.py to generate a new operation list called NYC_test.scn.
6. In BlueSky GUI, click “file->open” and choose NYC_test.scn, then you can play with that.

# Features of trajectory generator

1. The UAV will depart randomly in any ORIG by Poission dist.
2. The generator will fulfill all necessary waypoints the UAV need.
3. For confliction detection, currently we set the buffer radius as 100 meter and look ahead 1 second.


------------------------------------------------------------------------------------------------------------------------------



# BlueSky - The Open Air Traffic Simulator

[![Open in Visual Studio Code](https://open.vscode.dev/badges/open-in-vscode.svg)](https://open.vscode.dev/TUDelft-CNS-ATM/bluesky)

BlueSky is meant as a tool to perform research on Air Traffic Management and Air Traffic Flows, and is distributed under the GNU General Public License v3.

The goal of BlueSky is to provide everybody who wants to visualize, analyze or simulate air
traffic with a tool to do so without any restrictions, licenses or limitations. It can be copied,
modified, cited, etc. without any limitations.

**Citation info:** J. M. Hoekstra and J. Ellerbroek, "[BlueSky ATC Simulator Project: an Open Data and Open Source Approach](https://www.researchgate.net/publication/304490055_BlueSky_ATC_Simulator_Project_an_Open_Data_and_Open_Source_Approach)", Proceedings of the seventh International Conference for Research on Air Transport (ICRAT), 2016.

## BlueSky Releases
If you are not (yet) interested in reading and editing the source of BlueSky, you can also download a release version of BlueSky, that you can install directly, without having to worry about python and library dependencies. You can find the latest release here:
https://github.com/TUDelft-CNS-ATM/bluesky/releases

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
BlueSky is still under heavy development. We would like to encourage anyone with a strong interest in
ATM and/or Python to join us. Please feel free to comment, criticise, and contribute to this project. Please send suggestions, proposed changes or contributions through GitHub pull requests, preferably after debugging it and optimising it for run-time performance.
