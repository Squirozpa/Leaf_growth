### **1. Carbon Uptake**
\[
C_{\text{uptake}}(t) = k_C \cdot \text{LA}(t)
\]

### **2. Nitrogen Uptake**
\[
N_{\text{uptake}}(t) = \text{SNAR} \cdot C(N(t)) \cdot \text{RW}(t)
\]

### **3. Stored Carbon Dynamics**
\[
\frac{dC_{\text{stored}}}{dt} = C_{\text{uptake}}(t) - C_{\text{use}}(t)
\]

### **4. Stored Nitrogen Dynamics**
\[
\frac{dN_{\text{stored}}}{dt} = N_{\text{uptake}}(t) - N_{\text{use}}(t)
\]

### **5. Effective Nitrogen (Converted to Carbon Units)**
\[
N_{\text{eff}}(t) = \frac{N_{\text{stored}}(t)}{\mu}
\]

### **6. Maintenance Cost**
\[
M(t) = k_M \Bigl[\text{LA}(t) + \text{RW}(t) + c\Bigr]
\]

### **7. Available Nutrients for Growth**
\[
U_{\text{eff}}(t) = \min\Bigl\{ C_{\text{stored}}(t),\; N_{\text{eff}}(t) \Bigr\} - M(t)
\]

### **8. Leaf Area Growth**
\[
\frac{d\text{LA}}{dt} = \text{LNR} \cdot U_{\text{eff}}(t)
\]

### **9. Root Weight Dynamics**
\[
\frac{d\text{RW}}{dt} = k_{RW} \left(\alpha \cdot \text{LA}(t) - \text{RW}(t)\right)
\]

### **10. Soil Nitrogen Concentration**
\[ \frac{dC(N)}{dt} = -N_{\text{uptake}} + I \]

\[ \frac{\Delta A}{\Delta C} = \frac{r_{\text{leaf}} \times U_t(C_{\text{in}}, N_{\text{in}})}{C_{\text{growth}}} \]
