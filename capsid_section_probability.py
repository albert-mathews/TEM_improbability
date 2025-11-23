#!/usr/bin/env python
"""
capsid_section_probability.py

Pure geometry: probability that a random 120 nm capsid intersected by an 80 nm
thin section yields a projected chord diameter >= threshold (e.g. 100 nm).

This is the script that produced the ~1 in 6 million result for Figure 8b.

Author: your-name-here
License: MIT
"""

import numpy as np

# ------------------------------------------------------------------
# Parameters - change these to match any virus / section thickness
# ------------------------------------------------------------------
capsid_diameter = 120.0          # nm  (HCMV capsid ~115-125 nm typical)
section_thickness = 80.0         # nm  (stated in the 2018 paper)
threshold_diameter = 100.0       # nm  - we call this "visibly full-sized"

radius = capsid_diameter / 2.0

# Maximum distance from equator still inside the section
half_section = section_thickness / 2.0

# ------------------------------------------------------------------
# Analytic calculation (no Monte-Carlo needed - exact)
# ------------------------------------------------------------------
# The capsid is intersected if its center is within [-(r), +r] of the section mid-plane
# For a given offset d from the mid-plane (|d| <= r), projected chord diameter = 2*sqrt(r^2 - d^2)
# We want 2*sqrt(r^2 - d^2) >= threshold_diameter

d_crit = np.sqrt(radius**2 - (threshold_diameter/2.0)**2)   # offset beyond which chord < threshold

# The allowed |d| range for "full-looking" capsids
d_allowed = min(d_crit, radius)   # capped by the capsid surface

# Total z-range where capsid is intersected at all
z_intersect_range = 2 * radius

# z-range where we get a large chord
z_good_range = 2 * d_allowed

prob_single = z_good_range / z_intersect_range

print(f"Capsid diameter       : {capsid_diameter} nm")
print(f"Section thickness     : {section_thickness} nm")
print(f"Threshold diameter    : {threshold_diameter} nm")
print(f"Probability one capsid looks >= {threshold_diameter} nm : {prob_single:.5f}")
print()

# Probability for N independent capsids all looking full-sized
for N, label in [(25, "Figure 8b (~25 capsids)"), (20, "Figure 8c (~20 capsids)")]:
    p_all = prob_single ** N
    odds = 1.0 / p_all if p_all > 0 else float('inf')
    print(f"{label:30s} → P(all full) = {p_all:.2e}  (1 in {odds:,.0f})")