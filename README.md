# mms-competition-proxy

## Intro
This python script is meant for use in the Princeton University Robotics Club
Virtual Micromouse Competition. It acts as an intermediary proxy program between
the simulator and the competitors' algorithms. The purpose is to add several
features that are not part of the simulator itself, but which add to the
competition realism. It works by forwarding commands from the algorithm to the
simulator and forwarding responses from the simulator back to the algorithm. The
simulator itself can be found [here](https://github.com/mackorone/mms).

## Features
Generally, this program allows the algorithm to interact with the simulator the
same way it would without this proxy. However, the following features diverge
from the features of the simulator.
* Disable movement after crash: After crashing into a wall, the mouse cannot
move, turn, or detect walls, until the mouse is reset to the start square. If
any of these commands are called while crashed, the proxy will return `"crash"`
instead of forwarding the command to the simulator.
* Move limit: To simulate the time constraints of a real-life micromouse
competition, the proxy imposes a move limit. When the sum of total effective
distance and total turns exceeds the move limit, the program will terminate.
This feature is enabled with the `--limit` command-line argument, which allows
the user to specify the limit. For the competition, a limit of 2000 will be
used.
* Unable to view stats: The algorithm cannot call `getStat`. This is to
encourage algorithms to keep track of their own score without external
assistance.
* Logging: If the user passes a filename with the `--out` command-line argument,
the simulator will log the stats of the run to that file at the conclusion of
the run.

## Setup
1. Ensure Python is installed. This script was developed on Python 3.8 but should
be compatible with other versions of Python 3 as well.
1. Install the simulator, which is named "mms". The repository can be found
[here](https://github.com/mackorone/mms). Since the release version is not
always up-to-date with the latest changes, it is required to build the project
from source by following
[these instructions](https://github.com/mackorone/mms#building-from-source).

## Usage
Instructions for getting started can be found in the mms repository. Only
a few additional steps are needed to use this proxy. To get started, run one
of the sample algorithms, such as
[mms-cpp](https://github.com/mackorone/mms-cpp). First download the sample
algorithm and launch the mms simulator. Select the "+" button near the upper
right of the window to configure a new algorithm. For the directory, browse to
the mms-cpp directory. The build command should be `g++ API.cpp Main.cpp`. The
run command should be `python3.8 ../mms-competition-proxy/proxy.py --limit 2000 ./a.out`,
assuming the proxy is in a neighboring directory. Click OK and then click Run.
You should see the mouse follow the left wall until the move limit of 2000 is
reached.

If using the [sample Python program](https://github.com/mackorone/mms-python)
instead, there is no build command and the run command will be
`python3.8 ../mms-competition-proxy/proxy.py --limit 2000 python3.8 Main.py`.

## Bugs
Please report any bugs or unexpected behavior encountered with this script.