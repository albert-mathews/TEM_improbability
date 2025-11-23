#!/usr/bin/env python
"""
visualize_random_vs_planar.py

Clean, lightweight 3D visualisation:
- Perfectly spherical capsids (solid + semi-transparent)
- Random 3D distribution (left) vs perfectly planar (right)
- Designed for smooth interactive rotation in matplotlib's 3D window

Author: Your Name
License: MIT
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# ------------------------------------------------------------------
# Parameters
# ------------------------------------------------------------------
capsid_radius = 60.0          # nm → 120 nm diameter
section_thickness = 80.0      # nm
n_capsids = 28                # roughly matches density in Figure 8b

# High-resolution sphere (but still fast)
u = np.linspace(0, 2 * np.pi, 28)
v = np.linspace(0, np.pi, 20)
x_sphere = capsid_radius * np.outer(np.cos(u), np.sin(v))
y_sphere = capsid_radius * np.outer(np.sin(u), np.sin(v))
z_sphere = capsid_radius * np.outer(np.ones_like(u), np.cos(v))

def add_capsids(ax, centers, color='cyan', alpha=0.45):
    """Add solid semi-transparent spheres at given (x,y,z) centers"""
    for cx, cy, cz in centers:
        ax.plot_surface(x_sphere + cx, y_sphere + cy, z_sphere + cz,
                        color=color, alpha=alpha, linewidth=0, antialiased=True)

# ------------------------------------------------------------------
# Generate two distributions
# ------------------------------------------------------------------
rng = np.random.default_rng(123)

# Random 3D distribution (expected from biology)
centers_random = rng.uniform(low=-300, high=300, size=(n_capsids, 3))

# Perfectly planar distribution (what the TEM images actually show)
centers_planar = rng.uniform(low=-300, high=300, size=(n_capsids, 2))
centers_planar = np.column_stack([centers_planar, rng.uniform(-3, 3, n_capsids)])  # tiny z-jitter

# ------------------------------------------------------------------
# Plotting
# ------------------------------------------------------------------
fig = plt.figure(figsize=(16, 7))

# Random case
ax1 = fig.add_subplot(121, projection='3d')
add_capsids(ax1, centers_random, color='lightblue', alpha=0.5)
ax1.set_xlim(-400, 400)
ax1.set_ylim(-400, 400)
ax1.set_zlim(-250, 250)
ax1.set_xlabel('X (nm)')
ax1.set_ylabel('Y (nm)')
ax1.set_zlabel('Z (nm)')
ax1.set_title("Random 3D distribution\n(what geometry predicts)", fontsize=14, pad=20)

# Highlight the 80 nm section slab
X, Y = np.meshgrid(np.linspace(-500, 500, 4), np.linspace(-500, 500, 4))
ax1.plot_surface(X, Y, np.full_like(X, +section_thickness/2), color='gray', alpha=0.1)
ax1.plot_surface(X, Y, np.full_like(X, -section_thickness/2), color='gray', alpha=0.1)

# Planar case
ax2 = fig.add_subplot(122, projection='3d')
add_capsids(ax2, centers_planar, color='salmon', alpha=0.5)
ax2.set_xlim(-400, 400)
ax2.set_ylim(-400, 400)
ax2.set_zlim(-250, 250)
ax2.set_xlabel('X (nm)')
ax2.set_ylabel('Y (nm)')
ax2.set_zlabel('Z (nm)')
ax2.set_title("Perfectly planar alignment\n(what the TEM images show)", fontsize=14, pad=20)

# Same section slab
ax2.plot_surface(X, Y, np.full_like(X, +section_thickness/2), color='gray', alpha=0.1)
ax2.plot_surface(X, Y, np.full_like(X, -section_thickness/2), color='gray', alpha=0.1)

# Final touches
plt.suptitle("Why uniform capsid rings in thin-section TEM are geometrically extraordinary",
             fontsize=16, y=0.96)
fig.tight_layout()
plt.subplots_adjust(top=0.88)
plt.show()