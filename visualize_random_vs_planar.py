#!/usr/bin/env python
"""
capsid_section_side_by_side.py

Side-by-side static 3D figure:
- Left:  Random 3D distribution
- Right: Perfectly planar alignment
Both viewed straight into the 80 nm section (along the electron beam)
so readers instantly see how many capsids are properly centered in the slice.

Also optionally saves rotating GIFs (commented out by default).

Author: Your Name
License: MIT
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# ==============================================================
# Parameters
# ==============================================================
capsid_radius = 60.0          # nm → 120 nm diameter
n_capsids = 32
section_thickness = 80.0
rng = np.random.default_rng(123)

# Low-res sphere = fast rendering + clean look
u = np.linspace(0, 2 * np.pi, 24)
v = np.linspace(0, np.pi, 14)
x_sph = capsid_radius * np.outer(np.cos(u), np.sin(v))
y_sph = capsid_radius * np.outer(np.sin(u), np.sin(v))
z_sph = capsid_radius * np.outer(np.ones_like(u), np.cos(v))

# ==============================================================
# Generate two distributions
# ==============================================================
# Random
centers_random = rng.uniform(low=-300, high=300, size=(n_capsids, 3))

# Planar (tiny z-jitter so spheres don’t perfectly overlap visually)
xy = rng.uniform(low=-290, high=290, size=(n_capsids, 2))
z_planar = rng.uniform(low=-5, high=5, size=n_capsids)
centers_planar = np.column_stack([xy, z_planar])

# ==============================================================
# Plotting
# ==============================================================
fig = plt.figure(figsize=(16, 7.5))
# fig.suptitle("Why uniform capsid rings in TEM are geometrically extraordinary\n"
             # "View = looking straight into the 80 nm section (along the electron beam)",
             # fontsize=16, y=0.96)

# ——— Left: Random ———
ax1 = fig.add_subplot(121, projection='3d')
for cx, cy, cz in centers_random:
    ax1.plot_surface(x_sph + cx, y_sph + cy, z_sph + cz,
                     color='lightblue', alpha=0.55, linewidth=0)
ax1.view_init(elev=0, azim=-90)        # look straight down Z (into section)
ax1.set_title("Random 3D distribution\n(expected from geometry)", fontsize=14, pad=20)
ax1.set_xlim(-350, 350); ax1.set_ylim(-350, 350); ax1.set_zlim(-200, 200)
ax1.set_xlabel("X (nm)"); ax1.set_ylabel("Y (nm)"); ax1.set_zlabel("Z (nm)")

section_boundary_alpha=0.6
# Section boundaries
X, Y = np.meshgrid(np.linspace(-400,400,5), np.linspace(-400,400,5))
ax1.plot_surface(X, Y, np.full_like(X, +section_thickness/2), color='gray', alpha=section_boundary_alpha)
ax1.plot_surface(X, Y, np.full_like(X, -section_thickness/2), color='gray', alpha=section_boundary_alpha)

# ——— Right: Planar ———
ax2 = fig.add_subplot(122, projection='3d')
for cx, cy, cz in centers_planar:
    ax2.plot_surface(x_sph + cx, y_sph + cy, z_sph + cz,
                     color='salmon', alpha=0.55, linewidth=0)
ax2.view_init(elev=0, azim=-90)        # same view direction
ax2.set_title("Perfectly planar alignment\n(what the TEM images actually show)", fontsize=14, pad=20)
ax2.set_xlim(-350, 350); ax2.set_ylim(-350, 350); ax2.set_zlim(-200, 200)
ax2.set_xlabel("X (nm)"); ax2.set_ylabel("Y (nm)"); ax2.set_zlabel("Z (nm)")

ax2.plot_surface(X, Y, np.full_like(X, +section_thickness/2), color='gray', alpha=section_boundary_alpha)
ax2.plot_surface(X, Y, np.full_like(X, -section_thickness/2), color='gray', alpha=section_boundary_alpha)

plt.tight_layout()
plt.subplots_adjust(top=0.85)

# ==============================================================
# Save high-quality static image (perfect for README/Substack)
# ==============================================================
plt.savefig("capsid_random_vs_planar_straight_on.png", dpi=300, bbox_inches='tight')
plt.savefig("capsid_random_vs_planar_straight_on.svg", bbox_inches='tight')
print("Saved: capsid_random_vs_planar_straight_on.png  and .svg")

# Uncomment the block below if you also want the rotating GIFs
"""
import matplotlib.animation as animation
def rotate(angle):
    ax1.view_init(elev=20, azim=angle)
    ax2.view_init(elev=20, azim=angle)
ani = animation.FuncAnimation(fig, rotate, frames=range(0,360,4), interval=100)
ani.save("capsid_comparison_rotating.gif", writer='pillow', fps=15, dpi=120)
print("Also saved rotating GIF")
"""

plt.show()