# Leaf Growth Model: Carbon Assimilation and Nitrogen Modulation

Sebastián Quiroz  
February 2026

## 1. Introduction

This model predicts leaf growth based on nitrogen availability by extending a carbon assimilation framework. Nitrogen modulates physiological parameters to simulate plant development under varying soil conditions.

## 2. Carbon Model

Growth is driven by net available carbon ($C_{available}$), defined as photosynthetic intake minus maintenance costs.

### 2.1 Available Carbon

### Equation (1)
\[
C_{available} = C_{in} - C_{out}
\]
**Code references:**
- `growth.py` [`C_disp`](growth.py#L22)

### 2.1.1 Photosynthesis and Effective Area

### Equation (2)
\[
C_{in} = PR \cdot A_{eff} \cdot p
\]
**Code references:**
- `growth.py` [`C_in`](growth.py#L20)
- `params.py` [`PR`, `P`](params.py#L1-L4)

### Equation (3)
\[
A_{eff}(A) =
\begin{cases}
A & A \le 50 \\
50 + (A-50) - 0.009\,(A-50)^2 & 50 < A \le 100 \\
77.5 + 0.1\,(A-100) & A > 100
\end{cases}
\]
**Code references:**
- `effective_area.py` [`effective_area_function`](effective_area.py#L5-L16)
- `growth.py` usage via [`C_in`](growth.py#L20)

### 2.1.2 Tissue Maintenance

### Equation (4)
\[
C^{day}_{out} = p\,(\alpha_{root}\,RW + \alpha_{shoot}\,SW)
\]
**Code references:**
- `growth.py` [`C_mant_day`](growth.py#L15)
- `params.py` [`alpha_root`, `alpha_stem`, `P`](params.py#L4-L8)

### Equation (5)
\[
C^{night}_{out} = (1-p)\,(\alpha_{leaf}\,LW + \alpha_{root}\,RW + \alpha_{shoot}\,SW)
\]
**Code references:**
- `growth.py` [`C_mant_night`](growth.py#L16), [`C_out`](growth.py#L18)
- `params.py` [`alpha_leaf`, `alpha_root`, `alpha_stem`, `P`](params.py#L4-L8)

### 2.2 Carbon Allocation and Growth Rate

### Equation (6)
\[
\frac{dLW}{dt} = \frac{C_{available}\,k_{weight}}{\beta + \rho}
\]
**Code references:**
- `growth.py` [`dLW_dt`](growth.py#L25)
- `growth.py` carbon model update [`dLW`](growth.py#L49)
- `growth.py` nitrogen model update [`dLW`](growth.py#L76)
- `params.py` [`beta_leaf`, `RHO`](params.py#L11-L15)
- `k_over_time.py` [`leaf_partition_over_time`](k_over_time.py#L32)

### Equation (7)
\[
\frac{dLA}{dt} = \frac{C_{available}\,k_{area}}{(\beta + \rho)\,LMA}
\]
**Code references:**
- `growth.py` carbon model update [`dA`](growth.py#L51)
- `growth.py` nitrogen model update [`dA`](growth.py#L78)
- `k_over_time.py` [`leaf_area_partition_over_time`](k_over_time.py#L23)
- `lma_calculation.py` [`calculate_lma`](lma_calculation.py#L33)

### 2.3 Tissue Ratios

### Equation (8)
\[
SW = LW \cdot r_{shoot}(LW), \quad RW = LW \cdot r_{root}(LW)
\]
**Code references:**
- `growth.py` [`SW`](growth.py#L30), [`RW`](growth.py#L29)
- `sw_calculation.py` [`shoot_mass_from_leaf_mass`](sw_calculation.py#L25)
- `rw_calculation.py` [`root_mass_from_leaf_mass`](rw_calculation.py#L24)

## 3. Nitrogen Modulation

Nitrogen availability modulates photosynthetic rate and leaf-root allocation dynamics.

### 3.1 Nitrogen Intake and Distribution

### Equation (9)
\[
SNAR_{adj} = SNAR_{max}\,\frac{[N_{soil}]}{K_m + [N_{soil}]}
\]
**Code references:**
- `growth.py` [`SNAR_adjusted`](growth.py#L38)
- `michaelis_menten_nitrogen.py` [`michaelis_menten`](michaelis_menten_nitrogen.py#L6)
- `params.py` [`Km`](params.py#L13)

Related definition:
\[
N_{in} = SNAR_{adj} \cdot RW
\]
**Code references:**
- `growth.py` inline term `SAR*RW` in [`N_area`](growth.py#L41)

### Equation (10)
\[
N^{leaf}_{area} = \left(\frac{LW}{LW+SW+RW}\right)\cdot\frac{N_{in}}{LA}
\]
**Code references:**
- `growth.py` [`N_area`](growth.py#L41)

### 3.2 Modulated Parameters

Photosynthetic rate modulation:
\[
PR = f\left(N^{leaf}_{area}\right)
\]
**Code references:**
- `growth.py` [`PR_adjusted`](growth.py#L32)
- `pr_nitrogen.py` [`nitrogen_effect_on_photosynthesis`](pr_nitrogen.py#L13)

Leaf-root compensation (midpoint adjustment between actual and optimal ratio):
\[
L\!:\!R_{adj} = L\!:\!R_{actual} + \gamma\left(L\!:\!R_{opt}(SNAR) - L\!:\!R_{actual}\right)
\]
**Code references:**
- `leaf_root_ratio_nitrogen.py` [`L_R`](leaf_root_ratio_nitrogen.py#L11), [`adjusted_L_R`](leaf_root_ratio_nitrogen.py#L14)
- `growth.py` [`L_R_adjusted`](growth.py#L36)

## 4. Parameters (Model Inputs)

Core parameters used by the implementation:
- `PR`: `params.py` [L1](params.py#L1)
- `SNAR`: `params.py` [L2](params.py#L2)
- `P`: `params.py` [L4](params.py#L4)
- `alpha_leaf`, `alpha_root`, `alpha_stem`: `params.py` [L6-L8](params.py#L6-L8)
- `beta_leaf`: `params.py` [L11](params.py#L11)
- `Km`: `params.py` [L13](params.py#L13)
- `RHO`: `params.py` [L15](params.py#L15)

---

This Markdown version intentionally omits analysis/results discussion, conclusion text, and figure/image citations.