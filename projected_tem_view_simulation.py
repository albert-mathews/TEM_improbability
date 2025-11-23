#!/usr/bin/env python
"""
tem_5_capsids_final.py

Exactly what you want:
- Left : 5 capsids, random Z → different ring sizes (some small, some missing)
- Right: 5 capsids, all perfectly planar → five identical full-sized rings
- Zero overlap, zero clutter

Author: Your Name
License: MIT
"""

import numpy as np
import matplotlib.pyplot as plt

diameter = 120.0
radius = diameter / 2
section = 80.0

# 5 hand-picked, non-overlapping X-Y positions (nm)
positions = np.array([
    [-160,  100],
    [ -60,  140],
    [  80,   80],
    [-100,  -60],
    [ 140,  -80]
])

plt.figure(figsize=(12, 6))

for side, title in enumerate([
    "Random 3D distribution\n→ variable ring sizes",
    "Perfectly planar alignment\n→ five identical rings"
], 1):
    plt.subplot(1, 2, side)
    img = np.zeros((600, 600))
    extent = [-260, 260, -180, 180]

    X, Y = np.meshgrid(np.linspace(extent[0], extent[1], 600),
                       np.linspace(extent[2], extent[3], 600))

    # Z positions
    if side == 1:  # random
        z_values = [-55, -20, 10, 35, 70]           # hand-chosen to show variety
    else:          # planar
        z_values = [0, -3, 4, -2, 2]                # all near Z=0

    for (x0, y0), z0 in zip(positions, z_values):
        if abs(z0) > radius + section/2:
            continue
        chord_r = np.sqrt(radius**2 - z0**2) if abs(z0) <= radius else 0
        if chord_r < 10:
            continue

        R = np.sqrt((X - x0)**2 + (Y - y0)**2)
        ring = np.abs(R - chord_r) < 3.2
        img[ring] = 255

    plt.imshow(img, cmap='gray', extent=extent)
    plt.title(title, fontsize=15, pad=20)
    plt.xlim(-260, 260)
    plt.ylim(-180, 180)
    plt.axis('off')

plt.suptitle("Why TEM images show uniform rings — 5 capsids only", 
             fontsize=17, y=0.92)
plt.tight_layout()

plt.savefig("tem_5_capsids_final.png", dpi=300, bbox_inches='tight')
plt.savefig("tem_5_capsids_final.svg", bbox_inches='tight')
print("Done → tem_5_capsids_final.png + .svg")

plt.show()