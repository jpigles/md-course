---
title: Formula sheet
short: Formula sheet
summary: The equations of the course on one page, with the module where each is derived.
---

## Constants and conversions

| Quantity | Value |
|---|---|
| $k_B$ | 0.0083145 kJ mol$^{-1}$ K$^{-1}$ = 0.0019872 kcal mol$^{-1}$ K$^{-1}$ |
| $k_BT$ at 300 K | 2.494 kJ/mol = 0.596 kcal/mol |
| $RT\ln10$ at 298 K | 5.71 kJ/mol = 1.36 kcal/mol |
| $1/(4\pi\varepsilon_0)$ | 138.935 kJ mol$^{-1}$ nm $e^{-2}$ |
| Standard volume $V^\circ=1/C^\circ$ | 1.661 nm$^3$ per molecule at 1 mol/L |
| Debye length in water at 25 °C | $0.304/\sqrt{I[\text{M}]}$ nm |
| Harmonic constant, AMBER/CHARMM to GROMACS | $k=2K$; kcal mol$^{-1}$ Å$^{-2}$ × 418.4 = kJ mol$^{-1}$ nm$^{-2}$ |

## Mechanics (Module 2)

$$
m_i\ddot{\mathbf r}_i=\mathbf F_i=-\nabla_iU\qquad
H=\sum_i\frac{\mathbf p_i^2}{2m_i}+U(\mathbf r)\qquad
\dot q=\frac{\partial H}{\partial p},\ \ \dot p=-\frac{\partial H}{\partial q}
$$

$$
\text{Pair force: }\mathbf F_i=-\frac{du}{dr}\frac{\mathbf r_{ij}}{r_{ij}}\qquad
\text{Liouville: }\nabla_\Gamma\cdot\dot\Gamma=0,\ \ \frac{\partial\rho}{\partial t}=-\{\rho,H\}
$$

## Statistical mechanics (Module 3)

$$
P(\Gamma)=\frac{e^{-\beta H(\Gamma)}}{Q}\qquad
Q=\frac{1}{N!\,\Lambda^{3N}}\int e^{-\beta U(\mathbf r)}d\mathbf r\qquad
A=-k_BT\ln Q
$$

$$
T_{inst}=\frac{2K}{N_{df}k_B}\qquad\frac{\sigma_T}{T}=\sqrt{\frac{2}{N_{df}}}\qquad
C_V=\frac{\langle\delta E^2\rangle}{k_BT^2}\qquad\langle\delta V^2\rangle=k_BT\,V\kappa_T
$$

$$
P=\frac{1}{3V}\Big\langle2K+\sum_{i<j}\mathbf r_{ij}\cdot\mathbf F_{ij}\Big\rangle\qquad
\frac{P_B}{P_A}=e^{-\beta\Delta A_{AB}}\qquad
W(\xi)=-k_BT\ln P(\xi)
$$

## Integrators (Module 4)

$$
\mathbf v\leftarrow\mathbf v+\tfrac{\Delta t}{2m}\mathbf F;\quad\mathbf r\leftarrow\mathbf r+\Delta t\,\mathbf v;\quad\mathbf F\leftarrow\mathbf F(\mathbf r);\quad\mathbf v\leftarrow\mathbf v+\tfrac{\Delta t}{2m}\mathbf F
$$

$$
e^{iL\Delta t}\approx e^{iL_p\Delta t/2}e^{iL_r\Delta t}e^{iL_p\Delta t/2}\qquad
\text{stability: }\omega\Delta t<2\qquad
\tilde H=H+O(\Delta t^2)
$$

## Force field (Modules 5 and 6)

$$
U=\sum_{b}\tfrac12k_b(r-r_0)^2+\sum_{a}\tfrac12k_\theta(\theta-\theta_0)^2+\sum_{d}\sum_nk_n[1+\cos(n\phi-\delta_n)]
+\sum_{i<j}\left\{4\varepsilon_{ij}\left[\left(\tfrac{\sigma_{ij}}{r}\right)^{12}-\left(\tfrac{\sigma_{ij}}{r}\right)^{6}\right]+\frac{q_iq_j}{4\pi\varepsilon_0r}\right\}
$$

$$
r_{min}=2^{1/6}\sigma\qquad
\text{Lorentz-Berthelot: }\sigma_{ij}=\tfrac12(\sigma_i+\sigma_j),\ \varepsilon_{ij}=\sqrt{\varepsilon_i\varepsilon_j}\qquad
\text{harmonic fluctuation: }\sqrt{k_BT/k}
$$

## Boundaries and electrostatics (Module 7)

$$
\Delta x\leftarrow\Delta x-L\,\mathrm{round}(\Delta x/L)\qquad r_c\le L/2\qquad
U_{tail}=\tfrac83\pi N\rho\varepsilon\sigma^3\left[\tfrac13\left(\tfrac{\sigma}{r_c}\right)^9-\left(\tfrac{\sigma}{r_c}\right)^3\right]
$$

$$
U_{Ewald}=\frac12\sum_{\mathbf n}{}^{'}\sum_{i,j}q_iq_j\frac{\mathrm{erfc}(\alpha r)}{r}+\frac{2\pi}{V}\sum_{\mathbf k\ne0}\frac{e^{-k^2/4\alpha^2}}{k^2}|S(\mathbf k)|^2-\frac{\alpha}{\sqrt\pi}\sum_iq_i^2,\qquad S(\mathbf k)=\sum_jq_je^{i\mathbf k\cdot\mathbf r_j}
$$

## Thermostats and barostats (Module 8)

$$
\text{Berendsen: }\lambda^2=1+\frac{\Delta t}{\tau_T}\left(\frac{T_0}{T}-1\right)\qquad
\text{Langevin: }m\dot{\mathbf v}=\mathbf F-\gamma m\mathbf v+\sqrt{2\gamma mk_BT}\,\boldsymbol\eta
$$

$$
\text{O step: }\mathbf v\leftarrow e^{-\gamma\Delta t}\mathbf v+\sqrt{\tfrac{k_BT}{m}(1-e^{-2\gamma\Delta t})}\,\boldsymbol\xi\qquad
\text{Brownian: }d\mathbf r=\frac{D}{k_BT}\mathbf F\,dt+\sqrt{2D\,dt}\,\boldsymbol\xi
$$

$$
\text{Nosé-Hoover: }\dot{\mathbf p}_i=\mathbf F_i-\xi\mathbf p_i,\ \ \dot\xi=\frac1Q\Big(\sum_i\frac{\mathbf p_i^2}{m_i}-N_{df}k_BT_0\Big)
$$

$$
\text{Monte Carlo barostat: }P_{acc}=\min\{1,\exp[-\beta(\Delta U+P_0\Delta V)+N\ln(V'/V)]\}
$$

## Constraints (Module 9)

$$
\sigma_k=|\mathbf r_{ij}|^2-d_k^2=0\qquad m_i\ddot{\mathbf r}_i=\mathbf F_i-\sum_k\lambda_k\nabla_i\sigma_k\qquad
g\approx\frac{|\mathbf s'|^2-d^2}{2(m_i^{-1}+m_j^{-1})\,\mathbf s\cdot\mathbf s'}\qquad N_{df}=3N-N_c-3
$$

## Analysis and errors (Module 11)

$$
g(r)=\frac{\langle n(r,r+dr)\rangle}{4\pi r^2dr\,\rho}\qquad\mathrm{MSD}(t)\to6Dt\qquad
D_\infty=D_{PBC}+\frac{2.837\,k_BT}{6\pi\eta L}
$$

$$
g_{stat}=1+\frac{2\tau_{int}}{\Delta t_s}\qquad N_{eff}=\frac{N}{g_{stat}}\qquad\mathrm{SE}=\frac{\sigma}{\sqrt{N_{eff}}}\approx\sigma\sqrt{\frac{2\tau_{int}}{T_{sim}}}
$$

## Free energy (Modules 12 and 13)

$$
W(\xi)=-k_BT\ln P_i^b(\xi)-w_i(\xi)+F_i\qquad
\text{WHAM: }P(\xi)=\frac{\sum_in_i(\xi)}{\sum_iN_ie^{-\beta[w_i(\xi)-F_i]}},\ \ e^{-\beta F_i}=\sum_\xi P(\xi)e^{-\beta w_i(\xi)}
$$

$$
\text{MBAR: }f_i=-\ln\sum_{n}\frac{e^{-u_i(\mathbf x_n)}}{\sum_kN_ke^{f_k-u_k(\mathbf x_n)}}\qquad
\text{window width: }\sqrt{k_BT/k}
$$

$$
K_a=4\pi\int_{bound}r^2e^{-\beta W(r)}dr\qquad\Delta G^\circ=-k_BT\ln(K_aC^\circ)\qquad K_d=1/K_a
$$

$$
\text{FEP: }\Delta A=-k_BT\ln\langle e^{-\beta\Delta U}\rangle_A\qquad
\text{TI: }\Delta A=\int_0^1\Big\langle\frac{\partial U}{\partial\lambda}\Big\rangle_\lambda d\lambda\qquad
\text{BAR: }\sum_{A}\frac{1}{1+e^{\beta(\Delta U-\Delta A)}}=\sum_{B}\frac{1}{1+e^{-\beta(\Delta U-\Delta A)}}
$$

$$
\text{Jarzynski: }\langle e^{-\beta W}\rangle=e^{-\beta\Delta A}\qquad\text{Crooks: }\frac{P_F(W)}{P_R(-W)}=e^{\beta(W-\Delta A)}\qquad
\Delta\Delta G_{bind}=\Delta G_{complex}^{A\to B}-\Delta G_{free}^{A\to B}
$$

## Enhanced sampling (Module 14)

$$
\text{Replica exchange: }P_{acc}=\min\{1,\exp[(\beta_i-\beta_j)(U_i-U_j)]\}\qquad M\propto\sqrt{N_{df}}
$$

$$
\text{Well-tempered metadynamics: }w=w_0e^{-V(s,t)/k_B\Delta T},\ \ F(s)=-\frac{\gamma}{\gamma-1}V(s),\ \ \gamma=\frac{T+\Delta T}{T}
$$

## Coarse-graining (Module 15)

$$
U_{CG}(\mathbf R)=-k_BT\ln\int d\mathbf r\,\delta(\mathbf M(\mathbf r)-\mathbf R)e^{-\beta u(\mathbf r)}\qquad
\text{Gō contact: }\varepsilon\left[5\left(\tfrac{\sigma_{ij}}{r}\right)^{12}-6\left(\tfrac{\sigma_{ij}}{r}\right)^{10}\right]
$$

$$
U_{DH}=\frac{q_iq_j}{4\pi\varepsilon_0\varepsilon_rr}e^{-r/\lambda_D}\qquad
\Delta G_{GB}=-\frac{1}{8\pi\varepsilon_0}\left(\frac{1}{\varepsilon_{in}}-\frac{1}{\varepsilon_{out}}\right)\sum_{i,j}\frac{q_iq_j}{\sqrt{r_{ij}^2+R_iR_je^{-r_{ij}^2/4R_iR_j}}}
$$

## Kinetics (Module 16)

$$
K_d=\frac{k_{off}}{k_{on}}\qquad k_{TST}=\frac{\omega_0}{2\pi}e^{-\beta\Delta W^\ddagger}\qquad
k_{Kramers}=\frac{\omega_0\omega_b}{2\pi\gamma}e^{-\beta\Delta W^\ddagger}
$$

$$
\hat T_{ij}(\tau)=\frac{C_{ij}}{\sum_kC_{ik}}\qquad t_i=-\frac{\tau}{\ln\lambda_i(\tau)}\qquad\mathbf T(k\tau)\approx\mathbf T(\tau)^k\qquad
\mathbf C(\tau)\mathbf v=\lambda\,\mathbf C(0)\mathbf v
$$

## Machine learning (Module 17)

$$
E=\sum_iE_i(\text{environment within }r_c),\ \ \mathbf F_i=-\frac{\partial E}{\partial\mathbf r_i}\qquad
\mathcal L=w_E\sum(E_\theta-E_{QM})^2+w_F\sum|\mathbf F_\theta-\mathbf F_{QM}|^2\qquad
w(\mathbf x)\propto\frac{e^{-\beta U(\mathbf x)}}{p_X(\mathbf x)}
$$
