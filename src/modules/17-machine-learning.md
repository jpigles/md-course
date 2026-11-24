---
num: 17
title: Machine learning in molecular simulation
short: Machine-learned potentials
part: Part V · Beyond all-atom
hours: 7
summary: Understand how neural-network potentials are built and trained, how machine learning is used for coarse-graining and for generating equilibrium ensembles directly, and how to judge these tools with the statistics from the rest of the course.
videos: 16
papers: L
tags: ml-potentials
---

<div class="box goal" markdown="1">
#### After this module you can

- state the learning problem for an interatomic potential and the symmetries it must respect;
- describe descriptor-based (Behler-Parrinello, ANI) and message-passing (SchNet, NequIP, MACE) architectures;
- write the energy-and-force loss and explain why forces are the richer training signal;
- explain machine-learned coarse-graining as force matching with a neural network;
- explain what Boltzmann generators and diffusion-based ensemble emulators produce, and what they do not.
</div>

## Lectures for this module

The lesson below is written to be complete on its own. These lectures are a second explanation of the same material, for when you want to hear it from a lecturer.

{{WATCH}}

## The plan of this module

Every simulation in this course so far took its forces from a force field: a formula for the potential energy whose shape was chosen by people and whose numbers were then tuned. This module is about replacing that formula, or another part of the simulation, by a function that a computer fits to examples. "Machine learning" means no more than that here: choose a very flexible function with many adjustable numbers, and adjust the numbers until the function reproduces a set of known answers.

The module has four layers:

1. **The tools.** Why a learned potential is wanted, what a neural network is, and how it is fitted. No earlier knowledge of machine learning is assumed.
2. **Machine-learned potentials.** What exactly is learned, the symmetries that the energy must respect, the three main designs, how training on energies and forces works, and where these models fail.
3. **Learning other things.** Coarse-grained potentials, and models that generate equilibrium configurations without running any dynamics.
4. **Judging the result.** Five questions that apply to every tool of this kind.

Layer 1 is background that the later sections lean on. If you have trained a neural network before, skim it. The section on equivariant networks is the heaviest of the module, and it says at its start what to keep on a first reading.

### How to read the formulas

Every displayed formula is followed by a list that says what each letter in it means. The table lists the notation that first appears in this module. The general conventions (bold letters for vectors, $\sum$ for sums, $\partial$ for partial derivatives) are explained in the [maths toolbox](maths.html#notation).

| You see | It means |
|---|---|
| $\theta$ | All the adjustable numbers (the **parameters**) of a model, collected in one long list. Training changes $\theta$ and nothing else. In this module $\theta$ is never an angle. |
| $E_\theta$, $U_\theta$, $f_\theta$ | A subscript $\theta$ marks a function that the model computes. Its values depend on the present parameters. |
| $E_{QM}$, $\mathbf F_{QM}$ | The subscript $QM$ marks a reference value from a quantum-mechanical calculation. |
| $Z_i$ | The atomic number of atom $i$, which says what element it is: 1 for H, 6 for C, 7 for N, 8 for O. |
| $\mathcal L$, $\mathcal U$, $\mathcal M$, $\mathcal R$, $\mathcal N$ | Letters in a script font are symbols of their own, different from the plain letters. $\mathcal L$ is the **loss**, the number that training makes small. |
| $E^{(c)}$, $\mathbf h^{(t)}$ | A superscript in round brackets is a label ("configuration number $c$", "round number $t$"). It is not a power. |
| $\{\dots\}$ | Curly brackets around a list: a set, a collection of things in no particular order. |
| $\hat{\mathbf r}$ | A hat on a bold letter: a unit vector. It has length 1 and carries only a direction. |
| $\langle\dots\rangle$ | The average of what stands inside, here over the frames of a trajectory or over samples. |
| $\propto$ | "Is proportional to": equal up to a constant factor that does not matter here. |
| $f^{-1}$ | The inverse of the function $f$, the function that undoes it. It is not $1/f$. |

<div class="box warn" markdown="1">
**Letters and words that mean two things in this module.**

- $w$: a weight inside a neuron ($w_1$, $w_k$), the weights $w_E$ and $w_F$ of the two parts of a loss, and the importance weight $w(\mathbf x)$ of a generated sample.
- $T$: the number of message-passing rounds in the section on architectures, and the temperature wherever $k_BT$ appears.
- $Z_i$ is an atomic number. The lower-case $\mathbf z$ and the subscript in $p_Z$ belong to the random numbers of a Boltzmann generator.
- $\mathbf r$ is the list of atomic positions and $\mathbf R$ the list of coarse-grained positions. $\mathcal R$ is a readout function.
- $\mathbf M$ is a coarse-grained mapping and $\mathcal M$ a message function. $U$ is a potential energy and $\mathcal U$ an update function.
- $f$: $f_c$ is a cutoff function, $f_\theta$ a network, and $\mathbf f$ the atomistic forces in the section on coarse-graining.
- $\sigma$ is the activation function of a neuron here, not a Lennard-Jones diameter or a standard deviation.
- $x$: an input of a neuron or of a network ($x_1$, $x_n$), a Cartesian coordinate of an atom ($x_i$) and, in bold, a whole configuration $\mathbf x$ in the section on generating ensembles.
- $c$: the bias of the output neuron in the section on tools, the label of a reference configuration in the training loss ($E^{(c)}$, $N_c$), and a subscript for "cutoff" in $r_c$ and $f_c$.
- $n$ and $M$ are labels and counts that change from formula to formula (inputs of a neuron, examples, stored neighbourhoods, generated samples). Each list says what they count.
- $F$: bold $\mathbf F$ is a force. $F_A$ and $F_B$ in the section on Boltzmann generators are free energies.
- "Ensemble": a handful of models trained on the same data (under active learning), and a set of configurations (in the section on generating ensembles, as in Module 3).

The lists under the formulas say which meaning applies each time.
</div>

## Where the classical force field falls short

<div data-videos="LInWiab7q6Q"></div>

There are two ways to get the energy of an arrangement of atoms. One is fast and approximate, the other accurate and slow. This section says what each one lacks, because the gap between them is the reason for everything else in the module.

Modules 5 and 6 described an energy function with a fixed, simple form. The form is a sum of springs for bonds and angles, cosines for torsions, and Lennard-Jones and Coulomb terms between pairs of atoms. Its accuracy is limited by that form: no polarisation, no reactivity, a few thousand parameters shared across all chemistry. The three limits, one at a time:

- **No polarisation.** Each atom carries a fixed partial charge. In a real molecule the electrons shift when the surroundings change, so the same chemical group is charged a little differently in water and in the interior of a protein. A fixed-charge model cannot follow that ([primer](physics.html#dipoles)).
- **No reactivity.** The list of bonds is written down when the system is built. A harmonic bond can never break and a new bond can never form, so chemical reactions, proton transfer included, are outside the model.
- **A few thousand shared parameters.** Every atom of one atom type uses the same numbers, in whatever molecule it sits. The numbers are a compromise over all the molecules they were fitted to.

Quantum chemistry gives accurate energies and forces for any arrangement of atoms, but its cost grows steeply with system size, and even density functional theory is many orders of magnitude slower than a force field.

<div class="box physics" markdown="1">
**Physics you need here: where the reference energy comes from.** A molecule consists of nuclei and electrons. An electron is about 1,800 times lighter than a proton, so the electrons adjust almost instantly when the nuclei move. For every fixed arrangement of the nuclei, the electrons therefore settle into a state with a definite energy, and quantum mechanics can compute that energy by solving its equations for the electrons. This energy, with the repulsion between the nuclei added, as a function of the positions of the nuclei, is the **potential energy surface**. It is the true $U(\mathbf r)$ on which the atoms move.

A classical force field is one approximation to this surface, built from simple terms. **Quantum chemistry** is the family of methods that compute points on the surface numerically, one arrangement of atoms at a time. **Density functional theory** (DFT) is one of the less expensive members of the family. It works with the density of the electrons in space instead of the full description of every electron. More in the [primer](physics.html#quantum).
</div>

Two phrases in that sentence set the scale. An **order of magnitude** is a factor of ten, so three orders of magnitude is a factor of 1,000. And "grows steeply" means faster than in proportion. A force field with a cutoff costs about twice as much for twice as many atoms. For a quantum method the cost rises as a power of the size: if it grows as the third power, as it does for DFT in its usual form, twice as many atoms cost $2^3=8$ times more and ten times as many atoms cost 1,000 times more.

So there is a gap. On one side is a method that is fast but limited by its form. On the other is a method that is accurate but affordable only for small systems and short times.

A **machine-learned interatomic potential** (MLIP) is a flexible function, usually a neural network, trained to reproduce quantum-mechanical energies and forces. The aim is quantum accuracy at a cost within a few orders of magnitude of a force field.

"Interatomic potential" is another name for a function that gives the potential energy from the positions of the atoms. A force field is one too. The learned kind is made in four steps:

1. choose a set of arrangements of atoms, from hundreds to millions of them;
2. compute the quantum-mechanical energy and forces of each one, once;
3. fit a flexible function to these examples;
4. in the MD program, call the fitted function wherever the force field would have been called.

The fitted function solves no quantum equations. It interpolates between the examples it was given, in the way a smooth curve drawn through measured points gives values between the points. All the quantum mechanics it contains is in the examples.

| | Classical force field | Machine-learned potential |
|---|---|---|
| Shape of the function | Fixed by people: springs, cosines, pair terms | Flexible: the examples decide the shape |
| Adjustable numbers | A few thousand, each with a physical meaning (a bond length, a charge) | Usually many more, with no individual meaning |
| Fitted to | Quantum calculations on small molecules and experimental data (Module 6) | Quantum energies and forces of many configurations |
| Far from the data it was fitted to | Still reasonable, because the form is physical: atoms that come too close repel | Unconstrained, as the section on training shows |

## The tools: what a neural network is and how it is fitted

The models in this module are neural networks. This section builds one from its smallest part and then explains how its numbers are set. Nothing in it is specific to molecules.

### One neuron

A **neural network** is a function: numbers go in and numbers come out. Two things set it apart from the formulas of a force field. It is assembled from many copies of one very simple unit, the **neuron**, and it contains a large number of adjustable numbers.

A neuron takes several input numbers. It multiplies each input by its own **weight**, adds the results, adds one more number called the **bias**, and passes the sum through a fixed curve called the **activation function**:

$$
y=\sigma\big(w_1x_1+w_2x_2+\dots+w_nx_n+b\big).
$$

<div class="legend" markdown="1">
- $x_1,\dots,x_n$: the inputs of the neuron, $n$ numbers.
- $w_1,\dots,w_n$: the weights, one per input. A weight far from zero means that the neuron reacts strongly to that input. A weight of zero means that it ignores it. The weights are adjustable.
- $b$: the bias, a number that shifts the sum up or down. It is adjustable too.
- $\sigma$: the activation function, a fixed curve that is not a straight line. The examples in this module use the hyperbolic tangent, $\tanh$. This $\sigma$ is not the Lennard-Jones diameter of Module 5 and not a standard deviation.
- $y$: the output of the neuron, one number.
</div>

The function $\tanh(s)$ is an S-shaped curve. Near $s=0$ it is close to $s$ itself. For large positive $s$ it levels off at $+1$, and for large negative $s$ at $-1$. Some values: $\tanh(0)=0$, $\tanh(0.5)=0.46$, $\tanh(1)=0.76$, $\tanh(3)=0.995$.

<div class="box key" markdown="1">
**Worked example: one neuron by hand.** Take two inputs, $x_1=0.5$ and $x_2=-1.0$, the weights $w_1=0.8$ and $w_2=0.3$, and the bias $b=0.1$.

1. *Weighted sum.* $0.8\times0.5+0.3\times(-1.0)+0.1=0.4-0.3+0.1=0.2$.
2. *Activation.* $y=\tanh(0.2)=0.197$.

Now change one weight, $w_2$, from $0.3$ to $-0.3$. The sum becomes $0.4+0.3+0.1=0.8$ and the output $\tanh(0.8)=0.664$. Changing a weight changes the output. Training does this on purpose, to all weights at once.
</div>

### Layers, and why the curve is needed

One neuron can only produce one S-shaped response. A network gets its flexibility from having many of them. Neurons that receive the same inputs form a **layer**, and the outputs of one layer are the inputs of the next. The layers between the input and the output are called **hidden layers**.

The smallest useful network has one input, one hidden layer of $K$ neurons and one output:

$$
f_\theta(x)=c+\sum_{k=1}^{K}v_k\,\tanh\big(w_kx+b_k\big).
$$

<div class="legend" markdown="1">
- $x$: the input, one number (for example a distance).
- $f_\theta(x)$: the output of the network, one number (for example an energy).
- $K$: the number of neurons in the hidden layer. $k$ is the label of one of them, from 1 to $K$.
- $\sum_{k=1}^{K}$: add up the term that follows for every hidden neuron.
- $w_k$, $b_k$: the weight and the bias of hidden neuron $k$.
- $\tanh(w_kx+b_k)$: the output of hidden neuron $k$.
- $v_k$: the weight that the output neuron gives to hidden neuron $k$.
- $c$: the bias of the output neuron. The output neuron applies no activation function: it forms the weighted sum of the hidden outputs and adds $c$. The output can therefore take any value and is not confined to the range between $-1$ and $+1$.
- $\theta$: the list of all adjustable numbers, here all the $w_k$, $b_k$ and $v_k$ and the number $c$. That is $3K+1$ numbers, 31 of them for $K=10$.
</div>

Read it like this. Each hidden neuron contributes one smooth step. The step sits where $w_kx+b_k=0$, that is at $x=-b_k/w_k$. Its steepness is set by $w_k$ and its height and sign by $v_k$. The output is the sum of $K$ such steps plus a constant.

With enough steps in the right places, of the right steepness and height, the sum can follow any smooth curve on a finite interval as closely as you like. This is what "flexible function" means. A Lennard-Jones term has the shape $r^{-12}$ built in and only its size can be tuned. A network has no built-in shape: changing $\theta$ changes the shape itself.

The bend in the activation function is what makes this possible. Without it, a neuron would compute only a weighted sum, and a weighted sum of weighted sums is again a weighted sum. Take two "layers" without activation, $u=w_1x+b_1$ followed by $y=w_2u+b_2$. Substituting the first into the second gives $y=(w_2w_1)\,x+(w_2b_1+b_2)$, a straight line. However many such layers you stack, the result stays a straight line (a flat plane when there are several inputs).

Larger networks have more inputs, more neurons per layer and more layers. The demo further down uses one input, two hidden layers of 16 neurons and one output. Count its adjustable numbers: $16+16=32$ for the first hidden layer, $16\times16+16=272$ for the second and $16+1=17$ for the output, 321 in all. The curve it has to learn, a double well, fits in one short formula. A network spends many parameters to avoid assuming a form.

Two words are used from here on. The **parameters** of a network are its weights and biases together, the list $\theta$. The **architecture** is the wiring plan: how many layers, how many neurons, what goes in and what comes out. People choose the architecture. Training sets the parameters.

### Fitting: the loss function and gradient descent

How are hundreds or millions of numbers set? By the idea behind fitting a straight line through measured points ([least squares](maths.html#fitting)), on a larger scale.

You need a set of examples: inputs $x_n$ for which the correct outputs $y_n$ are known. The **loss function** measures how wrong the network is on them:

$$
\mathcal L(\theta)=\sum_{n=1}^{M}\big(f_\theta(x_n)-y_n\big)^2 .
$$

<div class="legend" markdown="1">
- $M$: the number of examples. $n$ is the label of one example, from 1 to $M$.
- $x_n$: the input of example $n$.
- $y_n$: the known correct output for it, called the **label** or the reference value.
- $f_\theta(x_n)$: what the network predicts for that input with its present parameters $\theta$.
- The square: it makes every error count as positive and makes large errors count much more than small ones.
- $\mathcal L(\theta)$: the loss, one number that depends on the parameters. Zero would mean that every example is reproduced exactly.
</div>

**Training** is the search for the parameters that make $\mathcal L$ small. The examples stay fixed and only $\theta$ changes.

Picture the loss as a surface, with the height $\mathcal L$ drawn over a space that has one axis per parameter. Training walks downhill on this surface. It is the picture of energy minimisation in Module 10, with the parameters in the place of the atomic coordinates and the loss in the place of the energy.

<div class="box maths" markdown="1">
**Maths you need here: gradient descent.** The gradient of the loss is the list of its slopes, $\partial\mathcal L/\partial\theta_a$, one for each parameter $\theta_a$ (the label $a$ numbers the parameters). It points in the direction in which the loss rises fastest ([toolbox](maths.html#gradient)). To make the loss smaller, change every parameter a little in the opposite direction:

$$
\theta_a\leftarrow\theta_a-\alpha\,\frac{\partial\mathcal L}{\partial\theta_a}.
$$

The arrow means "replace the value on the left by the value on the right". The small positive number $\alpha$ is the **learning rate**. It sets the length of the step. Then compute the slopes again at the new place and repeat, thousands of times.

A worked example with one parameter. Let $\mathcal L(w)=(w-3)^2$, which has its minimum at $w=3$. Its slope is $d\mathcal L/dw=2(w-3)$. Start at $w=0$ with $\alpha=0.1$.

- Step 1: the slope is $2\times(0-3)=-6$, so the new value is $0-0.1\times(-6)=0.6$.
- Step 2: the slope is $-4.8$, the new value $1.08$.
- Step 3: the slope is $-3.84$, the new value $1.464$.

Each step removes one fifth of the remaining distance to 3. After 20 steps $w=2.965$. With a learning rate that is too large the walk overshoots: with $\alpha=1.1$ the same start gives $6.6$, then $-1.32$, then $8.18$, further from 3 each time. An MD time step that is too long fails in the same way (Module 4).
</div>

Three practical points complete the picture.

**Where the slopes come from.** A network is a long chain of elementary operations: multiply, add, apply $\tanh$. The derivative of each operation is known, and the [chain rule](maths.html#chain-rule) combines them into the derivative of the whole chain. Machine-learning libraries do this mechanically. You write the code that computes the output, and the library returns the exact derivative of the output with respect to any parameter or any input you ask for.

This is **automatic differentiation**. Its cost is a small multiple of the cost of computing the output once. Applied to the parameters of a network it is also called backpropagation.

**Small batches.** With many examples it is wasteful to compute the loss on all of them for every step. Each step uses a small random subset of the examples, a **mini-batch**, which gives a noisy but cheap estimate of the gradient. This is **stochastic gradient descent**. One pass through all the examples is called an **epoch**.

**No guarantee of the lowest point.** Gradient descent starts from random parameters and stops in *a* low region of the loss surface. Start again from other random parameters and you get a different network that fits the examples about as well. The two networks agree where there are examples and can differ where there are none. This fact is used later to detect when a model should not be trusted.

### Training, validation and test sets, and overfitting

A flexible function has a danger that a stiff one does not. Take five measured points that lie roughly on a straight line, with some scatter. A straight line has two parameters and passes near all five. A polynomial of degree four has five parameters and passes exactly through all five, so its loss is zero. Between the points and beyond them it swings up and down, because it has fitted the scatter as well as the trend.

This is **overfitting**: a small error on the examples used for the fit and a large error everywhere else ([toolbox](maths.html#fitting)). A network with thousands of parameters can do the same. A small loss on the examples it was trained on therefore proves little.

The defence is to hold examples back. Before training, the examples are divided into three sets, for example 80, 10 and 10 per cent of them:

| Set | What it is used for |
|---|---|
| **Training set** | Computing the gradient. Only these examples move the parameters. |
| **Validation set** | Watching during training. When its error stops falling while the training error keeps falling, overfitting has begun and training is stopped. It is also used to choose settings such as the number of layers or the learning rate. |
| **Test set** | Reporting the final error, once, on examples that influenced nothing. |

The settings in the second row are called **hyperparameters**: the numbers that you choose, as opposed to the parameters that training sets.

A model **generalises** if its error on examples it has not seen is close to its error on the training set. The **capacity** of a model is how complicated a function it can represent, which grows with the number of parameters. More capacity allows a closer fit and makes overfitting easier.

One warning returns several times in this module. The test set usually comes from the same source as the training set. A small test error then says that the model interpolates well between examples of that kind. It says nothing about examples of another kind. The range of situations that the training examples cover is called the training **distribution**, and an example outside it is **out of distribution**.

## The learning problem

<div data-videos="tWeBrPTrSDE 8DPSLDUsqbA"></div>

This section states what a learned potential takes in and gives out, and what its examples are. It then gives three requirements that shape every design: the forces must come from the energy, the energy must respect the symmetries of space, and the energy must be built from local pieces.

Find a function $E_\theta(\mathbf r_1,\dots,\mathbf r_N;Z_1,\dots,Z_N)$ of atomic positions and element types such that $E_\theta\approx E_{QM}$, with forces obtained by differentiation, $\mathbf F_i=-\partial E_\theta/\partial\mathbf r_i$, so that the force field is conservative by construction (automatic differentiation makes this free).

<div class="legend" markdown="1">
- $E_\theta$: the energy that the model predicts for one arrangement of the atoms, one number (in kJ/mol in the units of this course).
- $\theta$: all the parameters of the model.
- $N$: the number of atoms. $i$ labels one atom, from 1 to $N$.
- $\mathbf r_1,\dots,\mathbf r_N$: the positions of the atoms, three numbers each, in nm.
- $Z_1,\dots,Z_N$: the element of each atom, given as its atomic number (1 for hydrogen, 6 for carbon, 7 for nitrogen, 8 for oxygen).
- The semicolon: it separates the two kinds of input, positions and elements.
- $E_{QM}$: the energy of the same arrangement from a quantum-mechanical calculation, the reference.
- $\approx$: "is approximately equal to".
- $\mathbf F_i$: the force on atom $i$, a vector.
- $\partial E_\theta/\partial\mathbf r_i$: the gradient of the predicted energy with respect to the position of atom $i$, written out further down.
</div>

Look at what the input does not contain. In the form written here there are no atom types, no list of bonds and no partial charges. The model is told only where the atoms are and which elements they are, and everything else has to follow from that.

### What the examples are, and what they cost

One training example is one **configuration**: a snapshot with the position of every atom of a molecule or of a small periodic box. Its labels are the quantum-mechanical energy of that snapshot (one number) and the quantum-mechanical force on every atom ($3N$ numbers).

Each configuration costs one quantum calculation, the expensive kind of calculation from the first section. The training sets quoted later in this module range from 133 configurations to about 17 million. The data set is therefore a large part of the cost of a learned potential, and it is paid before the first MD step. This is why a model that needs fewer examples is worth a great deal.

The labels also set a ceiling. A model trained on DFT energies reproduces DFT at best, with the errors of DFT included. The last section of this module comes back to this under "What is the reference?".

### Forces from the energy

A simulation needs forces. A network could output the three components of the force on each atom directly. The learning problem above asks for something else: the network outputs one number, the energy, and the forces are computed from it by differentiation:

$$
\mathbf F_i=-\frac{\partial E_\theta}{\partial\mathbf r_i}=-\left(\frac{\partial E_\theta}{\partial x_i},\ \frac{\partial E_\theta}{\partial y_i},\ \frac{\partial E_\theta}{\partial z_i}\right).
$$

<div class="legend" markdown="1">
- $\mathbf F_i$: the force on atom $i$, in kJ mol$^{-1}$ nm$^{-1}$.
- $E_\theta$: the energy predicted by the model.
- $x_i$, $y_i$, $z_i$: the three coordinates of atom $i$.
- $\partial E_\theta/\partial x_i$: a partial derivative, the slope of the energy when only $x_i$ changes and every other coordinate of every atom is held fixed ([toolbox](maths.html#partial-derivative)).
- $\partial E_\theta/\partial\mathbf r_i$: shorthand for the three partial derivatives together, the gradient with respect to the position of atom $i$. Module 2 wrote it $\nabla_iU$.
- The minus sign: the force points towards lower energy.
</div>

This is the relation between force and potential energy of Module 2, with the learned energy in the place of $U$. Module 2 called a force **conservative** when it is minus the gradient of a function of the positions only, and showed that the total energy, kinetic plus potential, is then constant in time. "Conservative by construction" means that this holds whatever the parameters are, because an energy function exists by design. Even a badly trained model conserves its own, wrong, energy. In a simulation this means what it means for a force field: the total energy stays constant up to the small error of the integrator (Module 4), provided the learned energy is a smooth function of the positions.

"Automatic differentiation makes this free" refers to the previous section. The machinery that gives the slope of the loss with respect to the parameters also gives the slope of the energy with respect to the positions. Nobody has to derive or program the force formulas by hand. In computer time the forces are not free: they cost a small multiple of the energy.

<div class="box key" markdown="1">
**Worked example: the force from a one-neuron "potential".** Let the energy of a particle on a line be $E(x)=v\tanh(wx+b)$ with $v=2$, $w=0.8$ and $b=0.1$ (round numbers for illustration, in arbitrary units).

The chain rule gives the slope in two factors. The derivative of $\tanh(s)$ with respect to $s$ is $1-\tanh^2(s)$, and the derivative of $s=wx+b$ with respect to $x$ is $w$. So $dE/dx=v\,w\,\big[1-\tanh^2(wx+b)\big]$.

At $x=0.5$: $wx+b=0.5$, $\tanh(0.5)=0.462$, and $1-0.462^2=0.786$. The slope is $2\times0.8\times0.786=1.26$ and the force is $F=-1.26$. Automatic differentiation carries out these same steps, operation by operation, for a network with millions of operations.
</div>

<div class="box physics" markdown="1">
**Physics you need here: why a force that is not a gradient breaks energy conservation.** When the force is minus the gradient of an energy, a particle that travels around any closed path and returns to its starting point is back at the same height on the energy surface. The work done on it along the way adds up to zero: what it gained going downhill it paid back going uphill ([primer](physics.html#energy)).

A force that a network outputs directly is three numbers per atom, and nothing ties them to a common energy surface. A small example in a plane shows what can go wrong.

Take the force $\mathbf F=(-y,\,x)$ and walk once anticlockwise around the circle of radius 1. At every point of the circle this force has size 1 and points along the direction of walking. The work is force times path length, $1\times2\pi\approx6.28$. Every lap adds 6.28 units of energy from nowhere.

No energy function has this force. The test is that for a gradient the mixed derivatives must agree, $\partial F_x/\partial y=\partial F_y/\partial x$ ([toolbox](maths.html#partial-derivative)), and here they are $-1$ and $+1$. An MD run with such forces heats up or cools down by itself, and the first test of Module 2, a constant total energy without a thermostat, cannot be passed.
</div>

### Symmetries: what must not change

A water molecule has the same energy wherever it is in the laboratory, however it is turned, and whichever of its two hydrogens is called "atom 2". A formula that takes raw coordinates as input does not know this. Turning the molecule changes all nine input numbers.

**Symmetries.** The energy must not change when the whole molecule is translated or rotated, or when two atoms of the same element are exchanged. Forces must rotate with the molecule (equivariance). A model that has to learn these from data wastes capacity and generalises poorly, so they are built into the architecture.

The three operations, spelled out:

- **Translation.** Add the same vector to the position of every atom. The whole system is shifted and no distance between atoms changes.
- **Rotation.** Turn the whole system about any axis by any angle. Again no distance and no angle inside it changes.
- **Exchange of identical atoms** (also called permutation). Swap the labels of two atoms of the same element. Nothing physical has changed, only the numbering.

Two words describe how a quantity responds to such an operation. A quantity is **invariant** if it stays the same. It is **equivariant** if it changes along with the operation, in the same way as the molecule itself.

<div class="box key" markdown="1">
**Worked example: invariant and equivariant.** Two atoms. Atom A sits at the origin and atom B at $(0.1,\,0,\,0)$ nm. Suppose the force on B is $(-5,\,0,\,0)$ in some unit: it points towards A. Now rotate the pair by 90° about the $z$ axis, so that B moves to $(0,\,0.1,\,0)$.

- *The distance* between A and B is 0.1 nm before and after. It is invariant. So is the energy.
- *The position of B* was $(0.1,\,0,\,0)$ and is now $(0,\,0.1,\,0)$. It turned with the molecule. It is equivariant.
- *The force on B* must now be $(0,\,-5,\,0)$, which again points towards A. It is equivariant. A model that still returned $(-5,\,0,\,0)$ for the rotated pair would push B sideways, which is wrong.
</div>

In symbols, for a rotation $Q$:

$$
E(Q\mathbf r_1,\dots,Q\mathbf r_N)=E(\mathbf r_1,\dots,\mathbf r_N),\qquad\mathbf F_i(Q\mathbf r_1,\dots,Q\mathbf r_N)=Q\,\mathbf F_i(\mathbf r_1,\dots,\mathbf r_N).
$$

<div class="legend" markdown="1">
- $Q$: a rotation. Applied to a vector it returns the turned vector. Written as numbers it is a table of $3\times3$ entries, a [matrix](maths.html#matrices).
- $Q\mathbf r_i$: the position of atom $i$ after the rotation.
- $E(\dots)$: the energy as a function of the positions listed in the brackets. The elements $Z_i$ are left out because a rotation does not change them.
- $\mathbf F_i(\dots)$: the force on atom $i$ as a function of the same positions.
- The first equation states invariance: rotate the input and the output is the same number.
- The second states equivariance: rotate the input and the output is rotated in the same way.
</div>

One fact saves work. If the energy is invariant and the forces are its gradient, the forces are equivariant automatically. In words: when the molecule turns, the whole energy surface turns with it, and so do its downhill directions. A model therefore only has to make the energy invariant.

<details markdown="1"><summary>Optional: why an invariant energy gives equivariant forces</summary>
Take one particle, to keep the notation short. Invariance says $E(Q\mathbf r)=E(\mathbf r)$ for every position $\mathbf r$. Differentiate both sides with respect to the component $r_a$ of the position (the label $a$ stands for $x$, $y$ or $z$). On the left the chain rule gives a sum over the components $b$ of the rotated position $\mathbf r'=Q\mathbf r$:

$$
\frac{\partial}{\partial r_a}E(Q\mathbf r)=\sum_b\frac{\partial E}{\partial r'_b}\,\frac{\partial r'_b}{\partial r_a}=\sum_b\frac{\partial E}{\partial r'_b}\,Q_{ba}.
$$

The last step uses $r'_b=Q_{bx}x+Q_{by}y+Q_{bz}z$, so that $\partial r'_b/\partial r_a=Q_{ba}$, the entry of the table $Q$ in row $b$ and column $a$. The right-hand side of the invariance condition gives $\partial E/\partial r_a$ at the original position. Set the two equal and write the force as $\mathbf F=-\nabla E$:

$$
\sum_bQ_{ba}\,F_b(Q\mathbf r)=F_a(\mathbf r).
$$

For a rotation, the table that undoes $Q$ is $Q$ with its rows and columns exchanged, and that is the table which appears on the left. Applying $Q$ to both sides therefore cancels it on the left, and what remains is $\mathbf F(Q\mathbf r)=Q\,\mathbf F(\mathbf r)$. With many atoms the same steps apply to the gradient with respect to each atom.
</details>

Each symmetry also has a consequence that Module 2 listed under conservation laws. If the energy does not change under translation, the forces on all atoms add up to zero and the total momentum is conserved. If it does not change under rotation, there is no net torque. A model without these symmetries would let an isolated molecule start to drift or to spin by itself.

Why does learning the symmetries from data waste capacity? A network fed with raw coordinates would have to be shown each molecule in many positions and orientations to learn that they all have the same energy. Part of its parameters would be spent on that. And for an orientation it had not seen, it would still be only approximately right. With the symmetry built in, one example teaches all orientations at once and the result is exact.

How the three symmetries are built in:

- **Translation.** Use only relative positions $\mathbf r_j-\mathbf r_i$, never absolute ones. A shift by a vector $\mathbf a$ cancels: $(\mathbf r_j+\mathbf a)-(\mathbf r_i+\mathbf a)=\mathbf r_j-\mathbf r_i$.
- **Exchange of identical atoms.** Treat every atom of one element by the same rule, and combine the neighbours of an atom by a sum. A sum does not depend on the order of its terms.
- **Rotation.** There are two routes. The first feeds the network only quantities that a rotation leaves unchanged, such as distances and angles. These are **invariant descriptors**. The second keeps directions inside the network and allows only operations whose results turn correctly with the molecule. These are **equivariant networks**. The section on architectures describes both.

### Locality: a sum of atomic energies

A single network that took all $3N$ coordinates of one protein as its input would be useless for any other protein, which has a different number of atoms. The way out is to cut the energy into pieces, one per atom, and to compute every piece with the same small function from the surroundings of that atom.

**Locality.** To scale to large systems and to transfer between molecules, almost all models write the energy as a sum of atomic contributions that depend only on the neighbourhood within a cutoff $r_c$ (typically 0.4 to 0.6 nm):

$$
E=\sum_{i=1}^{N}E_i\big(\{\mathbf r_j-\mathbf r_i,\ Z_j\}_{r_{ij}<r_c}\big).
$$

<div class="legend" markdown="1">
- $E$: the total energy that the model predicts.
- $\sum_{i=1}^{N}$: a sum over all $N$ atoms.
- $E_i$: the **atomic energy** of atom $i$, the output of the network for that atom.
- $\{\dots\}_{r_{ij}<r_c}$: curly brackets denote a set. The condition at the lower right says which atoms $j$ belong to it: those closer to atom $i$ than the cutoff. This set is the **neighbourhood**, or local environment, of atom $i$.
- $\mathbf r_j-\mathbf r_i$: the position of neighbour $j$ as seen from atom $i$.
- $Z_j$: the element of neighbour $j$.
- $r_{ij}$: the distance between atoms $i$ and $j$.
- $r_c$: the **cutoff** radius. 0.4 to 0.6 nm is 4 to 6 Å, a few bond lengths.
</div>

Read it like this. Visit each atom in turn and see which atoms lie within $r_c$ of it, where they are and what elements they are. Compute one number from that. Add up the numbers of all atoms. An atom further than $r_c$ from atom $i$ has no influence on $E_i$.

Three remarks.

**The atomic energies are a device.** Quantum mechanics gives one energy for the whole configuration. It gives no reference value for the share of one atom. Training compares only the sum $E$ and its gradient with the reference, and the network is free to divide the total among the atoms in whatever way fits best.

**Why this scales.** An atom has a limited number of neighbours within $r_c$, whatever the size of the system. Liquid water holds about 100 atoms per nm$^3$, and a sphere of radius 0.5 nm has a volume of 0.52 nm$^3$, so each atom has about 50 neighbours. The work per atom is fixed and the total work grows in proportion to the number of atoms.

**Why this transfers.** The function $E_i$ never sees a whole molecule, only neighbourhoods. An oxygen atom with the same surroundings looks the same to it in a small peptide and in a large protein. A model can therefore be trained on small systems, for which quantum calculations are affordable, and then used on large ones, for which they are not. This works to the extent that the large system contains only neighbourhoods like those in the training set.

Cost is then linear in $N$. The weak point is anything beyond the cutoff: electrostatics and dispersion at long range are missing unless added explicitly.

"Linear in $N$" means that twice as many atoms cost twice as much, as for a force field with a cutoff. The weak point needs numbers to be appreciated. Electrostatics is the Coulomb interaction between charges, whose energy falls off only as $1/r$ with the distance $r$. Dispersion is the attraction that all atoms feel, the $-1/r^6$ part of the Lennard-Jones term (Module 5, and the [primer](physics.html#intermolecular)).

Take two ions with charges $+1$ and $-1$ in vacuum. Their Coulomb energy has the size $138.935/r$ kJ/mol with $r$ in nm: 232 kJ/mol at 0.6 nm and still 69 kJ/mol at 2 nm, against a thermal energy $k_BT$ of 2.5 kJ/mol at 300 K. A model with a cutoff of 0.6 nm gives this pair exactly the same energy at 0.7 nm and at 7 nm, because in both cases neither ion is in the neighbourhood of the other. A classical force field handles the same interaction with the Ewald methods of Module 7. The section on training comes back to the remedies.

## Architectures

An **architecture** is the design of the function $E_i$: what is computed from the neighbourhood of an atom, and in which order. This section describes three designs in the order in which they appeared. Each one removes a limitation of the one before. All three keep the sum of atomic energies and the cutoff.

| Design | What describes the neighbourhood | How rotation is handled | Models named below |
|---|---|---|---|
| Descriptors plus a network | Formulas chosen by people | The descriptors are invariant | Behler-Parrinello, ANI |
| Message passing with invariant features | Features that the network learns | Only distances are used | SchNet |
| Equivariant networks | Learned features that include directions | The features turn with the molecule | NequIP, MACE, Allegro |

### Descriptors plus a network

A **descriptor** is a list of numbers computed from the neighbourhood of an atom. It has to change when the neighbourhood changes its shape, and it must not change when the neighbourhood is shifted, turned or renumbered. Think of it as a fingerprint of the surroundings of the atom. Once the inputs are invariant, the network that follows needs no knowledge of symmetry.

[Behler and Parrinello (2007)](cite:behler2007) introduced the template. Describe each atom's environment by a vector of **symmetry functions** that are invariant by construction, for example a radial function

$$
G_i^{rad}=\sum_{j\ne i}e^{-\eta\,(r_{ij}-r_s)^2}\,f_c(r_{ij}),
$$

for a set of widths $\eta$ and shifts $r_s$ (ANI uses one narrow $\eta$ and many evenly spaced $r_s$), where $f_c$ goes smoothly to zero at the cutoff, plus angular functions built from triples of atoms.

<div class="legend" markdown="1">
- $G_i^{rad}$: one radial symmetry function of atom $i$, a single number. The superscript "rad" is a label for "radial", not a power.
- $\sum_{j\ne i}$: a sum over all other atoms $j$. Only those within the cutoff contribute, because $f_c$ is zero beyond it.
- $r_{ij}$: the distance between atoms $i$ and $j$, in nm.
- $r_s$: the shift, the distance at which this function "looks".
- $\eta$ (Greek eta): the width parameter, in nm$^{-2}$. A larger $\eta$ gives a narrower bump: the exponential has fallen to $1/e\approx0.37$ at a distance $1/\sqrt\eta$ from $r_s$.
- $e^{-\eta\,(r_{ij}-r_s)^2}$: a Gaussian bump ([toolbox](maths.html#gaussian)). It equals 1 when the neighbour sits exactly at the distance $r_s$ and falls towards 0 as the neighbour moves away from that distance.
- $f_c(r_{ij})$: the cutoff function, a smooth function that is 0 at the cutoff distance $r_c$ and beyond.
</div>

The word "vector" here means a list of numbers, not an arrow in space.

Read the formula like this. Every neighbour adds a number between 0 and 1: close to 1 if its distance is near $r_s$, close to 0 otherwise. So $G_i^{rad}$ is a soft count of the neighbours at a distance of about $r_s$. There is one such function for each value of $r_s$, and together they form a smoothed histogram of the distances from atom $i$ to its neighbours.

A numerical example, with round values for illustration: $\eta=100$ nm$^{-2}$, three neighbours at 0.15, 0.20 and 0.30 nm, and $f_c$ set to 1 to keep the arithmetic short. For the shift $r_s=0.15$ nm the three terms are $e^{0}=1$, $e^{-100\times0.05^2}=e^{-0.25}=0.78$ and $e^{-100\times0.15^2}=e^{-2.25}=0.11$, which add up to 1.88. For the shift $r_s=0.30$ nm they are 0.11, $e^{-1}=0.37$ and 1, which add up to 1.47. The numbers 1.88 and 1.47 are two entries of the descriptor of this atom.

Three points about the design.

**Why it is invariant.** The function uses only distances, which a translation or a rotation does not change. And it is a sum over the neighbours, which does not depend on how they are numbered.

**Why the cutoff function is smooth.** If the contribution of a neighbour were switched off abruptly at $r_c$, the energy would jump every time an atom crossed that distance. The force is the slope of the energy, so it would be infinite at that instant, and the total energy would not be conserved. Force fields smooth their cutoffs for the same reason (Module 7).

**Why angular functions are needed.** A radial function registers only how far each neighbour is from the central atom. Two neighbours at the same distances can sit on the same side of the central atom or on opposite sides, and no radial function can tell these apart. An angular function is a sum over pairs of neighbours of a function of the angle that the two make at the central atom, multiplied by factors that fall off with the distances and vanish at the cutoff. That involves three atoms at a time, the "triples" in the text. An angle is invariant too.

Feed the vector to a small neural network that outputs $E_i$, the same network for every atom of one element (the 2007 paper treated only silicon, so a single network served all atoms).

The whole chain for one atom is: positions of the neighbours, then the descriptor (fixed formulas), then the network, then $E_i$. Using one network per element is what builds in the exchange symmetry: all carbon atoms are treated by the same rule, so swapping two of them changes nothing. It also lets the model handle any number of atoms. In this design only the weights of the network are trained. The formulas of the descriptor, with their widths and shifts, are fixed beforehand.

**ANI** ([Smith, Isayev and Roitberg 2017](cite:smith2017)) used a heavily modified version of this design, with neighbours resolved by element and shifted angular functions, for organic molecules made of H, C, N and O, trained on about 17 million conformations.

"Neighbours resolved by element" means that there are separate symmetry functions for the neighbours of each element: one histogram for the hydrogen neighbours, one for the carbon neighbours, and so on. The descriptor then says which elements sit at each distance as well as how many atoms. "Shifted angular functions" means that the angular functions received shifts too, in the way $r_s$ shifts the radial ones. A **conformation** is one three-dimensional shape of a molecule, so each conformation is one training configuration.

Gaussian approximation potentials use related local-environment descriptors (the bispectrum originally, later SOAP) with kernel regression in place of a network.

The bispectrum and SOAP are two particular descriptors. Their formulas are not needed here. They play the role that the symmetry functions play above. What is new in this sentence is the method that turns the descriptor into an energy.

<div class="box maths" markdown="1">
**Maths you need here: kernel regression, in words.** A neural network stores what it has learned in its weights, and the examples are no longer needed afterwards. Kernel regression keeps a set of examples and predicts by comparison with them. A **kernel** $\kappa(\mathbf d,\mathbf d')$ is a function that measures how similar two descriptors $\mathbf d$ and $\mathbf d'$ are: 1 if they are identical, and towards 0 as they become more different. The prediction for a new neighbourhood with descriptor $\mathbf d$ is a weighted sum of its similarities to the $M$ stored neighbourhoods:

$$
E_i=\sum_{m=1}^{M}c_m\,\kappa(\mathbf d,\mathbf d_m).
$$

Here $\mathbf d_m$ is the descriptor of stored neighbourhood $m$ and $c_m$ is its coefficient. The coefficients are the only fitted numbers. The prediction depends on them in a linear way, so the least-squares fit is solved in one step by linear algebra, with no gradient descent ([toolbox](maths.html#fitting)).

A tiny example with a one-number descriptor and the kernel $\kappa(d,d')=e^{-(d-d')^2}$. Two stored points, $d_1=0$ with $c_1=2$ and $d_2=1$ with $c_2=-1$. At $d=0.5$ both similarities are $e^{-0.25}=0.78$ and the prediction is $2\times0.78-1\times0.78=0.78$. At $d=0$ it is $2\times1-1\times0.37=1.63$. At $d=5$, far from both stored points, both similarities are practically zero and so is the prediction.
</div>

Kernel models are known for learning from few examples, a property that comes up again below. The price is that the cost of one prediction grows with the number of stored examples.

### Message passing

In the design above, people chose the descriptor, and the choice of widths and shifts limits what the network can see. Message passing removes that limit: the network builds its own description of each neighbourhood.

A picture first. Every atom holds a card with a list of numbers on it. In the usual scheme the card says at the start only which element the atom is. In each round, every atom reads the cards of its neighbours, together with how far away each neighbour is, and rewrites its own card. After a few rounds the card describes the surroundings of the atom, and a small network turns the card into the atomic energy.

Let the network learn the descriptors. Treat atoms as nodes of a graph, with edges between neighbours within the cutoff. A **graph** in this sense is a set of points (the nodes) with lines (the edges) that join some pairs of them. The edges are not chemical bonds: any two atoms closer than $r_c$ are joined. Each atom carries a feature vector $\mathbf h_i$, updated in several rounds using messages from its neighbours:

$$
\mathbf h_i^{(t+1)}=\mathcal U\Big(\mathbf h_i^{(t)},\ \sum_{j\in\mathcal N(i)}\mathcal M\big(\mathbf h_i^{(t)},\mathbf h_j^{(t)},\mathbf r_{ij}\big)\Big),\qquad E=\sum_i\mathcal R\big(\mathbf h_i^{(T)}\big).
$$

<div class="legend" markdown="1">
- $\mathbf h_i^{(t)}$: the **feature vector** of atom $i$ after round $t$, the "card" of the picture. It is a list of numbers (say 64 of them) with no fixed physical meaning. Training decides what they encode. Bold means "a list of numbers" here, not an arrow in space.
- $(t)$, $(t+1)$, $(T)$: labels of the round, not powers. $t$ runs from 0 to $T$.
- $T$: the total number of rounds, a small number such as 3. In this section $T$ is not the temperature.
- $\mathcal N(i)$: the set of neighbours of atom $i$, all atoms within $r_c$ of it.
- $\sum_{j\in\mathcal N(i)}$: a sum over those neighbours. The sign $\in$ means "is a member of".
- $\mathbf r_{ij}$: the relative position of the two atoms. Read it here as $\mathbf r_j-\mathbf r_i$, the vector from atom $i$ to its neighbour $j$, as in the formula for locality. (Module 2 defined its $\mathbf r_{ij}$ with the opposite sign. Either convention works as long as it is kept throughout.) Invariant models, such as the one described next, use only its length, the distance $r_{ij}$.
- $\mathcal M$: the **message function**, a small network. It computes the message that neighbour $j$ sends to atom $i$.
- $\mathcal U$: the **update function**, a small network. It combines the present features of the atom with the sum of the incoming messages into the new features.
- $\mathcal R$: the **readout function**, a small network that turns the final features of atom $i$ into its atomic energy.
- $E$: the total energy, the sum of the atomic energies over all atoms $i$.
</div>

Read the first formula as three steps per round: compute one message per neighbour, add the messages, update the card. The sum does two jobs. It makes the result independent of the numbering of the neighbours, and it lets the same functions handle an atom with 5 neighbours and an atom with 50. The second formula is the sum of atomic energies of the section on locality, with $E_i=\mathcal R(\mathbf h_i^{(T)})$.

**SchNet** ([Schütt et al. 2018](cite:schutt2018)) is the simplest case: the message from atom $j$ is its feature vector multiplied, element by element, by a learned function of the distance, so the features stay invariant. (SchNet itself used a cutoff only for crystals. Some later models, MACE among them, read the energy out from every layer and add the contributions.) After $T$ rounds an atom has received information from up to $T\times r_c$ away.

Three phrases of this paragraph need unpacking.

**"Multiplied, element by element."** Two lists of the same length are multiplied entry by entry: $(1,\,2,\,3)$ and $(0.5,\,0,\,2)$ give $(0.5,\,0,\,6)$. Here the first list is the card of neighbour $j$. The second list comes from a small network that takes the distance $r_{ij}$ as input, the "learned function of the distance". It decides how much of each feature of the neighbour is let through at that distance. It does the work of the Gaussian bumps of the previous section, with a shape that is trained and not chosen.

**"The features stay invariant."** The cards start as codes for the elements, which a rotation does not change. Each round uses only cards and distances. So every number on every card is unchanged when the molecule is turned, and so is the energy.

**"Up to $T\times r_c$ away."** In round 1, atom $i$ learns about the atoms within $r_c$. In round 2, the cards of those neighbours already contain what they learned about their own neighbours, which can be up to $2r_c$ from atom $i$. With $T=3$ and $r_c=0.5$ nm the reach is 1.5 nm.

This reach has a limit that matters later. Information travels only along chains of neighbours. Two molecules separated by more than $r_c$ of empty space share no edge and exchange nothing, however many rounds there are. Message passing extends the reach inside dense matter. It does not replace a true long-range interaction.

### Equivariant networks

<div data-videos="ZR1NTBPBDOo I9Y2le9e74A"></div>

This is the heaviest section of the module, and three statements are enough on a first reading. Models that use only distances have to work hard to recover angles. Equivariant models also carry directions on their cards, in a form that turns correctly when the molecule turns. In return they need far fewer training examples and cost more per evaluation. The two maths boxes explain the tools by name and can be skipped.

Distances alone discard directional information, which then has to be recovered from many-body combinations.

An atom that is told only "one neighbour at 0.10 nm, another at 0.15 nm" does not know the angle between the two. To find it, it needs a third number, the distance between the two neighbours, and that number involves three atoms at once. A quantity that depends on three or more atoms together is a **many-body** quantity. The number of atoms involved is the **body order**: a distance is two-body, an angle is three-body and a torsion angle is four-body.

**Equivariant** networks carry features that are vectors and higher-rank tensors and that rotate with the molecule.

The ladder of objects, from the bottom:

- A **scalar** is a single number that a rotation leaves unchanged: an energy, a distance, a charge. Invariant networks carry only scalars.
- A **vector** is three numbers that turn like an arrow: a force, a dipole moment, the direction to a neighbour.
- A **higher-rank tensor** has more components and carries finer angular detail, with its own fixed rule for how the components mix under a rotation. The shape of a d orbital is a good picture of the next level.

In an equivariant network the card of each atom holds some scalars, some vectors and some higher objects. When the molecule is turned, the scalars stay as they are and the vectors turn with it. Because the rule by which every feature changes under a rotation is known, the network can guarantee that the final energy is invariant.

Messages are built from spherical harmonics of the direction $\hat{\mathbf r}_{ij}$ and combined with tensor products that respect the rules for adding angular momenta.

Here $\hat{\mathbf r}_{ij}=\mathbf r_{ij}/r_{ij}$ is the unit vector that points from atom $i$ to its neighbour $j$: the direction to the neighbour without the distance. The two tools named in the sentence are explained in the boxes.

<div class="box maths" markdown="1">
**Maths you need here: spherical harmonics, in words.** A spherical harmonic is a function of a direction, that is, a function on the surface of a sphere. Spherical harmonics come in levels numbered $\ell=0,1,2,\dots$, with $2\ell+1$ functions at level $\ell$:

- $\ell=0$: one function, the same in all directions (the shape of an s orbital);
- $\ell=1$: three functions, proportional to the $x$, $y$ and $z$ components of the unit vector (the shapes of the p orbitals);
- $\ell=2$: five functions (the shapes of the d orbitals).

They do for directions what sines and cosines do for a periodic signal ([toolbox](maths.html#fourier)): any smooth function of direction is a sum of them, and a higher $\ell$ describes finer angular detail.

The property that matters here is how they behave under rotation: the $2\ell+1$ functions of one level mix only among themselves. Example for $\ell=1$: for the direction along $z$ the three functions have the values $(0,\,0,\,1)$, up to a common factor. Turn the direction by 90° to point along $x$ and the values become $(1,\,0,\,0)$. The three numbers were reshuffled, in the way the components of a vector are, and no number of another level entered. So a feature built from level $\ell$ has a known rule for how it turns.
</div>

<div class="box maths" markdown="1">
**Maths you need here: combining features without breaking the symmetry.** A network has to combine features in a way that is more than a plain sum. For scalars the curve of the activation function does this, and any product will do as well. A vector is different: a curve such as $\tanh$ applied to its three components one by one would spoil the way the vector turns, so equivariant networks multiply features with each other instead. For vectors only certain products give a result that again turns correctly. Two of them are familiar. Take $\mathbf a=(1,\,2,\,0)$ and $\mathbf b=(3,\,1,\,0)$.

- The [dot product](maths.html#dot-product) gives a scalar: $\mathbf a\cdot\mathbf b=1\times3+2\times1+0\times0=5$.
- The [cross product](maths.html#cross-product) gives a vector: $\mathbf a\times\mathbf b=(0,\,0,\,-5)$.

Now turn both vectors by 90° about the $x$ axis, which sends $(x,\,y,\,z)$ to $(x,\,-z,\,y)$. They become $(1,\,0,\,2)$ and $(3,\,0,\,1)$. The dot product is $3+0+2=5$, unchanged: it is invariant. The cross product is $(0,\,5,\,0)$, which is the old result $(0,\,0,\,-5)$ turned by the same rotation: it is equivariant.

A product such as "multiply the $y$ components and ignore the rest" gives 2 before the rotation and 0 after it. It is neither invariant nor a proper vector, and a network that used it would break the symmetry.

A **tensor product** is the general form of this: the complete list of ways in which a feature of level $\ell_1$ and a feature of level $\ell_2$ can be multiplied so that each result belongs to a definite level. Two vectors (level 1 and level 1) give one scalar, one vector and one level-2 object, $1+3+5=9$ numbers from $3\times3$. Quantum mechanics uses the same table to combine two angular momenta, which is where the phrase "rules for adding angular momenta" comes from. The table is fixed by geometry. Training does not change it.
</div>

With these two tools a message can carry the direction to a neighbour as well as its distance, and every step of the network keeps the turning rules intact. The angle between two neighbours, which an invariant model has to reconstruct from several distances, is available directly: it is contained in the dot product of two direction vectors.

**NequIP** ([Batzner et al. 2022](cite:batzner2022)) showed that this gives high accuracy from far less training data: on water and ice it reached lower force errors with 133 training structures than an earlier neural network trained on 133,500, and on small molecules it matched or beat kernel methods, which were already data-efficient.

A **force error** is the typical size of the difference between the predicted and the reference force components, measured on a test set. The comparison in numbers: 133 structures against 133,500 is about a thousand times fewer quantum calculations, and those are the expensive part of the whole procedure.

**MACE** ([Batatia et al. 2022](cite:batatia2022)) builds higher body-order messages in each layer, which allows fewer layers and faster evaluation.

In the message-passing formula above, each message involves the central atom and one neighbour, so it is two-body. A message of higher body order depends on several neighbours at once. More then happens within one round, and fewer rounds are needed.

These are the current standard, together with related designs (Allegro, which is strictly local and parallelises well).

"Strictly local" means that the atomic energy of an atom depends only on atoms within $r_c$ of it, with no growth of the reach from round to round. That is what makes parallel computing simple. The system can be cut into regions that are given to different processors, and each processor needs to know only a shell of thickness $r_c$ around its own region. With message passing over $T$ rounds, the shell has to be $T\times r_c$ thick.

Equivariant operations cost more per atom than invariant ones. The section on cost comes back to this.

## Training

<div data-videos="106sdeDF1oc"></div>

Training a potential follows the general recipe of the section on tools: examples, a loss, gradient descent, and sets held back for validation and testing. What is specific is the loss, which has to compare two kinds of quantity.

The loss combines energies and forces over a set of reference configurations:

$$
\mathcal L(\theta)=w_E\sum_{c}\big(E_\theta^{(c)}-E_{QM}^{(c)}\big)^2+w_F\sum_{c}\sum_{i=1}^{N_c}\big|\mathbf F_{\theta,i}^{(c)}-\mathbf F_{QM,i}^{(c)}\big|^2 .
$$

<div class="legend" markdown="1">
- $\mathcal L(\theta)$: the loss, one number that depends on the parameters $\theta$ of the model.
- $c$: the label of one reference configuration. $\sum_c$ is a sum over all configurations of the training set. The superscript $(c)$ is this label, not a power.
- $E_\theta^{(c)}$: the energy that the model predicts for configuration $c$.
- $E_{QM}^{(c)}$: the quantum-mechanical energy of the same configuration.
- $N_c$: the number of atoms in configuration $c$. $\sum_{i=1}^{N_c}$ is a sum over them.
- $\mathbf F_{\theta,i}^{(c)}$: the force on atom $i$ of configuration $c$ predicted by the model, that is, minus the gradient of $E_\theta$.
- $\mathbf F_{QM,i}^{(c)}$: the quantum-mechanical force on the same atom.
- $\vert\ \ \vert^2$: the squared length of the vector between the bars, the sum of the squares of its three components.
- $w_E$, $w_F$: two positive numbers chosen by the user, the weights of the energy part and of the force part. They are not the weights inside the network.
</div>

Read it like this. The first sum is the least-squares loss of the section on tools, with energies as labels. The second sum is the same thing for forces: for every atom of every configuration, the squared length of the difference between the predicted and the reference force. The weights $w_E$ and $w_F$ decide how much each part counts. They also make the two parts comparable, because a squared energy and a squared force have different units.

Each configuration supplies one energy but $3N$ force components, so forces carry most of the information and are usually weighted most.

Here $N$ is the number of atoms of the configuration, the $N_c$ of the loss above. A configuration of 100 atoms gives 1 energy and 300 force components. There is also a geometric way to see it. The energy says how high the surface is at one point. The forces say how the surface slopes in every direction around that point, which fixes the surface nearby as well. The demo at the end of this section shows the other side: a network trained on energies alone can reproduce every training energy and still have wrong forces between the points.

The force part of the loss contains a derivative of the network, since the predicted force is a gradient of the predicted energy. Its slope with respect to the parameters is then a derivative of a derivative. Automatic differentiation handles this without extra work from the user, at some extra cost in computer time.

### Where a learned potential can be trusted

A fitted function knows something only where it has examples. Between examples it interpolates, and that works well. Outside them it extrapolates, and for a network that means following whatever shape its parameters happen to give. A classical force field is in a better position there: its $r^{-12}$ repulsion keeps non-bonded atoms from overlapping, whether or not such a pair was in the fitting data. A network has no such wall unless it has learned one or been given one.

**Data matter more than architecture.** A model is reliable only for the kinds of configurations it was trained on. Outside them it does not degrade gracefully: it can predict a deep, unphysical energy minimum and the simulation falls into it. Remedies:

- **Active learning.** Run MD with the current model, detect configurations where the model is uncertain (typically where an ensemble of models disagree), compute those with quantum chemistry, add them and retrain.
- **Stability tests.** A low error on a test set of forces does not guarantee stable dynamics. Always run long simulations and check distributions and conservation of energy.

"Does not degrade gracefully" means that the error does not grow slowly as the simulation leaves the training data. It can become enormous at once. A "deep, unphysical energy minimum" is a hole in the learned energy surface at a geometry that in reality has a very high energy, for example two atoms almost on top of each other. Forces point towards lower energy, so the simulation is pulled into the hole. Atoms collapse onto each other or bonds fly apart, and the run crashes or, worse, continues with a meaningless structure.

**How active learning detects uncertainty.** A single network always returns a number and gives no sign of whether that number is a guess. The section on tools noted that networks trained from different random starting parameters agree where there are examples and can differ where there are none. An **ensemble** in this bullet is a handful of such networks trained on the same data (it is not the statistical ensemble of Module 3). Their disagreement on a configuration is a cheap alarm.

For example, suppose four models predict one force component as 102, 98, 101 and 99 kJ mol$^{-1}$ nm$^{-1}$. The mean is 100 and the spread ([standard deviation](maths.html#averages)) is about 2: the models agree, and the configuration is of a kind they know. For another configuration they predict 60, 140, 95 and 20. The mean is 79 and the spread is about 50, so this configuration is sent to the quantum program.

The loop of the bullet (run, detect, compute, add, retrain) is repeated until the simulation no longer raises alarms. Agreement is a good sign and not a proof, since all the models can be wrong in the same way.

**Why a small force error is not enough.** The test set usually consists of configurations of the same kind as the training set, so its error measures interpolation. An MD run is a different kind of test. It visits millions of configurations one after the other, each force error moves the atoms a little off course, and the run goes wherever the model sends it. One hole in the energy surface, reached once, is enough to ruin it. The practical checks are those of the earlier modules: a constant total energy without a thermostat (Module 2), a steady temperature, no pair of atoms closer than is physically possible, and distributions of bond lengths, angles and distances between atoms that stay reasonable for the whole run (Module 11).

### Cost, hybrid schemes and pretrained models

**Cost and reach.** Even the fastest learned potentials are one to three orders of magnitude slower than a classical force field for the same system ([Unke et al. 2021](cite:unke2021)), and the accurate equivariant networks sit at the slow end. That limits routine use to small systems or short times, or to a hybrid in which only a region of interest (a ligand) is treated by the learned potential and the rest by a force field (ML/MM): with a 53-atom learned region the OpenMM developers report a slowdown of only 3 to 5 times ([Eastman et al. 2024](cite:eastman2024)). General-purpose pretrained models for organic and biological chemistry exist (the ANI family, AIMNet2, MACE-OFF and others). OpenMM ships ANI-1ccx and ANI-2x and runs other PyTorch models through a plug-in; LAMMPS runs several others.

**What the slowdown means in practice.** One to three orders of magnitude is a factor of 10 to 1,000. If a force field gives 100 ns per day for some system (a round number for illustration), a learned potential 100 times slower gives 1 ns per day. The reason is the amount of arithmetic per atom. A force field evaluates a short formula for each pair of atoms. A learned potential passes each neighbourhood through a network with a great many multiplications, and then differentiates the result.

**The hybrid, ML/MM.** The idea is to spend the expensive model only where the force field is weakest. The system is divided into a small region, for example a ligand, and the rest: protein, water and ions. In the simplest scheme, called mechanical embedding, the learned potential replaces the force field only for the interactions inside the region. One general way to write this scheme is the formula below. It is a textbook form and is not an equation quoted from the papers cited above:

$$
E=E_{MM}(\text{whole system})-E_{MM}(\text{region})+E_{ML}(\text{region}).
$$

<div class="legend" markdown="1">
- $E$: the energy used for the simulation.
- $E_{MM}(\text{whole system})$: the force-field energy of everything. MM stands for molecular mechanics, another name for a classical force field.
- $E_{MM}(\text{region})$: the force-field energy of the region alone, as if it were in vacuum. Subtracting it removes the force-field description of the inside of the region.
- $E_{ML}(\text{region})$: the energy of the region alone from the learned potential, which takes its place.
</div>

Read it like this. The bonds, angles, torsions and internal non-bonded terms of the ligand now come from the learned potential. The interactions between the ligand and its surroundings are still those of the force field, charges and Lennard-Jones terms included. Such a scheme improves the internal energetics of the ligand, such as its torsion profiles and its strain, and leaves its interactions with the protein as accurate as the force field makes them. The cost stays low because the network is evaluated for some tens of atoms and not for the whole box.

**Pretrained, general-purpose models.** A **pretrained** model is one that its developers have already trained, on a broad data set, and that is distributed with its parameters. You use it as you use a force field: download it and run, with no quantum calculations of your own. Models of this kind that aim to cover a wide part of chemistry are also called **foundation models** or **universal potentials**. Those words describe the breadth of the training set, and the model is bounded by it. Before using such a model, check that your system lies inside what it was trained on: the elements, the charge states, and the kind of molecule.

A pretrained model can also serve as a starting point. Training is continued on a small set of your own reference calculations, which is called **fine-tuning**. **PyTorch**, named in the paragraph above, is a widely used Python library for building and training neural networks, with automatic differentiation built in. A model written with it can be loaded by an MD program through an interface, the "plug-in" of the text.

### Long range

**Long range.** Strictly local models miss electrostatics beyond the cutoff. Approaches include predicting atomic partial charges and adding an explicit Coulomb term (with an empirical dispersion correction), and learning a correction on top of a physical baseline.

The section on locality showed the size of what is missing: tens to hundreds of kJ/mol for a pair of ions beyond the cutoff. The two approaches of the paragraph work as follows.

**Predicted charges plus Coulomb.** The network outputs, for each atom, a partial charge in addition to an atomic energy. The charges then interact through Coulomb's law over all distances, as in a force field. In outline the energy has the form

$$
E=\sum_iE_i+\sum_{i<j}\frac{q_iq_j}{4\pi\epsilon_0\,r_{ij}}+E_{disp}.
$$

<div class="legend" markdown="1">
- $E$: the total energy that the model predicts.
- $\sum_iE_i$: the sum of the atomic energies from the network, which covers what happens within the cutoff.
- $q_i$, $q_j$: the partial charges of atoms $i$ and $j$, in units of the elementary charge $e$. The model predicts them from the neighbourhood of each atom, so they can change when the surroundings change. In a fixed-charge force field they are constants.
- $\sum_{i<j}$: a sum over all pairs of atoms, each pair counted once, at any distance.
- $r_{ij}$: the distance between the two atoms.
- $1/(4\pi\epsilon_0)$: the constant of Coulomb's law, 138.935 kJ mol$^{-1}$ nm $e^{-2}$ ([primer](physics.html#electrostatics)).
- $E_{disp}$: the dispersion correction, a sum over pairs of atoms of attractive terms that fall off as $1/r_{ij}^6$, as the attractive part of the Lennard-Jones term does. "Empirical" means that it is a simple fitted formula and not a quantum calculation.
</div>

In a periodic box the Coulomb sum is computed with the Ewald methods of Module 7, as for a force field. Details differ between models, in particular how the two added terms are switched off at short distances, where the network already describes the interaction.

**A correction on top of a baseline.** Here the total energy is written as $E=E_{base}+E_\theta$. The baseline $E_{base}$ is a cheap physical model that already has the right behaviour at long range, for example a force field or an approximate quantum method. The network $E_\theta$ is trained on the difference between the reference energy and the baseline. The aim is that this difference is smaller and smoother than the full energy and mostly short-ranged, so that a local network can learn it. A baseline with a repulsive term also provides the wall at short distances that a bare network lacks.

The demo below puts several points of this section together. It fits a network with two hidden layers of 16 neurons to the energy of a one-dimensional double well, $E(x)=(x^2-1)^2$, from points inside a range that you choose. It is trained on energies only, and its forces are obtained by differentiating the network. Look at three things: how good the fit is inside the range of the data, what the curve does outside it, and what happens to the forces when there are very few points.

<div class="widget" data-widget="nnfit"></div>

## Machine-learned coarse-graining

So far the network learned an energy from quantum calculations. The same machinery can learn a different function from a different source: the effective potential of a coarse-grained model, from atomistic MD trajectories.

Module 15 showed that the ideal coarse-grained potential is the many-body PMF, and that force matching finds it in principle. Pair potentials are too restrictive to represent it. A neural network is not.

<div class="box physics" markdown="1">
**Physics you need here: a reminder of Module 15.** A **coarse-grained** (CG) model replaces groups of atoms by single sites, often called beads, for example one bead per amino acid. The solvent can be removed altogether, so that its effect has to be contained in the interactions between the beads. The **mapping** $\mathbf R=\mathbf M(\mathbf r)$ is the rule that gives the positions of the beads, $\mathbf R$, from the positions of all atoms, $\mathbf r$.

Many different atomistic configurations map to the same $\mathbf R$. The ideal CG potential is the one that makes every bead configuration exactly as probable as it is in the atomistic simulation. It is $U_{CG}(\mathbf R)=-k_BT\ln p(\mathbf R)$ plus a constant, where $p(\mathbf R)$ is the probability density of finding the beads at $\mathbf R$ in the atomistic simulation, $k_B$ is the Boltzmann constant and $T$ the temperature. This is a free energy, called the **potential of mean force** (PMF): it contains the entropy of everything that was removed ([primer](physics.html#thermodynamics)).

The name comes from its slope. Minus the gradient of the PMF is the **mean force**: the force on the beads averaged over all the atomistic configurations that map to the same $\mathbf R$. **Many-body** means that the PMF cannot be written as a sum of terms that each depend on one pair of beads. **Force matching** chooses the CG potential whose forces are, in the least-squares sense, closest to the atomistic forces projected onto the beads.
</div>

**CGnet** ([Wang et al. 2019](cite:wang2019b)) trains a network $U_\theta(\mathbf R)$ on atomistic trajectories by minimising the force-matching loss

$$
\mathcal L(\theta)=\Big\langle\big|-\nabla_{\mathbf R}U_\theta\big(\mathbf M(\mathbf r)\big)-\mathbf M_F\,\mathbf f(\mathbf r)\big|^2\Big\rangle,
$$

where $\mathbf M_F\,\mathbf f$ is the atomistic force projected on the coarse-grained sites.

<div class="legend" markdown="1">
- $\mathcal L(\theta)$: the loss, a function of the parameters $\theta$ of the network.
- $\mathbf r$: the positions of all atoms in one frame of the atomistic trajectory.
- $\mathbf M(\mathbf r)$: the mapping, which gives the bead positions $\mathbf R$ of that frame.
- $U_\theta$: the network. Its input is the bead positions and its output is one number, the coarse-grained energy.
- $\nabla_{\mathbf R}$: the gradient with respect to the bead positions. $-\nabla_{\mathbf R}U_\theta$ is the force on the beads that the model predicts.
- $\mathbf f(\mathbf r)$: the forces on all atoms in that frame, from the atomistic force field.
- $\mathbf M_F$: the rule that turns the forces on the atoms into a force on each bead. For a bead placed at the centre of mass of a group of atoms it is the sum of the forces on those atoms.
- $\vert\ \ \vert^2$: the squared length of the difference, summed over all beads.
- $\langle\ \rangle$: the average over all frames of the trajectory.
</div>

Read it like this. For every frame: map the atoms to beads, ask the network for the forces on the beads, compare them with the projected atomistic forces and square the difference. Then average over the frames. It is the force part of the loss for potentials, with atomistic MD in the role that quantum chemistry had there. There is no energy part, because a simulation frame comes with forces but not with a value of the free energy.

The instantaneous projected force is extremely noisy, since it fluctuates around the mean force, so a large amount of data is needed.

<div class="box maths" markdown="1">
**Maths you need here: a least-squares fit to noisy labels returns their mean.** Suppose the same input comes with three different labels, 3, 5 and 10, because something that the model cannot see differs between the three cases. Which single prediction $a$ gives the smallest squared error $(a-3)^2+(a-5)^2+(a-10)^2$? Setting its derivative $2(a-3)+2(a-5)+2(a-10)$ to zero gives $a=18/3=6$, the mean of the labels.

Two things follow. The best prediction is the mean, although no label equals 6. And the loss at the best prediction is not zero: it is $9+1+16=26$, which is three times the [variance](maths.html#averages) of the labels (the mean squared deviation from the mean, $26/3\approx8.7$). No model can do better, because the remaining error is in the labels and not in the model.
</div>

This is the situation of force matching. For one bead configuration $\mathbf R$, the things that the model cannot see are the positions of the solvent and of all the atoms inside the beads. Each frame supplies one instantaneous force, and the network that minimises the loss predicts their mean, which is the mean force and therefore minus the gradient of the PMF. The scatter of the instantaneous forces around the mean is large, so many frames are needed before the mean emerges. For the same reason the value of the loss stays far from zero even for a perfect model.

A simple physical prior (bonded terms and a repulsion; in Majewski et al. also a term that fixes chirality) is added so that the model behaves sensibly in regions without data.

A **prior** is a fixed, hand-written energy to which the output of the network is added. With a prior, $U_\theta$ in the loss above stands for the sum of the two, and training changes only the network part. The network then has to learn only what the prior leaves over: the difference between the projected atomistic forces and the forces of the prior. It is needed for the reason given under training. The atomistic trajectory never contains two beads on top of each other or a bond stretched to twice its length, because such states have a very high energy. The network sees no data there and could put a hole there. Springs between bonded beads and a steep repulsion at short distance put the walls in by hand.

**Chirality** is handedness. Natural amino acids are left-handed, and a protein and its mirror image are different objects. All distances between beads are the same in a structure and in its mirror image, so a model that sees only distances gives both the same energy. A term that tells left from right removes the mirror image.

[Majewski et al. (2023)](cite:majewski2023) trained one model on twelve small fast-folding proteins. It recovered the native structure of ten of them and of a few helical mutants, and its authors state that it should not be expected to work for other sequences. Transfer to proteins outside the training set came later, from training on far more diverse data (Module 18). The state-dependence problem of Module 15 remains: the learned free energy is for the temperature and conditions of the training data.

Two terms in this paragraph. **Transfer** means using a model on systems that were not in its training set, here on other protein sequences. **State dependence** follows from the PMF being a free energy. It contains the entropy of the removed atoms, and entropy enters a free energy multiplied by the temperature. A model trained on a simulation at 300 K has learned the PMF of 300 K, and nothing guarantees that it is right at 350 K or at another salt concentration.

## Generating ensembles without running dynamics

MD produces equilibrium samples one correlated step at a time, and is slow because of barriers. Generative models try to draw independent samples from the Boltzmann distribution directly.

The terms, one by one. The **Boltzmann distribution** (Module 3) says how probable each configuration $\mathbf x$ is at temperature $T$: its probability density is proportional to $e^{-\beta U(\mathbf x)}$, where $U$ is the potential energy and $\beta=1/k_BT$. Equilibrium properties are averages over this distribution. A set of configurations drawn from it is called an **ensemble** in this part of the module.

MD draws from the distribution by following the motion. Each frame is almost the same as the one before, which is what **correlated** means (Module 11), and a crossing from one energy basin to another is rare when the barrier is many $k_BT$ high. Two **independent** samples have nothing to do with each other: knowing one tells you nothing about the other.

A **generative model** is a network that turns random numbers into new samples that resemble its training data. Image generators are the familiar example. Here the samples are molecular configurations, and the goal is that each call of the model returns a fresh configuration, with every kind of configuration appearing as often as the Boltzmann distribution says. Two families follow. The first can be corrected to be exact, and the second cannot.

### Boltzmann generators

<div data-videos="WuXJRswYIaA JZjeFBH0Jl4"></div>

Random numbers with a Gaussian (bell-shaped) distribution are easy to produce ([toolbox](maths.html#random-numbers)). A transformation can turn them into random numbers with another distribution. The smallest example: if $z$ is a standard Gaussian number, with mean 0 and width 1, then $x=\mu+s\,z$ is a Gaussian number with mean $\mu$ and width $s$. A Boltzmann generator does the same with a far more complicated transformation, one that turns a long list of Gaussian numbers into all the coordinates of a molecule.

[Noé et al. (2019)](cite:noe2019). Train an invertible network (a normalising flow) $\mathbf x=f_\theta(\mathbf z)$ that maps a simple Gaussian variable $\mathbf z$ to molecular configurations.

<div class="legend" markdown="1">
- $\mathbf z$: a list of independent standard Gaussian random numbers, as many as the molecule has coordinates. It has no physical meaning. It is the raw material.
- $\mathbf x$: a molecular configuration, the list of all coordinates.
- $f_\theta$: the network, a function with parameters $\theta$ that turns $\mathbf z$ into $\mathbf x$.
</div>

**Invertible** means that the map can be run backwards: every $\mathbf x$ comes from exactly one $\mathbf z$, and the network can compute it. An ordinary network is not invertible, so a **normalising flow** is assembled from layers that are each simple enough to be undone.

It is trained in two ways at once: by energy (a loss that needs only $U$ and pushes generated configurations towards low energy while keeping them spread out) and by example (maximum likelihood on a few known configurations of each state of interest). Training by energy alone collapses onto the most stable state.

**Training by energy** needs no simulation data. The network generates configurations, the force field gives their energies $U$, and the parameters are changed so that the energies go down. Low energy alone would put every sample at the single lowest point. The Boltzmann distribution is a balance between low energy and many configurations, that is, between energy and entropy (Module 3), so the loss has a second part that rewards spreading the samples out.

**Training by example** uses **maximum likelihood**: the parameters are changed so that the model gives a high probability density to configurations that are known to be important, such as a few structures of each folded or bound state.

**Why energy alone collapses.** In training by energy the network learns only from the configurations that it generates itself. If it never produces a configuration of state B, nothing in the loss tells it that state B exists. It then keeps refining the state that it has found. The examples show it where the other states are.

<div class="box maths" markdown="1">
**Maths you need here: how a probability density changes under a change of variable.** A [probability density](maths.html#probability) $p(x)$ gives the probability of finding $x$ in a small interval as $p(x)$ times the length of the interval. Let $x=f(z)$ with $f$ invertible. The numbers $z$ in a small interval of length $dz$ are sent to an interval of length $dx$, and the probability of being in it is the same before and after. Write $p_Z$ for the density of $z$ and $p_X$ for the density of $x$:

$$
p_X(x)\,|dx|=p_Z(z)\,|dz|\qquad\text{so}\qquad p_X(x)=p_Z(z)\,\left|\frac{dz}{dx}\right| .
$$

Where the map stretches an interval, the same probability is spread over more length and the density goes down. Example: $z$ is a standard Gaussian and $x=2z$. Then $z=x/2$, $dz/dx=1/2$, and $p_X(x)=\tfrac12\,p_Z(x/2)$. At the centre, $p_Z(0)=0.399$ and $p_X(0)=0.199$: the stretched distribution is twice as wide and half as high.

With many variables the factor $\vert dz/dx\vert$ becomes the factor by which the inverse map, from $\mathbf x$ back to $\mathbf z$, changes a small volume. Where the network stretches space, this factor is smaller than 1. It is the absolute value of the **determinant** of the table of all partial derivatives $\partial z_a/\partial x_b$, which is called the Jacobian matrix ([toolbox](maths.html#matrices)).
</div>

Because the map is invertible, the probability density of each generated configuration is known exactly:

$$
p_X(\mathbf x)=p_Z\big(f_\theta^{-1}(\mathbf x)\big)\,\left|\det\frac{\partial f_\theta^{-1}}{\partial\mathbf x}\right| .
$$

<div class="legend" markdown="1">
- $p_X(\mathbf x)$: the probability density with which the generator produces the configuration $\mathbf x$.
- $p_Z$: the probability density of the Gaussian variable, a known formula.
- $f_\theta^{-1}$: the inverse of the network, which takes a configuration back to the Gaussian numbers $\mathbf z$ that produce it. The $-1$ means "inverse function", not "one over".
- $\partial f_\theta^{-1}/\partial\mathbf x$: the table of all partial derivatives of the components of $\mathbf z=f_\theta^{-1}(\mathbf x)$ with respect to the components of $\mathbf x$, the Jacobian matrix.
- $\det$: the determinant of that table, the factor by which the inverse map changes a small volume.
- The vertical bars: the absolute value.
</div>

This is the formula of the box with many variables. In words: the density of a generated configuration is the Gaussian density of the numbers it came from, corrected for how much the network stretched or compressed space on the way. Many generative models can produce samples but cannot say how probable each sample was. A normalising flow can, and the next step depends on it.

The generated distribution is only approximately Boltzmann, but since $p_X$ is known, each sample can be given the importance weight

$$
w(\mathbf x)\propto\frac{e^{-\beta U(\mathbf x)}}{p_X(\mathbf x)},
$$

and reweighted averages are then exact in principle, including free-energy differences between states that MD would rarely connect. In practice the weights are usable only when the model overlaps well with the target, the same overlap condition as in free-energy perturbation (Module 13).

<div class="legend" markdown="1">
- $w(\mathbf x)$: the **importance weight** of the generated configuration $\mathbf x$, a positive number.
- $\propto$: "proportional to". A common factor in all weights does not matter, because averages divide by the sum of the weights.
- $U(\mathbf x)$: the potential energy of the configuration, from the force field.
- $\beta=1/k_BT$: with $k_B$ the Boltzmann constant and $T$ the temperature. $k_BT=2.494$ kJ/mol at 300 K.
- $e^{-\beta U(\mathbf x)}$: the Boltzmann factor, proportional to the density that the configuration should have.
- $p_X(\mathbf x)$: the density that the generator gave it.
</div>

Read it like this: the weight is "how often this configuration should appear" divided by "how often the generator produces it". A configuration that the generator produces too often gets a small weight, and one that it produces too rarely gets a large weight. An average of any quantity $A$ over the Boltzmann distribution is then estimated from $n$ generated samples as a weighted mean:

$$
\langle A\rangle\approx\frac{\sum_{k=1}^{n}w(\mathbf x_k)\,A(\mathbf x_k)}{\sum_{k=1}^{n}w(\mathbf x_k)} .
$$

<div class="legend" markdown="1">
- $A$: any quantity that can be computed from a configuration, for example a distance.
- $\langle A\rangle$: its average over the Boltzmann distribution.
- $\mathbf x_k$: generated sample number $k$, with $k$ from 1 to $n$.
- Other symbols: as in the list above.
</div>

A small example. Three samples have $A=2$, 4 and 10 and weights 1, 1 and 8. The weighted mean is $(2+4+80)/10=8.6$, against a plain mean of 5.3.

The example also shows the limit. The third sample carries 80 per cent of the total weight, so the estimate rests almost entirely on one configuration. This is poor **overlap**: the generator rarely produces the configurations that matter most, a few samples get huge weights, and the statistical error is large. Free-energy perturbation fails in the same way when the two states are too different (Module 13).

"Exact in principle" therefore means: with infinitely many samples the weighted average converges to the true Boltzmann average, whatever the imperfections of the generator, as long as it can produce every relevant configuration. A free-energy difference between two states A and B follows from the total weights of the samples that fall in each state, $F_B-F_A=-k_BT\ln(W_B/W_A)$, where $W_A$ and $W_B$ are those two sums of weights. MD would need to cross the barrier between the states many times to give the same number.

### Diffusion and flow-matching emulators

<div data-videos="LStKhWcL0VE zaZAAWUISGE oZZumtlUXag"></div>

The models of this section give up the reweighting: they have no energy function to reweight to, and usually no cheap exact density. In exchange they are trained on data from many proteins at once and can be applied to a new sequence. Two words first.

A **diffusion model** learns to remove noise. For training, real structures are blurred by adding random displacements to their coordinates in many small steps, until nothing but noise is left. A network is trained to undo one such step. To generate a structure, start from pure noise and apply the network step by step, and a structure emerges.

A **flow-matching model** reaches the same goal by another route. The network learns a velocity for every point in the space of coordinates, such that points which start out distributed as noise are carried into the distribution of the data. Generating a sample means following these velocities, which is the numerical solution of a differential equation ([toolbox](maths.html#ode)).

In both, the steps belong to the generation procedure. They are not time steps of the motion of the molecule.

A newer family trains a diffusion or flow-matching model to output protein conformations for a given sequence, as structure-prediction networks output one structure. Training data are structures from the PDB and predicted-structure databases, large collections of MD trajectories, and in some cases experimental stabilities used to adjust the relative weights of folded and unfolded states. **BioEmu** ([Lewis et al. 2025](cite:lewis2025)) is a prominent example, and AlphaFlow and Distributional Graphormer are related systems. They generate thousands of statistically independent conformations in about a GPU-hour (the figure the BioEmu authors give), far less than the MD needed to sample the same ensemble.

Some terms in this paragraph:

- **For a given sequence**: the amino-acid sequence is the input, so one trained model serves many proteins. The Boltzmann generator described above is trained for one system with one energy function $U$.
- **The PDB** is the Protein Data Bank, the public archive of experimentally determined structures. Predicted-structure databases hold structures computed by structure-prediction networks.
- **Experimental stabilities** are measured free energies of folding, $\Delta G$: the free energy of the folded state minus that of the unfolded state. They fix the ratio of folded to unfolded molecules at equilibrium, which is $e^{-\Delta G/k_BT}$ ([primer](physics.html#equilibrium)). For illustration, $\Delta G=-10$ kJ/mol at 300 K, where $k_BT=2.494$ kJ/mol, gives a ratio of $e^{4.0}\approx55$, that is, 98 per cent folded. A model that produced half of its samples unfolded for such a protein would have the weights wrong.
- **A GPU-hour** is one graphics processor running for one hour.
- **Statistically independent**: every sample starts from fresh random numbers, so there is no correlation between one sample and the next. In MD, frames that are close in time are correlated and count as less than one sample each (Module 11).

What to keep in mind:

- They are **emulators**: the samples follow the distribution the model learned, with no exact reweighting to a physical energy function. Their errors are model errors of a new kind and must be measured against experiment or converged MD for the property you care about.
- They give **ensembles, not dynamics**: no time axis, so no rates or pathways.
- Most are trained on single chains under one set of conditions. Complexes, ligands, mutations far from the training distribution, pH and temperature dependence are active research questions, and performance there has to be tested, not assumed.

The word **emulator** is chosen with care. An emulator imitates the output of a simulation without carrying it out. Its samples follow whatever distribution the network has learned from its training data. If that distribution is wrong for your protein, there is no formula like the importance weight above to repair it, because there is no energy function that the samples are supposed to follow and usually no cheap exact density $p_X$ to divide by. The only check is comparison with experiment or with converged MD.

"No time axis" follows from how the samples are made. Each one is generated separately from noise, so nothing says which conformation comes before which. Populations of states can be read off such an ensemble. Rates and pathways cannot (Module 16).

### Other uses

Learned collective variables for enhanced sampling (Module 14), VAMPnets for kinetic models (Module 16), differentiable simulation engines that allow force-field parameters to be optimised through the trajectory, and surrogate models that predict the outcome of a free-energy calculation.

One paragraph on the idea of each.

**Learned collective variables.** A collective variable (CV) is a function of the atomic coordinates that reduces a configuration to one or a few numbers, chosen to follow the slow process of interest: a distance, an angle, a number of contacts. The enhanced-sampling methods of Module 14 push the system along a CV, and they work only if the CV captures the slow motion. Choosing it by intuition is the hard part. A learned CV is a network that takes many simple inputs, such as a few hundred distances, and outputs one or two numbers. It is trained on existing simulation data so that its output separates the known states, or so that it changes as slowly as possible in time.

**VAMPnets.** Module 16 built kinetic models (Markov state models) with a pipeline whose first three steps are set up by hand: convert each frame into features, reduce their number, and cluster the frames into states. It also introduced a score, VAMP, that measures how well a choice of features and states captures the slow dynamics. A VAMPnet is a network that takes a frame and returns its state, trained to make that score as high as possible. It merges the three steps into one trained function.

**Differentiable simulation.** If the MD program itself is written in a library with automatic differentiation, a result of the simulation can be differentiated with respect to the force-field parameters. Gradient descent can then adjust the parameters so that a simulated quantity matches a target, in the way training adjusts the weights of a network. This is what "optimised through the trajectory" means. The chaos of Module 2 is the difficulty: a trajectory depends extremely sensitively on everything, and so does its derivative.

**Surrogate models.** A surrogate is a model trained on the results of many finished calculations to predict the result of a new one without running it. For example, the inputs are a protein and a ligand, and the output is the binding free energy that a full alchemical calculation (Module 13) would have given. A surrogate is fast. It inherits the errors of the calculations it was trained on and adds its own, and it is reliable only for systems like those in its training set.

## How to evaluate any of these tools

Every tool of this module is a fitted function, and the same few questions decide whether its output can be trusted. None of them is specific to machine learning.

The standards of the rest of this course apply unchanged:

1. **What is the reference?** A learned potential is at best as good as its training data: the quantum method for an MLIP, the atomistic force field for a learned coarse-grained model, the trajectory set for an emulator.
2. **Is the test out of distribution?** Performance on molecules or proteins similar to the training set says little about new ones.
3. **Are the statistics sound?** Independent repeats, uncertainty estimates, convergence (Module 11).
4. **Does it reproduce an observable, not just a loss value?** Densities, radial distribution functions, free-energy differences, experimental data.
5. **What is the cost, counted honestly**, including training and data generation?

On question 2: "out of distribution" was defined in the section on tools. For a learned potential it means molecules, phases or conditions that are not in the training set. For a learned coarse-grained model it means other sequences or another temperature. For an emulator it means proteins unlike those it was trained on.

On question 4: the **loss** is the quantity that training made small, so a small loss shows only that training worked. An **observable** is a quantity that can be compared with a measurement or with an independent calculation, such as those in the list. A radial distribution function is the histogram of the distances between pairs of atoms, divided by what a uniform fluid would give (Module 11).

On question 5: a learned model that runs, say, 1,000 times faster than the method it replaces has saved nothing if producing its training data took longer than the direct calculation would have.

## Check yourself

<details markdown="1"><summary>1. Why are forces obtained as the gradient of a learned energy instead of being predicted directly by the network?</summary>
A force field that is the gradient of a scalar energy is conservative: the work around any closed path is zero and energy is conserved in MD. Directly predicted forces are generally not the gradient of any function, and simulations with them gain or lose energy. (Some recent models do predict forces directly for speed and accept this.)
</details>

<details markdown="1"><summary>2. A model reaches a very low force error on its test set but the MD simulation explodes after 50 ps. How can both be true?</summary>
The test set comes from the same distribution as the training set. During MD the system drifted into configurations outside it (a slightly compressed bond, an unusual contact), where the model extrapolates without constraint. Test error measures interpolation. Stability requires coverage, which active learning supplies.
</details>

<details markdown="1"><summary>3. What makes a Boltzmann generator "exact" where a diffusion-based emulator is not?</summary>
The Boltzmann generator provides the probability density of every sample it draws, and a physical energy function $U$ is available, so each sample can be reweighted by $e^{-\beta U}/p_X$. An emulator trained on data has no target energy function to reweight against and, depending on the model type, no cheap exact density.
</details>

<details markdown="1"><summary>4. Why is the training signal in force-matching coarse-graining so noisy?</summary>
For a fixed coarse-grained configuration $\mathbf R$, many atomistic configurations (different solvent positions, side-chain orientations) map to it, each with a different instantaneous force. The target is their average, the mean force, but each training example supplies one instantaneous value that scatters around the mean force. This scatter is an irreducible noise term: the loss never reaches zero, and a lot of data is needed to average it out.
</details>

<details markdown="1"><summary>5. A neuron has the inputs $x_1=1$ and $x_2=2$, the weights $w_1=0.5$ and $w_2=-0.25$, the bias $b=0.5$ and the activation $\tanh$. What is its output?</summary>
The weighted sum is $0.5\times1+(-0.25)\times2+0.5=0.5$. The output is $\tanh(0.5)=0.46$.
</details>

<details markdown="1"><summary>6. Which of these are invariant and which are equivariant when a molecule is rotated: the distance between two atoms, the energy, the force on one atom, the dipole moment, the angle between two bonds?</summary>
Invariant: the distance, the energy and the angle. They are single numbers that do not depend on how the molecule is oriented. Equivariant: the force and the dipole moment. They are vectors that turn with the molecule.
</details>

<details markdown="1"><summary>7. A message-passing model uses $T=3$ rounds and a cutoff $r_c=0.5$ nm. Two molecules float in vacuum with 1.2 nm between their closest atoms. Does the model describe their interaction?</summary>
No. The product $T\times r_c=1.5$ nm is larger than 1.2 nm, but messages travel only along edges, and an edge joins two atoms closer than 0.5 nm. No edge crosses the gap, so no information passes and the predicted energy is the sum of the energies of the two separate molecules. An explicit long-range term is needed.
</details>

## Exercises

1. Fit a small neural network to the energy of a one-dimensional double well from 20 samples. Compare the predicted forces from differentiating the network with the exact ones, inside and outside the range of the training data.
2. Using a pretrained general-purpose potential available in OpenMM-ML, run a short gas-phase simulation of a small neutral molecule made of elements the model supports, and compare the distribution of one dihedral angle with the same simulation using GAFF2 or OpenFF.
3. For a one-dimensional double well, train a model on samples from overdamped Langevin dynamics by force matching with added noise on the forces. How does the error in the learned free energy scale with the number of samples?
4. Generate an ensemble for a small protein with an ensemble emulator and for the same protein with MD. Compare per-residue RMSF, radius of gyration and secondary-structure content, with error bars on the MD values. Where do they disagree, and which do you believe?

## Read

{{READ}}

## Key papers

{{PAPERS}}
