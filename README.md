# Integrated Conflict Management Platform for UAM
### Shulu Chen @ GWU

This project is a fork of the BlueSky Air Traffic Simulator developed by TU Delft, focused on advancing air traffic management for Urban Air Mobility (UAM).

The platform uses the Demand Capacity Balancing (DCB) algorithm to precondition traffic, followed by a tactical deconfliction method that provides maneuver advisories, such as speed changes, to mitigate in-air collisions. For detailed insights, refer to our research paper: [Integrated Conflict Management for UAM with Strategic Demand Capacity Balancing and Learning-based Tactical Deconfliction](https://arxiv.org/pdf/2305.10556.pdf).

Video Demonstrations:
* [Rule-based tactical deconflition with DCB](https://youtu.be/v3j6OxP5W9A?feature=shared)
* [Reinforcement learning tactical deconfliton with DCB](https://youtu.be/Ku6WXChRB0U?feature=shared)

Please note that this repository currently includes only the DCB algorithm and the rule-based tactical deconfliction method. The reinforcement learning tactical methods described in the paper will be publicly available soon after our internal review.

## How to Use

To get started with the Integrated Conflict Management Platform for UAM, follow these steps:

1. **Clone the Codebase:**
   Begin by cloning the codebase and installing the necessary packages.
2. **Generate Scenario Files:**
   Navigate to `bluesky-DCB/supports` and run `generate_scn_files.py`. This script calls the DCB module to generate scenario files.
3. **Run the Simulation:**
   Test the performance of the DCB and tactical deconfliction method by running the simulation script located at `bluesky-DCB/rule_based_tactical.py`.
4. **Replay Experiment and Access GUI:**
   To replay the experiment and view the GUI, run `bluesky-DCB/BlueSky.py`. Then, click `File -> Open` and select the saved scenario file `rb_result.scn`.
5. **View Experiment Results:**
   All necessary experiment results, including data and logs, are saved in the `bluesky-DCB/result` directory.

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
