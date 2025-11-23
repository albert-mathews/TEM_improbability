#!/usr/bin/env python
"""
capsid_section_monte_carlo.py

Monte-Carlo validation of the analytic probabilities + histogram of chord sizes.
"""

import numpy as np
import matplotlib.pyplot as plt

# Same parameters as script 1
capsid_diameter = 120.0
section_thickness = 80.0
radius = capsid_diameter / 2

N_trials = 1_000_000

# Random centers uniform in z, but we only keep those that intersect the section
z_center = np.random.uniform(-radius - section_thickness, radius + section_thickness, N_trials)
z_rel = z_center - section_thickness/2          # distance from section mid-plane

intersects = np.abs(z_rel) <= radius
z_rel = z_rel[intersects]

chord_diam = 2 * np.sqrt(radius**2 - z_rel**2)

# Plot
plt.figure(figsize=(8,5))
plt.hist(chord_diam, bins=100, density=True, alpha=0.7, color='steelblue')
plt.axvline(100, color='red', linestyle='--', label='100 nm threshold')
plt.xlabel('Projected chord diameter (nm)')
plt.ylabel('Probability density')
plt.title(f'Chord diameter distribution\n'
          f'{capsid_diameter} nm capsids, {section_thickness} nm section')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

print(f"Monte-Carlo P(≥100 nm) = {np.mean(chord_diam >= 100):.5f}")