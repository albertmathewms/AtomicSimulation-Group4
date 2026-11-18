# Atomic Simulation

A particle simulation project exploring interacting particles in a three-dimensional box. The project includes different implementations of the physics calculations, visualisations, energy plots, and experiments with performance optimisation.

## Features

- Particle interactions using a distance cut-off and spring-like pair forces
- Time-stepped updates to particle positions and velocities
- Boundary reflections and, in supported implementations, drag
- 3D particle visualisation using **VisPy** and **Matplotlib**
- Kinetic and potential energy plots
- Implementations and experiments using **NumPy**, **Numba**, and compiled **C**
- Experimental approaches to improving performance, including cell-linked lists

## Project structure

The repository is organised around a `simulations` directory. The structure below shows the main files and folders; other scripts and result files may also be present.

```text
AS-Final/
├── requirements.txt
├── README.md
├── simulations/
│   ├── __init__.py
│   ├── backend/
│   │   ├── __init__.py
│   │   ├── variables.py
│   │   ├── physicsnumba.py
│   │   ├── physicsnumpy.py
│   │   ├── physicsc.c
│   │   ├── physicsccompiled.dll
│   │   └── physicsc.py
│   ├── sim-vispy-numba.py
│   ├── sim-vispy-numpy.py
│   ├── sim-vispy-c.py
│   ├── sim-matplotlib-numba.py
│   ├── sim-matplotlib-numpy.py
│   ├── experiments/
│   ├── report/
│   └── results/
└── ...
```

> The file tree reflects the current project arrangement; please check the exact filenames against the latest repository before using the commands below.

## Requirements

- Python 3.12 or another version compatible with the dependencies
- Packages listed in `requirements.txt` (NumPy, Numba, Matplotlib, VisPy and PyQt6)
- **Windows (64-bit Python)** to run the supplied `physicsccompiled.dll`

### Installation

Open a terminal in the repository root (`AS-Final`):

```powershell
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
```

On macOS/Linux, virtual environment activation is `source .venv/bin/activate`. The included Windows DLL cannot be loaded directly on those systems; rebuild the C library for the target platform to use that backend.

## Running the simulations

Run commands **from the repository root**, so Python can resolve `simulations` as a package:

```powershell
# Numba physics with VisPy
python -m simulations.sim-vispy-numba

# NumPy physics with VisPy
python -m simulations.sim-vispy-numpy

# Compiled C physics with VisPy (Windows)
python -m simulations.sim-vispy-c
```

For Matplotlib visualisations, corresponding scripts are available in `simulations/`, such as `sim-matplotlib-numba.py` and `sim-matplotlib-numpy.py`.

If a script imports the physics modules directly, use package-aware imports such as:

```python
from simulations.backend.variables import *
from simulations.backend.physicsnumba import run_simulation
```

Inside a backend module, imports of neighbouring files can use relative imports, for example `from .variables import *`. Scripts should be run from the repository root using `python -m ...` when using these package imports.

### How the C version works

`physicsc.c` implements the physics functions, including force calculations, drag, wall reflections and time stepping. `physicsccompiled.dll` contains the compiled code. `physicsc.py` uses Python's `ctypes` to pass NumPy arrays and simulation parameters into the DLL. VisPy then displays the generated position history.

The C visualisation is intended to be **independent of `variables.py`**: it supplies initial conditions in its own script. Merely renaming a `.c` file does not rebuild the DLL; recompile after modifying the C source.

## Testing and results

The `experiments` directory contains exploratory implementations and optimisation tests. Graphs, timing measurements, and other outputs may be stored under `results` or documented in `report`. For meaningful performance comparisons, use the same particle counts, initial conditions and simulation settings, and confirm the implementations produce comparable results.

## Team members and contributions

| Member | Roll number | Contribution |
|---|---|---|
| Hitansh Jamneria | MS26BTECH11015 | Paddle flippers, live energy graphs and optimisation of the final code |
| Albert Joe Mathew | MS26BTECH11004 | Initial box-and-particles implementation, live simulation, VisPy and particle forces |
| Jahagirdar Rumana Jamir | MS26BTECH11017 | Initial code iteration and Numba/VisPy implementations |
| Surabhi A | MS26BTECH11036 | Combined kinetic and potential energy graphs |
| Shubham Agarwal | IC26BTECH11033 | Conversion of selected Python physics code to C |
| Abhinav Unni | MS26BTECH11003 | Drag implementation and exploration of a cell-linked-list algorithm |

## Shared project files

Additional shared materials: [Google Drive folder](https://drive.google.com/drive/folders/1z9Tzh6B66PLGxNHveu7Xawh6mRfdTgNW?usp=drive_link).

## AI usage

If AI tools were used during this project, document the tools, purposes, and relevant prompts or session records in the submitted project materials. **The team has not yet provided a confirmed AI-use statement for this README**, so no specific tool use is claimed here.
