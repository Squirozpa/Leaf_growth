import Growth_edo as ge
import Tomato_nitrogen as tn
import matplotlib.pyplot as plt
# Set up the figure
plt.figure(figsize=(12, 10))
plt.subplot(4, 1, 1)
plt.plot(tn.t, tn.W, label='Weight (W)', color='blue')
plt.xlabel('Time (days)')
plt.ylabel('Weight (W)')
plt.legend()
plt.grid()

# Plot 2: Leaf Area (A) over time
plt.subplot(4, 1, 2)
plt.plot(ge.sol.t, ge.sol.y[0], label='Leaf Area (A)', color='green')
plt.xlabel('Time (days)')
plt.ylabel('Leaf Area (m²)')
plt.title('Leaf Area Growth Over Time')
plt.legend()
plt.grid()

# Display the plots
plt.tight_layout()
plt.show()