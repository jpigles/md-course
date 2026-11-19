---
title: Toy data to play with
short: Toy data
summary: Every module has a small simulation that runs in the page. Each one makes its own data, and most let you download it as a CSV file to analyse yourself.
---

Nothing here needs an installation: the simulations run in your browser. Change the sliders, break things, and when a button says "Download", take the numbers into Python. The data are generated on your machine at the moment you press the button, so every download is a little different, which is the point: do the analysis twice and see how much the answer moves.

## What is in each module

| Module | Playground | What you can change | Download |
|---|---|---|---|
| [1](01-what-is-md.html) | A live 2D Lennard-Jones fluid | Time step, thermostat on or off, temperature | `toy_lj_energies.csv`: time, kinetic, potential and total energy per particle |
| [2](02-classical-mechanics.html) | A cloud of initial conditions in phase space | System (oscillator, pendulum, double well), friction | none (watch the area) |
| [3](03-statistical-mechanics.html) | A particle building the Boltzmann distribution | Potential, temperature | `boltzmann_samples.csv`: sample, x, U/k_BT |
| [4](04-integrators.html) | Three integrators on one spring | Time step | none |
| [5](05-force-field-form.html) | Lennard-Jones and Coulomb pair energy | ε, σ, charge product | none |
| [6](06-force-field-parameters.html) | Fitting torsion parameters to a toy quantum scan | k₁, k₂, k₃, or a least-squares fit | `toy_torsion_scan.csv`: dihedral angle, energy |
| [7](07-boundaries-electrostatics.html) | The Ewald split of 1/r | α, cutoff | none |
| [8](08-thermostats-barostats.html) | What each thermostat does to temperature fluctuations | Thermostat, coupling time | `thermostat_temperature.csv`: time, instantaneous temperature |
| [9](09-constraints.html) | Flexible bonds against SHAKE | Time step | none |
| [10](10-running-a-simulation.html) | System-size calculator | Protein size, padding, box shape, salt, run length | none |
| [11](11-analysis-statistics.html) | Correlated data and block averaging | Correlation time, number of frames | `toy_rg_series.csv`: frame, toy radius of gyration |
| [12](12-free-energy-pmf.html) | Umbrella sampling and WHAM on a double well | Barrier, number of windows, spring constant | `toy_umbrella_windows.csv`: window centre, spring constant, bin, count |
| [13](13-alchemical-free-energy.html) | Free-energy perturbation against BAR | Shift and stiffness of the second state, sample size | `toy_fep_samples.csv`: state, x, ΔU/k_BT |
| [14](14-enhanced-sampling.html) | Well-tempered metadynamics | Barrier, bias factor, hill height and width | none |
| [15](15-coarse-grained.html) | Contact potentials and salt screening | Ionic strength, dielectric constant | none |
| [16](16-kinetics-msm.html) | A Markov state model from a toy trajectory | Well depth, trajectory length | `toy_three_well_trajectory.csv`: frame, time, x |
| [17](17-machine-learning.html) | A neural network fitted to toy energies | Training range, number of points | none |

## Six things to do with the downloads

All of these need only NumPy. `np.loadtxt(name, delimiter=",", skiprows=1)` reads any of the files (for the FEP file, which has a text column, use `np.genfromtxt(..., dtype=None, encoding=None, names=True)`).

### 1. Check energy conservation (Module 1 and 4)

```python
import numpy as np
t, k, u, e = np.loadtxt("toy_lj_energies.csv", delimiter=",", skiprows=1).T
print("total energy: mean %.4f, standard deviation %.5f" % (e.mean(), e.std()))
print("kinetic energy standard deviation is %.0f times larger" % (k.std() / e.std()))
```

Download once with a time step of 0.005 and once with 0.02, thermostat off. The standard deviation of the total energy should grow by about 16 (the square of the ratio of the time steps).

### 2. Recover a potential from samples (Module 3)

```python
import numpy as np
i, x, u = np.loadtxt("boltzmann_samples.csv", delimiter=",", skiprows=1).T
h, edges = np.histogram(x, bins=60, density=True)
centres = 0.5 * (edges[1:] + edges[:-1])
F = -np.log(h[h > 0])                    # free energy in units of k_BT
F -= F.min()
print(np.c_[centres[h > 0], F][::6])
```

Compare `F` with the potential you chose. Then repeat at a low temperature, where the particle never crossed: the right-hand well is simply missing.

### 3. Fit the torsion yourself (Module 6)

```python
import numpy as np
phi, E = np.loadtxt("toy_torsion_scan.csv", delimiter=",", skiprows=1).T
r = np.radians(phi)
A = np.c_[np.ones_like(r), 1 + np.cos(r), 1 + np.cos(2 * r - np.pi), 1 + np.cos(3 * r)]
coef, res, *_ = np.linalg.lstsq(A, E, rcond=None)
print("offset, k1, k2, k3 =", np.round(coef, 2), " RMS error =", np.sqrt(np.mean((A @ coef - E) ** 2)).round(2))
```

This is the least-squares button of the demo. The RMS error should come out close to the 0.35 kJ/mol of noise that was added.

### 4. Find the real error bar (Module 11)

```python
import numpy as np
frame, rg = np.loadtxt("toy_rg_series.csv", delimiter=",", skiprows=1).T
for nb in (5, 10, 20, 40, 80, 160, 320):
    m = len(rg) // nb
    means = rg[: m * nb].reshape(nb, m).mean(axis=1)
    print("block length %6d  standard error %.5f" % (m, means.std(ddof=1) / np.sqrt(nb)))
print("naive standard error       %.5f" % (rg.std(ddof=1) / np.sqrt(len(rg))))
```

The block estimate rises with block length and flattens. Where it flattens is the error bar, and it is far larger than the naive one.

### 5. Write your own WHAM (Module 12)

```python
import numpy as np
c, k, x, n = np.loadtxt("toy_umbrella_windows.csv", delimiter=",", skiprows=1).T
centres, xs = np.unique(c), np.unique(x)
H = n.reshape(len(centres), len(xs))             # counts: one row per window
N = H.sum(axis=1)
bias = 0.5 * k[0] * (xs[None, :] - centres[:, None]) ** 2
f = np.zeros(len(centres))
for it in range(2000):
    P = H.sum(axis=0) / (N[:, None] * np.exp(-(bias - f[:, None]))).sum(axis=0)
    f_new = -np.log((P[None, :] * np.exp(-bias)).sum(axis=1))
    if np.abs(f_new - f).max() < 1e-7:
        break
    f = f_new
F = -np.log(P[P > 0]); F -= F.min()
print(np.c_[xs[P > 0], F][::6])
```

These are the two boxed equations of Module 12, iterated until they stop changing. Compare `F` with `h * (xs**2 - 1)**2` for the barrier you set.

### 6. Three free-energy estimators (Module 13)

```python
import numpy as np
d = np.genfromtxt("toy_fep_samples.csv", delimiter=",", names=True, dtype=None, encoding=None)
dA, dB = d["dU_over_kBT"][d["sampled_in_state"] == "A"], d["dU_over_kBT"][d["sampled_in_state"] == "B"]
fwd = -np.log(np.mean(np.exp(-dA)))
rev = np.log(np.mean(np.exp(dB)))
lo, hi = -60.0, 60.0
for _ in range(60):                              # bisection on the BAR equation
    C = 0.5 * (lo + hi)
    g = np.sum(1 / (1 + np.exp(dA - C))) - np.sum(1 / (1 + np.exp(-(dB - C))))
    lo, hi = (lo, C) if g > 0 else (C, hi)
print("FEP from A %.2f   FEP from B %.2f   BAR %.2f   (units of k_BT)" % (fwd, rev, 0.5 * (lo + hi)))
```

The exact answer is half the logarithm of the stiffness you set. Download with a large shift and few samples and watch the two one-sided estimates disagree while BAR stays close.

## Building a transition matrix (Module 16)

```python
import numpy as np
frame, t, x = np.loadtxt("toy_three_well_trajectory.csv", delimiter=",", skiprows=1).T
states = np.digitize(x, [-0.7, 0.7])             # three states: left, middle, right
for lag in (1, 10, 100):
    C = np.zeros((3, 3))
    np.add.at(C, (states[:-lag], states[lag:]), 1)
    C = 0.5 * (C + C.T)                          # symmetrise the counts (a simple reversible estimate)
    T = C / C.sum(axis=1, keepdims=True)
    ev = np.sort(np.linalg.eigvals(T).real)[::-1]
    dt = t[1] - t[0]
    print("lag %4d  slowest implied time scale %.1f" % (lag, -lag * dt / np.log(ev[1])))
```

With only three states the time scale keeps rising with the lag: three states are too coarse to be Markovian at short lags. Use thirty bins instead and it levels off sooner, as in the demo.
