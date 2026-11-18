"""VisPy player for the compiled C physics; does not import variables.py."""
import os
os.environ['QT_LOGGING_RULES'] = 'qt.qpa.*=false'

import numpy as np
from vispy import app, scene
from vispy.visuals.transforms import STTransform
from pathlib import Path
import sys

# Allow imports from the sibling backend folder when this file is run directly.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from backend.physicsc import run_simulation

# Initial conditions and settings (the C function needs these as inputs).
# The C code computes every force, time step and wall collision.
n = 500                 # Use a smaller initial test: C checks every particle pair.
t = 500
dt = 0.01
l = round((n * 10) ** (1 / 3))
rc = 2.5
k = 5.0
r0 = 2.0
g = 0.5
m = 1.0                 # C requires a single scalar mass, not an array.

rng = np.random.default_rng(42)
p = rng.uniform(0, l, size=(n, 3))
v = rng.uniform(-50, 50, size=(n, 3))
phistory = run_simulation(p, v, m, t, dt, l, rc, k, r0, g)

canvas = scene.SceneCanvas(keys='interactive', show=True, size=(800, 600))
view = canvas.central_widget.add_view()
view.camera = 'turntable'
view.camera.center = (l / 2, l / 2, l / 2)
view.camera.distance = 5 * l

axis = scene.visuals.XYZAxis(parent=view.scene)
axis.transform = STTransform(scale=(l, l, l))
markers = scene.visuals.Markers(parent=view.scene)

frame_index = 0
def update(event):
    global frame_index
    markers.set_data(pos=phistory[frame_index].astype(np.float32),
                     face_color='blue', size=15)
    frame_index = (frame_index + 1) % len(phistory)

update(None)
timer = app.Timer(interval=1 / 60, connect=update, start=True)
app.run()
