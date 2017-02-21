#!/usr/bin/env python3
# encoding: utf-8
"""
Julia fractal
"""

import numpy as np
cimport numpy as np
import cython
from cython.parallel cimport prange
import time
import sys
import matplotlib
import matplotlib.pyplot as plt
from scipy.ndimage.interpolation import zoom

@cython.boundscheck(False)
def julia_cython(int N):
    cdef np.ndarray[np.uint8_t, ndim=2] T = np.empty((N, 2*N), dtype=np.uint8)
    cdef double complex c = -0.835 - 0.2321j
    cdef double complex z
    cdef int J, I
    cdef double h = 2.0/N
    cdef double x, y
    for J in prange(N, nogil=True, schedule="guided"):
        for I in xrange(2*N):
            y = -1.0 + J*h
            x = -2.0 + I*h
            T[J,I] = 0
            z = x + 1j * y
            while z.imag**2 + z.real**2 <= 4:
                z = z**2 + c
                T[J,I] += 1

    return T


def save_png(T, filename):
    from PIL import Image
    # Normalize arbitrary range to [0,1] -> color tuples -> color tuples as uint8
    # This can be saved as an image.
    normalizer = plt.Normalize(vmin=0, vmax=70)
    mapper = plt.cm.ScalarMappable(norm=normalizer, cmap=plt.cm.viridis)
    im = Image.fromarray(np.uint8(mapper.to_rgba(T)*255))
    im.save(filename)


t0 = time.time()
N = 16000
T = julia_cython(N)
t1 = time.time()
print t1 - t0

matplotlib.use("Agg")


T = zoom(T, 0.20)
print "image has size", T.shape
save_png(T, "julia.png")


import numpy as np
def julia(c, extent, pixels):
    t, l, b, r = extent
    ny, nx = pixels
    ys, xs = np.ogrid[t:b:ny*1j, l:r:nx*1j]
    im = ys * 1j + xs
    counts = np.zeros(pixels)
    while True:
        im = im * im + c
        still_alive = [abs(im) < 2]
        counts[still_alive] += 1
        if not np.any(still_alive):
            break
    return counts

N = 1000
J = julia(-0.835 - 0.2321j, (-1, -2, 1, 2), (N, 2*N))

save_png(J, "/home/akopp/Desktop/julia.png")
