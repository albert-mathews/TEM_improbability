#!/usr/bin/env python
"""
visualize_capsid_alignment_fast.py

Ultra-fast 3D visualisation + auto-generated rotating GIF
- One plot only (maximum interactivity)
- Minimal polygons (fast rotation even on laptops)
- Saves animated GIF for Substack / GitHub

Author: Your Name
License: MIT
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation

# --------------------------------------------------------------
# Parameters - tweak these freely
# --------------------------------------------------------------
capsid_radius = 60.0          # nm → 120 nm diameter
n_capsids = 35                # looks dense like Figure 8b
section_thickness = 80.0      # nm
distribution = "random"       # "random" or "planar"

# Resolution trade-off: lower = faster rotation & smaller GIF
u_res = 20    # azimuth points
v_res = 12    # polar points  (12–16 is sweet spot for speed + looks)

# Pre-compute a single perfect sphere (re-used for every capsid)
u = np.linspace(0, 2 * np.pi, u_res)
v = np.linspace(0, np.pi, v_res)
x_sphere = capsid_radius * np.outer(np.cos(u), np.sin(v))
y_sphere = capsid_radius * np.outer(np.sin(u), np.sin(v))
z_sphere = capsid_radius * np.outer(np.ones_like(u), np.cos(v))

# --------------------------------------------------------------
# Generate capsid centers
# --------------------------------------------------------------
rng = np.random.default_rng(42)

if distribution == "random":
    centers = rng.uniform(low=-320, high=320, size=(n_capsids, 3))
    title = "Random 3D distribution (what geometry predicts)"
    gif_name = "capsids_random.gif"
else:  # planar
    xy = rng.uniform(low=-300, high=300, size=(n_capsids, 2))
    z = rng.uniform(low=-4, high=4, size=n_capsids)   # tiny jitter
    centers = np.column_stack([xy, z])
    title = "Perfectly planar alignment (what TEM images actually show)"
    gif_name = "capsids_planar.gif"

# --------------------------------------------------------------
# Set up figure
# --------------------------------------------------------------
fig = plt.figure(figsize=(9, 8))
ax = fig.add_subplot(111, projection='3d')
ax.set_facecolor('white')

# Add all capsids as solid semi-transparent spheres
for cx, cy, cz in centers:
    ax.plot_surface(x_sphere + cx, y_sphere + cy, z_sphere + cz,
                    color='salmon' if distribution == "planar" else 'lightblue',
                    alpha=0.55, linewidth=0, antialiased=True)

# Section slab (very light)
X, Y = np.meshgrid(np.linspace(-500,500,4), np.linspace(-500,500,4))
ax.plot_surface(X, Y, np.full_like(X, +section_thickness/2), color='gray', alpha=0.07)
ax.plot_surface(X, Y, np.full_like(X, -section_thickness/2), color='gray', alpha=0.07)

ax.set_xlim(-400, 400)
ax.set_ylim(-400, 400)
ax.set_zlim(-250, 250)
ax.set_xlabel('X (nm)')
ax.set_ylabel('Y (nm)')
ax.set_zlabel('Z (nm)')
ax.set_title(title + f"\n{n_capsids} capsids, 80 nm section", fontsize=14, pad=20)

# --------------------------------------------------------------
# Animation function
# --------------------------------------------------------------
def rotate(angle):
    ax.view_init(elev=20, azim=angle)
    return fig,

ani = animation.FuncAnimation(fig, rotate, frames=range(0, 360, 3),
                              interval=80, blit=False, repeat=True)

# Save GIF (fast, small file)
print(f"Saving {gif_name} ...")
ani.save(gif_name, writer='pillow', fps=15, dpi=100)
print(f"Done! → {gif_name} is ready for Substack/GitHub")

# Also show interactive plot
plt.tight_layout()
plt.show()