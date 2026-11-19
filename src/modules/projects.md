---
title: Capstone projects
short: Projects
summary: Eight projects, from a molecular dynamics program you write yourself to a binding free energy, each with a concrete deliverable and a way to check the answer.
---

Reading derivations builds familiarity. Building the thing builds understanding. Each project below states what to produce and how you will know it is right. The first four need only Python and NumPy. The last four need an MD package and a GPU or a cluster allocation.

## Project 1. Your own MD engine

**Modules 1, 4, 7, 8.** Extend the 35-line program of Module 1 into a small but complete code for a Lennard-Jones fluid in three dimensions.

- Add a cell list or Verlet neighbour list.
- Add a Langevin (BAOAB) thermostat, with the option to switch it off.
- Compute temperature, pressure (from the virial) and the radial distribution function.

**Check.** In NVE, the fluctuation of the total energy must scale as $\Delta t^2$. In NVT at reduced temperature 1.0 and density 0.8, the mean potential energy per particle and the pressure must match published values for the truncated Lennard-Jones fluid (tables are in Frenkel and Smit and in the NIST reference simulation data). The first peak of $g(r)$ should be near $r=1.1\,\sigma$ with a height close to 2.7.

## Project 2. Three integrators, one pendulum

**Modules 2, 4.** For the non-linear pendulum, implement forward Euler, velocity Verlet and fourth-order Runge-Kutta.

- Plot energy against time over 10,000 periods for each, at equal cost (four Verlet steps per Runge-Kutta step).
- Plot the phase portrait of each.
- For velocity Verlet on the harmonic oscillator, verify numerically that $\tfrac12v^2+\tfrac12\omega^2(1-\tfrac14\omega^2\Delta t^2)x^2$ is conserved to round-off.

**Check.** Euler's energy grows without bound, Runge-Kutta's drifts monotonically, Verlet's oscillates within a fixed band.

## Project 3. Umbrella sampling and WHAM from scratch

**Modules 8, 11, 12.** One particle in the double well $U(x)=h(x^2-1)^2$ with overdamped Langevin dynamics.

- Run plain dynamics and show the histogram-based free energy fails for $h=10\,k_BT$.
- Run umbrella windows, write WHAM yourself (the two boxed equations of Module 12, iterated), and recover $U(x)$.
- Estimate error bars by repeating the whole calculation ten times with different seeds.
- Repeat the analysis with `pymbar`.

**Check.** The recovered profile agrees with the exact potential within your error bars everywhere, and the error bars shrink as $1/\sqrt{\text{run length}}$.

## Project 4. Rates three ways

**Modules 14, 16.** Same double well.

- Measure the crossing rate directly by counting transitions in long runs for $h$ = 3, 4, 5, 6 $k_BT$.
- Compare with the Kramers high-friction formula and with the mean first-passage time integral.
- Build a Markov state model from many short trajectories for $h=8\,k_BT$, where direct counting is too slow, and predict the rate. Validate with implied time scales.

**Check.** For this potential the Kramers prefactor is itself proportional to $h$ (the curvatures at the well and at the barrier top are $8h$ and $4h$), so $k\propto h\,e^{-h}$. A plot of $\ln(k/h)$ against $h$, with $h$ in units of $k_BT$, is a straight line of slope $-1$; a plot of $\ln k$ alone is curved, with slope $-1+1/h$. The three estimates agree where they overlap.

## Project 5. A protein in water, done properly

**Modules 6, 10, 11.** Choose a small, well-studied protein (ubiquitin, lysozyme, the GB1 domain).

- Prepare, solvate, neutralise, minimise, equilibrate and run three repeats of 100 ns or more.
- Report backbone RMSD, per-residue RMSF against crystallographic B-factors, radius of gyration, and secondary structure over time.
- Give every average with a standard error from block averaging and from the three repeats, and compare the two.
- Write a methods section that meets the reporting list of Module 10.

**Check.** The three repeats agree within their error bars for global observables. If they do not, find out why: that is the result.

## Project 6. Hydration free energy of a small molecule

**Module 13.** Compute the hydration free energy of ethanol or of another neutral small molecule by alchemical decoupling.

- Use about 20 $\lambda$ windows, charges first, then Lennard-Jones with soft-core.
- Analyse with thermodynamic integration, BAR and MBAR.
- Show the overlap matrix and a forward-and-reverse convergence plot.

**Check.** The three estimators agree within their uncertainties, and the result is within about 4 kJ/mol of the experimental value (ethanol: about $-21$ kJ/mol). The FreeSolv database has experimental and reference calculated values for hundreds of molecules.

## Project 7. Binding free-energy profile of a small complex

**Modules 12, 14.** Choose a small host-guest pair or a short peptide bound to a protein domain.

- Generate starting configurations by pulling the partners apart slowly.
- Run umbrella sampling along the centre-of-mass distance, with exchange between windows if your software supports it.
- Remove the Jacobian, integrate the profile to obtain $K_d$ with the 1 M standard state, and state exactly which restraints were or were not applied.
- Estimate uncertainty from independent repeats, and check hysteresis by also generating windows in the association direction.

**Check.** The profile is flat at large separation. The result does not change beyond its error bar when the first half of each window is discarded. Compare with experiment and discuss which of the three kinds of error (Module 1) is most likely to dominate the difference.

## Project 8. One system at three resolutions

**Modules 15, 17.** Take one short disordered peptide or a small fast-folding protein.

- Simulate it all-atom in explicit water.
- Simulate it with a coarse-grained model suited to it: a C$\alpha$ structure-based model for the folder, or a residue-level model such as CALVADOS for the disordered peptide.
- Generate an ensemble with a machine-learned ensemble emulator.
- Compare the radius of gyration distribution, the contact map and one experimental observable across the three.

**Check.** You can state, with numbers and error bars, what each resolution gets right, what it gets wrong, and what it cost in computer time.
