#!/usr/bin/env python
"""
visualize_random_vs_planar.py

3D matplotlib visualisation showing:
  - Left : truly random z-distribution (what geometry predicts)
  - Right: perfectly planar aligned capsids (what the TEM images look like)

Uses simple spheres (good enough - icosahedron would be overkill for the point).
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def plot_capsids(ax, centers, radius=60, color='cyan', alpha=0.6, edgecolor='black'):
    u = np.linspace(0, 2 * np.pi, 20)
    v = np.linspace(0, np.pi, 20)
    x = radius * np.outer(np.cos(u), np.sin(v))
    y = radius * np.outer(np.sin(u), np.sin(v))
    z = radius * np.outer(np.ones(np.size(u)), np.cos(v))

    for center in centers:
        surf_x = x + center[0]
        surf_y = y + center[1]
        surf_z = z + center[2]
        ax.plot_wireframe(surf_x, surf_y, surf_z, color=edgecolor, linewidth=0.5, alpha=0.3)
        ax.plot_surface(surf_x, surf_y, surf_z, color=color, alpha=alpha)

# ------------------------------------------------------------------
# Parameters
# ------------------------------------------------------------------
section_thickness = 80.0
radius = 60.0

# Generate ~25 capsids
np.random.seed(42)

# Random in z
centers_random = np.random.uniform(
    low=(-400, -400, -300),
    high=(400, 400, 300),
    size=(25, 3)
)

# Perfectly planar (z = 0 plane) - mimics a replication compartment layer
centers_planar = np.random.uniform(
    low=(-300, -300, -0.1),   # tiny z jitter for visual separation
    high=(300, 300, 0.1),
    size=(25, 3)
)

fig = plt.figure(figsize=(16, 7))

# Random case
ax1 = fig.add_subplot(121, projection='3d')
plot_capsids(ax1, centers_random, radius=radius)
ax1.set_zlim(-200, 200)
ax1.view_init(elev=20, azim=30)
ax1.set_title("Random 3D distribution (expected in thin section)", fontsize=14)
ax1.text2D(0.5, 0.02, f"Section slab = ±{section_thickness/2:.0f} nm (gray)",
           transform=ax1.transAxes, ha='center')

# Highlight the section slab
z_section = np.linspace(-section_thickness/2, section_thickness/2, 10)
X, Y = np.meshgrid(np.linspace(-500,500,10), np.linspace(-500,500,10))
ax1.plot_surface(X, Y, np.full_like(X, section_thickness/2), alpha=0.15, color='gray')
ax1.plot_surface(X, Y, np.full_like(X, -section_thickness/2), alpha=0.15, color='gray')

# Planar case
ax2 = fig.add_subplot(122, projection='3d')
plot_capsids(ax2, centers_planar, radius=radius, color='orange')
ax2.set_zlim(-200, 200)
ax2.view_init(elev=20, azim=30)
ax2.set_title("Perfectly planar alignment (what TEM images show)", fontsize=14)

# Same section slab highlight
ax2.plot_surface(X, Y, np.full_like(X, section_thickness/2), alpha=0.15, color='gray')
ax2.plot_surface(X, Y, np.full_like(X, -section_thickness/2), alpha=0.15, color='gray')

plt.suptitle("Why Figure 8b/8c is geometrically extraordinary", fontsize=16)
plt.tight_layout()
plt.show()