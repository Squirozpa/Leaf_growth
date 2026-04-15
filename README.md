# Leaf Growth Model: Carbon Assimilation and Nitrogen Modulation

Sebastián Quiroz — February 2026

Simulation of *Arabidopsis thaliana* Col-0 leaf growth based on carbon assimilation and nitrogen modulation, as described in `Leaf_Growth_Model_Proposal_10_4.pdf`.

---

## Usage

**Run a simulation:**
```bash
python main.py [params.json] [output.csv]
```
Defaults to `params/default.json` and `results.csv`.

Set `"nitrogen": -1` in the params file to run the carbon-only model.  
Set `"nitrogen"` to any `[N_soil]` value (µmol g⁻¹) to run the nitrogen-modulated model.

**Visualize results:**
```bash
python visualize/leaf_area.py results.csv [data/Data\ Sheet\ 2\ model.csv]
python visualize/rgr.py       results.csv [data/Data\ Sheet\ 2\ model.csv]
python visualize/allometry.py
```

---

## File Structure

```
main.py
visualize/
    leaf_area.py          Leaf area over time vs measured data
    rgr.py                RGR of leaf area and total weight over time
    allometry.py          Fitted allometric relationships (LMA, R_root, R_shoot, k)
params/
    default.json          Default parameters (Arabidopsis thaliana Col-0)
data/
    Data Sheet 2 model.csv   Weraduwage et al. (2014) reference data
src/
    functions/
        carbon/
            effective_area.py   A_eff(LA)             — eq. 3
            balance.py          C_in, C_out, C_available — eqs. 1–2, 4–6
        nitrogen/
            michaelis_menten.py michaelis_menten()    — used for SNAR_adj (eq. 10)
            photosynthesis.py   f_r_ph()              — N-dependent r_ph (sec. 3.2)
            leaf_root_ratio.py  L_R_opt, L_R_adj      — L:R adjustment (sec. 3.2)
        allometry/
            lma.py              LMA(day)              — leaf mass per area (fig. 3)
            root_mass.py        R_root(LW)            — root-to-leaf ratio (eq. 9)
            shoot_mass.py       R_shoot(LW)           — shoot-to-leaf ratio (eq. 9)
            partition.py        k_weight(t), k_area(t) — allocation coefficients (eqs. 7–8)
        growth/
            carbon_growth.py    growth_carbon()       — Euler step, carbon model
            nitrogen_growth.py  growth_nitrogen()     — Euler step, N-modulated model
    utils/
        config.py               Config dataclasses + Config.from_json()
        simulation.py           run_simulation(config)
        output.py               save_results() — write CSV
```

---

## Parameters (`params/default.json`)

All parameter names match the notation in the paper.

### `simulation`
| Key | Description | Default | Units |
|---|---|---|---|
| `dt` | Time step | 1/24 | days |
| `total_time` | Simulation end | 89 | days after sowing |
| `start_time` | Simulation start | 5 | days after sowing |
| `starting_leaf_area` | Initial LA | 0.05 | cm² |
| `nitrogen` | Soil [N_soil] (-1 = carbon-only) | -1 | µmol g⁻¹ |

### `physiology`
| Key | Description | Default | Units |
|---|---|---|---|
| `PR_base` | Base photosynthetic rate | 42 | µmol cm⁻² d⁻¹ |
| `p` | Photoperiod fraction | 0.5 | — |
| `r_leaf` | Leaf maintenance respiration rate | 12.024 | µmol g⁻¹ d⁻¹ |
| `r_root` | Root maintenance respiration rate | 1682.4 | µmol g⁻¹ d⁻¹ |
| `r_shoot` | Shoot maintenance respiration rate | 604.8 | µmol g⁻¹ d⁻¹ |
| `f_N_leaf` | Nitrogen fraction allocated to leaf | 0.21 | — |
| `beta` | Growth respiration coefficient | 8660 | µmol g⁻¹ |
| `rho` | Tissue carbon concentration | 37500 | µmol g⁻¹ |

### `nitrogen`
| Key | Description | Default | Units |
|---|---|---|---|
| `SNAR_max` | Max nitrogen absorption rate | 3360 | µmol g⁻¹ d⁻¹ |
| `K_m` | Michaelis-Menten half-saturation constant | 400 | µmol g⁻¹ |

### `photosynthesis`
| Key | Description | Default | Units |
|---|---|---|---|
| `a_PR` | Max photosynthetic rate (N-response) | 55.5 | µmol cm⁻² d⁻¹ |
| `b_PR` | Curvature of N-response | 2.7 | — |
| `N_max` | Optimal relative leaf nitrogen | 0.9 | — |

### `light`
| Key | Description | Default | Units |
|---|---|---|---|
| `max_irradiance_area` | Full-irradiance threshold | 50 | cm² |
| `partial_shade_band_width` | Partial-shade band width | 50 | cm² |

### `leaf_root_ratio`
| Key | Description | Default | Units |
|---|---|---|---|
| `LR_0` | Base leaf-to-root ratio | 1.9 | — |
| `a_LR` | L:R saturation amplitude | 12.5 | — |
| `b_LR` | L:R half-saturation constant | 1900 | µmol g⁻¹ d⁻¹ |
| `adjustment_factor` | Midpoint adjustment weight | 0.5 | — |

---

## Output CSV

Columns: `time, leaf_weight, leaf_area, shoot_weight, root_weight`

Units: days after sowing, g, cm², g, g.

---

## Model Equations Reference

| Eq. | Expression | Code |
|---|---|---|
| 1 | `Ċ_available = Ċ_in − Ċ_out` | [balance.py](src/functions/carbon/balance.py) `C_available` |
| 2 | `Ċ_in = r_ph · A_eff · p` | [balance.py](src/functions/carbon/balance.py) `C_in` |
| 3 | `A_eff(LA)` piecewise | [effective_area.py](src/functions/carbon/effective_area.py) `A_eff` |
| 4 | `Ċ_out^day = p·(r_root·RW + r_shoot·SW)` | [balance.py](src/functions/carbon/balance.py) `C_out_day` |
| 5 | `Ċ_out^night = (1−p)·(r_leaf·LW + r_root·RW + r_shoot·SW)` | [balance.py](src/functions/carbon/balance.py) `C_out_night` |
| 6 | `Ċ_out = LW·r_leaf·(1−p) + RW·r_root + SW·r_shoot` | [balance.py](src/functions/carbon/balance.py) `C_out` |
| 7 | `dLW/dt = Ċ_available · k_weight / (β+ρ)` | [carbon_growth.py](src/functions/growth/carbon_growth.py) |
| 8 | `dLA/dt = Ċ_available · k_area / ((β+ρ)·LMA)` | [carbon_growth.py](src/functions/growth/carbon_growth.py) |
| 9 | `SW = LW·R_shoot(LW)`, `RW = LW·R_root(LW)` | [shoot_mass.py](src/functions/allometry/shoot_mass.py), [root_mass.py](src/functions/allometry/root_mass.py) |
| 10 | `SNAR_adj = SNAR_max·[N_soil] / (K_m + [N_soil])` | [michaelis_menten.py](src/functions/nitrogen/michaelis_menten.py) |
| 11 | `N_leaf^area = (LW/(LW+SW+RW)) · N_in / LA` | [nitrogen_growth.py](src/functions/growth/nitrogen_growth.py) |
| — | `r_ph = f(N_leaf^area)` | [photosynthesis.py](src/functions/nitrogen/photosynthesis.py) `f_r_ph` |

---

## Model Methodology

### 2 Carbon Model

Growth is driven by net available carbon ($\dot{C}_{available}$), defined as the surplus of photosynthetic intake over maintenance costs [1]. All carbon quantities represent organic carbon (C) — carbon fixed from atmospheric CO₂ and incorporated into biomass — rather than CO₂ itself.

#### 2.1 Available Carbon

Available carbon for growth is calculated as the total photosynthetic intake during the day, minus the total maintenance cost of all tissues across both day and night.

$$\dot{C}_{available} = \dot{C}_{in} - \dot{C}_{out} \tag{1}$$

→ [`C_available`](src/functions/carbon/balance.py)

##### 2.1.1 Photosynthesis and Effective Area

Carbon intake ($\dot{C}_{in}$) is a function of the photosynthetic rate ($r_{ph}$), the photoperiod fraction ($p$), and the **Effective Area** ($A_{eff}$), which accounts for self-shading:

$$\dot{C}_{in} = r_{ph} \cdot A_{eff} \cdot p \tag{2}$$

→ [`C_in`](src/functions/carbon/balance.py)

The effective area concept is based on the principle that early leaves grow in a single plane maximising light exposure, while later leaves increasingly overlap, introducing self-shading. The function defines three regimes: below 50 cm² all leaf area is assumed fully exposed; between 50 and 100 cm² photosynthetic contribution declines linearly from 100% to 10% as overlap increases; above 100 cm² new area contributes only 10% of its potential rate.

$$A_{eff}(LA) = \begin{cases} LA & \text{if } LA \le 50 \\ 50 + (LA - 50) - 0.009 \cdot (LA - 50)^2 & \text{if } 50 < LA \le 100 \\ 77.5 + 0.1 \cdot (LA - 100) & \text{if } LA > 100 \end{cases} \tag{3}$$

→ [`A_eff`](src/functions/carbon/effective_area.py)

##### 2.1.2 Tissue Maintenance

Maintenance costs ($\dot{C}_{out}$) are partitioned into diurnal and nocturnal periods. During the day, leaf maintenance is excluded because $r_{ph}$ was measured as net assimilation — that cost is already embedded in the photosynthetic rate measurement. Root weight ($RW$), shoot weight ($SW$), and leaf weight ($LW$) are factored by their respective maintenance rates ($r$):

$$\dot{C}_{out}^{day} = p \cdot (r_{root} \cdot RW + r_{shoot} \cdot SW) \tag{4}$$

→ [`C_out_day`](src/functions/carbon/balance.py)

$$\dot{C}_{out}^{night} = (1 - p) \cdot (r_{leaf} \cdot LW + r_{root} \cdot RW + r_{shoot} \cdot SW) \tag{5}$$

→ [`C_out_night`](src/functions/carbon/balance.py)

Total maintenance costs are given by $\dot{C}_{out} = \dot{C}_{out}^{day} + \dot{C}_{out}^{night}$, which simplifies to:

$$\dot{C}_{out} = LW \cdot r_{leaf} \cdot (1-p) + RW \cdot r_{root} + SW \cdot r_{shoot} \tag{6}$$

→ [`C_out`](src/functions/carbon/balance.py)

#### 2.2 Carbon Allocation and Growth Rate

Carbon designated for leaf growth is partitioned between weight growth ($k_{weight}$) and area expansion ($k_{area}$) — dynamic coefficients derived by quadratic interpolation of empirical shoot weight data. These coefficients represent the fraction of total available carbon directed toward the leaf. Area expansion is necessarily coupled to weight growth, but weight growth does not always produce area expansion. The difference $k_{weight} - k_{area}$ therefore represents the fraction of leaf-allocated carbon that contributes solely to thickening, corresponding to an increase in $LMA$.

Leaf weight growth is governed by the fraction of available carbon allocated to leaf weight, converted to biomass using the combined carbon cost $\beta + \rho$:

$$\frac{dLW}{dt} = \frac{\dot{C}_{available} \cdot k_{weight}}{\beta + \rho} \tag{7}$$

→ [`growth_carbon`](src/functions/growth/carbon_growth.py), [`growth_nitrogen`](src/functions/growth/nitrogen_growth.py), [`k_weight`](src/functions/allometry/partition.py)

Here $\beta$ is the growth respiration cost — the carbon consumed as energy to synthesise 1 g of biomass — and $\rho$ is the tissue carbon concentration — the carbon structurally incorporated per gram of biomass. Their sum gives the total carbon required per gram of new tissue [1]. Leaf area growth follows the same logic, with only the $k_{area}$ fraction contributing to lateral expansion; dividing by $LMA$ converts the resulting mass growth rate into an area growth rate:

$$\frac{dLA}{dt} = \frac{\dot{C}_{available} \cdot k_{area}}{(\beta + \rho) \cdot LMA} \tag{8}$$

→ [`growth_carbon`](src/functions/growth/carbon_growth.py), [`growth_nitrogen`](src/functions/growth/nitrogen_growth.py), [`k_area`](src/functions/allometry/partition.py), [`LMA`](src/functions/allometry/lma.py)

$LMA$ is treated as an externally interpolated quantity rather than an emergent property of the system.

#### 2.3 Tissue Ratios

Shoot and root biomass are calculated as proportions of leaf weight using interpolated ratios ($R$). These ratios vary strongly with leaf weight and are derived via quadratic interpolation of empirical data. Because shoot mass spans several orders of magnitude across growth stages, $R_{shoot}$ is interpolated on the log-mass of shoot weight rather than raw mass, avoiding distortion from the large variance in shoot weight magnitudes.

$$SW = LW \cdot R_{shoot}(LW), \quad RW = LW \cdot R_{root}(LW) \tag{9}$$

→ [`R_shoot`](src/functions/allometry/shoot_mass.py), [`R_root`](src/functions/allometry/root_mass.py)

---

### 3 Nitrogen Modulation

The model's main environmental driver is the photoperiod fraction $p$, with the photosynthetic rate $r_{ph}$ and all other parameters treated as plant-specific constants. The model is extended by introducing soil nitrogen concentration $[N_{soil}]$ as an environmental variable that dynamically modulates growth. Nitrogen availability influences growth by modulating the photosynthetic rate ($r_{ph}$) and triggering compensatory changes in the Leaf-to-Root (L:R) ratio.

#### 3.1 Nitrogen Intake and Distribution

The Specific Nitrogen Absorption Rate ($SNAR$) follows Michaelis-Menten kinetics relative to soil nitrogen concentration $[N_{soil}]$:

$$SNAR_{adj} = \frac{SNAR_{max} \cdot [N_{soil}]}{K_m + [N_{soil}]} \tag{10}$$

→ [`michaelis_menten`](src/functions/nitrogen/michaelis_menten.py), [`growth_nitrogen`](src/functions/growth/nitrogen_growth.py)

Total nitrogen intake ($N_{in} = SNAR_{adj} \cdot RW$) is distributed across tissues. A direct modulation of $r_{ph}$ by $[N_{soil}]$ alone is not straightforward because the relationship between soil nitrogen concentration and plant nitrogen content is non-trivial, and the photosynthetic response to nitrogen is best characterised at the leaf level [3]. For this reason, nitrogen is first expressed as a leaf-level quantity — the nitrogen concentration per unit leaf area ($N_{leaf}^{area}$) — which then drives the photosynthetic response curve:

$$N_{leaf}^{area} = \left(\frac{LW}{LW + SW + RW}\right) \cdot \frac{N_{in}}{LA} \tag{11}$$

→ [`growth_nitrogen`](src/functions/growth/nitrogen_growth.py)

#### 3.2 Modulated Parameters

**Photosynthetic Rate:** $r_{ph}$ is dynamically adjusted as a function of leaf nitrogen, $r_{ph} = f(N_{leaf}^{area})$. The response curve is based on Sugiura & Tateno (2011) [3]:

$$r_{ph} = a_{PR} \cdot \left(1 - e^{-b_{PR} \cdot (N_{leaf}^{area} / N_{max})}\right)$$

→ [`f_r_ph`](src/functions/nitrogen/photosynthesis.py)

**Leaf-Root Ratio:** Under nitrogen deficiency, plants tend to increase root mass to compensate for reduced nitrogen availability [3]. While this compensatory mechanism can partially restore leaf nitrogen concentration by increasing uptake capacity, it simultaneously raises total maintenance costs ($\dot{C}_{out}$) due to the higher root biomass — creating a secondary drag on growth. To capture this, the model adjusts the L:R ratio toward the biologically optimal value derived from $SNAR$, using the midpoint between the current calculated ratio and the optimal. This allows the plant to exhibit nitrogen-deficiency compensation while still reflecting the carbon cost of maintaining a larger root system.

The optimal L:R ratio as a saturating function of $SNAR_{adj}$:

$$L\!:\!R_{opt}(SNAR_{adj}) = LR_0 + \frac{a_{LR} \cdot SNAR_{adj}}{b_{LR} + SNAR_{adj}}$$

→ [`L_R_opt`](src/functions/nitrogen/leaf_root_ratio.py)

The adjusted ratio as the midpoint between actual and optimal:

$$L\!:\!R_{adj} = L\!:\!R_{actual} + \gamma \cdot \left(L\!:\!R_{opt}(SNAR_{adj}) - L\!:\!R_{actual}\right)$$

→ [`L_R_adj`](src/functions/nitrogen/leaf_root_ratio.py), [`growth_nitrogen`](src/functions/growth/nitrogen_growth.py)

---

### References

[1] Weraduwage SM, Chen J, Anozie FC, Morales A, Weise SE, Sharkey TD. The relationship between leaf area growth and biomass accumulation in *Arabidopsis thaliana*. Frontiers in Plant Science. 2015;6:167.

[2] Honda H, Fisher JB. Tree branch angle: Maximizing effective leaf area. Science. 1978;199(4331):888–90.

[3] Sugiura D, Tateno M. Optimal leaf-to-root ratio and leaf nitrogen content determined by light and nitrogen availabilities. PLoS ONE. 2011;6(6):e21306.

[4] Shaw R, Cheung CYM. A dynamic multi-tissue flux balance model captures carbon and nitrogen metabolism and optimal resource partitioning during *Arabidopsis* growth. Frontiers in Plant Science. 2018;9:884.

[5] Osone Y, Tateno M. Nitrogen absorption capacity and leaf nitrogen content as factors determining the relative growth rate of plant species from different successional habitats. Functional Ecology. 2005;19(3):502–10.
