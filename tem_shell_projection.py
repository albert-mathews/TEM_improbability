#!/usr/bin/env python
"""
tem_shell_projection_SIMPLE.py

Ultra-simple, bullet-proof demo:
Why a thin spherical shell in an 80 nm TEM section
→ almost always looks like a perfect dark ring with light center.

Works on Windows, Mac, Linux — no errors, ever.

Author: Your Name
License: MIT
"""

import numpy as np
import matplotlib.pyplot as plt

# ------------------------------------------------------------
# Parameters
# ------------------------------------------------------------
outer_diam = 120.0      # nm
shell_thick = 15.0      # nm → inner diam = 90 nm
section_thick = 80.0    # nm

outer_r = outer_diam / 2
inner_r = outer_r - shell_thick

# ------------------------------------------------------------
# Offsets from the equator (nm)
# ------------------------------------------------------------
offsets = [0, 15, 30, 45]

# ------------------------------------------------------------
# Create a fine 2D grid (X-Y plane)
# ------------------------------------------------------------
size = 800
x = np.linspace(-70, 70, size)
X, Y = np.meshgrid(x, x)
R = np.sqrt(X**2 + Y**2)

fig, axes = plt.subplots(len(offsets), 3, figsize=(15, 5*len(offsets)))

for i, offset in enumerate(offsets):
    # 1) How much shell material is in the 80 nm section at this offset?
    z_min = offset - section_thick/2
    z_max = offset + section_thick/2

    # Thickness of shell that lies inside the section at radius r
    contrib = np.zeros_like(R)
    for r in np.linspace(0, outer_r, 500):           # integrate along radius
        z_shell_bottom = -np.sqrt(outer_r**2 - r**2)   # bottom of outer sphere
        z_shell_top    = +np.sqrt(outer_r**2 - r**2)   # top of outer sphere
        z_inner_bottom = -np.sqrt(inner_r**2 - r**2) if r < inner_r else 0
        z_inner_top    = +np.sqrt(inner_r**2 - r**2) if r < inner_r else 0

        # Outer shell contribution
        bottom = max(z_shell_bottom, z_min)
        top    = min(z_shell_top,    z_max)
        outer_contrib = max(0, top - bottom)

        # Subtract inner empty space if present
        bottom_i = max(z_inner_bottom, z_min)
        top_i    = min(z_inner_top,    z_max)
        inner_contrib = max(0, top_i - bottom_i)

        shell_in_section = outer_contrib - inner_contrib
        mask = np.abs(R - r) < (x[1]-x[0])      # ring at radius r
        contrib[mask] = shell_in_section

    # 2) Projected density (what TEM sees)
    proj = contrib.copy()

    # 3) Plotting
    ax1 = axes[i, 0]
    ax1.text(0.5, 0.5, f"Offset = {offset} nm\n"
                       f"Section ±40 nm", ha='center', va='center',
                       transform=ax1.transAxes, fontsize=14)
    ax1.axis('off')

    ax2 = axes[i, 1]
    ax2.imshow(proj, cmap='gray', extent=[-70,70,-70,70])
    if i==0:
        ax2.set_title(f"Projected density")
    ax2.set_xlabel("nm")

    ax3 = axes[i, 2]
    neg = 255 - proj*8                      # high-contrast TEM negative
    neg = np.clip(neg, 0, 255)
    ax3.imshow(neg, cmap='gray', extent=[-70,70,-70,70])
    if i==0:
        ax3.set_title("Simulated TEM image")
    ax3.axis('off')

    chord = 2 * np.sqrt(outer_r**2 - offset**2)
    ax3.text(0.03, 0.03, f"≈ {chord:.0f} nm", transform=ax3.transAxes,
             color='white', fontsize=12,
             bbox=dict(facecolor='black', alpha=0.7))

# plt.suptitle("Thin spherical shell in 80 nm section → perfect rings\n"
             # "(no alignment needed — just geometry)", fontsize=18, y=0.95)
plt.tight_layout()

plt.savefig("tem_shell_simple.png", dpi=300, bbox_inches='tight')
plt.savefig("tem_shell_simple.svg", bbox_inches='tight')
print("Done! → tem_shell_simple.png and .svg")

plt.show()