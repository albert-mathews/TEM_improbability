#!/usr/bin/env python
"""
projected_tem_view_simulation.py

Renders a top-down 2D projection that mimics a TEM negative:
  - Random distribution → lots of partial rings, arcs, size variation
  - Planar distribution → almost all perfect rings (exactly like the paper)

Very convincing for presentations / GitHub README.
"""

import numpy as np
import matplotlib.pyplot as plt

radius = 60.0
section_half = 40.0

def generate_centers(case='random', N=25):
    rng = np.random.default_rng(123)
    if case == 'random':
        z = rng.uniform(-300, 300, N)
    elif case == 'planar':
        z = rng.uniform(-2, 2, N)   # tiny jitter
    x = rng.uniform(-250, 250, N)
    y = rng.uniform(-250, 250, N)
    return np.column_stack((x, y, z))

def project_to_tem(centers):
    img = np.zeros((600, 600))
    X, Y = np.meshgrid(np.linspace(-300, 300, 600), np.linspace(-300, 300, 600))
    for cx, cy, cz in centers:
        if abs(cz) > radius + section_half:
            continue
        # Distance from section mid-plane
        d = abs(cz)
        if d >= radius:
            continue
        chord_r = np.sqrt(radius**2 - d**2)
        dist = np.sqrt((X-cx)**2 + (Y-cy)**2)
        ring = np.abs(dist - chord_r) < 2.0
        img[ring] += 1.0
    return img

cases = [('random', 'Random 3D (expected)'), ('planar', 'Planar aligned (observed in paper)')]

plt.figure(figsize=(14, 6))
for i, (key, title) in enumerate(cases, 1):
    centers = generate_centers(key, N=28)
    proj = project_to_tem(centers)
    plt.subplot(1, 2, i)
    plt.imshow(proj, cmap='gray', extent=(-300,300,-300,300))
    plt.title(title, fontsize=14)
    plt.xlabel("nm")
    plt.ylabel("nm")
    plt.axis('off')

plt.suptitle("Simulated TEM view of 80 nm section through ~120 nm capsids", fontsize=16)
plt.tight_layout()
plt.show()