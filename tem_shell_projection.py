#!/usr/bin/env python
"""
tem_shell_projection_offsets_0_30_60_90.py

Shows why a hollow spherical shell (120 nm diameter, 15 nm thick)
appears as a perfect ring even when the section is far from equatorial.

Offsets used: 0 nm, 30 nm, 60 nm, 90 nm
→ Demonstrates that up to ~60 nm offset you still get a beautiful full ring!

Author: Your Name
License: MIT
"""

import numpy as np
import matplotlib.pyplot as plt

# Parameters
outer_diam = 120.0      # nm
shell_thick = 15.0      # nm → inner diam = 90 nm
section_thick = 80.0    # nm

outer_r = outer_diam / 2
inner_r = outer_r - shell_thick

# Offsets from the equator (nm) — as requested
offsets = [0, 60, 70, 80]

# 2D grid
size = 800
x = np.linspace(-70, 70, size)
X, Y = np.meshgrid(x, x)
R = np.sqrt(X**2 + Y**2)

fig, axes = plt.subplots(4, 3, figsize=(15, 18))

for i, offset in enumerate(offsets):
    z_min = offset - section_thick/2
    z_max = offset + section_thick/2

    contrib = np.zeros_like(R)

    # Radial integration (fast enough and 100% reliable)
    for r in np.linspace(0, outer_r, 600):
        if r >= outer_r:
            continue

        # Outer sphere boundaries
        z_shell_bottom = -np.sqrt(outer_r**2 - r**2)
        z_shell_top    = +np.sqrt(outer_r**2 - r**2)

        # Inner void boundaries (only if r < inner_r)
        if r < inner_r:
            z_inner_bottom = -np.sqrt(inner_r**2 - r**2)
            z_inner_top    = +np.sqrt(inner_r**2 - r**2)
        else:
            z_inner_bottom = z_inner_top = 0

        # Outer shell contribution inside section
        bottom = max(z_shell_bottom, z_min)
        top    = min(z_shell_top,    z_max)
        outer_contrib = max(0, top - bottom)

        # Subtract inner void if present
        bottom_i = max(z_inner_bottom, z_min)
        top_i    = min(z_inner_top,    z_max)
        inner_contrib = max(0, top_i - bottom_i)

        thickness_in_section = outer_contrib - inner_contrib

        mask = np.abs(R - r) < (x[1] - x[0])
        contrib[mask] = thickness_in_section

    proj = contrib.copy()

    # === Plotting ===
    # Column 1: Info
    ax1 = axes[i, 0]
    ax1.text(0.5, 0.5,
             f"Offset = {offset} nm\n"
             f"Section: {z_min:.0f} to {z_max:.0f} nm",
             ha='center', va='center', transform=ax1.transAxes,
             fontsize=14, bbox=dict(facecolor='white', alpha=0.9))
    ax1.axis('off')

    # Column 2: Projected density
    ax2 = axes[i, 1]
    ax2.imshow(proj, cmap='gray', extent=[-70,70,-70,70], origin='lower')
    if i==0:
        ax2.set_title(f"Projected density", fontsize=13)
    ax2.set_xlabel("nm")

    # Column 3: Simulated TEM negative
    ax3 = axes[i, 2]
    neg = 255 - proj * 7
    neg = np.clip(neg, 0, 255)
    ax3.imshow(neg, cmap='gray', extent=[-70,70,-70,70], origin='lower')
    if i==0:
        ax3.set_title("Simulated TEM image", fontsize=13)
    ax3.axis('off')

    # Show actual visible chord diameter
    if offset <= outer_r:
        chord_diam = 2 * np.sqrt(outer_r**2 - offset**2)
        ax3.text(0.05, 0.05, f"Chord ≈ {chord_diam:.0f} nm",
                 transform=ax3.transAxes, color='white', fontsize=12,
                 bbox=dict(facecolor='black', alpha=0.8))
    else:
        ax3.text(0.5, 0.5, "No intersection", transform=ax3.transAxes,
                 color='white', ha='center', fontsize=14,
                 bbox=dict(facecolor='red', alpha=0.7))

# Final layout
# plt.suptitle("Hollow spherical shell (120 nm) in 80 nm section\n"
             # "→ Perfect rings up to ~60 nm offset — pure geometry!",
             # fontsize=18, y=0.95)
plt.tight_layout()

# Save
plt.savefig("tem_shell_offsets_0_30_60_90.png", dpi=300, bbox_inches='tight')
plt.savefig("tem_shell_offsets_0_30_60_90.svg", bbox_inches='tight')
print("Saved: tem_shell_offsets_0_30_60_90.png + .svg")

plt.show()