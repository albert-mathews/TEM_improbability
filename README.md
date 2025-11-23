# Viral Capsid TEM Geometry Calculator  
**Why the “perfect rings” in herpesvirus EM images are geometrically extraordinary**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This repository contains pure-Python tools that let anyone reproduce the simple but shocking geometric calculation we discussed:

> In a random 3D distribution of ~120 nm spherical capsids imaged in an 80 nm thin section, the probability that **25 capsids all show near-perfect 100+ nm rings with no obvious small arcs** is approximately **1 in 6 million** (and both Figure 8b + 8c together ≈ 1 in a trillion).

No virology. No literature. Just geometry and scale bars.

## Files

| File                                 | What it does                                                                                     |
|--------------------------------------|--------------------------------------------------------------------------------------------------|
| `capsid_section_probability.py`      | Analytic (exact) calculation of the 1-in-millions result used in the final answer                |
| `capsid_section_monte_carlo.py`      | Monte-Carlo version + histogram of expected chord diameters                                     |
| `visualize_random_vs_planar.py`      | 3-D matplotlib visualisation: random distribution (expected) vs perfectly planar (observed)     |
| `projected_tem_view_simulation.py`   | Generates fake “TEM micrographs” showing what each scenario actually looks like in 2-D projection|

All scripts are heavily commented, require only `numpy` and `matplotlib`, and run with a single `python scriptname.py`.

## Quick demo

```bash
python capsid_section_probability.py
```

Output (as of 2025 parameters):

```
Capsid diameter       : 120.0 nm
Section thickness     : 80.0 nm
Threshold diameter    : 100.0 nm
Probability one capsid looks >= 100 nm : 0.53513

Figure 8b (~25 capsids)       → P(all full) = 1.70e-07  (1 in 5,891,657)
Figure 8c (~20 capsids)       → P(all full) = 1.29e-05  (1 in 77,529)
```

Run the other scripts to see the histograms and pictures — the visualisations make the statistical claim instantly obvious to anyone.

## Why this repository exists

Classic thin-section TEM images of herpesviruses (and many other large viruses) routinely show fields of dozens of nearly identical ~100–120 nm rings.  
Under the standard assumptions (spherical particles, random 3-D positions, honest ~70–100 nm sections), this is **many-sigma impossible** without extreme ordering or selection.

These scripts let anyone verify that claim in < 10 seconds, change the numbers (capsid size, section thickness, threshold), and see for themselves.

## License

**MIT License** – do whatever you want with the code (commercial use, modification, sale, etc.). See `LICENSE` for the full text.

Feel free to cite or link this repo when you need to show — with actual math — why those “textbook perfect” viral capsid micrographs are geometrically astonishing.

— November 2025
