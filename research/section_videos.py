#!/usr/bin/env python3
"""Attach specific lectures to specific sections of the modules.

Each entry maps a section heading to YouTube video ids. Every id must be in the verified registry
(a catalogued video, or a lecture listed inside a catalogued playlist): the site builder refuses anything else.
The choice of lecture for each section was made from the lecture's own title and description as read
from YouTube (research/video_meta.json, research/lecture_meta.json), not from memory.

Re-runnable: an existing tag under a heading is replaced.
"""
import os, re, sys
here = os.path.dirname(os.path.abspath(__file__)); mods = os.path.join(os.path.dirname(here), "src", "modules")

MAP = {
"01-what-is-md.md": {
    "## The idea in one paragraph": "dEmAnuO8RhQ GcGClviieOU",
    "## The algorithm": "IlwC3PSyZ0Q QiZk_uT-40E AtExb5EprvE NItXk8epkNM",
    "### The same thing in 35 lines of Python": "kvJ1siWcBfM",
    "## Which physics is kept, and which is dropped": "4uloreO4qHA qnDkRUaz57g",
    "## Time and length scales": "_TiQYNWJwYg",
    "## A short history": "PGqCeSjNuTY eNuV8pYd-is SgH_GcFhQf8",
},
"02-classical-mechanics.md": {
    "## Newton's formulation": "H0BCYDXEDco 031AX4AsueA",
    "## Lagrange's formulation": "OpqJjKDPJBA 3apIZCpmdls",
    "## Hamilton's formulation": "61CWqyocuOM hk4fOXsSJzM",
    "### Phase space": "IVQRfHAgLxk yV25sV3rAlo",
    "### Time evolution of any observable": "5OZO5GPuSJY",
    "## Conservation laws": "HLr5ZeQUrBk PuDproV-17s",
    "## Liouville's theorem": "MFqA1nePCNg ddKRdrf9iqI XiFEXVWNlpg 8w4az6IQsNc",
},
"03-statistical-mechanics.md": {
    "## Microstates, macrostates, ensembles": "lKyrJhN8MFY tcTmOEk8cc4 lLhUpB6oOr8 5LALoxDs0ic HDl63ZSFVwM",
    "## Where the Boltzmann factor comes from": "_6AFgt2gkr0 tDKjLzbXYQI aFEovHmSvQk J-qTchJh4Ok",
    "### The classical partition function": "UxJCRnNJCPw 34OuWjAwI8w RT_v0PhXP5E",
    "## From the partition function to thermodynamics": "_ErxZOHwtaA AhNHsYpemII",
    "## Equipartition and temperature": "KthbNCxnj2g b8n1k3Iob0Q uoieTQ3Qb3M",
    "## Why a time average equals an ensemble average": "rBni87N8cBs WneHzwWh0Ws Iq9ZxMRbpmc",
    "## Free energy": "3XyGqsgBpIM Lq8GwTlJ9Z8 BznPadIkfKM mg9JWntdfyE",
    "### The potential of mean force": "pjT7waGUGDI",
    "### Binding constants": "Srj-ZqBzNv4",
},
"04-integrators.md": {
    "## Verlet from Taylor series": "g55QvpAev0I qT8pxV53FA4 ld5VABtBkF0",
    "### Velocity Verlet": "ii-N61PeeQU 1kER3-3x8VI",
    "### Leap-frog": "pVudb6-_FaM",
    "## Velocity Verlet from the Liouville operator": "5OZO5GPuSJY Uyg9asVcMOc",
    "## Why not a higher-order method?": "zLnIWwvfuo4",
    "## Multiple time steps": "CRbC_-iGnZM",
},
"05-force-field-form.md": {
    "## The functional form": "OBg5wtvNuv4 1oQlCIUm0Bo 8oZSa0zlnIc vpqo0q3zvJU MK5BrpgUMUM",
    "## Bond stretching": "7yEGYWIqSdU",
    "## Angle bending": "baRZYahRmSc",
    "## Torsions (proper dihedrals)": "H-NiSB-2bmo KmuYjxL0Kfw fst8oSeAQ98",
    "## Lennard-Jones: repulsion and dispersion": "D3kHLAj8ozI EuwL12-5pXY keXmqiGN1Qc zNiUrSxZdsQ",
    "## Electrostatics": "_CElNDa1hoI ZdZXckzHktM 5z8IWRDqgy8",
    "## From energy to force": "BnT6Onll1eQ",
    "## What this model leaves out": "nO4c0CfZx3k",
},
"06-force-field-parameters.md": {
    "## Parameterisation is a fitting problem": "1yAba9WBSS4 QCE6eyHWx6Y -EVNaaA6hYk gP6HfBQ_LkI",
    "## The protein force-field families": "kglSEWaMGyU OrfOZ1wmElo Ck7EMuIStpM",
    "## Water models": "6RzCFya08iE",
    "## The disordered-protein problem": "jFmGNUUVHzg _6iAcwmknek",
    "## Beyond fixed charges: polarizable force fields": "Y2ixvZBrM8Q I2zm3hAO-eI",
    "## What a topology file contains": "uLlWNqoPNA0",
},
"07-boundaries-electrostatics.md": {
    "## Periodic boundary conditions": "gVVqjmTAJGI x20QP1x3U7c J3aB9xp1YIE Wbzopzywt-Q IpdTtx98AWQ",
    "### The minimum-image convention": "pzM7ju9DNtM AbidqaoH7Wo",
    "## Cutting off short-range interactions": "JQPHMpR37Co y-jUCgk4rCI hi7gvv-I-0o",
    "### Neighbour lists": "OURKkL8XqDo",
    "## Ewald summation": "SSmIMof0KvA DnOTgjUZxbE YPryFf7MQTg",
    "### Particle-mesh Ewald": "VWsMUaA7UWw",
},
"08-thermostats-barostats.md": {
    "## Why control temperature at all": "5LALoxDs0ic",
    "## Thermostats": "l-uZaSvlycY ey1tv0yoyGc HiZ7gvtmDbk pCm2i6kQs4E X3K5A96-U4E",
    "### Langevin dynamics": "AzCzDYLimvc jonJHFcYTso",
    "## Barostats": "rGOyUWV0fX0",
},
"09-constraints.md": {
    "## Constrained equations of motion": "N2Lf-U8aIgM -6QUI57indo",
    "## SHAKE": "9Vj7h1TJePw --zH0AJjVqk _zwgPkBeO_I",
    "## SETTLE": "fueOYcMgFfQ",
},
"10-running-a-simulation.md": {
    "## The workflow at a glance": "EFtbEkuJ9tk ZKNUR5Uz2r0 HPk5SiEqFIM",
    "## Step 1: the starting structure": "YQ8eRyScuyk RvvSvC8YyVo",
    "## Steps 2 to 4: topology, box, water, ions": "8oGZn1NdvbY Kbq6Gf9m2T8 GRH81ABCq54",
    "## Step 5: energy minimisation": "OCcxxddYrDg WvkSCxLqkxY AyFXfAhwVBQ",
    "## Steps 6 and 7: equilibration": "WU_8wdSSZC8 3T5-m-FNR8Y",
    "## Step 8: production, an annotated input file": "P9pyJmbK3tM xS4r2bLATvo IArpsQsZ95U",
    "### The same workflow in OpenMM": "hbQ_dfgWPc8 AlWsbbdUNC0 yLnjbjtRgdg 71snkHHku1c",
    "## Planning: length, repeats, output, cost": "EsKsPEdYksE F-SsbOw2YrM",
},
"11-analysis-statistics.md": {
    "## Structural observables": "whO1h7rAMSs 42-bolWBrBM UvH-h9i03rM",
    "### Radial distribution function": "FqqPhoyRCCM X0vdXv7aTvk",
    "## Dynamical observables": "3b6ZM21PmPU rWoV7HoufdA Mm1WfLi86-0 nuAs_GlCdDU",
    "## Statistical error: the part most often done wrong": "e3Ygft3fjRg 8Y9dgl6jsBo",
    "### Block averaging": "BACN9Ydiw5I 0KqCK0yG9T0",
    "## Collective motions: principal component analysis": "qcfV1z_UZLE 0pK0EWyinVo",
    "## Free-energy surfaces from histograms": "yt6-v3jZals",
    "## Comparing with experiment": "TlKg7luoRmY a15IlXIhz1k",
    "## Tools": "_v3WU0RAfRM Tso29WxWWHg x39p_SrJLY4 8ZhNuhBXB0o p3OUUnHXQjU",
},
"12-free-energy-pmf.md": {
    "## The potential of mean force, again": "pjT7waGUGDI LCKtsR1ijsA",
    "## Umbrella sampling": "1tMd68ankiA LVxFGBxgrLo c-dKO66Sx9A",
    "## WHAM: joining the windows optimally": "V1RCMp4wM2k",
    "## MBAR: the binless limit": "5tKnjRdVz3E fhMjOYvnGcY",
    "## Designing an umbrella sampling calculation": "J7F2aguxTXs A3SxYkoKlnM dvo6noErrbc",
    "## From a PMF to a binding constant": "z2C6siB6Qqo iLw7acCoCrs",
},
"13-alchemical-free-energy.md": {
    "## The idea": "ypg1doAqVPM ov0mMvR3wrM a2axeq_E3RQ",
    "## Free-energy perturbation": "D_We9YYxpkM bMvzvlqVqzU",
    "## Thermodynamic integration": "iCzHM5Lb_m8",
    "### Relative binding free energy": "iweSKUD2YBI WhUEc5YMT2Q HSh4AzzhGKM",
    "### Absolute binding free energy": "LPYzLZ1WmG4",
    "## Non-equilibrium work relations": "nI3pHiPbxeg NeGjghk0im4 LXcQx6Bu3OQ gsq3irAz8Ok",
    "## End-point methods": "Hy-Cc7nn2MY",
    "## Good practice": "cQQM1DTLR5g id5D_9PC1mA fxPNNVkSIWo",
},
"14-enhanced-sampling.md": {
    "## The problem in one formula": "PkTCrc0P_Xs 9JiorFETCTo EwGZ39PS1qk",
    "## Collective variables": "TYz9W8d54zM",
    "## Replica exchange (parallel tempering)": "qITm4laxhtk ktkmgiFJSGQ 5upvgbp_elI 5w6rRqq2Dhg",
    "## Metadynamics": "QP5F83g1G0E b8aViZKaKFs bZZggbV2r5E BYvsNThvXlk",
    "## Steered MD": "RJMQ70K8UmA",
    "## Accelerated MD": "cc_5q6Od6XU f4faPQU58oA",
    "## Weighted ensemble": "EMZu-n4WCH0 ShtrAD-tT7c ziRedoLEb2o",
    "## Choosing": "st5XKYuJHQE",
},
"15-coarse-grained.md": {
    "## Why coarse-grain": "yBnn567JXdo 0XZ8tAwNHdE 0NJxWb-sXg8",
    "## Martini": "Yq1f8vDfPe4 EVcw-w-Lcnk",
    "## Structure-based (Gō) models": "tRVeUbgcGVY AsKi8lXJWyM",
    "## Residue-level models for disordered proteins and condensates": "jFmGNUUVHzg _6iAcwmknek",
    "## Implicit solvent": "2yf__V4EhGI AzCzDYLimvc",
},
"16-kinetics-msm.md": {
    "## Thermodynamics is not kinetics": "rFavri_VYfk balC-1gTQro",
    "## Transition state theory": "c-dKO66Sx9A",
    "## The committor and what makes a good reaction coordinate": "ziRedoLEb2o",
    "## Markov state models": "xNjQatR2rRU 0pB3pUXULmo YXppP_QTut8",
    "### The model": "kKC4ccoUHGU gSR2xp2NFIc",
    "### Estimation": "pVl7TPFuHwk",
    "### What the eigenvalues mean": "opx_wViFlTs",
    "### The pipeline": "A3AUWXqqONc QHQBVmVq-Vo u4ec4EYsgkQ jXMaCSSOSgg CNYreswqJAQ",
    "### Validation": "aO_DmbqHWYs",
    "### Sampling for a Markov model": "B8uo60u9TqI Fuai8_MSxaw HfTdS-kgG70",
},
"17-machine-learning.md": {
    "## The learning problem": "tWeBrPTrSDE 8DPSLDUsqbA",
    "### Equivariant networks": "ZR1NTBPBDOo I9Y2le9e74A",
    "## Training": "106sdeDF1oc",
    "### Boltzmann generators": "WuXJRswYIaA JZjeFBH0Jl4",
    "### Diffusion and flow-matching emulators": "LStKhWcL0VE zaZAAWUISGE oZZumtlUXag",
},
}
# extra placements added after the lecture descriptions were read (research/lecture_meta.json)
extra = os.path.join(here, "section_videos_extra.json")
if os.path.exists(extra):
    import json
    for fn, d in json.load(open(extra, encoding="utf-8")).items():
        for h, ids in d.items():
            MAP.setdefault(fn, {})[h] = (MAP.get(fn, {}).get(h, "") + " " + ids).strip()

n = 0
for fn, d in MAP.items():
    p = os.path.join(mods, fn); lines = open(p, encoding="utf-8").read().split("\n")
    for head, ids in d.items():
        idx = [i for i, l in enumerate(lines) if l.strip() == head]
        if len(idx) != 1:
            print("heading not found exactly once in", fn, ":", head, idx); sys.exit(1)
        i = idx[0]
        ids = " ".join(dict.fromkeys(ids.split()))             # drop duplicates, keep order
        tag = f'<div data-videos="{ids}"></div>'
        j = i + 1
        while j < len(lines) and lines[j].strip() == "":
            j += 1
        if j < len(lines) and lines[j].startswith('<div data-videos="'):
            lines[j] = tag
        else:
            lines[i + 1:i + 1] = ["", tag]
        n += len(ids.split())
    open(p, "w", encoding="utf-8", newline="\n").write("\n".join(lines))
print("placed", n, "lecture links in", sum(len(d) for d in MAP.values()), "sections of", len(MAP), "modules")
