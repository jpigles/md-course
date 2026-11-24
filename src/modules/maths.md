---
title: Maths toolbox
short: Maths toolbox
summary: Every piece of mathematics the course uses, explained from zero with worked numbers. Read it once from top to bottom, or arrive from a link in a lesson, read one section and go back.
---

This page explains the mathematics that the 18 lessons use, starting from school level. A lesson explains a new tool briefly at the place where it needs it, and links here for the longer version.

There are two ways to use the page. You can read it once from top to bottom, before or alongside Modules 1 to 4: the sections build on each other in the order given. Or you can arrive from a link in a lesson, read one section, and go back.

Every section has the same parts, in the same order: the idea in plain words, the notation and how to read it aloud, one or more worked examples with numbers that you can check by hand, the lessons that use the tool, and a common mistake. You do not need to be fast at these calculations. You need to recognise each symbol when it appears and to know what it asks you to do.

The physics background (units, energy, temperature, charges) is on a separate page, the [physics primer](physics.html#units).

**Reading formulas, and three basic functions**

- [How to read a formula](#notation)
- [Functions and graphs](#functions)
- [Exponential and logarithm](#exp-log)

**Rates of change and sums: calculus**

- [The derivative](#derivative)
- [The chain rule](#chain-rule)
- [Partial derivatives](#partial-derivative)
- [The gradient](#gradient)
- [Divergence and Laplacian](#divergence)
- [The integral](#integral)
- [Taylor expansion](#taylor)

**Quantities with a direction: vectors and matrices**

- [Vectors](#vectors)
- [The dot product](#dot-product)
- [The cross product](#cross-product)
- [Matrices](#matrices)
- [Eigenvalues and eigenvectors](#eigen)

**Oscillation and change in time**

- [Complex numbers](#complex)
- [Differential equations](#ode)
- [Operators](#operators)

**Chance**

- [Probability and densities](#probability)
- [Mean, variance, standard error](#averages)
- [The Gaussian](#gaussian)
- [Delta functions](#delta)

**Special tools**

- [Fourier series and transforms](#fourier)
- [Lagrange multipliers](#lagrange-multipliers)
- [The Legendre transform](#legendre)
- [Counting and Stirling's formula](#combinatorics)
- [Least squares and fitting](#fitting)
- [Random numbers and noise](#random-numbers)

## How to read a formula {#notation}

**The idea.** A formula is a sentence written in symbols. It has nouns (quantities such as a position or an energy), verbs (operations such as "add up" or "take the slope") and small marks that change the meaning of a letter, the way an accent does. Most of the difficulty of reading a formula is in the small marks. This section lists them. Each operation has its own section further down.

Take Newton's law as the course writes it, $m_i\,\ddot{\mathbf r}_i = \mathbf F_i$. The small $i$ says "for atom number $i$". The bold letters say "this quantity has a direction". The two dots say "how fast the velocity is changing". Read aloud: "the mass of atom $i$ times its acceleration equals the force on atom $i$".

**The notation.** First the marks that are attached to a letter.

| You see | Read it as | It means |
|---|---|---|
| $x_i$ | "x i" or "x sub i" | A **subscript** is a label. $x_i$ is the $x$ of item number $i$, for example of atom $i$. A subscript can also be a letter or a word that names a thing: $k_B$ is Boltzmann's constant, $r_c$ a cutoff distance. |
| $r_{ij}$ | "r i j" | Two labels: a quantity that belongs to a pair, here the distance between atoms $i$ and $j$. |
| $x^2$, $x^{-1}$, $x^{1/2}$ | "x squared", "x to the minus one", "x to the one half" | A **superscript** is usually a power. $x^{-1}$ is $1/x$ and $x^{1/2}$ is $\sqrt{x}$. |
| $\mathbf r^N$, $U^{b}$ | "r N", "U b" | Sometimes a superscript is a label and not a power: $\mathbf r^N$ stands for the positions of all $N$ atoms, $U^{b}$ for a biased energy. The text says so when this happens. |
| $\mathbf r$ | "vector r" | Bold: a [vector](#vectors), a quantity with a direction, stored as three numbers. A [matrix](#matrices) is also written in bold, usually as a capital ($\mathbf A$, $\mathbf T$). The list under the formula says which of the two a bold letter is. |
| $\dot x$, $\ddot x$ | "x dot", "x double dot" | Dots: [derivatives](#derivative) with respect to time. $\dot x$ is $dx/dt$. |
| $\hat{\mathbf r}$ | "r hat" | A hat on a bold letter: a unit vector, of length 1. A hat on another letter marks an estimate from data or an [operator](#operators). |
| $\tilde\rho$ | "rho tilde" | A tilde: a changed version of the same quantity, for example its [Fourier transform](#fourier) or a mass-weighted coordinate. |
| $\bar x$ | "x bar" | A bar over a letter: the average of the data you have. |
| $x'$ | "x prime" | A prime: either a second value of the same kind of quantity ($t$ and $t'$ are two times), or the derivative of a function ($f'$). |
| $\Delta x$ | "delta x" | Capital delta: a difference, final value minus initial value. $\Delta t$ is the time step. |
| $\delta x$, $dx$ | "delta x", "d x" | A small, or infinitely small, change of $x$. In statistics, $\delta A$ is the deviation of $A$ from its mean. |
| $\lvert x\rvert$ | "absolute value of x" | Bars around a number: its size without the sign. $\lvert -3\rvert = 3$. |
| $\lvert\mathbf r\rvert$ | "length of r" | Bars around a vector: its length. Often written as the same letter without bold, $r$. |
| $\langle A\rangle$ | "the average of A" | Angle brackets: the [mean](#averages) over an ensemble or over a trajectory. A subscript says which one. |
| $f(x)$ | "f of x" | Round brackets after the name of a [function](#functions): what the function depends on. It is not a multiplication. |
| $f\vert_{x_0}$ | "f at x zero" | A vertical bar with a subscript after an expression: evaluate it at this value. |
| $P(A\mid B)$ | "probability of A given B" | A bar inside a probability: a [condition](#probability). |

Then the signs that stand between two expressions.

| Sign | Read it as | Meaning |
|---|---|---|
| $=$ | "equals" | Both sides are the same. |
| $\equiv$ | "is defined as" | The left side is a new name for the right side. |
| $\approx$ | "is approximately" | Equal up to a small error. |
| $\sim$ | "is of the order of", or "is distributed as" | Roughly this size, within a factor of a few. For a random number: it follows this distribution. |
| $\propto$ | "is proportional to" | The left side doubles when the right side doubles. A constant factor has been left out. |
| $\ne$ | "is not equal to" | |
| $\le$, $\ge$ | "at most", "at least" | Smaller than or equal to, larger than or equal to. |
| $\ll$, $\gg$ | "much smaller than", "much larger than" | So different in size that the smaller one can be neglected. |
| $\to$ | "goes to" | $t\to\infty$: as $t$ grows without limit. |
| $\leftarrow$ | "is replaced by" | In an algorithm: compute the right side and store it under the name on the left. |
| $\Rightarrow$ | "it follows that" | |
| $\pm$ | "plus or minus" | |
| $\in$ | "in" | $i\in A$: $i$ is one of the members of the set $A$. |
| $\infty$ | "infinity" | Larger than any number. |

Two verbs appear in almost every formula of the course, the sum and the product:

$$
\sum_{i=1}^{N} a_i = a_1 + a_2 + \dots + a_N , \qquad \prod_{i=1}^{N} a_i = a_1 \times a_2 \times \dots \times a_N .
$$

<div class="legend" markdown="1">
- $\sum$: capital Greek sigma, for "sum". Add up the expression that follows for every value of the label.
- $\prod$: capital Greek pi, for "product". Multiply where the sum adds.
- $i$: the label that runs. It is a counter and has no meaning outside the sum. Any other letter would give the same result.
- $i=1$ below the sign and $N$ above it: the first and the last value of the label. When they are left out, as in $\sum_i$, the sum runs over all values that make sense, for example over all atoms.
- $a_i$: the term for one value of $i$.
- $\dots$: "and so on".
</div>

Sums over pairs of atoms come in two forms. $\sum_{i<j}$ takes each pair once. $\sum_{i\ne j}$ takes each pair twice, once as $(i,j)$ and once as $(j,i)$, and is then usually multiplied by $\tfrac12$. A double sum $\sum_i\sum_j$ means: for each value of $i$, add up over all values of $j$.

<div class="box key" markdown="1">
**Worked example.** $\sum_{i=1}^{4} i^2 = 1 + 4 + 9 + 16 = 30$ and $\prod_{i=1}^{4} i = 1\times2\times3\times4 = 24$.

For four atoms, $\sum_{i<j}$ runs over the six pairs 1-2, 1-3, 1-4, 2-3, 2-4 and 3-4. For $N$ atoms there are $N(N-1)/2$ pairs, which is 499,500 for 1000 atoms.

The average of the three numbers 2, 4 and 9 is $\bar x = (2+4+9)/3 = 5$.
</div>

**The Greek alphabet.** Formulas run out of Latin letters quickly, so Greek ones are used too. The last column gives the usual meanings in this course. A letter can have several, and the list under each formula says which one applies.

| Small | Capital | Name | Usual meaning in this course |
|---|---|---|---|
| $\alpha$ | A | alpha | a constant that sets a width or a strength (Modules 7 and 13) |
| $\beta$ | B | beta | $\beta = 1/k_BT$, the inverse temperature |
| $\gamma$ | $\Gamma$ | gamma | $\gamma$: a friction coefficient. $\Gamma$: one point in phase space |
| $\delta$ | $\Delta$ | delta | $\delta$: a small change, or a [delta function](#delta). $\Delta$: a difference |
| $\epsilon$, $\varepsilon$ | E | epsilon | the depth of an energy well; a dielectric constant; any small number |
| $\zeta$ | Z | zeta | rarely used |
| $\eta$ | H | eta | a random force; a viscosity |
| $\theta$ | $\Theta$ | theta | $\theta$: an angle, or the parameters of a machine-learning model. $\Theta$: the [step function](#delta) |
| $\iota$ | I | iota | not used |
| $\kappa$ | K | kappa | $\kappa_T$, the compressibility; a transmission coefficient (Module 16) |
| $\lambda$ | $\Lambda$ | lambda | $\lambda$: a [Lagrange multiplier](#lagrange-multipliers), a coupling parameter, an [eigenvalue](#eigen), a wavelength. $\Lambda$: the thermal wavelength |
| $\mu$ | M | mu | a reduced mass; a mean; a dipole moment (Module 6); a chemical potential (Module 3) |
| $\nu$ | N | nu | a frequency |
| $\xi$ | $\Xi$ | xi | $\xi$: a collective variable, a thermostat variable, or a random number. $\Xi$: the virial |
| o | O | omicron | not used, because it looks like the Latin o |
| $\pi$ | $\Pi$ | pi | $\pi$: the number 3.14159..., or an equilibrium distribution. $\prod$: the product sign |
| $\rho$ | P | rho | a density |
| $\sigma$ | $\Sigma$ | sigma | $\sigma$: an atomic diameter, a standard deviation, or a constraint. $\sum$: the sum sign |
| $\tau$ | T | tau | a time constant; a lag time |
| $\upsilon$ | $\Upsilon$ | upsilon | not used |
| $\phi$, $\varphi$ | $\Phi$ | phi | a dihedral angle; the electrostatic potential |
| $\chi$ | X | chi | $\chi^2$, the quantity made small in a [fit](#fitting); a side-chain dihedral angle |
| $\psi$ | $\Psi$ | psi | a dihedral angle of the protein backbone |
| $\omega$ | $\Omega$ | omega | $\omega$: an angular frequency, or an improper dihedral angle (Module 5). $\Omega$: the number of microstates |

**Where the course uses it.**

- All 18 lessons use these conventions.
- [Module 2](02-classical-mechanics.html), Classical mechanics: has a short table of the marks that appear first there (bold letters, dots, partial derivatives).

<div class="box warn" markdown="1">
**A common mistake.** Reading a label as a power or as a product. $\mathbf r^N$ is not "r to the power N", $f(x)$ is not "f times x", and in $k_BT$ the $B$ is a label on $k$ while the $T$ is a separate quantity that multiplies it. When a letter carries a mark you do not recognise, look it up in the list under the formula before you read on.
</div>

## Functions and graphs {#functions}

**The idea.** A function is a rule that takes a number and returns a number. Think of a machine with an input and an output: put in a bond length, get out an energy. The potential energy of a molecule is a function of the positions of its atoms, and a time series is a function of time. A graph is a picture of the rule, with the input on the horizontal axis and the output on the vertical axis.

**The notation.** $f(x)$, read "f of x", is the output of the function $f$ for the input $x$. The input is called the **argument** or the **variable**. A function of several variables takes several inputs: $U(\mathbf r_1,\dots,\mathbf r_N)$ needs all the positions to return one energy. Letters in the rule that stay fixed while the variable changes are **parameters**.

The simplest function is the straight line:

$$
f(x) = a\,x + b .
$$

<div class="legend" markdown="1">
- $x$: the variable, the input.
- $f(x)$: the value of the function for that input, the output.
- $a$: the **slope**. It says how much $f$ changes when $x$ grows by 1. A negative $a$ means that the line goes down to the right.
- $b$: the **intercept**, the value of $f$ at $x = 0$.
</div>

For any function, the slope between two points on its graph is the change of the output divided by the change of the input:

$$
\text{slope} = \frac{f(x_2) - f(x_1)}{x_2 - x_1} = \frac{\Delta f}{\Delta x} .
$$

<div class="legend" markdown="1">
- $x_1$, $x_2$: two values of the input.
- $f(x_1)$, $f(x_2)$: the outputs at these two values.
- $\Delta f$, $\Delta x$: the two differences. $\Delta$ is read "the change of".
</div>

For a straight line this ratio is $a$ wherever you take the two points. For a curve it depends on where you measure, and [the derivative](#derivative) is the tool that deals with that.

**Units.** The input and the output each have a unit, and the slope has the unit of the output divided by the unit of the input. An energy in kJ/mol as a function of a distance in nm has a slope in kJ mol$^{-1}$ nm$^{-1}$, which is the unit of a force. The exponential $e^x$ and the logarithm $\ln x$ of [the next section](#exp-log), and the sine and the cosine, accept only pure numbers, with no unit. This is why an energy inside an exponential is always divided by $k_BT$, which is also an energy. Angles inside a sine or a cosine are in radians: 180 degrees is $\pi$ radians.

<div class="box key" markdown="1">
**Worked example.** A bond is modelled as a spring, $U(r) = \tfrac12 k\,(r-r_0)^2$, with, say, $k = 1000$ kJ mol$^{-1}$ nm$^{-2}$ and $r_0 = 0.15$ nm. The variable is the bond length $r$. The stiffness $k$ and the rest length $r_0$ are parameters.

| $r$ (nm) | 0.14 | 0.15 | 0.16 | 0.17 |
|---|---|---|---|---|
| $U$ (kJ/mol) | 0.05 | 0 | 0.05 | 0.20 |

The graph is a parabola with its lowest point at $r = r_0$. Between 0.16 and 0.17 nm the slope is $(0.20 - 0.05)/(0.17 - 0.16) = 15$ kJ mol$^{-1}$ nm$^{-1}$. Between 0.15 and 0.16 nm it is 5 in the same unit. The curve gets steeper as the bond is stretched further.
</div>

**Where the course uses it.**

- [Module 1](01-what-is-md.html), What MD is: the potential energy $U(\mathbf r)$ is a function of all atomic positions.
- [Module 5](05-force-field-form.html), The form of a force field: every term of the energy is a function of one distance or one angle, with a few parameters.
- [Module 6](06-force-field-parameters.html), Force-field parameters: where the values of the parameters come from.
- [Module 11](11-analysis-statistics.html), Analysis and statistics: the radial distribution function $g(r)$ and the correlation function $c(t)$.
- [Module 12](12-free-energy-pmf.html), Free energy and the potential of mean force: a free energy as a function of one chosen coordinate.

<div class="box warn" markdown="1">
**A common mistake.** Putting a quantity with a unit into an exponential, a logarithm or a cosine. If you find yourself computing $e^{-U}$ with $U$ in kJ/mol, a division by $k_BT$ is missing. A second one: confusing the variable with the parameters. For the spring above, a plot of $U$ against $r$ at fixed $k$ is a parabola, and a plot of $U$ against $k$ at fixed $r$ is a straight line.
</div>

## Exponential and logarithm {#exp-log}

**The idea.** Some quantities change at a rate proportional to their own size. A colony of bacteria with plenty of food doubles in a fixed time, whatever its size. A set of bound ligands, each with the same chance of leaving per second, shrinks by the same *fraction* every second. Growth or decay of this kind is **exponential**: equal steps of time multiply the quantity by equal factors. The logarithm asks the reverse question: how many steps are needed to reach a given factor?

In this course the exponential appears for a second reason. At temperature $T$, the probability of a state of energy $E$ is proportional to $e^{-E/k_BT}$, the Boltzmann factor of Module 3. Every free energy in the course is $-k_BT$ times the logarithm of a probability, or of a sum of such factors.

**The notation.** $e = 2.71828\ldots$ is a fixed number, like $\pi$. $e^x$ is "e to the power x". It is also written $\exp(x)$, which is easier to read when the exponent is long.

$\ln x$ is the **natural logarithm**: the power to which $e$ must be raised to give $x$. So $\ln(e^x) = x$ and $e^{\ln x} = x$. The logarithm exists only for $x > 0$.

| Rule | Example |
|---|---|
| $e^{a+b} = e^{a}\,e^{b}$ | $e^{3} = e^{2}\,e^{1} = 7.39\times2.72 = 20.1$ |
| $e^{-a} = 1/e^{a}$ | $e^{-1} = 1/2.718 = 0.368$ |
| $(e^{a})^{b} = e^{ab}$ | $(e^{2})^{3} = e^{6}$ |
| $e^{0} = 1$ | |
| $\ln(ab) = \ln a + \ln b$ | $\ln 2 + \ln 5 = 0.69315 + 1.60944 = 2.30259 = \ln 10$ |
| $\ln(a/b) = \ln a - \ln b$ | $\ln(1/2) = -\ln 2 = -0.693$ |
| $\ln(a^{n}) = n\ln a$ | $\ln 8 = 3\ln 2 = 2.079$ |
| $\ln 1 = 0$ and $\ln e = 1$ | |
| $\log_{10}x = \ln x/\ln 10 = \ln x/2.303$ | $\log_{10}1000 = 3$ |

$\log_{10}$ is the logarithm to base 10: the power to which 10 must be raised. It is used for pH, for p$K_a$ and for the axes of plots.

Decay at a rate proportional to the amount that is left has the form

$$
N(t) = N_0\,e^{-t/\tau}, \qquad t_{1/2} = \tau\ln 2 \approx 0.693\,\tau .
$$

<div class="legend" markdown="1">
- $t$: the time.
- $N(t)$: the amount left at time $t$, for example the number of ligands still bound.
- $N_0$: the amount at $t = 0$.
- $\tau$ (Greek tau): the **time constant**, with the unit of time. After a time $\tau$ the amount has fallen to $1/e$, that is 36.8 %, of what it was. The rate constant is $1/\tau$.
- $t_{1/2}$: the **half-life**, the time after which half is left. It follows from $e^{-t_{1/2}/\tau} = \tfrac12$ by taking the logarithm of both sides.
</div>

Exponential growth is the same formula with a plus sign in the exponent.

**Log scales.** On a logarithmic axis, equal distances mean equal factors: the ticks are 1, 10, 100, 1000. An exponential decay plotted with a logarithmic vertical axis is a straight line, because $\ln N = \ln N_0 - t/\tau$. The slope of $\ln N$ against $t$ is $-1/\tau$. This is the standard way to read a time constant off a plot. If you read the slope in powers of ten per unit of time, as the ticks of a logarithmic axis suggest, it is $-1/(2.303\,\tau)$: the amount falls by a factor of 10 in the time $2.303\,\tau$.

A power law, $y\propto x^{n}$, is a straight line of slope $n$ when both axes are logarithmic.

<div class="box key" markdown="1">
**Worked example: a Boltzmann factor.** Two states differ in energy by 5 kJ/mol. At 300 K, $k_BT = 2.494$ kJ/mol, so the exponent is $5/2.494 = 2.005$ and the ratio of the two probabilities is $e^{-2.005} = 0.135$. The upper state is about 7.4 times less populated.

In the other direction: a state that is seen 100 times less often than another lies $-k_BT\ln(0.01) = 2.494\times4.605 = 11.5$ kJ/mol higher. A number worth remembering is $k_BT\ln 10 = 5.74$ kJ/mol, or 1.37 kcal/mol, at 300 K. Each factor of 10 in population corresponds to that much energy.

**Worked example: a decay.** A correlation decays with $\tau = 5$ ns. After 5 ns, $e^{-1}$ or 36.8 % is left. After 15 ns, $e^{-3}$ or 5.0 % is left. The half-life is $5\times0.693 = 3.47$ ns.
</div>

**Where the course uses it.**

- [Module 2](02-classical-mechanics.html), Classical mechanics: the distance between two nearby trajectories grows as $e^{\lambda t}$, where $t$ is the time and $\lambda$ is a positive rate, the Lyapunov exponent.
- [Module 3](03-statistical-mechanics.html), Statistical mechanics: the Boltzmann factor $e^{-\beta E}$, the entropy $S = k_B\ln\Omega$ and the free energy $A = -k_BT\ln Q$.
- [Module 8](08-thermostats-barostats.html), Thermostats and barostats: the temperature relaxes exponentially towards its target.
- [Module 11](11-analysis-statistics.html), Analysis and statistics: the decay of a correlation function gives a relaxation time.
- [Module 12](12-free-energy-pmf.html), Free energy and the potential of mean force: $W(\xi) = -k_BT\ln P(\xi)$.
- [Module 13](13-alchemical-free-energy.html), Alchemical free energy: averages of exponentials, $\langle e^{-\beta\Delta U}\rangle$.
- [Module 14](14-enhanced-sampling.html), Enhanced sampling: rates fall exponentially with the height of a barrier.
- [Module 16](16-kinetics-msm.html), Kinetics and Markov state models: relaxation times from the logarithm of eigenvalues.

<div class="box warn" markdown="1">
**A common mistake.** $\ln(a+b)$ is not $\ln a + \ln b$, and the average of an exponential is not the exponential of the average. Take the two energies 0 and 4, in units of $k_BT$. The average of $e^{-E}$ is $(1 + 0.018)/2 = 0.509$. The exponential of minus the average energy is $e^{-2} = 0.135$. The exponential average is dominated by the lowest energy, and Module 13 depends on this.

A second trap: "log" means $\log_{10}$ in some texts and $\ln$ in others. Check which one is meant, in a text and in code.
</div>

## The derivative {#derivative}

**The idea.** The derivative of a function is its slope at one point: how fast the output changes when the input changes a little. The speedometer of a car shows a derivative, the rate of change of position with time. For a potential energy plotted against a distance, the slope tells you how hard the system is pushed, and in which direction.

A curve has a different slope at every point, so "slope" needs a definition. Take two points on the curve a small distance $h$ apart, compute the slope of the straight line through them as in [the section on functions](#functions), and let $h$ shrink. The value that the slope settles to is the derivative.

**The notation.**

$$
\frac{df}{dx} = \lim_{h\to0}\frac{f(x+h) - f(x)}{h} .
$$

<div class="legend" markdown="1">
- $f$: a function of the variable $x$.
- $h$: a small step in $x$.
- $f(x+h) - f(x)$: the change of the function over that step.
- $\lim_{h\to0}$: "the limit as $h$ goes to zero": the value that the ratio approaches when $h$ is made smaller and smaller.
- $\dfrac{df}{dx}$: the derivative, read "d f d x". The letter $d$ stands for "a very small change of". It belongs to the letter after it and does not multiply anything.
</div>

Two other ways of writing the same thing are $f'(x)$, read "f prime", and, when the variable is time, $\dot f$, read "f dot". The derivative is itself a function of $x$. Its unit is the unit of $f$ divided by the unit of $x$.

You rarely use the definition directly. A few rules cover every function in this course. In the table, $a$, $c$ and $n$ are constants and angles are in radians.

| Function $f(x)$ | Derivative $df/dx$ |
|---|---|
| a constant $c$ | $0$ |
| $x^{n}$ | $n\,x^{n-1}$ |
| $1/x$, which is $x^{-1}$ | $-1/x^{2}$ |
| $\sqrt{x}$, which is $x^{1/2}$ | $1/(2\sqrt{x})$ |
| $e^{ax}$ | $a\,e^{ax}$ |
| $\ln x$ | $1/x$ |
| $\sin(ax)$ | $a\cos(ax)$ |
| $\cos(ax)$ | $-a\sin(ax)$ |
| $c\,f(x)$ | $c\,f'(x)$ |
| $f(x) + g(x)$ | $f'(x) + g'(x)$ |

Products of functions, and functions inside functions, need two more rules. They are in [the next section](#chain-rule).

**The second derivative** is the derivative of the derivative, written $d^2f/dx^2$ or $f''(x)$. It measures **curvature**: how fast the slope itself changes. Where $f'' > 0$ the graph bends upwards like a bowl. Where $f'' < 0$ it bends downwards like a dome. With time as the variable, the first derivative of a position is the velocity and the second is the acceleration.

**Minimum and maximum.** At the bottom of a valley and at the top of a hill the graph is flat, so $f' = 0$. The second derivative tells the two apart: where $f' = 0$, a positive $f''$ means a minimum and a negative $f''$ means a maximum. If $f''$ is zero as well, this test does not decide, and you look at the graph. For a potential energy, a minimum is a stable structure, and $f''$ at the minimum is the stiffness of the spring that holds the structure there.

<div class="box key" markdown="1">
**Worked example: the definition at work.** Take $f(x) = x^2$ at $x = 3$. With $h = 0.1$ the ratio is $(3.1^2 - 3^2)/0.1 = 6.1$. With $h = 0.01$ it is 6.01, and with $h = 0.0001$ it is 6.0001. The limit is 6, which is what the rule gives: $df/dx = 2x = 6$.

**Worked example: the Lennard-Jones minimum.** Two atoms that are not bonded interact with the energy $U(r) = 4\varepsilon\left[(\sigma/r)^{12} - (\sigma/r)^{6}\right]$ of Module 5. Here $r$ is their distance, $\varepsilon$ is an energy and $\sigma$ is a length. Write it as $4\varepsilon\,(\sigma^{12}r^{-12} - \sigma^{6}r^{-6})$ and use the rule for $x^{n}$ on each term:

$$
\frac{dU}{dr} = 4\varepsilon\left(-12\,\frac{\sigma^{12}}{r^{13}} + 6\,\frac{\sigma^{6}}{r^{7}}\right).
$$

The slope is zero where the two terms cancel, that is where $r^6 = 2\sigma^6$. So the minimum is at $r_{\min} = 2^{1/6}\sigma = 1.122\,\sigma$. There $(\sigma/r)^6 = \tfrac12$, and $U = 4\varepsilon\,(\tfrac14 - \tfrac12) = -\varepsilon$: the depth of the well is $\varepsilon$.

Now with numbers, say $\sigma = 0.34$ nm and $\varepsilon = 1$ kJ/mol. The minimum is at 0.382 nm. At $r = 0.45$ nm the slope is $+6.2$ kJ mol$^{-1}$ nm$^{-1}$: the energy rises as the atoms move apart, so they attract each other.

Differentiating once more gives the second derivative $d^2U/dr^2 = 4\varepsilon\,(156\,\sigma^{12}/r^{14} - 42\,\sigma^{6}/r^{8})$. At $r_{\min}$, where $\sigma^{6}/r^{6} = \tfrac12$ and $\sigma^{12}/r^{12} = \tfrac14$, this is $4\varepsilon\,(39 - 21)/r_{\min}^2 = 72\,\varepsilon/r_{\min}^2 = 494$ kJ mol$^{-1}$ nm$^{-2}$. It is positive, as it must be at a minimum.
</div>

**Where the course uses it.**

- [Module 1](01-what-is-md.html), What MD is: velocity and acceleration are the first and second time derivatives of position.
- [Module 2](02-classical-mechanics.html), Classical mechanics: the force is minus the derivative of the potential energy, $F = -dU/dx$.
- [Module 4](04-integrators.html), Integrators: a time step replaces the limit $h\to0$ by a small but finite $\Delta t$.
- [Module 5](05-force-field-form.html), The form of a force field: the force that belongs to each energy term.
- [Module 12](12-free-energy-pmf.html), Free energy and the potential of mean force: the mean force is minus the derivative of the potential of mean force.
- [Module 13](13-alchemical-free-energy.html), Alchemical free energy: thermodynamic integration adds up the derivative $dA/d\lambda$.

<div class="box warn" markdown="1">
**A common mistake.** Forgetting the minus sign between energy and force. Where the energy rises to the right, the force points to the left. A second one: a zero derivative alone does not make a minimum. Check the sign of the second derivative, or look at the graph.
</div>

## The chain rule {#chain-rule}

**The idea.** Many quantities depend on something that itself depends on something else. The energy of a bond depends on its length, and the length depends on time as the atoms move. The chain rule says how to get the rate of change through such a chain: multiply the rates of the links. Gears show it well. If gear A turns 3 times for each turn of gear B, and B turns 2 times for each turn of gear C, then A turns 6 times for each turn of C.

**The notation.** Call the inner function $g(x)$ and the outer function $f(g)$.

$$
\frac{d}{dx}\,f\big(g(x)\big) = \frac{df}{dg}\,\frac{dg}{dx} .
$$

<div class="legend" markdown="1">
- $g(x)$: the inner function, the one that is applied first.
- $f\big(g(x)\big)$: the outer function applied to the result, read "f of g of x".
- $\dfrac{d}{dx}$ in front of an expression: "take the derivative of what follows with respect to $x$".
- $df/dg$: the [derivative](#derivative) of the outer function with respect to its own argument, evaluated at $g(x)$.
- $dg/dx$: the derivative of the inner function.
</div>

In practice: differentiate the outside and leave the inside as it is, then multiply by the derivative of the inside.

**Several variables.** When a function depends on several quantities that all change with time, each one contributes "slope times rate", and the contributions add:

$$
\frac{d}{dt}\,f\big(x(t),y(t)\big) = \frac{\partial f}{\partial x}\,\frac{dx}{dt} + \frac{\partial f}{\partial y}\,\frac{dy}{dt} .
$$

<div class="legend" markdown="1">
- $f(x,y)$: a function of two variables.
- $x(t)$, $y(t)$: the two variables, each changing with the time $t$.
- $\partial f/\partial x$: the [partial derivative](#partial-derivative), the slope of $f$ when only $x$ changes. It is explained in the next section.
- $dx/dt$, $dy/dt$: how fast $x$ and $y$ change.
</div>

With $3N$ coordinates the sum has $3N$ terms. Module 2 uses this step to prove that the energy is conserved.

**The product rule.** For a product of two functions,

$$
\frac{d}{dx}\big(f\,g\big) = \frac{df}{dx}\,g + f\,\frac{dg}{dx} .
$$

<div class="legend" markdown="1">
- $f$, $g$: two functions of $x$.
- $f\,g$: their product.
- Each term on the right differentiates one factor and leaves the other as it is.
</div>

<div class="box key" markdown="1">
**Worked example: a bell-shaped curve.** $f(x) = e^{-ax^2}$. The outside is $e^{g}$, whose derivative is $e^{g}$. The inside is $g = -ax^2$, whose derivative is $-2ax$. So $df/dx = -2ax\,e^{-ax^2}$.

With $a = 2$ and $x = 0.5$: $f = e^{-0.5} = 0.6065$ and $df/dx = -2\times2\times0.5\times0.6065 = -1.213$. A check with the definition of the derivative gives the same: $[f(0.5001) - f(0.5)]/0.0001 = -1.213$.

**Worked example: energy changing in time.** A spring has $U = \tfrac12 kx^2$, and its end moves with the velocity $v = dx/dt$. Then $dU/dt = (dU/dx)(dx/dt) = kx\,v$. With $k = 100$ kJ mol$^{-1}$ nm$^{-2}$, $x = 0.1$ nm and $v = 0.5$ nm/ps, the energy rises at $100\times0.1\times0.5 = 5$ kJ mol$^{-1}$ ps$^{-1}$.

**Worked example: a product.** $f(x) = x\,e^{-x}$ gives $f' = 1\times e^{-x} + x\times(-e^{-x}) = (1-x)\,e^{-x}$. This is zero at $x = 1$, where $f$ has its maximum, $e^{-1} = 0.368$.
</div>

**Where the course uses it.**

- [Module 2](02-classical-mechanics.html), Classical mechanics: the proof of energy conservation, the force from a pair energy (the energy depends on a distance, and the distance on the positions), and the Poisson bracket.
- [Module 5](05-force-field-form.html), The form of a force field: forces from angle and dihedral terms, where the energy depends on an angle and the angle on the positions of three or four atoms.
- [Module 13](13-alchemical-free-energy.html), Alchemical free energy: the derivative $dA/d\lambda$ of $A = -k_BT\ln Q$.
- [Module 17](17-machine-learning.html), Machine-learned potentials: the force is the derivative of a learned energy, computed by the chain rule through every layer of the model.

<div class="box warn" markdown="1">
**A common mistake.** Forgetting the derivative of the inside. The derivative of $\cos(3x)$ is $-3\sin(3x)$, and the derivative of $e^{-\beta U(x)}$ with respect to $x$ is $-\beta\,(dU/dx)\,e^{-\beta U(x)}$. The factor that comes from the inside is the one that gets lost.
</div>

## Partial derivatives {#partial-derivative}

**The idea.** Most functions in this course depend on many variables: the potential energy depends on $3N$ coordinates. A partial derivative asks the same question as an ordinary derivative, for one variable at a time: how fast does the function change if I change only this variable and keep all the others fixed? On a hillside, the height depends on how far east and how far north you are. The partial derivative with respect to "east" is the slope you feel when you walk due east.

**The notation.**

$$
\frac{\partial f}{\partial x} = \lim_{h\to0}\frac{f(x+h,\,y) - f(x,\,y)}{h} .
$$

<div class="legend" markdown="1">
- $f(x,y)$: a function of two (or more) variables.
- $\partial$: a rounded d, read "partial" or "d". It signals that other variables exist and are held fixed.
- $\partial f/\partial x$: the partial derivative of $f$ with respect to $x$.
- $h$: a small step in $x$. The other variable, $y$, has the same value in both terms.
- $\lim_{h\to0}$: the limit of a smaller and smaller step, as in [the derivative](#derivative).
</div>

To compute a partial derivative, treat every other variable as a constant and use the ordinary rules. Thermodynamics often writes the fixed variables as a subscript: $(\partial A/\partial V)_{T}$ is "the slope of $A$ with respect to $V$ at constant $T$". Here $A$ is the Helmholtz free energy, $V$ the volume and $T$ the temperature ([primer](physics.html#thermodynamics)).

**Second derivatives.** You can differentiate twice with respect to the same variable, $\partial^2 f/\partial x^2$, or once with respect to each of two variables. For the smooth functions of this course the order does not matter:

$$
\frac{\partial^2 f}{\partial x\,\partial y} = \frac{\partial^2 f}{\partial y\,\partial x} .
$$

<div class="legend" markdown="1">
- $\dfrac{\partial^2 f}{\partial x\,\partial y}$: differentiate $f$ with respect to $y$, then differentiate the result with respect to $x$.
- $\dfrac{\partial^2 f}{\partial y\,\partial x}$: the same two steps in the other order.
</div>

For a potential energy, a mixed second derivative says how much the force along one coordinate changes when another coordinate moves. It is the coupling between the two. The table of all second derivatives of the energy is the Hessian matrix of Module 2.

**Small changes.** If $x$ changes by a small amount $dx$ and $y$ by a small amount $dy$, the function changes by

$$
df = \frac{\partial f}{\partial x}\,dx + \frac{\partial f}{\partial y}\,dy .
$$

<div class="legend" markdown="1">
- $dx$, $dy$: small changes of the two variables.
- $df$: the resulting small change of $f$, called the total differential.
- Other symbols: as in the lists above.
</div>

Each variable contributes its slope times its change. Thermodynamic relations such as $dA = -S\,dT - P\,dV$, where $S$ is the entropy and $P$ the pressure, have this form, and you can read the partial derivatives off them: here $(\partial A/\partial T)_V = -S$ and $(\partial A/\partial V)_T = -P$.

<div class="box key" markdown="1">
**Worked example.** $f(x,y) = x^2y + 3y$. Holding $y$ fixed, $\partial f/\partial x = 2xy$. Holding $x$ fixed, $\partial f/\partial y = x^2 + 3$. The mixed derivatives agree: $\partial(2xy)/\partial y = 2x$ and $\partial(x^2+3)/\partial x = 2x$.

At $x = 1$, $y = 2$ the function is 8 and both partial derivatives are 4. Now change $x$ by $+0.01$ and $y$ by $-0.02$. The formula for small changes predicts $df = 4\times0.01 + 4\times(-0.02) = -0.040$. The exact change is $f(1.01, 1.98) - f(1, 2) = 7.9598 - 8 = -0.0402$.
</div>

**Where the course uses it.**

- [Module 2](02-classical-mechanics.html), Classical mechanics: the equations of Lagrange and Hamilton are written with partial derivatives, Liouville's theorem uses the equality of mixed derivatives, and the Hessian collects the second derivatives of the energy.
- [Module 3](03-statistical-mechanics.html), Statistical mechanics: energy, pressure and entropy are partial derivatives of $\ln Q$ or of the free energy $A$.
- [Module 5](05-force-field-form.html), The form of a force field: the force on an atom is built from the partial derivatives of $U$ with respect to its three coordinates.
- [Module 13](13-alchemical-free-energy.html), Alchemical free energy: $\partial U/\partial\lambda$, the slope of the energy with respect to the coupling parameter.

<div class="box warn" markdown="1">
**A common mistake.** Not knowing what is held fixed. $\partial f/\partial x$ has a meaning only when the full list of variables is known. The slope of the energy with respect to the volume at constant temperature is a different number from the slope at constant entropy.

Keep $d$ and $\partial$ apart as well. $df/dt$ follows the system while everything changes. $\partial f/\partial t$ is the change at one fixed place, with all other variables held still. Liouville's equation in Module 2 contains both.
</div>

## The gradient {#gradient}

**The idea.** Stand on a hillside. In every direction the ground has some slope. There is one direction in which it rises most steeply, and the **gradient** is an arrow that points that way, with a length equal to that steepest slope. A ball released there rolls the opposite way, straight downhill. This is the picture behind every force in MD: the force on an atom is minus the gradient of the potential energy.

**The notation.**

$$
\nabla f = \left(\frac{\partial f}{\partial x},\ \frac{\partial f}{\partial y},\ \frac{\partial f}{\partial z}\right).
$$

<div class="legend" markdown="1">
- $f(x,y,z)$: a function of position. It returns one number at each point.
- $\nabla$: the symbol "nabla" or "del". $\nabla f$ is read "grad f" or "del f".
- $\partial f/\partial x$, $\partial f/\partial y$, $\partial f/\partial z$: the three [partial derivatives](#partial-derivative).
- The brackets with commas: the three numbers together form one [vector](#vectors).
</div>

Three facts make the gradient useful. It points in the direction of steepest increase. Its length is the slope in that direction. And for a small step $\Delta\mathbf r$ in any direction, the function changes by

$$
\Delta f \approx \nabla f\cdot\Delta\mathbf r .
$$

<div class="legend" markdown="1">
- $\Delta\mathbf r = (\Delta x, \Delta y, \Delta z)$: a small displacement.
- $\Delta f$: the change of $f$ over that displacement.
- $\cdot$: the [dot product](#dot-product). Written out, the right side is $\frac{\partial f}{\partial x}\Delta x + \frac{\partial f}{\partial y}\Delta y + \frac{\partial f}{\partial z}\Delta z$.
- $\approx$: the smaller the step, the better the approximation.
</div>

A step at right angles to the gradient leaves $f$ unchanged to first order. That is walking along a contour line of the hill, a line of equal height on a map.

**Force from energy.** The energy $U$ of a system depends on the positions of all atoms. The gradient with respect to the position of atom $i$ alone is written $\nabla_i U$ or $\partial U/\partial\mathbf r_i$, and

$$
\mathbf F_i = -\nabla_i U = -\left(\frac{\partial U}{\partial x_i},\ \frac{\partial U}{\partial y_i},\ \frac{\partial U}{\partial z_i}\right).
$$

<div class="legend" markdown="1">
- $\mathbf F_i$: the force on atom $i$, a vector.
- $U$: the potential energy, a function of all atomic positions.
- $\nabla_i$: the gradient taken with respect to the coordinates $x_i$, $y_i$, $z_i$ of atom $i$, with all other atoms held still.
- The minus sign: the force points in the direction in which the energy falls fastest.
</div>

With energies in kJ/mol and distances in nm, forces are in kJ mol$^{-1}$ nm$^{-1}$.

<div class="box key" markdown="1">
**Worked example: a function of two variables.** $f(x,y) = x^2 + 3y^2$ at the point $(1,1)$. The gradient is $(2x, 6y) = (2, 6)$, of length $\sqrt{2^2+6^2} = 6.32$. A step of length 0.01 along the gradient raises $f$ by about $6.32\times0.01 = 0.063$. The same step along $x$ raises it by 0.020, and along $y$ by 0.060. No direction does better than the gradient.

**Worked example: the force of a stretched bond.** Atom $j$ sits at the origin and atom $i$ at $(0.3, 0.4, 0)$ nm, so their distance is $r = 0.5$ nm. They are joined by a spring, $U = \tfrac12k(r-r_0)^2$, with, say, $k = 1000$ kJ mol$^{-1}$ nm$^{-2}$ and $r_0 = 0.4$ nm.

By the [chain rule](#chain-rule), $\nabla_iU$ is $dU/dr$ times the gradient of the distance $r$. The first factor is $k(r-r_0) = 100$ kJ mol$^{-1}$ nm$^{-1}$. The second is the [unit vector](#vectors) (a vector of length 1) that points from $j$ to $i$, here $(0.3, 0.4, 0)/0.5 = (0.6, 0.8, 0)$, because the distance grows fastest when atom $i$ moves straight away from atom $j$ (Module 2 derives this).

So $\nabla_iU = (60, 80, 0)$ and $\mathbf F_i = (-60, -80, 0)$ kJ mol$^{-1}$ nm$^{-1}$. The force points from $i$ towards $j$: the stretched bond pulls the atom back.
</div>

**Where the course uses it.**

- [Module 1](01-what-is-md.html), What MD is, and [Module 2](02-classical-mechanics.html), Classical mechanics: $\mathbf F_i = -\nabla_iU$, the starting point of the method.
- [Module 5](05-force-field-form.html), The form of a force field: the gradient of each energy term, worked out with the chain rule.
- [Module 9](09-constraints.html), Constraints: a constraint force acts along the gradient of the constraint.
- [Module 10](10-running-a-simulation.html), Running a simulation: energy minimisation moves the atoms along the force, that is, down the gradient.
- [Module 15](15-coarse-grained.html), Coarse-grained models, and [Module 17](17-machine-learning.html), Machine-learned potentials: models are trained so that minus the gradient of their energy matches reference forces.

<div class="box warn" markdown="1">
**A common mistake.** Treating the gradient as a single number. It is a vector with one component per coordinate. For a system of $N$ atoms the full gradient of $U$ has $3N$ components, three per atom. And mind the sign: the gradient points uphill, the force downhill.
</div>

## Divergence and Laplacian {#divergence}

**The idea.** Picture water flowing in a shallow tray, with an arrow at every point that shows the velocity of the water there. Such a set of arrows, one at each point, is a **vector field**.

Now mark a small region and ask: does more water leave it than enters? If yes, the flow is spreading out there, as it does under a tap. If less leaves than enters, the flow is converging, as it does above a drain. The **divergence** is the number that measures this: the net outflow per unit volume.

Zero divergence means that what flows in flows out, and a marked blob of water changes its shape but keeps its volume. The **Laplacian** applies the same idea to the gradient of a function. It is the divergence of the gradient, and it compares the value of a function at a point with the average over the points around it.

**The notation.**

$$
\nabla\cdot\mathbf v = \frac{\partial v_x}{\partial x} + \frac{\partial v_y}{\partial y} + \frac{\partial v_z}{\partial z} .
$$

<div class="legend" markdown="1">
- $\mathbf v(x,y,z) = (v_x, v_y, v_z)$: a vector field, that is a [vector](#vectors) at every point, for example a flow velocity.
- $\nabla\cdot$: the divergence, read "div v" or "del dot v". The dot is there because the formula looks like a [dot product](#dot-product) of $\nabla$ with $\mathbf v$.
- $\partial v_x/\partial x$: how the $x$ component of the flow changes as you move along $x$. If it is positive, the water in front moves away faster than the water behind follows.
- The result is a single number at each point.
</div>

$$
\nabla^2 f = \nabla\cdot(\nabla f) = \frac{\partial^2 f}{\partial x^2} + \frac{\partial^2 f}{\partial y^2} + \frac{\partial^2 f}{\partial z^2} .
$$

<div class="legend" markdown="1">
- $f(x,y,z)$: a function that returns one number at each point.
- $\nabla f$: its [gradient](#gradient), which is a vector field.
- $\nabla^2$: the Laplacian, read "del squared". Some books write $\Delta$ for it.
- $\partial^2 f/\partial x^2$: the second derivative along $x$, the curvature in that direction.
</div>

The Laplacian is the sum of the curvatures along the three axes. At the bottom of a bowl all three are positive, and the value at the centre is lower than the average around it. Where the Laplacian is zero, the value at each point equals the average over a small sphere around it.

**Where Poisson's equation comes from.** Two statements from electrostatics combine ([primer](physics.html#electrostatics)). First, electric charge is the source of the electric field $\mathbf E$: the divergence of the field at a point is proportional to the charge density there, $\nabla\cdot\mathbf E = \rho/\epsilon_0$. Second, the field is minus the gradient of the electrostatic potential $\phi$, $\mathbf E = -\nabla\phi$, in the same way that a force is minus the gradient of an energy. Put the second statement into the first:

$$
\nabla^2\phi = -\frac{\rho}{\epsilon_0} .
$$

<div class="legend" markdown="1">
- $\phi$ (Greek phi): the electrostatic potential, the energy per unit charge that a small test charge would have at each point.
- $\rho$ (Greek rho): the charge density, the amount of charge per unit volume at each point.
- $\epsilon_0$: the permittivity of vacuum, a constant of nature whose value depends on the system of units.
- $\nabla^2$: the Laplacian.
</div>

This is Poisson's equation. It gives the potential everywhere once you know where the charges are. Module 7 writes it as $\nabla^2\phi = -4\pi\rho$, in units in which the constant $1/(4\pi\epsilon_0)$ is equal to 1.

<div class="box key" markdown="1">
**Worked example: three flows.** For $\mathbf v = (x, y, z)$ every point moves straight away from the origin, faster the further out it is. $\nabla\cdot\mathbf v = 1 + 1 + 1 = 3$: the flow expands everywhere. For $\mathbf v = (-y, x, 0)$, a rigid rotation about the $z$ axis, $\nabla\cdot\mathbf v = 0 + 0 + 0 = 0$: a rotation moves a blob without changing its volume.

The same recipe works in any space, with any coordinates in place of $x$, $y$ and $z$: take the rate of change of each coordinate, differentiate it with respect to that same coordinate, and add up. Modules 2 and 8 do this in phase space, where the coordinates are the positions and the momenta of the atoms. For a friction that slows every momentum, $\dot p = -\gamma p$ in one dimension, the rate of change of the coordinate $p$ is $-\gamma p$, and the divergence is $\partial(-\gamma p)/\partial p = -\gamma$. It is negative, so a cloud of points shrinks.

**Worked example: a Laplacian that vanishes.** The potential of a point charge is proportional to $1/r$, with $r = \sqrt{x^2+y^2+z^2}$. By the [chain rule](#chain-rule), $\partial(1/r)/\partial x = -x/r^3$: the derivative of $1/r$ with respect to $r$ is $-1/r^2$, and $\partial r/\partial x = x/r$. Differentiating again, with the product rule on $-x\times r^{-3}$, gives $\partial^2(1/r)/\partial x^2 = -1/r^3 + 3x^2/r^5$, and the same holds for $y$ and $z$.

Adding the three: $-3/r^3 + 3(x^2+y^2+z^2)/r^5 = -3/r^3 + 3/r^3 = 0$. At the point $(1,2,2)$, where $r = 3$, the three terms are $-0.0247$, $+0.0123$ and $+0.0123$. So $\nabla^2(1/r) = 0$ everywhere away from the charge, as Poisson's equation requires where $\rho = 0$.
</div>

**Where the course uses it.**

- [Module 2](02-classical-mechanics.html), Classical mechanics: Liouville's theorem says that the flow in phase space has zero divergence.
- [Module 7](07-boundaries-electrostatics.html), Boundaries and electrostatics: Poisson's equation, solved wave by wave for the Ewald sum.
- [Module 8](08-thermostats-barostats.html), Thermostats and barostats: a thermostat adds terms that make the divergence non-zero, and the lesson uses this to find which distribution is sampled.
- [Module 15](15-coarse-grained.html), Coarse-grained models: the Poisson-Boltzmann equation, used when the solvent is not represented by explicit molecules, contains a divergence and a gradient.

<div class="box warn" markdown="1">
**A common mistake.** Mixing up three look-alikes. $\nabla f$, the gradient, turns a field of numbers into a field of vectors. $\nabla\cdot\mathbf v$, the divergence, turns a field of vectors into a field of numbers. $\nabla^2 f$, the Laplacian, turns a field of numbers into another field of numbers.
</div>

## The integral {#integral}

**The idea.** An integral is a sum of very many very small pieces. If you drive at a changing speed, the distance covered is the sum, over many short moments, of the speed times the length of the moment. On a graph of speed against time each piece is a thin strip, and the sum is the area under the curve. Integration is also the reverse of differentiation: the derivative turns distance into speed, and the integral turns speed back into distance.

In this course most integrals are sums over all the arrangements that a system can take. The partition function of Module 3 is such a sum, and so is every average.

**The notation.**

$$
\int_a^b f(x)\,dx = \lim_{\Delta x\to0}\ \sum_{n} f(x_n)\,\Delta x .
$$

<div class="legend" markdown="1">
- $\int$: the integral sign, a stretched S for "sum".
- $a$, $b$: the **limits**, where the sum starts and where it ends. With limits the integral is called **definite**, and it is a number.
- $f(x)$: the function that is summed, the **integrand**.
- $dx$: the width of one very thin strip. It also says which variable is summed over.
- $x_n$, $\Delta x$: on the right side, the range from $a$ to $b$ is cut into strips of width $\Delta x$, and $x_n$ is a point in strip number $n$.
- $\lim_{\Delta x\to0}$: the strips are made thinner and thinner.
</div>

The unit of an integral is the unit of $f$ times the unit of $x$. The name of the integration variable does not matter: $\int_a^b f(x)\,dx$ and $\int_a^b f(y)\,dy$ are the same number.

**Integral and derivative.** A function $F$ whose [derivative](#derivative) is $f$ is called an **antiderivative** or **indefinite integral** of $f$, written $\int f(x)\,dx$ without limits. It is defined up to an added constant, because the derivative of a constant is zero. The link between the two kinds of integral is

$$
\int_a^b f(x)\,dx = F(b) - F(a), \qquad\text{where}\qquad \frac{dF}{dx} = f .
$$

<div class="legend" markdown="1">
- $F$: an antiderivative of $f$.
- $F(b) - F(a)$: its value at the upper limit minus its value at the lower limit, often written $\big[F(x)\big]_a^b$.
- Other symbols: as in the list above.
</div>

| $f(x)$ | $\int f(x)\,dx$ |
|---|---|
| $x^{n}$, with $n\ne-1$ | $x^{n+1}/(n+1)$ |
| $1/x$, with $x > 0$ | $\ln x$ |
| $e^{ax}$ | $e^{ax}/a$ |
| $\cos(ax)$ | $\sin(ax)/a$ |
| $\sin(ax)$ | $-\cos(ax)/a$ |

Many integrals have no formula of this kind and are computed numerically, by adding up strips.

**Integrals over space and over many variables.** $\int f(\mathbf r)\,d\mathbf r$ means: cut space into small boxes of volume $dx\,dy\,dz$, multiply the value of $f$ in each box by the volume of the box, and add. With $f = 1$ the result is the volume. When $f$ depends only on the distance $r$ from a centre, it is easier to cut space into thin spherical shells. A shell of radius $r$ and thickness $dr$ has the volume $4\pi r^2\,dr$, its surface area times its thickness, so

$$
\int f(r)\,d\mathbf r = \int_0^\infty f(r)\,4\pi r^2\,dr .
$$

<div class="legend" markdown="1">
- $d\mathbf r$: a small volume element, $dx\,dy\,dz$.
- $r$: the distance from the centre.
- $4\pi r^2\,dr$: the volume of a thin spherical shell.
- $\infty$: the upper limit "infinity". The sum runs over all distances.
</div>

The symbol $\int d\mathbf r^N$ in Module 3 is an integral over the positions of all $N$ atoms, $3N$ variables in all. It means "sum over every possible arrangement of the atoms". Nobody evaluates it strip by strip, and a simulation does not compute it either. What a simulation estimates by sampling is an average, which is the ratio of two such integrals (Module 3).

**Changing the variable.** An integral can be rewritten in a new variable. If the old variable is a function of the new one, $x = x(u)$, a thin strip of width $du$ in the new variable covers the width $(dx/du)\,du$ in the old one, so

$$
\int_{x(a)}^{x(b)} f(x)\,dx = \int_a^b f\big(x(u)\big)\,\frac{dx}{du}\,du .
$$

<div class="legend" markdown="1">
- $u$: the new variable. $x(u)$: the old variable written as a function of the new one.
- $a$, $b$: the limits of $u$. The limits of $x$ are the matching values $x(a)$ and $x(b)$.
- $dx/du$: the [derivative](#derivative) of the old variable with respect to the new one. It says how much a small step is stretched, and it is called the **Jacobian** of the change of variable.
- Other symbols: as in the lists above.
</div>

Three things change together: the function, the limits and the width of the strip. Example: in $\int_0^3 x^2\,dx = 9$ put $x = 3s$, so that $s$ runs from 0 to 1 and $dx/ds = 3$. The integral becomes $\int_0^1 (3s)^2\times3\,ds = 27\times\tfrac13 = 9$, the same number.

In space the Jacobian is the volume that belongs to one small step in each of the new coordinates. The case used in this course is spherical coordinates: the distance $r$ from the origin, the angle $\theta$ measured from the $z$ axis (from 0 to $\pi$) and the angle $\phi$ around the $z$ axis (from 0 to $2\pi$). A small piece has the sides $dr$, $r\,d\theta$ and $r\sin\theta\,d\phi$, so

$$
d\mathbf r = r^2\sin\theta\,dr\,d\theta\,d\phi .
$$

<div class="legend" markdown="1">
- $d\mathbf r$: the small volume, $dx\,dy\,dz$ in Cartesian coordinates.
- $r$, $\theta$ (Greek theta), $\phi$ (Greek phi): the distance and the two angles, in radians.
- $r^2\sin\theta$: the Jacobian of spherical coordinates. The piece is larger far from the origin, and smaller near the $z$ axis, where a step in $\phi$ covers little distance.
</div>

Adding up over all directions gives $\int_0^{\pi}\sin\theta\,d\theta\times\int_0^{2\pi}d\phi = 2\times2\pi = 4\pi$. What is left is $4\pi r^2\,dr$, the shell used above.

The same factor appears when a probability is expressed in a new variable. Suppose the vector from one particle to another is found with the density $p$ per unit volume, and $p$ depends only on the distance $r$. The probability that the distance lies between $r$ and $r + dr$ is $p(r)$ times the volume of the shell, so the density per unit distance is $P(r) = 4\pi r^2\,p(r)$. Take $-k_BT$ times the logarithm: $-k_BT\ln P(r) = -k_BT\ln p(r) - 2k_BT\ln r - k_BT\ln(4\pi)$.

The middle term comes from geometry alone. Each doubling of the distance multiplies the volume of the shell by 4 and lowers $-k_BT\ln P$ by $k_BT\ln 4 = 3.46$ kJ/mol at 300 K, with no force between the particles. Module 12 removes it by adding $2k_BT\ln r$. (A logarithm needs a pure number, so read $\ln r$ as the logarithm of $r$ divided by 1 nm. Another unit of length only changes the constant.)

**Integration by parts.** The [product rule](#chain-rule) says $d(uv)/dx = (du/dx)\,v + u\,(dv/dx)$. Integrate both sides from $a$ to $b$. The left side gives $\big[u\,v\big]_a^b$, because integration undoes the derivative. Then move the first term of the right side to the left:

$$
\int_a^b u\,\frac{dv}{dx}\,dx = \big[u\,v\big]_a^b - \int_a^b \frac{du}{dx}\,v\,dx .
$$

<div class="legend" markdown="1">
- $u$, $v$: two functions of $x$.
- $\big[u\,v\big]_a^b$: the product at $b$ minus the product at $a$, the **boundary term**.
- The rule moves the derivative from $v$ onto $u$, at the price of a minus sign and the boundary term.
</div>

<div class="box key" markdown="1">
**Worked example: strips against the exact value.** $\int_0^2 x^2\,dx = \big[x^3/3\big]_0^2 = 8/3 = 2.667$. Now use four strips of width 0.5 and take the function at the middle of each, at 0.25, 0.75, 1.25 and 1.75. The sum is $0.5\times(0.0625+0.5625+1.5625+3.0625) = 2.625$. With eight strips it is 2.656, and with a hundred 2.6666.

**Worked example: counting neighbours with shells.** Liquid water has about 33 molecules per nm$^3$. The number within 0.5 nm of a given point is $\int_0^{0.5}33\times4\pi r^2\,dr = 33\times\tfrac43\pi\times0.5^3 = 33\times0.524$, which is about 17.

**Worked example: by parts.** $\int_0^\infty x\,e^{-x}\,dx$. Take $u = x$ and $dv/dx = e^{-x}$, so that $v = -e^{-x}$. The boundary term $\big[-x\,e^{-x}\big]_0^\infty$ is zero at both ends. What remains is $\int_0^\infty e^{-x}\,dx = \big[-e^{-x}\big]_0^\infty = 1$.
</div>

**Where the course uses it.**

- [Module 2](02-classical-mechanics.html), Classical mechanics: the action is an integral over time, and the Euler-Lagrange equation follows from it by integration by parts.
- [Module 3](03-statistical-mechanics.html), Statistical mechanics: the partition function is an integral over all positions and momenta, and an average is a ratio of two such integrals.
- [Module 7](07-boundaries-electrostatics.html), Boundaries and electrostatics: the correction for a cutoff is an integral over shells from the cutoff to infinity.
- [Module 11](11-analysis-statistics.html), Analysis and statistics: the integral of a radial distribution function over the first shell counts neighbours.
- [Module 12](12-free-energy-pmf.html), Free energy and the potential of mean force: a binding constant is an integral of $e^{-\beta W(r)}$ over the bound region.
- [Module 13](13-alchemical-free-energy.html), Alchemical free energy: thermodynamic integration.

<div class="box warn" markdown="1">
**A common mistake.** Forgetting the volume of the shell. A histogram of the distance between two particles grows as $r^2$ even when they do not interact, because there is more room at a larger distance. Module 12 calls the factor $4\pi r^2$ the Jacobian of the distance and removes it before a free energy is read off.
</div>

## Taylor expansion {#taylor}

**The idea.** Look at any smooth curve through a strong magnifying glass and it looks like a straight line. Look a little less closely and it looks like a parabola. The Taylor expansion makes this exact: close to a chosen point, a function is approximated by a polynomial (a sum of powers of the distance from the point), whose coefficients are fixed by the derivatives at that point. The further you go from the point, the more terms you need.

Physics uses it to replace a complicated function by a simple one that is valid over the small range that matters. A time step is small, so the motion during one step is expanded in the time step. A molecule near its energy minimum moves little, so its energy is expanded around the minimum.

**The notation.**

$$
f(x_0 + h) = f(x_0) + f'(x_0)\,h + \tfrac12 f''(x_0)\,h^2 + \tfrac16 f'''(x_0)\,h^3 + \dots
$$

<div class="legend" markdown="1">
- $x_0$: the point around which you expand.
- $h$: the distance from that point. The expansion is useful when $h$ is small.
- $f'(x_0)$, $f''(x_0)$, $f'''(x_0)$: the first, second and third [derivatives](#derivative) of $f$, evaluated at $x_0$. They are fixed numbers.
- $\tfrac12$, $\tfrac16$: the term with $h^n$ carries the factor $1/n!$, where $n! = 1\times2\times\dots\times n$ is a [factorial](#combinatorics).
- $\dots$: terms with higher powers of $h$.
</div>

Stopping after the term in $h$ gives the straight-line approximation, also called linear or first-order. Stopping after the term in $h^2$ gives the parabola, also called second-order or harmonic.

**Several variables.** The same pattern holds for a function of several variables, with [partial derivatives](#partial-derivative) in place of $f'$ and $f''$. For two variables and the small steps $\Delta x$ and $\Delta y$, the first-order term is $\frac{\partial f}{\partial x}\Delta x + \frac{\partial f}{\partial y}\Delta y$, and the second-order term is $\tfrac12\big(\frac{\partial^2 f}{\partial x^2}\Delta x^2 + 2\frac{\partial^2 f}{\partial x\,\partial y}\Delta x\,\Delta y + \frac{\partial^2 f}{\partial y^2}\Delta y^2\big)$, with all derivatives taken at the starting point. With many variables $r_1, r_2, \dots$ the second-order term is $\tfrac12\sum_a\sum_b H_{ab}\,\Delta r_a\,\Delta r_b$, where $H_{ab} = \partial^2 f/\partial r_a\,\partial r_b$ is the table of all second derivatives, the Hessian of Module 2.

Check with the example of [the section on partial derivatives](#partial-derivative), $f = x^2y + 3y$ at $(1, 2)$ with the steps $+0.01$ and $-0.02$. The three second derivatives are $2y = 4$, $2x = 2$ and $0$, so the second-order term is $\tfrac12\,(4\times0.0001 - 2\times2\times0.0002 + 0) = -0.0002$. Added to the first-order value $-0.040$ it gives $-0.0402$, the exact change to four decimals.

**The order of the error.** When you stop, the first term that you left out dominates the error. If you keep the terms up to $h$, the error is about $\tfrac12f''(x_0)\,h^2$. The shorthand is

$$
f(x_0 + h) = f(x_0) + f'(x_0)\,h + O(h^2) .
$$

<div class="legend" markdown="1">
- $O(h^2)$: read "of order h squared". It stands for everything that was left out and says how it scales: at most a constant times $h^2$ when $h$ is small. Halve $h$ and this error falls by a factor of 4. With $O(h^3)$ it falls by 8, and with $O(h^4)$ by 16.
- Other symbols: as in the list above.
</div>

The same letter describes the cost of an algorithm: $O(N^2)$ means that the computing time grows as the square of the number of atoms $N$ when $N$ is large.

A few expansions around zero are used so often that they are worth knowing:

| Function | For small $x$ | Exact value at $x = 0.1$ | Approximation at $x = 0.1$ |
|---|---|---|---|
| $e^{x}$ | $1 + x + \tfrac12x^2$ | 1.10517 | 1.10500 |
| $\ln(1+x)$ | $x - \tfrac12x^2$ | 0.09531 | 0.09500 |
| $\sin x$ | $x - \tfrac16x^3$ | 0.099833 | 0.099833 |
| $\cos x$ | $1 - \tfrac12x^2$ | 0.99500 | 0.99500 |
| $1/(1-x)$ | $1 + x + x^2$ | 1.1111 | 1.1100 |
| $\sqrt{1+x}$ | $1 + \tfrac12x$ | 1.0488 | 1.0500 |

<div class="box key" markdown="1">
**Worked example: watching the error shrink.** Approximate $e^{h}$ by $1 + h$. At $h = 0.1$ the exact value is 1.10517, so the error is 0.00517. At $h = 0.05$ the exact value is 1.05127 and the error is 0.00127. Halving $h$ divided the error by 4.07, as expected for an error of $O(h^2)$.

With the next term, $\tfrac12h^2$, the errors are 0.000171 and 0.000021. Their ratio is 8.1, as expected for $O(h^3)$.

**Worked example: the step behind the Verlet integrator.** Expand a position forwards and backwards in time. Forwards, $x(t+h) = x + \dot x\,h + \tfrac12\ddot x\,h^2 + \tfrac16 b\,h^3 + O(h^4)$. Backwards, $x(t-h) = x - \dot x\,h + \tfrac12\ddot x\,h^2 - \tfrac16 b\,h^3 + O(h^4)$. Here $x$, the velocity $\dot x$, the acceleration $\ddot x$ and the third derivative $b$ are all taken at the time $t$.

Add the two lines. The terms with odd powers of $h$ cancel, and $x(t+h) = 2x(t) - x(t-h) + \ddot x(t)\,h^2 + O(h^4)$.

Test it on $x(t) = \cos t$, for which $\ddot x = -\cos t$, at $t = 1$ with $h = 0.1$. The right side is $2\times0.5403023 - 0.6216100 - 0.5403023\times0.01 = 0.4535916$. The exact value of $\cos(1.1)$ is 0.4535961. The error is only $4.5\times10^{-6}$, because it is of fourth order.
</div>

**Where the course uses it.**

- [Module 2](02-classical-mechanics.html), Classical mechanics: the potential energy near a minimum, expanded to second order, gives the normal modes.
- [Module 3](03-statistical-mechanics.html), Statistical mechanics: a first-order expansion of the logarithm of the number of states of the heat bath gives the Boltzmann factor.
- [Module 4](04-integrators.html), Integrators: the Verlet integrators and the order of their errors.
- [Module 7](07-boundaries-electrostatics.html), Boundaries and electrostatics: the notation $O(N^2)$ for the cost of testing all pairs of atoms, and $O(N^{3/2})$ and $O(N\log N)$ for the cost of the Ewald sum and of particle-mesh Ewald.
- [Module 9](09-constraints.html), Constraints: SHAKE drops a small second-order term to get an equation that it can solve directly.
- [Module 13](13-alchemical-free-energy.html), Alchemical free energy: the expansion of a free-energy difference in the mean and the variance of an energy difference.

<div class="box warn" markdown="1">
**A common mistake.** Using an expansion outside its range. $e^{x}\approx1+x$ is good to half a percent at $x = 0.1$ and useless at $x = 2$, where it gives 3 while the exact value is 7.39. An order such as $O(h^2)$ says how the error changes when $h$ changes. It does not say that the error is small for the $h$ you happen to use.

Also keep the error of one step apart from the error of a whole run. A run of fixed length contains more steps when the step is smaller, so the two errors are of different orders. Module 4 states both for the Verlet method.
</div>

## Vectors {#vectors}

**The idea.** Some quantities are fully described by one number: a mass, a temperature, an energy. They are called **scalars**. Others also have a direction: the displacement from one atom to another, a velocity, a force. They are **vectors**, and the picture is an arrow. The length of the arrow is the size of the quantity, and the arrow points where the quantity points.

To compute with an arrow, describe it by its **components**: how far it reaches along the $x$, $y$ and $z$ axes. A vector in space is then a list of three numbers.

**The notation.**

$$
\mathbf a = (a_x,\ a_y,\ a_z), \qquad \lvert\mathbf a\rvert = \sqrt{a_x^2 + a_y^2 + a_z^2}, \qquad \hat{\mathbf a} = \frac{\mathbf a}{\lvert\mathbf a\rvert} .
$$

<div class="legend" markdown="1">
- $\mathbf a$: a vector, written in bold. In handwriting an arrow over the letter is used.
- $a_x$, $a_y$, $a_z$: its components along the three axes. Each is an ordinary number with a sign.
- $\lvert\mathbf a\rvert$: the **length** (or magnitude, or norm) of the vector, from Pythagoras' theorem. It is never negative. It is often written as the same letter without bold, $a$.
- $\hat{\mathbf a}$: the **unit vector** along $\mathbf a$, read "a hat". It has length 1 and no unit. It keeps only the direction.
</div>

Calculations are done component by component:

$$
\mathbf a + \mathbf b = (a_x + b_x,\ a_y + b_y,\ a_z + b_z), \qquad c\,\mathbf a = (c\,a_x,\ c\,a_y,\ c\,a_z) .
$$

<div class="legend" markdown="1">
- $\mathbf a$, $\mathbf b$: two vectors.
- $\mathbf a + \mathbf b$: their sum. As arrows: put the tail of $\mathbf b$ at the tip of $\mathbf a$. The forces on one atom add in this way.
- $c$: an ordinary number. $c\,\mathbf a$ is $\mathbf a$ stretched by the factor $c$. A negative $c$ reverses the direction.
</div>

Subtraction gives the arrow from one point to another. If $\mathbf r_i$ and $\mathbf r_j$ are the positions of two atoms, then $\mathbf r_{ij} = \mathbf r_i - \mathbf r_j$ points from atom $j$ to atom $i$, and its length $r_{ij}$ is the distance between them. This is the convention of this course for pair forces (Module 2). Some books define $\mathbf r_{ij}$ with the opposite sign, and so does one formula of the course: in the angle force of Module 5, $\hat{\mathbf r}_{ji}$ points from atom $j$ to atom $i$.

A vector can have more than three components. The coordinates of all $N$ atoms, written one after the other, form a vector with $3N$ components, and the rules above apply unchanged.

<div class="box key" markdown="1">
**Worked example.** Atom $i$ is at $\mathbf r_i = (0.5, 0.7, 0.2)$ nm and atom $j$ at $\mathbf r_j = (0.2, 0.3, 0.2)$ nm. Then $\mathbf r_{ij} = (0.3, 0.4, 0)$ nm. Its length is $\sqrt{0.09 + 0.16 + 0} = 0.5$ nm, the distance between the atoms. The unit vector from $j$ to $i$ is $(0.3, 0.4, 0)/0.5 = (0.6, 0.8, 0)$, and its length is $\sqrt{0.36 + 0.64} = 1$.

Two forces act on one atom, $(3, 0, -1)$ and $(-1, 2, 1)$ in kJ mol$^{-1}$ nm$^{-1}$. The total force is $(2, 2, 0)$, of length $\sqrt{8} = 2.83$. The two forces alone have the lengths 3.16 and 2.45, which add up to 5.61. Lengths do not add unless the vectors are parallel.
</div>

**Where the course uses it.**

- [Module 1](01-what-is-md.html), What MD is, and [Module 2](02-classical-mechanics.html), Classical mechanics: the positions, velocities, momenta and forces of the atoms are vectors.
- [Module 5](05-force-field-form.html), The form of a force field: a pair force acts along the unit vector between the two atoms.
- [Module 7](07-boundaries-electrostatics.html), Boundaries and electrostatics: the shortest vector between two atoms across a periodic boundary, and the wave vectors of the Ewald sum.
- [Module 9](09-constraints.html), Constraints: the bond vectors in the SHAKE and LINCS algorithms.
- [Module 11](11-analysis-statistics.html), Analysis and statistics: displacement vectors in the RMSD and in the mean squared displacement.

<div class="box warn" markdown="1">
**A common mistake.** Adding lengths where vectors should be added, or comparing a vector with a number. "The force is 500" is a statement about a length or about one component, and you need to know which. A related trap is the sign convention of $\mathbf r_{ij}$: check from which atom the arrow starts before you copy a formula for a force.
</div>

## The dot product {#dot-product}

**The idea.** The dot product answers the question: how much of one vector lies along another? Pull a sledge with a rope that points partly upwards. Only the part of your force that points along the direction of travel moves the sledge forwards, and the work you do is that part times the distance. The dot product computes "the part along" for you. It takes two vectors and returns one number.

**The notation.**

$$
\mathbf a\cdot\mathbf b = a_xb_x + a_yb_y + a_zb_z = \lvert\mathbf a\rvert\,\lvert\mathbf b\rvert\cos\theta .
$$

<div class="legend" markdown="1">
- $\mathbf a$, $\mathbf b$: two [vectors](#vectors).
- $\cdot$: the dot product, read "a dot b". It is also called the scalar product, because the result is a scalar.
- $a_xb_x + a_yb_y + a_zb_z$: how to compute it from the components.
- $\lvert\mathbf a\rvert$, $\lvert\mathbf b\rvert$: the lengths of the two vectors.
- $\theta$ (Greek theta): the angle between the two arrows when they start from the same point, between 0 and 180 degrees.
</div>

The second form shows what the dot product means. $\lvert\mathbf b\rvert\cos\theta$ is the length of the shadow that $\mathbf b$ casts on the line of $\mathbf a$, its **projection**. So the dot product is the length of $\mathbf a$ times the projection of $\mathbf b$ on $\mathbf a$. Three cases are worth remembering:

- parallel vectors: $\cos\theta = 1$, and the dot product is the product of the lengths;
- perpendicular vectors: $\cos\theta = 0$, and the dot product is zero;
- opposite vectors: $\cos\theta = -1$, and the dot product is negative.

A vector dotted with itself gives its length squared, $\mathbf a\cdot\mathbf a = \lvert\mathbf a\rvert^2$, written $\mathbf a^2$ for short. That is the meaning of $\mathbf p^2$ in the kinetic energy $\mathbf p^2/2m$. Solving the formula for the angle gives the standard way to compute an angle from coordinates:

$$
\cos\theta = \frac{\mathbf a\cdot\mathbf b}{\lvert\mathbf a\rvert\,\lvert\mathbf b\rvert} .
$$

<div class="legend" markdown="1">
- $\cos\theta$: the cosine of the angle between the two vectors. The angle itself is $\arccos$ of the right side, where $\arccos$ is the inverse function of the cosine.
- Other symbols: as in the list above.
</div>

<div class="box key" markdown="1">
**Worked example: a bond angle.** Three atoms $i$, $j$, $k$, with $j$ in the middle. The two bond vectors that start from $j$ are $\mathbf a = (0.10, 0, 0)$ nm and $\mathbf b = (-0.03, 0.09, 0.03)$ nm. Their dot product is $0.10\times(-0.03) + 0 + 0 = -0.003$ nm$^2$. The lengths are 0.10 nm and $\sqrt{0.0009 + 0.0081 + 0.0009} = 0.0995$ nm. So $\cos\theta = -0.003/(0.10\times0.0995) = -0.3015$, and the angle is 107.5 degrees.

**Worked example: the energy cost of a small move.** In [the gradient section](#gradient) a stretched bond had $\nabla_iU = (60, 80, 0)$ kJ mol$^{-1}$ nm$^{-1}$. Moving atom $i$ by $(0.001, 0, 0)$ nm changes the energy by about $60\times0.001 = 0.06$ kJ/mol. Moving it by $(0.0008, -0.0006, 0)$ nm, which is at right angles to the bond, changes it by $60\times0.0008 - 80\times0.0006 = 0$.
</div>

**Where the course uses it.**

- [Module 2](02-classical-mechanics.html), Classical mechanics: the kinetic energy contains $\mathbf p\cdot\mathbf p$, and the rate of change of the energy contains $\dot{\mathbf r}_i\cdot\mathbf F_i$.
- [Module 3](03-statistical-mechanics.html), Statistical mechanics: the virial $\sum_i\mathbf r_i\cdot\mathbf F_i$ in the formula for the pressure.
- [Module 5](05-force-field-form.html), The form of a force field: the angle between two bonds.
- [Module 7](07-boundaries-electrostatics.html), Boundaries and electrostatics: $\mathbf k\cdot\mathbf r_j$, the phase of a wave at the position of an atom.
- [Module 9](09-constraints.html), Constraints: the SHAKE formula contains the dot product of the old and the new bond vector.

<div class="box warn" markdown="1">
**A common mistake.** Expecting a vector as the result. The dot product is a number, and the directions are gone. Also, $\arccos$ returns an angle between 0 and 180 degrees. The dot product alone therefore cannot give the sign of a dihedral angle, which runs from $-180$ to $180$ degrees. That needs the [cross product](#cross-product).
</div>

## The cross product {#cross-product}

**The idea.** The cross product takes two vectors and returns a third vector that is perpendicular to both. Its length is the area of the parallelogram that the two vectors span. It is the tool for everything that involves rotation or planes. Loosen a bolt with a spanner: what counts is the force, the length of the handle and the angle between them, and the bolt moves along its axis, at right angles to both. That is a cross product.

**The notation.**

$$
\mathbf a\times\mathbf b = \big(a_yb_z - a_zb_y,\ \ a_zb_x - a_xb_z,\ \ a_xb_y - a_yb_x\big), \qquad \lvert\mathbf a\times\mathbf b\rvert = \lvert\mathbf a\rvert\,\lvert\mathbf b\rvert\sin\theta .
$$

<div class="legend" markdown="1">
- $\mathbf a$, $\mathbf b$: two [vectors](#vectors) in three dimensions.
- $\times$: the cross product, read "a cross b". It is also called the vector product, because the result is a vector.
- The three expressions in the bracket: the $x$, $y$ and $z$ components of the result.
- $\theta$: the angle between $\mathbf a$ and $\mathbf b$.
- $\lvert\mathbf a\rvert\,\lvert\mathbf b\rvert\sin\theta$: the area of the parallelogram with the sides $\mathbf a$ and $\mathbf b$.
</div>

The direction follows the **right-hand rule**: point the fingers of your right hand along $\mathbf a$, curl them towards $\mathbf b$, and the thumb points along $\mathbf a\times\mathbf b$. Two consequences follow. Swapping the vectors reverses the result, $\mathbf b\times\mathbf a = -\mathbf a\times\mathbf b$. And the cross product of two parallel vectors is zero, because they span no area.

Two quantities from mechanics are cross products ([primer](physics.html#momentum)):

$$
\mathbf L = \mathbf r\times\mathbf p, \qquad \boldsymbol\tau = \mathbf r\times\mathbf F .
$$

<div class="legend" markdown="1">
- $\mathbf r$: the position of a particle, measured from a chosen origin.
- $\mathbf p$: its momentum, mass times velocity.
- $\mathbf L$: its **angular momentum** about the origin. It points along the axis around which the particle circles.
- $\mathbf F$: the force on the particle.
- $\boldsymbol\tau$ (bold Greek tau): the **torque**, the turning effect of the force. It is the rate of change of $\mathbf L$.
</div>

The geometry of molecules uses the cross product to describe planes. Three atoms define a plane, and the cross product of two bond vectors in that plane is perpendicular to it. A dihedral angle is the angle between two such planes. The volume of a simulation box with the edge vectors $\mathbf a$, $\mathbf b$ and $\mathbf c$ is $\lvert\mathbf a\cdot(\mathbf b\times\mathbf c)\rvert$, whatever the shape of the box.

<div class="box key" markdown="1">
**Worked example: components.** $\mathbf a = (1, 2, 3)$ and $\mathbf b = (4, 5, 6)$. Then $\mathbf a\times\mathbf b = (2\times6 - 3\times5,\ 3\times4 - 1\times6,\ 1\times5 - 2\times4) = (-3, 6, -3)$. Check with the [dot product](#dot-product) that it is perpendicular to both: $\mathbf a\cdot(-3,6,-3) = -3 + 12 - 9 = 0$ and $\mathbf b\cdot(-3,6,-3) = -12 + 30 - 18 = 0$. Its length, $\sqrt{9+36+9} = 7.35$, is the area of the parallelogram.

**Worked example: angular momentum.** An atom of mass 16 u is at $\mathbf r = (0.2, 0, 0)$ nm and moves with the velocity $(0, 0.5, 0)$ nm/ps, so $\mathbf p = (0, 8, 0)$ u nm ps$^{-1}$. The formula gives $\mathbf L = (0\times0 - 0\times8,\ 0\times0 - 0.2\times0,\ 0.2\times8 - 0\times0) = (0, 0, 1.6)$ u nm$^2$ ps$^{-1}$. The atom circles in the $xy$ plane, and $\mathbf L$ points along $z$, the axis of the rotation.
</div>

**Where the course uses it.**

- [Module 2](02-classical-mechanics.html), Classical mechanics: the total angular momentum $\mathbf L = \sum_i\mathbf r_i\times\mathbf p_i$, and why a periodic box does not conserve it.
- [Module 5](05-force-field-form.html), The form of a force field: a dihedral angle is the angle between two planes, and the direction perpendicular to each plane is a cross product of two bond vectors.
- [Module 17](17-machine-learning.html), Machine-learned potentials: the dot product and the cross product as the two familiar products of vectors that respect rotation. The dot product does not change when both vectors are rotated, and the cross product turns with them.

<div class="box warn" markdown="1">
**A common mistake.** Forgetting that the order matters. $\mathbf a\times\mathbf b$ and $\mathbf b\times\mathbf a$ point in opposite directions, and a swapped order flips the sign of an angular momentum or of a dihedral angle. Do not confuse this $\times$ with the same sign used for the ordinary multiplication of numbers, as in $3\times10^5$, or for the size of a matrix, as in $3\times3$.
</div>

## Matrices {#matrices}

**The idea.** A matrix is a rectangular table of numbers. It has two uses. The first is storage: a table of how strongly each pair of things is related, such as the [covariance](#averages) between every pair of coordinates. The second is action: a matrix is a rule that turns one vector into another. Rotating a molecule, advancing a set of probabilities by one time step, and computing the forces that small displacements produce are all "matrix times vector".

**The notation.** A matrix is written as a bold capital, $\mathbf A$, and its entry in row $i$ and column $j$ as $A_{ij}$: row first, column second. The action on a vector is

$$
\mathbf y = \mathbf A\,\mathbf x \qquad\text{means}\qquad y_i = \sum_j A_{ij}\,x_j .
$$

<div class="legend" markdown="1">
- $\mathbf A$: a matrix with the entries $A_{ij}$.
- $\mathbf x$: the [vector](#vectors) it acts on, with the components $x_j$.
- $\mathbf y$: the resulting vector, with the components $y_i$.
- $\sum_j$: a sum over the columns. Component $i$ of the result is the [dot product](#dot-product) of row $i$ of the matrix with $\mathbf x$.
</div>

Written out for two dimensions:

$$
\begin{pmatrix} a & b\\ c & d\end{pmatrix}\begin{pmatrix} x_1\\ x_2\end{pmatrix} = \begin{pmatrix} a\,x_1 + b\,x_2\\ c\,x_1 + d\,x_2\end{pmatrix}.
$$

<div class="legend" markdown="1">
- $a$, $b$, $c$, $d$: the four entries of a matrix with two rows and two columns, a "2 by 2" matrix, written $2\times2$.
- $x_1$, $x_2$: the two components of the vector, written as a column.
</div>

Two matrices are multiplied by the rule $(\mathbf A\mathbf B)_{ij} = \sum_k A_{ik}B_{kj}$, where $k$ runs over the columns of $\mathbf A$ and the rows of $\mathbf B$. When the product acts on a column vector to its right, $\mathbf A\mathbf B$ means "apply $\mathbf B$ first, then $\mathbf A$". In general $\mathbf A\mathbf B\ne\mathbf B\mathbf A$.

A vector can also stand to the left of a matrix. It is then written as a row, $\mathbf x^{T}$ (the superscript $T$ turns a column into a row), and the rule is $(\mathbf x^{T}\mathbf A)_j = \sum_i x_i\,A_{ij}$, a sum over the rows. Component $j$ of the result is the [dot product](#dot-product) of $\mathbf x$ with column $j$ of the matrix. For the $2\times2$ matrix above the result is $(a\,x_1 + c\,x_2,\ b\,x_1 + d\,x_2)$: compared with the column result, $b$ and $c$ have changed places, so the two results differ unless $b = c$.

Module 16 uses the row form: the populations of the states stand to the left of the transition matrix. With a row on the left, the leftmost matrix acts first.

| Name | Symbol | Meaning |
|---|---|---|
| Identity | $\mathbf 1$ or $\mathbf I$ | Ones on the diagonal, zeros elsewhere. It leaves every vector unchanged. |
| Diagonal matrix | | Entries other than zero only on the diagonal, where $i = j$. It stretches each axis separately. |
| Transpose | $\mathbf A^{T}$ | Rows and columns swapped: $(\mathbf A^{T})_{ij} = A_{ji}$. |
| Symmetric matrix | $\mathbf A^{T} = \mathbf A$ | $A_{ij} = A_{ji}$. Tables of pair relations, such as a covariance matrix, are symmetric. |
| Inverse | $\mathbf A^{-1}$ | The matrix that undoes $\mathbf A$: $\mathbf A^{-1}\mathbf A = \mathbf A\mathbf A^{-1} = \mathbf 1$. Only a square matrix, with as many rows as columns, can have one. It solves $\mathbf A\mathbf x = \mathbf y$ for $\mathbf x$, as $\mathbf x = \mathbf A^{-1}\mathbf y$. |
| Determinant | $\det\mathbf A$ | One number, defined for a square matrix: the factor by which $\mathbf A$ multiplies volumes (areas in two dimensions). A negative sign means that the shape is also turned into its mirror image. If the determinant is zero, the matrix flattens space and has no inverse. If the columns of $\mathbf A$ are the three edge vectors of a simulation box, the determinant is, up to its sign, the volume of the box: the same number as the triple product in [the cross product section](#cross-product). |

For a $2\times2$ matrix,

$$
\det\begin{pmatrix} a & b\\ c & d\end{pmatrix} = ad - bc, \qquad \begin{pmatrix} a & b\\ c & d\end{pmatrix}^{-1} = \frac{1}{ad - bc}\begin{pmatrix} d & -b\\ -c & a\end{pmatrix}.
$$

<div class="legend" markdown="1">
- $\det$: the determinant.
- The superscript $-1$: the inverse matrix. It is not the table of the numbers $1/a$, $1/b$, $1/c$, $1/d$.
- $ad - bc$: the determinant appears in the denominator of the inverse. This is why a zero determinant means that there is no inverse.
</div>

For larger matrices the same quantities exist, and a numerical library computes them.

**The Jacobian matrix.** A table of [partial derivatives](#partial-derivative) is also a matrix. If new variables $y_1, y_2, \dots$ are functions of old variables $x_1, x_2, \dots$, the matrix with the entries $J_{ij} = \partial y_i/\partial x_j$ is called the **Jacobian matrix** of the change of variables. Its determinant, taken without its sign, is the factor by which a small volume (in two dimensions, a small area) changes when it is carried from the old variables to the new ones. Modules 4 and 17 use it.

Example: polar coordinates describe a point in the plane by its distance $r$ from the origin and an angle $\theta$, with $x = r\cos\theta$ and $y = r\sin\theta$. The table of the derivatives of $(x, y)$ with respect to $(r, \theta)$ is $\begin{pmatrix}\cos\theta&-r\sin\theta\\ \sin\theta&r\cos\theta\end{pmatrix}$. Its determinant is $r\cos^2\theta + r\sin^2\theta = r$, so a small piece with the sides $dr$ and $d\theta$ has the area $r\,dr\,d\theta$.

<div class="box key" markdown="1">
**Worked example: acting and undoing.** Let $\mathbf A = \begin{pmatrix}2&1\\1&3\end{pmatrix}$ and $\mathbf x = (1, 2)$. Then $\mathbf A\mathbf x = (2\times1 + 1\times2,\ 1\times1 + 3\times2) = (4, 7)$. The determinant is $2\times3 - 1\times1 = 5$, and the inverse is $\tfrac15\begin{pmatrix}3&-1\\-1&2\end{pmatrix} = \begin{pmatrix}0.6&-0.2\\-0.2&0.4\end{pmatrix}$.

Applying the inverse to $(4, 7)$ gives $(2.4 - 1.4,\ -0.8 + 2.8) = (1, 2)$, the vector we started from. Said differently: the two equations $2x_1 + x_2 = 4$ and $x_1 + 3x_2 = 7$ have the solution $x_1 = 1$, $x_2 = 2$.

**Worked example: a rotation.** $\mathbf R = \begin{pmatrix}0&-1\\1&0\end{pmatrix}$ turns $(1, 0)$ into $(0, 1)$: a rotation by 90 degrees. Its determinant is $0\times0 - (-1)\times1 = 1$, so areas are unchanged. Its inverse is its transpose, $\begin{pmatrix}0&1\\-1&0\end{pmatrix}$, the rotation back. Both properties hold for every rotation matrix.

The order matters: $\mathbf A\mathbf R = \begin{pmatrix}1&-2\\3&-1\end{pmatrix}$, but $\mathbf R\mathbf A = \begin{pmatrix}-1&-3\\2&1\end{pmatrix}$.
</div>

**Where the course uses it.**

- [Module 2](02-classical-mechanics.html), Classical mechanics: the Hessian, the matrix of the second derivatives of the energy.
- [Module 4](04-integrators.html), Integrators: one integration step of an oscillator written as a $2\times2$ matrix with determinant 1.
- [Module 8](08-thermostats-barostats.html), Thermostats and barostats: the matrix that holds the size and the shape of the simulation box.
- [Module 9](09-constraints.html), Constraints: LINCS writes all constraints as one matrix equation and needs the inverse of a matrix.
- [Module 11](11-analysis-statistics.html), Analysis and statistics: the rotation matrix that superimposes two structures, and the covariance matrix.
- [Module 16](16-kinetics-msm.html), Kinetics and Markov state models: the matrix of transition probabilities.
- [Module 17](17-machine-learning.html), Machine-learned potentials: the determinant of a matrix of derivatives, in models that turn one probability distribution into another.

<div class="box warn" markdown="1">
**A common mistake.** Treating matrices like numbers. $\mathbf A\mathbf B$ and $\mathbf B\mathbf A$ differ, you cannot divide by a matrix (use the inverse, on the correct side), and $\mathbf A^{-1}$ is not the table of the numbers $1/A_{ij}$. When several matrices stand one after the other in front of a column vector, the rightmost one acts first. Behind a row vector, as in Module 16, the leftmost one acts first.
</div>

## Eigenvalues and eigenvectors {#eigen}

**The idea.** A matrix usually turns a vector into one that points somewhere else. Many matrices, and all symmetric ones, have a few special directions that they do not turn: a vector along one of them is only made longer or shorter. These directions are the **eigenvectors**, and the stretch factors are the **eigenvalues**. ("Eigen" is German for "own".)

They matter because along its eigenvectors a matrix acts as plain multiplication by a number. A problem with many coupled variables, written in terms of the eigenvectors, falls apart into independent problems with one variable each. The vibrations of a molecule become independent oscillators, the fluctuations of a protein become independent directions of motion, and the kinetics of a network of states becomes a set of independent exponential decays.

**The notation.**

$$
\mathbf A\,\mathbf v = \lambda\,\mathbf v .
$$

<div class="legend" markdown="1">
- $\mathbf A$: a square [matrix](#matrices), with as many rows as columns.
- $\mathbf v$: an **eigenvector** of $\mathbf A$, a vector that is not zero.
- $\lambda$ (Greek lambda): its **eigenvalue**, an ordinary number. $\lambda > 1$ stretches, $\lambda$ between 0 and 1 shrinks, and a negative $\lambda$ also reverses the direction.
</div>

A matrix with $n$ rows and $n$ columns has $n$ eigenvalues, some of which may coincide. The set of all eigenvalues is called the **spectrum** of the matrix (the same word is used for the list of waves in [Fourier analysis](#fourier)). Finding all eigenvalues and eigenvectors is called **diagonalising** the matrix. The name comes from this: if you use the eigenvectors as new coordinate axes, the matrix becomes diagonal, with the eigenvalues on the diagonal and zeros elsewhere. For anything larger than $2\times2$ a numerical library does the work.

**Symmetric matrices**, with $A_{ij} = A_{ji}$, are the easy case and the common one: Hessians (matrices of second derivatives, see [partial derivatives](#partial-derivative)) and covariance matrices (see [the section on averages](#averages)) are symmetric. Their eigenvalues are real numbers, and their eigenvectors can be chosen perpendicular to each other, so that they form a proper set of axes. A matrix that is not symmetric can have [complex](#complex) eigenvalues. The rotation by 90 degrees in [the section on matrices](#matrices) is the simplest case: it turns every vector, so it has no real eigenvector, and its eigenvalues are $i$ and $-i$. When a matrix that is not symmetric does have real eigenvectors, they are in general not perpendicular to each other.

**Repeated action.** Applying the matrix $n$ times multiplies an eigenvector by its eigenvalue $n$ times:

$$
\mathbf A^{n}\,\mathbf v = \lambda^{n}\,\mathbf v .
$$

<div class="legend" markdown="1">
- $\mathbf A^{n}$: the matrix applied $n$ times in a row.
- $\lambda^{n}$: the eigenvalue to the power $n$.
- Other symbols: as in the list above.
</div>

So a component along an eigenvector with $\lvert\lambda\rvert < 1$ dies out, one with $\lvert\lambda\rvert > 1$ grows without limit, and one with $\lvert\lambda\rvert = 1$ persists. This one fact decides whether an integrator is stable (Module 4), whether an iteration converges (Module 9) and how fast a Markov model relaxes (Module 16).

**Two matrices at once.** Module 16 meets an equation with a second matrix on the right-hand side, the **generalised eigenvalue problem**:

$$
\mathbf A\,\mathbf v = \lambda\,\mathbf B\,\mathbf v .
$$

<div class="legend" markdown="1">
- $\mathbf A$, $\mathbf B$: two square matrices of the same size. In Module 16, $\mathbf B$ is the covariance matrix $\mathbf C(0)$ of a set of coordinates, and $\mathbf A$ is $\mathbf C(\tau)$, the covariances between the coordinates now and the same coordinates a lag time $\tau$ later.
- $\mathbf v$: a generalised eigenvector, a vector that is not zero.
- $\lambda$: its generalised eigenvalue, an ordinary number.
</div>

The equation asks for the directions along which $\mathbf A$ acts as a multiple of $\mathbf B$. The ordinary problem is the special case in which $\mathbf B$ is the identity. If $\mathbf B$ has an inverse, multiplying both sides by $\mathbf B^{-1}$ turns the equation into an ordinary eigenvalue problem for the matrix $\mathbf B^{-1}\mathbf A$. That matrix is in general not symmetric, even when $\mathbf A$ and $\mathbf B$ are, so a numerical library solves the equation in its original form.

The case in the course is the favourable one: $\mathbf A$ and $\mathbf B$ are symmetric, and all eigenvalues of $\mathbf B$ are positive. Then every $\lambda$ is a real number. Two eigenvectors with different eigenvalues satisfy $\mathbf v_1\cdot(\mathbf B\mathbf v_2) = 0$: they are perpendicular as measured by $\mathbf B$, and in general not perpendicular in the ordinary sense.

Taking the dot product of both sides of the equation with $\mathbf v$ shows what the eigenvalue measures: $\lambda = \mathbf v\cdot(\mathbf A\mathbf v)\,/\,\mathbf v\cdot(\mathbf B\mathbf v)$. In Module 16 this ratio is the correlation coefficient between the combination of coordinates given by $\mathbf v$ and the same combination one lag time later. The eigenvector with the largest $\lambda$ is therefore the combination that changes most slowly.

<div class="box key" markdown="1">
**Worked example: large is not the same as slow.** Take two coordinates that are not correlated with each other. The first has the variance 1 and keeps 90 % of its correlation after one lag time. The second has the variance 4 and keeps 50 %. Then $\mathbf B = \begin{pmatrix}1&0\\0&4\end{pmatrix}$ and $\mathbf A = \begin{pmatrix}0.9&0\\0&2\end{pmatrix}$.

For $\mathbf v = (1, 0)$ the equation reads $0.9 = \lambda\times1$, so $\lambda = 0.9$. For $\mathbf v = (0, 1)$ it reads $2 = \lambda\times4$, so $\lambda = 0.5$. The slowest direction is the first coordinate. A principal component analysis, which diagonalises $\mathbf B$ alone, would put the second coordinate first, because its variance is four times larger.

**Worked example: perpendicular as measured by B.** $\mathbf A = \begin{pmatrix}2&1\\1&2\end{pmatrix}$ and $\mathbf B = \begin{pmatrix}2&0\\0&1\end{pmatrix}$. The condition $\det(\mathbf A - \lambda\mathbf B) = 0$ is $(2-2\lambda)(2-\lambda) - 1 = 0$, which gives $\lambda = (3\pm\sqrt3)/2$: 2.366 and 0.634. The eigenvectors are $(1, 2.732)$ and $(1, -0.732)$.

Their ordinary dot product is $1 - 2.732\times0.732 = -1$, which is not zero. With $\mathbf B$ in between it is $2\times1\times1 - 1\times2.732\times0.732 = 2 - 2 = 0$.
</div>

<div class="box key" markdown="1">
**Worked example: two coupled springs.** Two equal masses on a line. Each is tied to a wall by a spring of stiffness $k$, and a third spring of stiffness $k$ joins them. In units of $k$, the matrix of the second derivatives of the energy is $\mathbf H = \begin{pmatrix}2&-1\\-1&2\end{pmatrix}$.

Try $\mathbf v_1 = (1, 1)$: $\mathbf H\mathbf v_1 = (2-1,\ -1+2) = (1, 1)$, so it is an eigenvector with $\lambda_1 = 1$. Try $\mathbf v_2 = (1, -1)$: $\mathbf H\mathbf v_2 = (2+1,\ -1-2) = (3, -3)$, so $\lambda_2 = 3$. In the first pattern both masses move together and the middle spring is not stretched. In the second they move against each other, the middle spring works too, and the stiffness is three times larger.

The vector $(1, 0)$ is not an eigenvector: $\mathbf H\,(1,0) = (2, -1)$ points elsewhere. The two eigenvectors are perpendicular, since $(1,1)\cdot(1,-1) = 0$. To find eigenvalues without guessing, solve $\det(\mathbf A - \lambda\mathbf 1) = 0$. Here that is $(2-\lambda)^2 - 1 = 0$, which gives $\lambda = 1$ and $\lambda = 3$.

**Worked example: a Markov model with two states.** $\mathbf T = \begin{pmatrix}0.9&0.1\\0.2&0.8\end{pmatrix}$, where $T_{ij}$ is the probability of being in state $j$ one step after being in state $i$. Its eigenvalues are 1 and 0.7. One step turns the populations $p_i$ into $\sum_ip_i\,T_{ij}$: the populations stand to the left of the matrix, as a row. The eigenvalue 1 belongs to the set of populations that does not change, $(2/3, 1/3)$: after one step the first population is $\tfrac23\times0.9 + \tfrac13\times0.2 = \tfrac23$ again.

Any deviation from these populations shrinks by the factor 0.7 per step. If one step is 1 ns, the deviation decays as $e^{-t/t_2}$ with the relaxation time $t_2 = -1/\ln0.7 = 2.8$ ns.
</div>

**Where the course uses it.**

- [Module 2](02-classical-mechanics.html), Classical mechanics: the normal modes are the eigenvectors of the mass-weighted Hessian, and the eigenvalues are the squared frequencies.
- [Module 4](04-integrators.html), Integrators: an integrator is stable as long as the eigenvalues of its one-step matrix stay on the [unit circle](#complex), which means that they are complex numbers with $\lvert\lambda\rvert = 1$.
- [Module 9](09-constraints.html), Constraints: the series used by LINCS converges when all eigenvalues are smaller than 1 in absolute value.
- [Module 11](11-analysis-statistics.html), Analysis and statistics: principal component analysis diagonalises the covariance matrix.
- [Module 16](16-kinetics-msm.html), Kinetics and Markov state models: the eigenvalues of the transition matrix give the relaxation times, and the eigenvector with eigenvalue 1 gives the equilibrium populations.

<div class="box warn" markdown="1">
**A common mistake.** Reading a meaning into the length or the sign of an eigenvector. If $\mathbf v$ is an eigenvector, so are $-\mathbf v$ and $5\mathbf v$. By convention eigenvectors are given with length 1, and the sign is arbitrary, so a principal component can come out flipped between two runs of the same analysis.

A second point: a matrix that is not symmetric, such as a transition matrix, has two sets of eigenvectors. One set belongs to columns placed to its right, $\mathbf T\mathbf v = \lambda\mathbf v$. The other belongs to rows placed to its left, as the populations in the example. Both sets have the same eigenvalues.

For the matrix of the example the first set is $(1, 1)$ for the eigenvalue 1 and $(1, -2)$ for the eigenvalue 0.7, and the second set is $(2/3, 1/3)$ and $(1, -1)$. Module 16 takes the equilibrium populations from the second set, the left eigenvectors. Populations are scaled so that they add up to 1, and not to length 1.
</div>

## Complex numbers {#complex}

**The idea.** A complex number is a pair of ordinary numbers that is handled as one object. You can picture it as a point in a plane, or as an arrow from the origin to that point. Complex numbers appear in this course for one reason: they are the most compact way to describe something that oscillates or rotates. A wave needs an amplitude and a phase (where in its cycle it is), and one complex number carries both.

**The notation.** The starting point is a new number $i$, the **imaginary unit**, defined by $i^2 = -1$. No ordinary number has a negative square, so $i$ is something new. Ordinary numbers are called **real** numbers to tell them apart.

$$
z = a + i\,b, \qquad z^{*} = a - i\,b, \qquad \lvert z\rvert = \sqrt{a^2 + b^2} .
$$

<div class="legend" markdown="1">
- $z$: a complex number.
- $a$: its **real part**, an ordinary number, also written $\mathrm{Re}\,z$.
- $b$: its **imaginary part**, also an ordinary number, written $\mathrm{Im}\,z$.
- $i$: the imaginary unit, with $i^2 = -1$.
- $z^{*}$: the **complex conjugate**, with the sign of the imaginary part reversed. Some books write $\bar z$.
- $\lvert z\rvert$: the **modulus** or absolute value, the distance of the point $(a, b)$ from the origin. It satisfies $\lvert z\rvert^2 = z\,z^{*}$.
</div>

You add and multiply complex numbers like ordinary expressions, and replace $i^2$ by $-1$ whenever it appears.

**Euler's formula** connects the exponential function with rotation:

$$
e^{i\theta} = \cos\theta + i\sin\theta .
$$

<div class="legend" markdown="1">
- $\theta$: an angle in radians, an ordinary number.
- $e^{i\theta}$: the [exponential](#exp-log) with an imaginary exponent. It is the point on the circle of radius 1 at the angle $\theta$ from the real axis.
- $\cos\theta$, $\sin\theta$: its real and imaginary parts.
</div>

As $\theta$ grows, the point $e^{i\theta}$ runs around the unit circle, and its real part oscillates as a cosine. Its modulus is always 1, because $\cos^2\theta + \sin^2\theta = 1$. The rule $e^{i\theta_1}e^{i\theta_2} = e^{i(\theta_1+\theta_2)}$ says that multiplying by $e^{i\theta}$ rotates a complex number by the angle $\theta$.

Every complex number can be written as $z = \lvert z\rvert\,e^{i\theta}$: its distance from the origin times a point on the unit circle. For a wave, $\lvert z\rvert$ is the amplitude and the angle $\theta$ is the **phase**. For example, $3 + 4i = 5\,e^{i\theta}$ with $\theta = 0.927$ radians, which is 53.1 degrees.

This is why calculations with waves are easier with $e^{i\theta}$ than with sines and cosines: products of exponentials add their exponents, while products of cosines need trigonometric identities. At the end of a calculation the physical answer is a real number, often a modulus squared.

<div class="box key" markdown="1">
**Worked example: arithmetic.** $(1+2i)(3-i) = 3 - i + 6i - 2i^2 = 3 + 5i + 2 = 5 + 5i$. The modulus of $3 + 4i$ is $\sqrt{9+16} = 5$, and $(3+4i)(3-4i) = 9 + 16 = 25$, which is $5^2$.

Points on the unit circle: $e^{i\pi/3} = 0.5 + 0.866\,i$, the cosine and the sine of 60 degrees. A quarter turn, a half turn and a full turn are $e^{i\pi/2} = i$, $e^{i\pi} = -1$ and $e^{2\pi i} = 1$.

**Worked example: two charges and a wave.** Module 7 adds up $q_j\,e^{ikx_j}$ over all charges, where $q_j$ is a charge, $x_j$ its position and $k$ the wave number of a wave (see [Fourier series](#fourier)). Take a charge $+1$ at $x = 0$ and a charge $-1$ at $x = L/2$, and the wave with $k = 2\pi/L$, whose wavelength $2\pi/k$ is $L$. The sum is $e^{0} - e^{i\pi} = 1 - (-1) = 2$, with modulus squared 4. This wave responds strongly to the pair, because the two charges sit half a wavelength apart.

For $k = 4\pi/L$ the sum is $1 - e^{2\pi i} = 0$. Now the charges sit a full wavelength apart, and their contributions cancel.
</div>

**Where the course uses it.**

- [Module 2](02-classical-mechanics.html), Classical mechanics: the Liouville operator is written $iL$. The $i$ is a convention, and all results are real.
- [Module 4](04-integrators.html), Integrators: the stability analysis inserts the trial solution $x_n = e^{i\theta n}$ into the Verlet recursion, and the eigenvalues of one integration step of an oscillator are complex numbers on the unit circle while the time step is small enough.
- [Module 7](07-boundaries-electrostatics.html), Boundaries and electrostatics: the structure factor $S(\mathbf k) = \sum_jq_j\,e^{i\mathbf k\cdot\mathbf r_j}$ and its modulus squared in the Ewald sum.

<div class="box warn" markdown="1">
**A common mistake.** Squaring where the modulus squared is needed. $\lvert z\rvert^2 = z\,z^{*}$ is real and never negative. $z^2$ is another complex number: $(3+4i)^2 = -7 + 24i$.

Also check what the letter $i$ is doing. As a subscript, in $x_i$ or $\sum_i$, it is a label. In an exponent next to an angle or a wave vector it is the imaginary unit.
</div>

## Differential equations {#ode}

**The idea.** An ordinary equation asks for a number: which $x$ satisfies $2x + 1 = 7$? A differential equation asks for a whole function. It states a rule for how a quantity changes, and the task is to find how the quantity behaves in time. "The coffee cools at a rate proportional to how much hotter it is than the room" is a differential equation. Its solution is the temperature of the coffee at every later time.

Newton's law is a differential equation: it gives the acceleration of each atom from the present positions. An MD program is a machine for solving it. To pick out one solution you also need the starting values, the **initial conditions**. The same law with different starting positions and velocities gives a different trajectory.

**The notation.** A **first-order** equation contains only the first derivative. The most important one in this course describes relaxation towards a target value:

$$
\frac{dx}{dt} = -\frac{x - x_\infty}{\tau} \qquad\Longrightarrow\qquad x(t) = x_\infty + (x_0 - x_\infty)\,e^{-t/\tau} .
$$

<div class="legend" markdown="1">
- $x(t)$: the unknown function of the time $t$.
- $dx/dt$: its rate of change, a [derivative](#derivative).
- $x_\infty$: the target value, which is reached after a long time.
- $\tau$: the **relaxation time**. The larger it is, the slower the approach.
- $x_0$: the initial condition, the value at $t = 0$.
- $\Longrightarrow$: here "has the solution".
- $e^{-t/\tau}$: the [exponential decay](#exp-log) of the distance from the target.
</div>

You can check a proposed solution by putting it into the equation. Differentiating the formula on the right gives $dx/dt = -(x_0 - x_\infty)\,e^{-t/\tau}/\tau$, and that is $-(x - x_\infty)/\tau$. At $t = 0$ the formula gives $x_0$. A check by substitution is always possible, even when you could not have found the solution yourself.

A **second-order** equation contains the second derivative. The most important one is the harmonic oscillator, a mass on a spring ([primer](physics.html#oscillator)):

$$
\frac{d^2x}{dt^2} = -\omega^2x \qquad\Longrightarrow\qquad x(t) = x_0\cos(\omega t) + \frac{v_0}{\omega}\sin(\omega t) .
$$

<div class="legend" markdown="1">
- $x(t)$: the displacement from the rest position.
- $d^2x/dt^2$: the acceleration, also written $\ddot x$.
- $\omega$ (Greek omega): the **angular frequency**, in radians per unit of time. One full oscillation takes the period $2\pi/\omega$. For a mass $m$ on a spring of stiffness $k$, $\omega = \sqrt{k/m}$.
- $x_0$, $v_0$: the two initial conditions, the position and the velocity at $t = 0$. A second-order equation needs two.
</div>

The check: differentiating $\cos(\omega t)$ twice gives $-\omega^2\cos(\omega t)$, and the same holds for the sine.

A second-order equation can always be written as two first-order equations, by giving the first derivative its own name: $dx/dt = v$ and $dv/dt = -\omega^2x$. Hamilton's equations in Module 2 have this form.

**Solving step by step on a computer.** Most differential equations have no solution in formulas. A computer then advances the solution in small steps. The simplest scheme, Euler's method, assumes that the rate of change stays constant during one step:

$$
x(t + h) \approx x(t) + h\,f\big(x(t)\big) \qquad\text{for the equation}\qquad \frac{dx}{dt} = f(x) .
$$

<div class="legend" markdown="1">
- $h$: the step, a small interval of time. In MD it is called $\Delta t$.
- $f(x)$: the right-hand side of the equation, the rate of change as a function of the present value.
- $x(t+h)$: the value one step later. The formula is the [Taylor expansion](#taylor) cut after the first-order term, so each step has an error of $O(h^2)$.
</div>

Repeating the step many times gives the whole solution, with an error that depends on $h$. To cover a fixed time you need a number of steps proportional to $1/h$, and each step adds an error of $O(h^2)$, so the error at the end is $O(h)$. A method whose final error is proportional to $h$ is called a method of first order.

<div class="box key" markdown="1">
**Worked example: relaxation, exact and by steps.** A temperature starts at 280 K and relaxes to 300 K with $\tau = 1$ ps, so $T(t) = 300 - 20\,e^{-t}$ with $t$ in ps. After 1 ps it is $300 - 20\times0.368 = 292.6$ K, and after 3 ps it is 299.0 K.

Now Euler's method with $h = 0.1$ ps. The first step gives $280 + 0.1\times(300-280)/1 = 282.0$ K, against the exact 281.9 K. After ten steps it gives 293.03 K against the exact 292.64 K, an error of 0.38 K. With $h = 0.01$ ps the error after 1 ps is 0.037 K. A step ten times smaller gives an error ten times smaller: Euler's method is of first order.

**Worked example: why MD does not use Euler's method.** Apply it to the oscillator with $\omega = 1$: $x\leftarrow x + h\,v$ and $v\leftarrow v - h\,x$, both computed from the old values. Start from $x = 1$, $v = 0$ with $h = 0.1$. One step gives $x = 1$, $v = -0.1$, and $x^2 + v^2$, which is twice the energy, has grown from 1 to 1.01.

Every step multiplies the energy by $1 + h^2$. After 100 steps it is $1.01^{100} = 2.70$ times too large, while the exact solution keeps it constant. The integrators of Module 4 are built to avoid this.
</div>

**Where the course uses it.**

- [Module 1](01-what-is-md.html), What MD is, and [Module 2](02-classical-mechanics.html), Classical mechanics: the equations of motion of Newton and of Hamilton.
- [Module 4](04-integrators.html), Integrators: integrators are step-by-step solvers of these equations.
- [Module 8](08-thermostats-barostats.html), Thermostats and barostats: the Berendsen thermostat makes the temperature relax as in the first equation above, and the Langevin equation adds a friction force and a random force to Newton's law. The random term is explained in [the section on random numbers](#random-numbers).
- [Module 16](16-kinetics-msm.html), Kinetics and Markov state models: rate equations for the populations of states, whose solutions are exponentials.

<div class="box warn" markdown="1">
**A common mistake.** Choosing the step for convenience and not from the fastest motion in the system. A step-by-step solution is meaningful only when the step is much shorter than the shortest time scale of the equation, which is $\tau$ or the period $2\pi/\omega$. Above a certain step size the numerical solution grows without limit.

Do not mix up the angular frequency $\omega$ with the frequency $\nu = \omega/2\pi$, the number of oscillations per unit of time.
</div>

## Operators {#operators}

**The idea.** A function takes a number and returns a number. An **operator** takes a whole function and returns another function. "Differentiate" is an operator: give it $x^2$ and it returns $2x$. "Multiply by $x$" is another one, and "shift the graph to the left by $c$" is a third. An operator is an instruction, and it does nothing until it is given a function to act on.

Operators enter this course in Modules 2 and 4, where "advance the system by a time $t$" is written as an operator. The reason for the abstraction is practical. Once the time evolution is an operator, an integrator can be designed by cutting that operator into pieces that are each easy to apply.

**The notation.** Operators are often marked with a hat, $\hat A$, or written as a capital letter. An operator acts on whatever stands to its right, and a product of operators is applied from right to left: $\hat A\hat Bf$ means "apply $\hat B$ to $f$, then apply $\hat A$ to the result". The square $\hat A^2$ means "apply twice".

**The exponential of an operator** is defined by the same series as the ordinary exponential:

$$
e^{\hat A} = 1 + \hat A + \tfrac12\hat A^{2} + \tfrac16\hat A^{3} + \dots
$$

<div class="legend" markdown="1">
- $\hat A$: an operator.
- $e^{\hat A}$: a new operator, defined by the sum on the right.
- $1$: the operator "do nothing".
- $\hat A^{n}$: apply $\hat A$ $n$ times. The term with $\hat A^{n}$ carries the factor $1/n!$, as in the [Taylor expansion](#taylor).
</div>

It is needed because of the following fact. If the rate of change of a quantity is obtained by applying a fixed operator, $df/dt = \hat Af$, then the solution is $f(t) = e^{\hat At}f(0)$. This is the operator version of "a rate proportional to the amount gives an exponential" from [the section on exponentials](#exp-log).

One example can be worked out completely. Take the operator $c\,d/dx$, "differentiate and multiply by the constant $c$". Then

$$
e^{c\,d/dx}f(x) = f(x) + c\,f'(x) + \tfrac12c^2f''(x) + \dots = f(x + c) .
$$

<div class="legend" markdown="1">
- $c$: a constant, the size of the shift.
- $d/dx$: the operator "differentiate with respect to $x$".
- $f'$, $f''$: the first and second derivatives of $f$.
- The last equality: the series in the middle is the Taylor expansion of $f$ around $x$ with the step $c$.
</div>

So the exponential of a derivative is a shift. Module 4 uses this: one part of the time-evolution operator shifts all positions by velocity times time, and the other shifts all momenta by force times time.

**Why order can matter.** Two operators **commute** if the order in which they are applied makes no difference. Many pairs do not. Take "differentiate" and "multiply by $x$": multiplying first and then differentiating gives $(xf)' = f + xf'$, while differentiating first and then multiplying gives $xf'$. The difference between the two orders is measured by the **commutator**:

$$
[\hat A,\hat B] = \hat A\hat B - \hat B\hat A .
$$

<div class="legend" markdown="1">
- $[\ ,\ ]$: square brackets with a comma, the commutator.
- $\hat A\hat B$: apply $\hat B$ first, then $\hat A$.
- $\hat B\hat A$: the other order.
- If the result is zero for every function, the two operators commute.
</div>

For ordinary numbers $e^{a+b} = e^{a}e^{b}$. For operators this is guaranteed only when they commute. If they do not, splitting the exponential in general makes an error, and the way of splitting decides how large it is.

For a small number $h$, the simple product $e^{h\hat A}e^{h\hat B}$ differs from $e^{h(\hat A+\hat B)}$ by terms of order $h^2$. The symmetric product $e^{h\hat B/2}e^{h\hat A}e^{h\hat B/2}$ differs only by terms of order $h^3$. The leading errors are built from commutators.

<div class="box key" markdown="1">
**Worked example: the shift, checked.** $f(x) = x^2$, so $f' = 2x$, $f'' = 2$, and all higher derivatives are zero. The series gives $x^2 + c\times2x + \tfrac12c^2\times2 = x^2 + 2cx + c^2 = (x+c)^2$, which is $f(x+c)$.

**Worked example: splitting, with numbers.** A [matrix](#matrices) is an operator on vectors, so the rules can be tested with $2\times2$ matrices. Take the oscillator with $\omega = 1$ and the pair $(x, v)$.

A drift for a time $h$ (move $x$ at fixed $v$) is $\begin{pmatrix}1&h\\0&1\end{pmatrix}$. A kick (change $v$ at fixed $x$) is $\begin{pmatrix}1&0\\-h&1\end{pmatrix}$. The exact motion is a rotation, $\begin{pmatrix}\cos h&\sin h\\-\sin h&\cos h\end{pmatrix}$.

These three matrices are exponentials. With $\mathbf A = \begin{pmatrix}0&1\\0&0\end{pmatrix}$ the drift is $e^{h\mathbf A}$: because $\mathbf A^2 = 0$, the series stops after two terms, $\mathbf 1 + h\mathbf A$. With $\mathbf B = \begin{pmatrix}0&0\\-1&0\end{pmatrix}$ the kick is $e^{h\mathbf B} = \mathbf 1 + h\mathbf B$, and the exact rotation is $e^{h(\mathbf A+\mathbf B)}$. The two do not commute: $\mathbf A\mathbf B - \mathbf B\mathbf A = \begin{pmatrix}-1&0\\0&1\end{pmatrix}$. With $h = 0.1$:

| Scheme | Matrix | Largest error |
|---|---|---|
| exact | $\begin{pmatrix}0.99500&0.09983\\-0.09983&0.99500\end{pmatrix}$ | |
| kick, then drift | $\begin{pmatrix}0.99&0.1\\-0.1&1\end{pmatrix}$ | 0.0050 |
| half kick, drift, half kick | $\begin{pmatrix}0.995&0.1\\-0.09975&0.995\end{pmatrix}$ | 0.00017 |

Halving $h$ divides the first error by 4 and the second by 8. The last line is the velocity Verlet step of Module 4.
</div>

**Where the course uses it.**

- [Module 2](02-classical-mechanics.html), Classical mechanics: the Liouville operator $iL$ and the propagator $e^{iLt}$, the operator that advances the system by the time $t$.
- [Module 4](04-integrators.html), Integrators: splitting the propagator into a kick and a drift gives velocity Verlet. The same idea gives schemes with several time steps and schemes with a thermostat.

<div class="box warn" markdown="1">
**A common mistake.** Reading a product of operators from left to right. In $e^{\hat A}e^{\hat B}e^{\hat C}$ acting on a state, $e^{\hat C}$ acts first. A second one: using rules for numbers, such as $e^{\hat A+\hat B} = e^{\hat A}e^{\hat B}$, without checking that the operators commute.
</div>

## Probability and densities {#probability}

**The idea.** The probability of an outcome is the fraction of times it happens when the same situation is repeated very often. If a salt bridge is formed in 300 of 1000 frames of a simulation, the estimated probability of "formed" is 0.3. Probabilities lie between 0 and 1, and the probabilities of all possible outcomes add up to 1.

This works when the outcomes can be counted: formed or broken, state 1, 2 or 3. A distance is different. It can take any value, and the probability that it is exactly 0.350000... nm is zero. The useful question is "what is the probability of finding it between 0.34 and 0.36 nm?", and the tool is the **probability density**: probability per unit of the variable. A histogram of a trajectory, divided by the number of frames and by the bin width, is an estimate of a probability density.

**The notation.** For outcomes that can be counted, $P_i$ is the probability of outcome $i$, and $\sum_iP_i = 1$. For a continuous variable $x$:

$$
\text{probability that } x \text{ lies between } a \text{ and } b = \int_a^b P(x)\,dx , \qquad \int_{-\infty}^{\infty}P(x)\,dx = 1 .
$$

<div class="legend" markdown="1">
- $P(x)$: the probability density of $x$. It is never negative. Its unit is one over the unit of $x$, for a distance in nm it is nm$^{-1}$.
- $P(x)\,dx$: the probability of finding the variable in the small interval of width $dx$ around $x$.
- $\int_a^b$: the [integral](#integral), here the area under the density between $a$ and $b$.
- The second equation: **normalisation**. The variable has some value with certainty, so the total area is 1.
</div>

Often only the relative weights of the outcomes are known, as in $P_i\propto e^{-E_i/k_BT}$. Normalising means dividing each weight by the sum of all weights. For the Boltzmann weights that sum is the partition function of Module 3.

**Two variables.** The **joint** probability $P(x,y)$ describes two quantities at once. From it:

$$
P(x) = \int P(x,y)\,dy , \qquad P(x\mid y) = \frac{P(x,y)}{P(y)} .
$$

<div class="legend" markdown="1">
- $P(x,y)$: the joint density, the probability of finding both values together, per unit of $x$ and per unit of $y$.
- $P(x)$: the **marginal** density of $x$, whatever $y$ is. It is obtained by adding up over all values of $y$. For outcomes that can be counted, the integral is a sum.
- $P(x\mid y)$: the **conditional** density, read "the probability of $x$ given $y$". It is the distribution of $x$ among only those cases in which the second variable has the value $y$.
- $P(y)$: the marginal density of $y$.
</div>

Two variables are **independent** if knowing one tells you nothing about the other. Then $P(x\mid y) = P(x)$, and the joint probability is the product $P(x,y) = P(x)\,P(y)$.

**Comparing two distributions.** Module 15 needs a single number that says how far a model distribution is from a reference distribution over the same outcomes. The standard choice is the **relative entropy**, also called the Kullback-Leibler divergence:

$$
S_{rel} = \sum_i P_i\,\ln\frac{P_i}{Q_i} .
$$

<div class="legend" markdown="1">
- $P_i$: the probability of outcome $i$ in the reference distribution. In Module 15 this is the atomistic simulation.
- $Q_i$: the probability of the same outcome in the model that is judged. In Module 15 this is the coarse-grained model.
- $\ln(P_i/Q_i)$: how far the model is off for outcome $i$, on a [logarithmic](#exp-log) scale. It is positive where the model gives too little probability and negative where it gives too much.
- $\sum_iP_i\dots$: the average of that logarithm, with each outcome weighted by its reference probability. For a continuous variable the sum becomes an [integral](#integral) over the two densities, whose units cancel in the ratio.
- $S_{rel}$: the relative entropy, a pure number.
</div>

It has three properties. It is never negative. It is zero only when the two distributions are the same, $Q_i = P_i$ for every $i$. And it is not symmetric: exchanging $P$ and $Q$ changes the value, so it is not a distance in the usual sense.

The asymmetry has a meaning. An outcome that the reference visits often and that the model calls nearly impossible has a large $\ln(P_i/Q_i)$ and a large weight $P_i$, so it is punished hard. An outcome that the model invents and the reference never visits has the weight $P_i = 0$ and costs nothing directly.

Making $S_{rel}$ as small as possible by changing the model is the same as making $\sum_iP_i\ln Q_i$ as large as possible, because the remaining part $\sum_iP_i\ln P_i$ does not depend on the model. In words: choose the model that gives the highest probability to the reference data. This is called **maximum likelihood**, a term that appears in Modules 16 and 17.

<details markdown="1"><summary>Optional: why it is never negative</summary>
The logarithm lies below its tangent at 1: $\ln x\le x - 1$ for every positive $x$. Apply this with $x = Q_i/P_i$: $-S_{rel} = \sum_iP_i\ln(Q_i/P_i)\le\sum_iP_i\,(Q_i/P_i - 1) = \sum_iQ_i - \sum_iP_i = 1 - 1 = 0$. Equality needs $Q_i = P_i$ for every $i$.
</details>

<div class="box key" markdown="1">
**Worked example: relative entropy.** The reference has two states with $P = (0.5, 0.5)$, and a model gives $Q = (0.9, 0.1)$. Then $S_{rel} = 0.5\ln(0.5/0.9) + 0.5\ln(0.5/0.1) = -0.294 + 0.805 = 0.511$. With the roles exchanged it is $0.9\ln(0.9/0.5) + 0.1\ln(0.1/0.5) = 0.529 - 0.161 = 0.368$: a different number. A model with $Q = (0.5, 0.5)$ gives 0.
</div>

A free-energy profile along a coordinate $\xi$ is built from a marginal density, with all other coordinates summed over: $W(\xi) = -k_BT\ln P(\xi)$ plus a constant (Module 12). The constant absorbs the unit of the density, since a logarithm needs a pure number.

<div class="box key" markdown="1">
**Worked example: normalising Boltzmann weights.** Three states have the energies 0, 2 and 5 kJ/mol. At 300 K, with $k_BT = 2.494$ kJ/mol, their weights $e^{-E/k_BT}$ are 1, 0.448 and 0.135. The sum is 1.583. Dividing by it gives the probabilities 0.632, 0.283 and 0.085, which add up to 1.

**Worked example: a density from a histogram.** Of 1000 frames, 150 have a distance between 0.30 and 0.32 nm. The probability of that bin is 0.15. The density there is 0.15 divided by the bin width of 0.02 nm, which is 7.5 nm$^{-1}$. A density can be larger than 1. Only its integral is limited to 1.

**Worked example: joint, marginal, conditional.** In 1000 frames a ligand is bound or unbound, and a loop is open or closed:

| | loop closed | loop open | total |
|---|---|---|---|
| bound | 540 | 60 | 600 |
| unbound | 120 | 280 | 400 |
| total | 660 | 340 | 1000 |

The joint probability of "bound and open" is $60/1000 = 0.06$. The marginal probabilities are 0.60 for "bound" and 0.34 for "open". The conditional probability of an open loop given a bound ligand is $60/600 = 0.10$, against $280/400 = 0.70$ given no ligand. The two events are not independent: independence would require a joint probability of $0.60\times0.34 = 0.204$.
</div>

**Where the course uses it.**

- [Module 3](03-statistical-mechanics.html), Statistical mechanics: the Boltzmann distribution, with the partition function as its normalisation.
- [Module 8](08-thermostats-barostats.html), Thermostats and barostats: a thermostat is judged by whether it produces the correct probability distribution of the kinetic energy.
- [Module 11](11-analysis-statistics.html), Analysis and statistics: histograms and the radial distribution function.
- [Module 12](12-free-energy-pmf.html), Free energy and the potential of mean force: the density $P(\xi)$ along a coordinate gives the potential of mean force.
- [Module 16](16-kinetics-msm.html), Kinetics and Markov state models: transition probabilities are conditional probabilities.
- [Module 17](17-machine-learning.html), Machine-learned potentials: models that generate structures directly must give each structure the correct probability.

<div class="box warn" markdown="1">
**A common mistake.** Reading a density as a probability. A density has a unit, can exceed 1, and changes its numerical value when the unit or the variable is changed. Two histograms with different bin widths cannot be compared until each is divided by its bin width.

Also, $P(x\mid y)$ and $P(y\mid x)$ are different. In the table, the probability of an open loop given a bound ligand is 0.10, but the probability of a bound ligand given an open loop is $60/340 = 0.18$.
</div>

## Mean, variance, standard error {#averages}

**The idea.** A distribution is summarised by two numbers: where its centre is, and how wide it is. The **mean** is the centre, and the **variance** and the **standard deviation** measure the width. A third number answers a different question: how well do I know the mean from the limited data that I have? That is the **standard error**. Almost every number reported from a simulation is a mean, and it is incomplete without its standard error.

**The notation.**

$$
\langle x\rangle = \sum_i x_i\,P_i \quad\text{or}\quad \int x\,P(x)\,dx , \qquad \sigma^2 = \big\langle (x - \langle x\rangle)^2\big\rangle = \langle x^2\rangle - \langle x\rangle^2 .
$$

<div class="legend" markdown="1">
- $\langle x\rangle$: the **mean** or **expectation value** of $x$: each possible value weighted by its [probability](#probability). The sum is for outcomes that can be counted, the integral for a continuous variable.
- $x - \langle x\rangle$: the deviation from the mean, often written $\delta x$.
- $\sigma^2$ (sigma squared): the **variance**, the mean of the squared deviation. Its unit is the unit of $x$ squared.
- $\sigma$: the **standard deviation**, the square root of the variance. It has the unit of $x$ and is the typical distance of a single value from the mean.
- $\langle x^2\rangle - \langle x\rangle^2$: a second way to compute the variance, as the mean of the square minus the square of the mean.
</div>

From $N$ measured values $x_1,\dots,x_N$ the same quantities are estimated by

$$
\bar x = \frac1N\sum_{n=1}^{N}x_n , \qquad s^2 = \frac{1}{N-1}\sum_{n=1}^{N}(x_n - \bar x)^2 , \qquad \mathrm{SE} = \frac{s}{\sqrt N} .
$$

<div class="legend" markdown="1">
- $x_n$: the $n$-th measured value, for example the value in frame $n$.
- $N$: the number of values.
- $\bar x$: the sample mean, the estimate of $\langle x\rangle$.
- $s^2$, $s$: the sample variance and the sample standard deviation, the estimates of $\sigma^2$ and $\sigma$. Dividing by $N-1$ in place of $N$ corrects for the fact that $\bar x$ was computed from the same data.
- $\mathrm{SE}$: the **standard error of the mean**: the standard deviation that $\bar x$ itself would show if the whole measurement were repeated many times. The formula holds for $N$ independent values.
</div>

The $\sqrt N$ in the standard error comes from one rule: the variances of independent values add (the reason is given in [the section on random numbers](#random-numbers)). The sum of $N$ independent values has the variance $N\sigma^2$. The mean is that sum divided by $N$, so its variance is $N\sigma^2/N^2 = \sigma^2/N$ and its standard deviation is $\sigma/\sqrt N$. To halve the error you need four times as much data.

The **central limit theorem** adds the shape. It says that the mean of $N$ independent values drawn from the same distribution has a distribution that approaches a [Gaussian](#gaussian) of width $\sigma/\sqrt N$ around $\langle x\rangle$ as $N$ grows, whatever the distribution of the single values, as long as their variance is finite.

For two quantities measured together, the **covariance** and the **correlation coefficient** say whether they vary together:

$$
\mathrm{cov}(x,y) = \big\langle (x - \langle x\rangle)(y - \langle y\rangle)\big\rangle , \qquad r = \frac{\mathrm{cov}(x,y)}{\sigma_x\,\sigma_y} .
$$

<div class="legend" markdown="1">
- $x$, $y$: two quantities measured in the same frames.
- $\mathrm{cov}(x,y)$: the covariance. It is positive if $y$ tends to be above its mean when $x$ is above its mean, negative if $y$ then tends to be below, and zero if there is no linear relation. The covariance of $x$ with itself is the variance.
- $\sigma_x$, $\sigma_y$: the standard deviations of $x$ and of $y$.
- $r$: the correlation coefficient, a pure number between $-1$ and $1$.
</div>

For many quantities $x_1, x_2, \dots$ measured together, the covariances of all pairs are collected in the **covariance matrix**, with the entries $C_{ab} = \mathrm{cov}(x_a, x_b)$. It is a symmetric [matrix](#matrices), and its diagonal holds the variances. The correlation coefficient of a quantity with the same quantity a time $t$ later, taken as a function of $t$, is its **autocorrelation function**. It starts at 1, and its decay tells you after how long two frames can be counted as independent (Module 11).

<div class="box key" markdown="1">
**Worked example: five values.** The values are 2.1, 2.5, 1.9, 2.3 and 2.2, and their mean is $11.0/5 = 2.2$. The deviations are $-0.1$, $0.3$, $-0.3$, $0.1$ and $0$. Their squares add up to 0.20, so $s^2 = 0.20/4 = 0.05$ and $s = 0.224$. The standard error is $0.224/\sqrt5 = 0.10$. Report $2.2\pm0.1$, and say that the number after the $\pm$ sign is one standard error.

One standard error on each side of the mean covers the true value in about 68 % of the cases, and only when $N$ is large. A 95 % **confidence interval** is wider: the mean $\pm\,t\,s/\sqrt N$. The factor $t$ (a convention for the letter, and not a time here) is 1.96 for large $N$ and grows when $N$ is small: 2.78 for five values and 4.30 for three. For the five values above the interval is $2.2\pm0.28$. Module 11 uses this for a small number of repeated simulations.

**Worked example: a die.** Each of the six faces has the probability 1/6. Then $\langle x\rangle = (1+2+\dots+6)/6 = 3.5$ and $\langle x^2\rangle = (1+4+\dots+36)/6 = 15.17$, so $\sigma^2 = 15.17 - 12.25 = 2.92$ and $\sigma = 1.71$. The mean of 100 throws has a standard error of $1.71/\sqrt{100} = 0.17$. Its distribution is close to a Gaussian, although a single throw is spread evenly over six values.

**Worked example: correlation.** $x = (1, 2, 3)$ and $y = (2, 4, 7)$. The means are 2 and 4.33. The products of the deviations are $(-1)\times(-2.33)$, $0$ and $1\times2.67$, which add up to 5.0. Dividing by $N-1 = 2$ gives a covariance of 2.5. The standard deviations are 1 and 2.52, so $r = 2.5/(1\times2.52) = 0.99$.
</div>

**Where the course uses it.**

- [Module 3](03-statistical-mechanics.html), Statistical mechanics: every observable is an ensemble average, and the heat capacity is the variance of the energy.
- [Module 5](05-force-field-form.html), The form of a force field: the variance of a harmonic coordinate shows how stiff a bond or an angle is.
- [Module 8](08-thermostats-barostats.html), Thermostats and barostats: a correct thermostat gives the right variance of the kinetic energy as well as the right mean.
- [Module 11](11-analysis-statistics.html), Analysis and statistics: the autocorrelation function, standard errors from correlated data, block averaging, confidence intervals from a few repeats, and the covariance matrix behind principal component analysis.
- [Module 12](12-free-energy-pmf.html), Free energy and the potential of mean force, and [Module 13](13-alchemical-free-energy.html), Alchemical free energy: estimators (recipes that turn the samples into a free energy) that are chosen to have the smallest variance.

<div class="box warn" markdown="1">
**A common mistake.** Confusing the standard deviation with the standard error. The standard deviation is the spread of single values. It is a property of the system and does not shrink when you collect more data. The standard error is the uncertainty of the mean, and it shrinks as $1/\sqrt N$.

A second mistake is specific to simulations. Successive frames are not independent, so the $N$ in the formula is not the number of frames. Module 11 shows how to find the effective number of independent values.
</div>

## The Gaussian {#gaussian}

**The idea.** The Gaussian, or normal distribution, is the bell-shaped curve. It appears for two reasons. The first is statistical: whenever a quantity is the sum of many small independent contributions, its distribution is close to a Gaussian (the central limit theorem of [the previous section](#averages)). The second is physical: at a fixed temperature, a coordinate with a quadratic energy has an exactly Gaussian distribution. A bond near its rest length, a velocity component of an atom and a restrained distance are all of this kind.

**The notation.**

$$
P(x) = \frac{1}{\sqrt{2\pi\sigma^2}}\,\exp\left(-\frac{(x-\mu)^2}{2\sigma^2}\right).
$$

<div class="legend" markdown="1">
- $x$: the variable.
- $\mu$ (Greek mu): the mean, the position of the peak.
- $\sigma$: the standard deviation, the width. About 68.3 % of the probability lies within one $\sigma$ of the mean, 95.4 % within two and 99.7 % within three.
- $\exp(\dots)$: the [exponential function](#exp-log). The exponent is minus one half of the squared distance from the mean, measured in units of $\sigma$.
- $1/\sqrt{2\pi\sigma^2}$: the factor that makes the total area equal to 1. It is also the height of the peak.
</div>

A Gaussian is fixed completely by its mean and its variance. The shorthand $x\sim\mathcal N(\mu,\sigma^2)$ means "$x$ is distributed as a Gaussian with mean $\mu$ and variance $\sigma^2$".

**Gaussian integrals.** Two integrals are used again and again in statistical mechanics:

$$
\int_{-\infty}^{\infty}e^{-ax^2}\,dx = \sqrt{\frac{\pi}{a}} , \qquad \int_{-\infty}^{\infty}x^2\,e^{-ax^2}\,dx = \frac{1}{2a}\sqrt{\frac{\pi}{a}} .
$$

<div class="legend" markdown="1">
- $a$: a positive constant. A large $a$ gives a narrow curve.
- $e^{-ax^2}$: a Gaussian centred at zero that is not normalised.
- $\pi$: the number 3.14159...
- The limits $-\infty$ and $\infty$: the [integral](#integral) runs over all values of $x$.
</div>

With $a = 1/(2\sigma^2)$ the first integral is $\sqrt{2\pi\sigma^2}$. This is where the factor in front of the Gaussian comes from: dividing by it makes the area equal to 1. Dividing the second integral by the first gives the mean of $x^2$ under the weight $e^{-ax^2}$: $\langle x^2\rangle = 1/(2a)$, which is $\sigma^2$ for the same $a$. Now apply this to a spring at the temperature $T$. Its Boltzmann weight is $e^{-kx^2/2k_BT}$, so $a = k/2k_BT$ and

$$
\langle x^2\rangle = \frac{k_BT}{k} , \qquad \big\langle\tfrac12kx^2\big\rangle = \tfrac12k_BT .
$$

<div class="legend" markdown="1">
- $k$: the stiffness of the spring.
- $k_B$: Boltzmann's constant, and $T$: the temperature. $k_BT = 2.494$ kJ/mol at 300 K.
- $\langle x^2\rangle$: the variance of the displacement $x$, whose mean is zero.
- $\langle\tfrac12kx^2\rangle$: the mean potential energy of the spring.
</div>

A stiff spring fluctuates little and a hot one more, and the mean energy is $\tfrac12k_BT$ whatever the stiffness. Module 3 calls this equipartition. The same calculation with $\tfrac12mv^2$ in place of $\tfrac12kx^2$ gives the distribution of a velocity component: a Gaussian with the variance $k_BT/m$.

**The error function.** The area under a Gaussian up to a finite limit cannot be written with elementary functions, so it has its own name:

$$
\operatorname{erf}(x) = \frac{2}{\sqrt\pi}\int_0^{x}e^{-t^2}\,dt , \qquad \operatorname{erfc}(x) = 1 - \operatorname{erf}(x) .
$$

<div class="legend" markdown="1">
- $\operatorname{erf}$: the **error function**. It rises from 0 at $x = 0$ towards 1 as $x\to\infty$.
- $\operatorname{erfc}$: the **complementary error function**, the part of the area that lies beyond $x$. It falls from 1 towards 0, faster than an exponential.
- $t$: the integration variable. It is not a time here.
- $2/\sqrt\pi$: the factor that makes the limiting value equal to 1.
</div>

The probability that a Gaussian variable lies within $n$ standard deviations of its mean is $\operatorname{erf}(n/\sqrt2)$.

<div class="box key" markdown="1">
**Worked example: the width of a restrained coordinate.** A distance is held by a spring with, say, $k = 1000$ kJ mol$^{-1}$ nm$^{-2}$ at 300 K. Its standard deviation is $\sqrt{k_BT/k} = \sqrt{2.494/1000} = 0.050$ nm. About 95 % of the frames lie within 0.10 nm of the centre.

**Worked example: the velocity of a water molecule.** With $m = 18$ u, each velocity component has $\sigma = \sqrt{k_BT/m} = \sqrt{2.494/18} = 0.372$ nm/ps, which is 372 m/s. The speed combines the three components, and its root-mean-square value is $\sqrt3$ times larger, 645 m/s. The units work out because 1 kJ/mol is 1 u nm$^2$ ps$^{-2}$.

**Worked example: values of the error function.** $\operatorname{erf}(1/\sqrt2) = 0.683$, $\operatorname{erf}(2/\sqrt2) = 0.954$ and $\operatorname{erf}(3/\sqrt2) = 0.997$: the three percentages quoted above. And $\operatorname{erfc}(1) = 0.157$, $\operatorname{erfc}(2) = 0.0047$, $\operatorname{erfc}(3) = 0.000022$. This fast decay lets Module 7 cut off one part of the electrostatic sum at a short distance.
</div>

**Where the course uses it.**

- [Module 3](03-statistical-mechanics.html), Statistical mechanics: the momentum integrals of the partition function are Gaussian integrals, and the velocities follow a Gaussian (Maxwell-Boltzmann) distribution.
- [Module 5](05-force-field-form.html), The form of a force field: the thermal fluctuation $\sqrt{k_BT/k}$ of a bond length or an angle.
- [Module 7](07-boundaries-electrostatics.html), Boundaries and electrostatics: Ewald summation surrounds each charge with a Gaussian cloud, and erf and erfc appear in the energy.
- [Module 8](08-thermostats-barostats.html), Thermostats and barostats: thermostats that draw velocities from a Gaussian.
- [Module 12](12-free-energy-pmf.html), Free energy and the potential of mean force: the Gaussian distribution of a restrained coordinate sets the spacing of umbrella windows.
- [Module 13](13-alchemical-free-energy.html), Alchemical free energy: a Gaussian approximation for the distributions of energy differences and of work.
- [Module 14](14-enhanced-sampling.html), Enhanced sampling: metadynamics builds its bias from Gaussian hills.

<div class="box warn" markdown="1">
**A common mistake.** Mixing up $\sigma$ and $\sigma^2$, or losing the 2 in $2\sigma^2$. In $e^{-ax^2}$ the variance is $1/(2a)$, and not $1/a$. And not everything is Gaussian: a distribution with two peaks, or with a long tail, is badly described by a mean and a standard deviation alone.
</div>

## Delta functions {#delta}

**The idea.** A delta is a selector. It is zero almost everywhere and picks out the one case in which two things are equal. There are two versions, one for labels that are counted and one for continuous variables.

The **Kronecker delta** $\delta_{ij}$ compares two labels: it is 1 if they are the same and 0 otherwise. The **Dirac delta** $\delta(x)$ does the same for a continuous variable.

Picture a histogram bar centred at zero whose area is 1. Make the bar narrower and narrower while keeping its area at 1, and it gets taller and taller. The Dirac delta is the limit: an infinitely narrow, infinitely tall spike of area 1. It is used to write "count only those configurations in which this quantity has exactly this value".

**The notation.**

$$
\delta_{ij} = \begin{cases}1 & \text{if } i = j\\ 0 & \text{if } i\ne j\end{cases} \qquad\text{so that}\qquad \sum_j a_j\,\delta_{ij} = a_i .
$$

<div class="legend" markdown="1">
- $i$, $j$: two labels, for example two atom numbers or two of the directions $x$, $y$, $z$.
- $\delta_{ij}$: the Kronecker delta.
- The brace: a definition by cases.
- $\sum_ja_j\,\delta_{ij}$: in the sum over $j$, every term is zero except the one with $j = i$. The delta "picks out" $a_i$.
</div>

The entries of the identity [matrix](#matrices) are $\delta_{ij}$.

$$
\int f(x)\,\delta(x - a)\,dx = f(a) , \qquad \int\delta(x - a)\,dx = 1 .
$$

<div class="legend" markdown="1">
- $\delta(x - a)$: the Dirac delta, a spike located at $x = a$, where its argument is zero.
- $f(x)$: any smooth function.
- The first equation: the spike is so narrow that only the value of $f$ at $a$ contributes. The delta picks out $f(a)$.
- The second equation: the area of the spike is 1.
- The integrals run over any range that contains the point $a$.
</div>

Because its integral over $x$ is the pure number 1, $\delta(x)$ has the unit of $1/x$, like a [probability density](#probability). A probability density can be written with it. The density of a quantity $\xi$ that is computed from the configuration $\mathbf r$ is the average $\langle\delta(\xi(\mathbf r) - \xi')\rangle$: the fraction of configurations whose $\xi$ equals the chosen value $\xi'$, per unit of $\xi$. A histogram with a finite bin width is the practical version of this formula.

**The step function.** The step function $\Theta(x)$ is 0 for $x < 0$ and 1 for $x > 0$. It switches something on at a threshold: $\Theta(r_c - r)$ is 1 for distances $r$ inside a cutoff $r_c$ and 0 outside. Its derivative is the Dirac delta, because the step rises by 1 within an infinitely narrow interval.

<div class="box key" markdown="1">
**Worked example: Kronecker and Dirac.** With $a_1 = 5$, $a_2 = 7$ and $a_3 = 9$, the sum $\sum_{j=1}^{3}a_j\,\delta_{2j}$ is $5\times0 + 7\times1 + 9\times0 = 7$.

$\int(x^2+1)\,\delta(x-2)\,dx = 2^2 + 1 = 5$. To see the limit at work, replace the delta by a normalised [Gaussian](#gaussian) centred at 2. With the width $\sigma = 0.5$ the integral is 5.25, with $\sigma = 0.1$ it is 5.01, and with $\sigma = 0.01$ it is 5.0001.

**Worked example: from a delta to a histogram.** In [the section on probability](#probability), 150 of 1000 frames fell in a bin of width 0.02 nm, which gave a density of 7.5 nm$^{-1}$. That number is an estimate of $\langle\delta(r - r')\rangle$ at $r' = 0.31$ nm, with the infinitely narrow spike replaced by a bar of width 0.02 nm and height $1/0.02 = 50$ nm$^{-1}$. The bar has area 1, and its average over the frames is $0.15\times50 = 7.5$ nm$^{-1}$.
</div>

**Where the course uses it.**

- [Module 2](02-classical-mechanics.html), Classical mechanics, and [Module 3](03-statistical-mechanics.html), Statistical mechanics: $\delta(H - E)$ describes a system whose energy is exactly $E$.
- [Module 3](03-statistical-mechanics.html), Statistical mechanics, and [Module 12](12-free-energy-pmf.html), Free energy and the potential of mean force: the definition of the probability density along a collective variable, a single coordinate $\xi(\mathbf r)$ computed from the positions, such as a distance.
- [Module 8](08-thermostats-barostats.html), Thermostats and barostats: the random force of Langevin dynamics is uncorrelated between different directions, $\delta_{ab}$, and between different times, $\delta(t-t')$.
- [Module 15](15-coarse-grained.html), Coarse-grained models: in the definition of a coarse-grained potential, a delta selects all atomistic configurations that map to the same coarse-grained one.

<div class="box warn" markdown="1">
**A common mistake.** Several different things share the letter. $\delta_{ij}$ with two labels is the Kronecker delta, and $\delta(\dots)$ with an argument in brackets is usually the Dirac delta. $\delta x$ or $\delta A$ directly in front of a quantity is a small change or a deviation from the mean. And in Module 2, $\delta(t)$ is the distance between two trajectories, an ordinary function of time. The list under each formula says which one is meant.

Also, a Dirac delta has a value only inside an integral. On its own, "$\delta(0)$" is not a number.
</div>

## Fourier series and transforms {#fourier}

**The idea.** A musical chord is several pure notes sounding together, and a trained ear can name the notes. Fourier analysis does this for any function: it writes the function as a sum of pure waves (sines and cosines) and tells you how much of each wave is present. The list of amounts is the **spectrum**. Nothing is lost: the function and its spectrum are two descriptions of the same thing.

Two cases matter for MD. A simulation box that repeats periodically makes every quantity inside it a periodic function of position, and periodic functions are sums of waves that fit into the box. And some problems that are hard in ordinary space become easy when they are written wave by wave. The long-range part of the electrostatic energy is the main example.

**The notation.** A wave along $x$ is $\cos(kx)$, and a wave in time is $\cos(\omega t)$.

$$
k = \frac{2\pi}{\lambda} , \qquad \omega = \frac{2\pi}{T} = 2\pi\nu .
$$

<div class="legend" markdown="1">
- $\lambda$: the **wavelength**, the distance after which the wave repeats.
- $k$: the **wave number**, in radians per unit of length. A short wavelength means a large $k$. In three dimensions it becomes the **wave vector** $\mathbf k$, which points along the direction in which the wave varies, and the wave is $\cos(\mathbf k\cdot\mathbf r)$.
- $T$: for a wave in time, the **period** after which it repeats. It is not the temperature here.
- $\nu$ (Greek nu): the **frequency**, the number of oscillations per unit of time, $1/T$.
- $\omega$: the **angular frequency**, in radians per unit of time.
</div>

A function $f(x)$ that repeats after a length $L$ can be written as a **Fourier series**:

$$
f(x) = \sum_{n=-\infty}^{\infty}c_n\,e^{ik_nx} , \qquad k_n = \frac{2\pi n}{L} , \qquad c_n = \frac1L\int_0^{L}f(x)\,e^{-ik_nx}\,dx .
$$

<div class="legend" markdown="1">
- $L$: the length after which $f$ repeats, for example the edge of a periodic simulation box.
- $\sum_{n=-\infty}^{\infty}$: a sum over all whole numbers, the negative ones included.
- $n$: a whole number that labels the waves. $n = 0$ is the constant part, $n = \pm1$ the wave with one full oscillation per length $L$, $n = \pm2$ the wave with two, and so on.
- $k_n$: the allowed wave numbers. Only waves that fit a whole number of times into $L$ occur.
- $e^{ik_nx}$: a wave written as a [complex exponential](#complex), $\cos(k_nx) + i\sin(k_nx)$.
- $c_n$: the **Fourier coefficient**, a complex number that says how much of wave $n$ is in $f$, and with which phase. $c_0$ is the average of $f$.
- The integral: the recipe for the coefficients. Multiplying by $e^{-ik_nx}$ and averaging over one period filters out wave $n$.
</div>

For a real function the terms $n$ and $-n$ combine into $a_n\cos(k_nx) + b_n\sin(k_nx)$, the form with cosines and sines. The set of all wave vectors is called **reciprocal space** or Fourier space, because $k$ has the unit of one over length. Ordinary space is then called real space. In a box with the edges $L_x$, $L_y$, $L_z$ the allowed wave vectors are $\mathbf k = 2\pi(n_x/L_x,\ n_y/L_y,\ n_z/L_z)$ with whole numbers $n_x$, $n_y$, $n_z$.

A function that does not repeat needs all wave numbers, and the sum becomes an integral, the **Fourier transform**:

$$
\tilde f(k) = \int_{-\infty}^{\infty}f(x)\,e^{-ikx}\,dx , \qquad f(x) = \frac{1}{2\pi}\int_{-\infty}^{\infty}\tilde f(k)\,e^{ikx}\,dk .
$$

<div class="legend" markdown="1">
- $\tilde f(k)$: the Fourier transform of $f$, read "f tilde". It plays the role of the coefficients $c_n$ for a continuous $k$.
- The second formula: the inverse transform, which rebuilds $f$ from its spectrum.
- $k$: the wave number, which can now be any real number and is no longer limited to the values $k_n$.
- $1/2\pi$: a factor whose place is a convention. Some books put it in the first formula or split it between the two.
- The signs of the exponents: also a convention. This page uses $e^{-ikx}$ to go from $f$ to its spectrum and $e^{+ikx}$ to go back, in the series and in the transform. Other texts swap the two signs. Module 7 writes its structure factor with the plus sign, $S(\mathbf k) = \sum_jq_j\,e^{i\mathbf k\cdot\mathbf r_j}$. For a real function the two choices give complex conjugates of each other, so a modulus squared such as $\lvert S(\mathbf k)\rvert^2$ is the same with both.
- Other symbols: as in the list above.
</div>

**Why reciprocal space helps.** Three properties do most of the work.

1. *Smooth functions need few waves.* The coefficients of a smooth function fall off quickly with $n$, so a short sum is enough. A function with a jump or a spike needs very many.
2. *Narrow becomes wide.* A Gaussian of width $\sigma$ in $x$ has a Gaussian spectrum of width $1/\sigma$ in $k$: the function $e^{-x^2/2\sigma^2}$ transforms into $\sigma\sqrt{2\pi}\,e^{-\sigma^2k^2/2}$.
3. *Derivatives become multiplications.* Since $\frac{d}{dx}e^{ikx} = ik\,e^{ikx}$, differentiating a function multiplies each of its Fourier coefficients by $ik$, and the [Laplacian](#divergence) multiplies them by $-k^2$. A differential equation becomes an ordinary equation for each wave separately.

Property 3 solves Poisson's equation at once. In the units of Module 7 it reads $\nabla^2\phi = -4\pi\rho$. For each wave vector this becomes $-k^2\tilde\phi(\mathbf k) = -4\pi\tilde\rho(\mathbf k)$, so $\tilde\phi(\mathbf k) = 4\pi\tilde\rho(\mathbf k)/k^2$ for every wave vector except $\mathbf k = 0$, where the division is not possible (Module 7 leaves that term out).

Properties 1 and 2 explain the Ewald method of the same module. Point charges are spikes and would need endless waves, so each charge is first smeared into a Gaussian cloud, whose spectrum dies out quickly. Module 7 writes the cloud as $e^{-\alpha^2r^2}$, which is a Gaussian with $\sigma^2 = 1/(2\alpha^2)$. By property 2 its spectrum falls as $e^{-\sigma^2k^2/2} = e^{-k^2/4\alpha^2}$, the factor that appears in the reciprocal-space sum of that module.

For data stored on a grid of $M$ points, the transform is computed by the fast Fourier transform (FFT), whose cost grows as $M\log M$.

<div class="box key" markdown="1">
**Worked example: a torsion energy is a short Fourier series.** The energy of rotation about a bond repeats after a full turn, so it is a sum of cosines of multiples of the angle $\phi$. Take, say, $U(\phi) = 2\,[1+\cos\phi] + 5\,[1+\cos3\phi]$ in kJ/mol. At 0, 60, 120 and 180 degrees it gives 14, 3, 11 and 0 kJ/mol. The term with $\cos3\phi$ makes three barriers per turn, and the term with $\cos\phi$ makes them unequal.

**Worked example: a jump needs many waves, a smooth cloud few.** The square wave that is $+1$ on the first half of its period and $-1$ on the second half is $\tfrac4\pi\left[\sin(k_1x) + \tfrac13\sin(3k_1x) + \tfrac15\sin(5k_1x) + \dots\right]$. At the quarter-period point, where the function is 1, the sum of the first 1, 2, 3, 10 and 100 terms is 1.273, 0.849, 1.103, 0.968 and 0.997. The coefficients fall only as $1/n$.

Compare a Gaussian of width $\sigma = 0.1\,L$ repeated in every box. Its coefficients fall as $e^{-\sigma^2k_n^2/2}$. Relative to $n = 0$ they are 0.82, 0.45 and 0.17 for $n = 1$, 2 and 3, then 0.007 for $n = 5$ and $3\times10^{-9}$ for $n = 10$.

**Worked example: Poisson's equation for one wave.** If $\rho(x) = \cos(kx)$, then $\phi(x) = (4\pi/k^2)\cos(kx)$. The check: differentiating $\phi$ twice gives $-k^2\phi = -4\pi\cos(kx)$, which is $-4\pi\rho$.
</div>

**Where the course uses it.**

- [Module 5](05-force-field-form.html), The form of a force field: the torsion energy is a short Fourier series in the dihedral angle.
- [Module 7](07-boundaries-electrostatics.html), Boundaries and electrostatics: the reciprocal-space part of the Ewald sum, the structure factor, and the fast Fourier transform in particle-mesh Ewald.
- [Module 10](10-running-a-simulation.html), Running a simulation: the input file sets the largest allowed spacing of the grid on which that transform is done (the line `fourierspacing`).

<div class="box warn" markdown="1">
**A common mistake.** Factors of $2\pi$. The frequency $\nu$ and the angular frequency $\omega = 2\pi\nu$ differ by $2\pi$. So do the wavenumber $1/\lambda$ of spectroscopy ([primer](physics.html#waves)) and the wave number $k = 2\pi/\lambda$ used here. Before you compare two formulas, check which one each of them uses and where the $1/2\pi$ of the transform has been put.
</div>

## Lagrange multipliers {#lagrange-multipliers}

**The idea.** Finding the highest point of a hill is one problem. Finding the highest point *along a given path* across the hill is another, and its answer is usually not the summit. Many problems are of the second kind: make something as large or as small as possible while a condition holds. Find the charges that best reproduce a potential, under the condition that they add up to the total charge of the molecule. Move the atoms as Newton's law demands, under the condition that a bond keeps its length.

The method of Lagrange multipliers turns such a problem into an ordinary one. Walk along the path and watch the contour lines of the hill. As long as the path crosses contour lines, you are going up or down. At the highest point of the path, the path touches a contour line without crossing it. At that point the direction of steepest ascent of the hill is perpendicular to the path.

**The notation.** Maximise or minimise $f(x,y)$ under the condition $g(x,y) = 0$. At the solution,

$$
\nabla f = \lambda\,\nabla g \qquad\text{together with}\qquad g(x,y) = 0 .
$$

<div class="legend" markdown="1">
- $f(x,y)$: the function to be made as large or as small as possible.
- $g(x,y) = 0$: the condition, also called the constraint. It defines the allowed path.
- $\nabla f$, $\nabla g$: the two [gradients](#gradient). $\nabla g$ is perpendicular to the path, because $g$ does not change along it.
- $\lambda$: the **Lagrange multiplier**, an extra unknown number. The first equation says that the two gradients are parallel, and $\lambda$ is the factor between their lengths.
</div>

A compact way to remember this: form $f - \lambda g$ and set its partial derivatives with respect to $x$, $y$ and $\lambda$ to zero. The first two give $\nabla f = \lambda\nabla g$, and the third gives back the condition. With several conditions there is one multiplier per condition. Some texts write $f + \lambda g$, which only changes the sign of $\lambda$.

The multiplier has a meaning. It says how much the best value of $f$ would change if the condition were relaxed a little.

In mechanics this becomes a force. A constraint $\sigma(\mathbf r) = 0$ on the positions adds to each atom a force $-\lambda\nabla_i\sigma$. Its direction is known in advance: along the gradient of the constraint, which for a bond is along the bond. The multiplier is its unknown strength, and it is found from the requirement that the constraint still holds after the time step.

<div class="box key" markdown="1">
**Worked example: the largest rectangle.** Maximise the area $f = xy$ of a rectangle whose two sides add up to 10, so $g = x + y - 10$. The gradients are $\nabla f = (y, x)$ and $\nabla g = (1, 1)$, and the two conditions are $y = \lambda$ and $x = \lambda$. Then $x = y$, and from $x + y = 10$: $x = y = 5$, $f = 25$ and $\lambda = 5$. Neighbouring allowed points are worse: $(4, 6)$ gives 24 and $(5.5, 4.5)$ gives 24.75.

Now relax the condition to $x + y = 10.1$. The best area becomes $5.05^2 = 25.50$, an increase of 0.50. That is $\lambda$ times the change of the condition, $5\times0.1$. The agreement is not exact (the increase is 0.5025), and it gets better the smaller the change is.

**Worked example: the Boltzmann distribution.** Which probabilities $p_i$ make the entropy $-\sum_ip_i\ln p_i$ (in units of $k_B$) largest, when they must add up to 1 and give a fixed mean energy $\sum_ip_iE_i$? There are two conditions, so two multipliers, $\alpha$ and $\beta$.

Set the derivative of $-\sum_ip_i\ln p_i - \alpha\sum_ip_i - \beta\sum_ip_iE_i$ with respect to one $p_i$ to zero: $-\ln p_i - 1 - \alpha - \beta E_i = 0$. So $p_i = e^{-1-\alpha}\,e^{-\beta E_i}$. The multiplier $\beta$ of the energy condition is the inverse temperature $1/k_BT$, and the factor $e^{-1-\alpha}$ is fixed by normalisation. Module 3 reaches the same distribution by another route.
</div>

**Where the course uses it.**

- [Module 2](02-classical-mechanics.html), Classical mechanics: constraints are added to the Lagrangian with Lagrange multipliers.
- [Module 6](06-force-field-parameters.html), Force-field parameters: atomic charges are fitted with the total charge fixed by a Lagrange multiplier.
- [Module 9](09-constraints.html), Constraints: the equations of constrained dynamics. SHAKE, RATTLE and LINCS are ways of computing the multipliers at each step.

<div class="box warn" markdown="1">
**A common mistake.** Mixing up names. The Lagrange *multiplier* $\lambda$ is a number attached to a condition. The *Lagrangian* $L$ of Module 2 is a function, the kinetic minus the potential energy. The letter $\lambda$ is also used for the coupling parameter of Module 13 and for eigenvalues.

A second point: the equations give candidates for a maximum or a minimum and do not say which of the two you have found. Check neighbouring points, as in the example.
</div>

## The Legendre transform {#legendre}

**The idea.** A function can be described in two ways. The usual way: for each position $x$, give the height $f(x)$. The other way: for each *slope*, say where the curve has that slope. For a curve that bends upwards everywhere, like a bowl, each slope occurs at one place only, so nothing is lost when the slope is used as the variable. The Legendre transform is the recipe that produces the new function of the slope.

It is used because the slope is often the quantity that you control or measure. In mechanics, the slope of the Lagrangian with respect to the velocity is the momentum, and Hamilton's formulation uses the momentum as its variable. In thermodynamics, the slope of the energy with respect to the entropy is the temperature, and in the laboratory you fix the temperature.

**The notation.**

$$
p = \frac{df}{dx} , \qquad g(p) = p\,x - f(x) \quad\text{with } x \text{ expressed through } p .
$$

<div class="legend" markdown="1">
- $f(x)$: the original function of the variable $x$.
- $p$: the slope of $f$, which becomes the new variable.
- $g(p)$: the **Legendre transform** of $f$, a function of $p$ alone.
- "$x$ expressed through $p$": solve $p = df/dx$ for $x$ and insert the result, so that no $x$ is left.
</div>

The construction is symmetric. The slope of the new function gives back the old variable:

$$
\frac{dg}{dp} = x .
$$

<div class="legend" markdown="1">
- $dg/dp$: the derivative of the transform with respect to its variable $p$.
- $x$: the original variable.
</div>

The reason takes one line. A small change of $g = px - f$ is $dg = p\,dx + x\,dp - df$, by the [product rule](#chain-rule). Since $df = p\,dx$, the first and the last term cancel, and $dg = x\,dp$. Transforming twice returns the original function.

With several variables, you transform with respect to one and leave the others alone. Two sign conventions are in use. Mechanics uses the one above: $H = p\,\dot q - L$. Thermodynamics uses the opposite sign, $f - px$: the Helmholtz free energy is $A = E - TS$, with $T = \partial E/\partial S$.

<div class="box key" markdown="1">
**Worked example: a parabola, and the step from Lagrange to Hamilton.** $f(x) = \tfrac12ax^2$. The slope is $p = ax$, so $x = p/a$. Then $g(p) = p\times\tfrac pa - \tfrac12a\left(\tfrac pa\right)^2 = \dfrac{p^2}{2a}$. With $a = 2$ and $x = 3$: $f = 9$ and $p = 6$, and $g = 6\times3 - 9 = 9$, which agrees with $6^2/(2\times2)$. The slope of $g$ is $p/a = 3$, the old variable.

Now read $x$ as a velocity $v$ and $a$ as a mass $m$. Then $f = \tfrac12mv^2$ is the kinetic energy as a function of the velocity, the slope $p = mv$ is the momentum, and $g = p^2/2m$ is the kinetic energy as a function of the momentum. This is the step from the Lagrangian to the Hamiltonian in Module 2. The full Lagrangian is $L = \tfrac12mv^2 - U$, and the potential energy $U$ does not depend on the velocity. It passes through the transform with its sign reversed, because of the minus sign in $p\,v - L$, and the result is $H = p^2/2m + U$, the total energy.

**Worked example: from energy to free energy.** The energy $E$ of a system is naturally a function of its entropy $S$ and its volume $V$, with $dE = T\,dS - P\,dV$. Transforming from $S$ to its slope $T$ gives $A = E - TS$, and $dA = dE - T\,dS - S\,dT = -S\,dT - P\,dV$. So $A$ is the natural function when $T$ and $V$ are controlled, as in a simulation at constant temperature and volume.

One more transform, from $V$ to the pressure $P$, gives the Gibbs free energy $G = A + PV$ for constant temperature and pressure. More in the [primer](physics.html#thermodynamics).
</div>

**Where the course uses it.**

- [Module 2](02-classical-mechanics.html), Classical mechanics: the Hamiltonian is the Legendre transform of the Lagrangian.
- [Module 3](03-statistical-mechanics.html), Statistical mechanics: the lesson uses the free energies $A$ and $G$ of simulations at constant temperature and at constant pressure, and writes $A = \langle E\rangle - TS$, without naming the transform. They are Legendre transforms of the energy, as in the second example above.

<div class="box warn" markdown="1">
**A common mistake.** Leaving the old variable in the result. $H$ must be written with positions and momenta, with no velocity left in it, and $A$ with $T$ and $V$, with no $S$ left in it. The expression $p\,\dot q - L$ with velocities still in it is not yet the Hamiltonian. Also, do not confuse the Legendre *transform* with Legendre *polynomials*, which are something else.
</div>

## Counting and Stirling's formula {#combinatorics}

**The idea.** Statistical mechanics rests on counting: in how many ways can the molecules be arranged so that the system looks the same from outside? The more ways, the higher the entropy. The counts are products of long runs of whole numbers, and they become astronomically large. Two tools keep them manageable: the factorial notation, and Stirling's formula for the logarithm of a factorial.

**The notation.**

$$
N! = N\times(N-1)\times\dots\times2\times1 , \qquad \binom{N}{k} = \frac{N!}{k!\,(N-k)!} .
$$

<div class="legend" markdown="1">
- $N!$: "N factorial", the number of different orders in which $N$ distinct objects can be lined up. There are $N$ choices for the first place, $N-1$ for the second, and so on. By definition $0! = 1$.
- $\binom{N}{k}$: the **binomial coefficient**, read "N choose k": the number of ways to choose $k$ objects out of $N$ when the order of choosing does not matter.
- $k!\,(N-k)!$: the division removes the orders within the chosen group and within the rest, which do not give new choices.
</div>

The number of pairs among $N$ atoms is $\binom N2 = N(N-1)/2$. More generally, the number of ways to divide $N$ objects into groups of the sizes $n_1, n_2, \dots$ is $N!/(n_1!\,n_2!\cdots)$.

Factorials grow faster than exponentials: $10!$ is about 3.6 million and $20!$ about $2.4\times10^{18}$. For the $10^{23}$ molecules of a sample that you can see, only the logarithm can be handled, and for it there is **Stirling's formula**:

$$
\ln N! \approx N\ln N - N .
$$

<div class="legend" markdown="1">
- $\ln$: the natural [logarithm](#exp-log). Since the logarithm of a product is the sum of the logarithms, $\ln N! = \ln1 + \ln2 + \dots + \ln N$.
- $N\ln N - N$: the approximation, good when $N$ is large. The next correction is $\tfrac12\ln(2\pi N)$, which is negligible for large $N$.
</div>

It comes from replacing the sum $\ln1 + \dots + \ln N$ by the [integral](#integral) $\int_1^{N}\ln x\,dx = N\ln N - N + 1$.

**Why $N!$ appears in a partition function.** Two molecules of the same kind cannot be told apart. Exchanging them gives the same physical state, yet an integral over the positions of all molecules counts both versions. Each physical state is counted $N!$ times, once for every order of the $N$ labels, and the classical partition function of Module 3 is divided by $N!$ to correct this.

<div class="box key" markdown="1">
**Worked example: small numbers, and how good Stirling is.** $4! = 24$. The number of ways to choose which 2 of 4 binding sites are occupied is $\binom42 = 24/(2\times2) = 6$. For 3 out of 10 it is 120.

$\ln10! = 15.10$. The formula gives $10\ln10 - 10 = 13.03$, which is 14 % too low. Adding $\tfrac12\ln(2\pi\times10) = 2.07$ gives 15.10. For $N = 100$ the exact value is 363.74 and the formula gives 360.52, an error of 0.9 %. For $N = 10^6$ the error is less than one part in a million.

**Worked example: the entropy of mixing.** Put 50 molecules of A and 50 of B on 100 sites. The number of arrangements is $\binom{100}{50}\approx1.0\times10^{29}$, and its logarithm is 66.8. Stirling's formula gives $100\ln100 - 2\times50\ln50 = 100\ln2 = 69.3$. For large numbers the entropy of an even mixture is $k_B\ln2$ per molecule.
</div>

**Where the course uses it.**

- [Module 3](03-statistical-mechanics.html), Statistical mechanics: the entropy is $k_B$ times the logarithm of the number of microstates, and the classical partition function contains the factor $1/N!$.
- [Module 5](05-force-field-form.html), The form of a force field, and [Module 7](07-boundaries-electrostatics.html), Boundaries and electrostatics: the number of atom pairs, $N(N-1)/2$, about $5\times10^{9}$ for 100,000 atoms, is the reason why computing every interaction directly is too slow.

<div class="box warn" markdown="1">
**A common mistake.** Using the short form of Stirling's formula for small $N$: at $N = 10$ it is off by 14 %. A second one: computing $N!$ itself when only its logarithm is needed. Already $171!$ exceeds the largest number in ordinary double-precision computer arithmetic, which is about $1.8\times10^{308}$. Work with $\ln N!$ from the start.
</div>

## Least squares and fitting {#fitting}

**The idea.** You have data points and a model with adjustable parameters, and you want the parameter values that make the model pass as close to the data as possible. The standard measure of "close" is the sum of the squared differences between model and data. Squaring makes all differences positive and punishes large misses more than small ones. Making that sum as small as possible is the method of **least squares**.

Drawing a straight line through scattered points is the simplest case. The parameters of a force field are found in the same way, with a large set of reference values in place of the points, and so are the many parameters of a machine-learned potential.

**The notation.**

$$
\chi^2(a,b) = \sum_{n=1}^{N}\big[y_n - (a\,x_n + b)\big]^2 .
$$

<div class="legend" markdown="1">
- $(x_n, y_n)$: data point number $n$, for example a time and a value measured at that time. $N$ is the number of points.
- $a\,x_n + b$: the prediction of the model, here a straight line with the slope $a$ and the intercept $b$.
- $y_n - (a\,x_n + b)$: the **residual** of point $n$, the vertical distance between the point and the line.
- $\chi^2$ (chi squared): the sum of the squared residuals, a function of the parameters $a$ and $b$. It is one symbol and not the square of a quantity $\chi$.
</div>

The best parameters are those at the minimum of $\chi^2$, where both [partial derivatives](#partial-derivative) vanish: $\partial\chi^2/\partial a = 0$ and $\partial\chi^2/\partial b = 0$. For a straight line these two equations can be solved by hand. By the [chain rule](#chain-rule), the derivative with respect to $b$ is $-2\sum_n[y_n - a\,x_n - b]$. Setting it to zero and dividing by $-2N$ gives $\bar y - a\,\bar x - b = 0$, where $\bar x$ and $\bar y$ are the means of the data. This is the formula for $b$ below.

The derivative with respect to $a$ is $-2\sum_nx_n\,[y_n - a\,x_n - b]$. Insert $b = \bar y - a\,\bar x$: the bracket becomes $(y_n - \bar y) - a\,(x_n - \bar x)$, and setting the derivative to zero gives $\sum_nx_n(y_n - \bar y) = a\sum_nx_n(x_n - \bar x)$. In both sums the first factor $x_n$ may be replaced by $x_n - \bar x$. This changes nothing, because deviations from a mean add up to zero: $\sum_n(y_n - \bar y) = 0$ and $\sum_n(x_n - \bar x) = 0$. Solving for $a$ gives the result:

$$
a = \frac{\sum_n(x_n - \bar x)(y_n - \bar y)}{\sum_n(x_n - \bar x)^2} , \qquad b = \bar y - a\,\bar x .
$$

<div class="legend" markdown="1">
- $\bar x$, $\bar y$: the [means](#averages) of the $x$ values and of the $y$ values.
- The numerator of $a$: $N-1$ times the covariance of $x$ and $y$. The denominator: $N-1$ times the variance of $x$. So the slope is the covariance divided by the variance.
- $b$: chosen so that the line passes through the point $(\bar x, \bar y)$.
</div>

The same steps work for any model in which every parameter multiplies a fixed function of $x$, such as a polynomial: the conditions are again linear equations for the parameters, which a numerical library solves. For other models, such as a neural network, the minimum is found numerically, by walking down the [gradient](#gradient) of $\chi^2$ in the space of the parameters.

Two refinements appear in the course. **Weights**: when some data points are more reliable or more important than others, each squared residual is multiplied by a weight before the sum is taken. **Restraints**: an extra term is added to $\chi^2$ that grows when the parameters move away from reasonable values. It keeps the fit from using extreme parameter values to gain a tiny improvement.

A remark on the name: in statistics, $\chi^2$ stands for the sum in which each residual is divided by the uncertainty $\sigma_n$ of its data point before it is squared. That $\chi^2$ is a pure number, and for a model that fits within the uncertainties it is about $N$ minus the number of fitted parameters. The $\chi^2$ of this section has the unit of $y$ squared, and its size has a meaning only when two fits of the same data are compared.

**Overfitting.** A model with enough parameters can pass through every data point, noise included. Its $\chi^2$ is zero, and its predictions between and beyond the points can be absurd. The defence is to judge a model on data that were not used in the fit (a test set), and to prefer the model with fewer parameters when two fit equally well.

<div class="box key" markdown="1">
**Worked example.** Four points: $x = 1, 2, 3, 4$ and $y = 2.1, 3.9, 6.2, 7.8$. The means are $\bar x = 2.5$ and $\bar y = 5.0$. The products $(x_n-\bar x)(y_n-\bar y)$ are 4.35, 0.55, 0.60 and 4.20, with the sum 9.70. The squares $(x_n-\bar x)^2$ are 2.25, 0.25, 0.25 and 2.25, with the sum 5.00. So $a = 9.70/5.00 = 1.94$ and $b = 5.0 - 1.94\times2.5 = 0.15$.

The line predicts 2.09, 4.03, 5.97 and 7.91. The residuals are 0.01, $-0.13$, 0.23 and $-0.11$, and $\chi^2 = 0.0001 + 0.0169 + 0.0529 + 0.0121 = 0.082$. Another line does worse: $a = 2$ and $b = 0$ give $\chi^2 = 0.100$.

Now overfit. The cubic $y = -0.2x^3 + 1.45x^2 - 1.15x + 2$ has four parameters and passes through all four points exactly, so its $\chi^2$ is 0. At $x = 5$ the line predicts 9.85, in step with the trend of the data, and the cubic predicts 7.5. At $x = 6$ the line gives 11.8 and the cubic 4.1.
</div>

**Where the course uses it.**

- [Module 6](06-force-field-parameters.html), Force-field parameters: parameters are chosen by minimising a weighted $\chi^2$ against reference data, and charges are fitted to an electrostatic potential with a restraint.
- [Module 11](11-analysis-statistics.html), Analysis and statistics: each frame is superimposed on a reference by a least-squares fit before the RMSD is computed, and the diffusion constant is read from the slope of the mean squared displacement against time.
- [Module 15](15-coarse-grained.html), Coarse-grained models: coarse-grained potentials are fitted to reproduce atomistic forces or distributions.
- [Module 17](17-machine-learning.html), Machine-learned potentials: training is a least-squares fit of energies and forces, and the result is judged on a test set.

<div class="box warn" markdown="1">
**A common mistake.** Trusting a small $\chi^2$. It measures how well the model reproduces the data it was fitted to, and says nothing about data it has not seen. A second mistake is to fit a straight line to data that are visibly curved and to report the slope. Always plot the data together with the fitted curve.
</div>

## Random numbers and noise {#random-numbers}

**The idea.** Many steps of a simulation need chance. Initial velocities are drawn at random, some thermostats give the atoms random kicks, and Monte Carlo methods accept or reject a proposed move at random. A computer has no dice. It uses a **pseudo-random number generator**: a rule that produces a long sequence of numbers that pass statistical tests of randomness, although each number follows from the one before.

The sequence is fixed by a starting number, the **seed**. The same seed gives the same sequence, which makes a run repeatable. A different seed gives a statistically independent run.

**The notation.** Two kinds of random numbers do almost all the work.

A **uniform** random number $u$ lies between 0 and 1, and every value in that range is equally likely. Its mean is $\tfrac12$ and its variance is $\tfrac1{12}$. It is used to make a yes-or-no decision with a given probability $p$: draw $u$ and say yes if $u < p$.

A **Gaussian** (or normal) random number has the bell-shaped distribution of [the Gaussian section](#gaussian). The standard one has mean 0 and variance 1:

$$
\xi\sim\mathcal N(0,1) , \qquad x = \mu + \sigma\,\xi .
$$

<div class="legend" markdown="1">
- $\xi$ (Greek xi): a standard Gaussian random number. Each time it appears, a fresh value is drawn.
- $\sim$: "is distributed as".
- $\mathcal N(0,1)$: the normal distribution with mean 0 and variance 1.
- $x$: a Gaussian random number with the mean $\mu$ and the standard deviation $\sigma$, obtained by scaling and shifting $\xi$.
</div>

**The random walk.** Add up many independent random steps and you get a random walk, the model of diffusion. Let each step $s_n$ have the mean zero and the variance $a^2$. After $n$ steps the position is $x_n = s_1 + s_2 + \dots + s_n$, and

$$
\langle x_n\rangle = 0 , \qquad \langle x_n^2\rangle = n\,a^2 .
$$

<div class="legend" markdown="1">
- $s_n$: the $n$-th step, a random number.
- $a$: the typical size of one step, its standard deviation.
- $x_n$: the position after $n$ steps.
- $\langle\ \rangle$: the [mean](#averages) over many independent walks.
- $\langle x_n^2\rangle$: the mean squared displacement.
</div>

The first result says that the walk goes nowhere on average. The second holds because the variances of independent steps add. For two steps, $\langle(s_1+s_2)^2\rangle = \langle s_1^2\rangle + 2\langle s_1s_2\rangle + \langle s_2^2\rangle$. The middle term is zero, because for independent steps $\langle s_1s_2\rangle = \langle s_1\rangle\langle s_2\rangle$, and each of these means is zero. So $\langle(s_1+s_2)^2\rangle = 2a^2$, and each further step adds another $a^2$.

The second result means that the typical distance from the start grows as $\sqrt n$: to get twice as far, a diffusing particle needs four times as long.

If one step takes the time $\Delta t$, then $n = t/\Delta t$ and $\langle x^2\rangle = (a^2/\Delta t)\,t$: the mean squared displacement grows linearly in time. The slope defines the diffusion constant $D$, through $\langle x^2\rangle = 2Dt$ in one dimension and $6Dt$ in three ([primer](physics.html#diffusion)).

**White noise.** A random force that acts all the time and has no memory is called white noise, written $\eta(t)$. "No memory" means that its values at two different times are uncorrelated:

$$
\langle\eta(t)\rangle = 0 , \qquad \langle\eta(t)\,\eta(t')\rangle = \delta(t - t') .
$$

<div class="legend" markdown="1">
- $\eta(t)$ (Greek eta): the noise at the time $t$. Its unit is one over the square root of a time, because the delta function on the right-hand side has the unit of one over time.
- $t$, $t'$: two times.
- $\delta(t-t')$: the [Dirac delta](#delta), which is zero unless the two times are the same.
- $\langle\ \rangle$: the mean over many independent repeats (realisations) of the noise.
</div>

White noise is an idealisation, like the Dirac delta itself. What a program needs is its effect over one time step, and that is simple. The integral of $\eta$ over a step of length $\Delta t$ is a Gaussian random number with mean 0 and variance $\Delta t$, that is $\sqrt{\Delta t}\,\xi$. It is Gaussian because it is the sum of very many independent small kicks (the central limit theorem of [the section on averages](#averages)). It is one step of a random walk.

This integrated noise is what the symbol $dW$ stands for in Module 8. It is the reason why random terms in an integrator carry $\sqrt{\Delta t}$ while systematic terms carry $\Delta t$.

**Equations with a noise term.** Module 8 writes several equations of motion that contain a random term. They come in two forms that say the same thing:

$$
\frac{dx}{dt} = a(x) + b\,\eta(t) \qquad\text{or}\qquad dx = a(x)\,dt + b\,dW .
$$

<div class="legend" markdown="1">
- $x$: the quantity that changes in time, for example a velocity component or the kinetic energy.
- $a(x)$: the systematic part, the rate of change that $x$ would have without noise.
- $b$: the strength of the noise. Its square has the unit of $x$ squared per unit of time.
- $\eta(t)$: white noise, as defined above.
- $dx$, $dt$: the small change of $x$ during the small time $dt$.
- $dW$: the noise integrated over $dt$, a Gaussian random number with mean 0 and variance $dt$. The second form is the first one multiplied by $dt$, with $\eta\,dt$ written as $dW$.
</div>

Such an equation is called a **stochastic differential equation**. Read it as a recipe for one small step. It is Euler's method of [the section on differential equations](#ode) with a random kick added:

$$
x(t+\Delta t) \approx x(t) + a\big(x(t)\big)\,\Delta t + b\,\sqrt{\Delta t}\;\xi .
$$

<div class="legend" markdown="1">
- $\Delta t$: the time step.
- $\xi$: a standard Gaussian random number, drawn afresh for every step.
- Other symbols: as in the list above.
</div>

Two runs with different random numbers give two different paths. What can be reproduced is the statistics over many paths: means, variances and distributions.

If $b$ itself depends on $x$, as in the equation for the kinetic energy in Module 8, one more agreement is needed: at which value of $x$ within the step $b$ is taken. The recipe above takes it at the start of the step. This choice is called the Itô convention. If $b$ is a constant, as in the Langevin equation, the question does not arise.

<div class="box key" markdown="1">
**Worked example: friction and noise in balance.** Module 8 studies $dv = -\gamma v\,dt + \sigma\,dW$ for one velocity component, with a friction rate $\gamma$ and a noise strength $\sigma$, and states that the variance of $v$ settles at $\sigma^2/2\gamma$. Take $\gamma = 1$ ps$^{-1}$ and a water molecule at 300 K. The value of Module 8 is $\sigma^2 = 2\gamma k_BT/m = 2\times1\times2.494/18 = 0.277$ nm$^2$ ps$^{-3}$, so $\sigma = 0.526$ in these units.

With $\Delta t = 0.01$ ps the recipe is $v\leftarrow v - 0.01\,v + 0.526\times0.1\,\xi = 0.99\,v + 0.0526\,\xi$. Starting from $v = 0.5$ nm/ps and drawing $\xi = -0.8$ gives $0.495 - 0.042 = 0.453$ nm/ps.

After many steps the variance stops changing, when the part that friction removes equals the part that the noise adds: $\mathrm{var} = 0.99^2\,\mathrm{var} + 0.0526^2$. This gives $\mathrm{var} = 0.00277/0.0199 = 0.139$ nm$^2$/ps$^2$. The exact value is $\sigma^2/2\gamma = k_BT/m = 0.1386$ nm$^2$/ps$^2$, the variance of the Maxwell-Boltzmann distribution. The recipe is 0.5 % too high, an error of the finite step that vanishes as $\Delta t\to0$.
</div>

<div class="box key" markdown="1">
**Worked example: a decision and a velocity.** A move is to be accepted with the probability $p = 0.3$. Draw $u = 0.47$: this is larger than 0.3, so reject. Draw $u = 0.12$: accept. Over many draws, 30 % are accepted.

For a water molecule at 300 K, each velocity component is Gaussian with $\sigma = 0.372$ nm/ps (from [the Gaussian section](#gaussian)). If the generator returns $\xi = -0.8$, the component is $0.372\times(-0.8) = -0.30$ nm/ps.

**Worked example: how far a random walk gets.** 100 steps of size $a = 0.1$ nm give a root-mean-square displacement of $0.1\times\sqrt{100} = 1.0$ nm, and not 10 nm. 400 steps give 2.0 nm. If one step takes 1 ps, the diffusion constant in one dimension is $D = a^2/2\Delta t = 0.005$ nm$^2$/ps.

**Worked example: noise in a time step.** A particle that diffuses with, say, $D = 0.002$ nm$^2$/ps is moved in a step of $\Delta t = 0.002$ ps by a random displacement with the standard deviation $\sqrt{2D\Delta t} = 0.0028$ nm. With a step four times longer the displacement is only twice as large, 0.0057 nm.
</div>

**Where the course uses it.**

- [Module 1](01-what-is-md.html), What MD is, and [Module 3](03-statistical-mechanics.html), Statistical mechanics: initial velocities are drawn from the Maxwell-Boltzmann distribution.
- [Module 4](04-integrators.html), Integrators, and [Module 8](08-thermostats-barostats.html), Thermostats and barostats: stochastic integrators, and thermostats and barostats that use random numbers.
- [Module 10](10-running-a-simulation.html), Running a simulation: different seeds give independent repeats of a run.
- [Module 11](11-analysis-statistics.html), Analysis and statistics: the mean squared displacement and the diffusion constant, and how a random walk can imitate a meaningful motion in principal component analysis.
- [Module 14](14-enhanced-sampling.html), Enhanced sampling: replica exchange accepts or rejects a swap with a given probability.
- [Module 17](17-machine-learning.html), Machine-learned potentials: a generative model turns Gaussian random numbers into molecular structures.

<div class="box warn" markdown="1">
**A common mistake.** Reusing a seed. Two "independent" repeats started with the same seed and the same input are the same run. And for diffusion: expecting the distance to grow in proportion to the time. It grows as the square root of the time, and the random part of a time step scales as $\sqrt{\Delta t}$.
</div>
