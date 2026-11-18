"""Small Python interface to the compiled C simulation (physicsccompiled.dll)."""
import ctypes as ct
from pathlib import Path
import numpy as np

_dll = ct.CDLL(str(Path(__file__).with_name('physicsccompiled.dll')))
_array = np.ctypeslib.ndpointer(dtype=np.float64, ndim=1, flags='C_CONTIGUOUS')
_dll.run_simulation.argtypes = [
    _array, _array, _array, _array, ct.c_int, ct.c_int,
    ct.c_double, ct.c_double, ct.c_double, ct.c_double,
    ct.c_double, ct.c_double, ct.c_double,
]
_dll.run_simulation.restype = None


def run_simulation(p, v, m, t, dt, l, rc, k, r0, g):
    """Return (t, N, 3) positions calculated entirely by the C DLL."""
    p = np.array(p, dtype=np.float64, order='C', copy=True).reshape(-1)
    v = np.array(v, dtype=np.float64, order='C', copy=True).reshape(-1)
    n = p.size // 3
    if p.size != 3 * n or v.size != p.size:
        raise ValueError('Positions and velocities must both have shape (N, 3)')
    f = np.empty_like(p)
    history = np.empty((t, n, 3), dtype=np.float64)
    _dll.run_simulation(p, v, f, history.reshape(-1), n, t,
                        float(m), float(dt), float(l), float(rc),
                        float(k), float(r0), float(g))
    return history
