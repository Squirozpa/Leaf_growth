import GrowthModelV2 as gm
import matplotlib.pyplot as plt


def main():
    model = gm.GrowthModel()
    initial_leaf_weight = 0.05
    model2 = gm.GrowthModelNitrogen()
    soil_nitrogen = 2000
    model2.soil_nitrogen = soil_nitrogen
    model3 = gm.GrowthModelNitrogen()
    model3.soil_nitrogen = 600
    initial_carbon = 1
    time_steps = 86
    dt = 1
    A_list, R_list, C_list = model.simulate_growth_euler(
        initial_leaf_weight, soil_nitrogen, initial_carbon, time_steps, dt
    )
    A_list2, R_list2, C_list2 = model2.simulate_growth_euler(
        initial_leaf_weight, soil_nitrogen, initial_carbon, time_steps, dt
    )
    A_list3, R_list3, C_list3 = model3.simulate_growth_euler(
        initial_leaf_weight, soil_nitrogen, initial_carbon, time_steps, dt
    )
    relative_growth_rate_A = [
        (A_list[i] - A_list[i - 1]) / A_list[i - 1] for i in range(1, len(A_list))
    ]
    relative_growth_rate_A2 = [
        (A_list2[i] - A_list2[i - 1]) / A_list2[i - 1] for i in range(1, len(A_list2))
    ]
    relative_growth_rate_A3 = [
        (A_list3[i] - A_list3[i - 1]) / A_list3[i - 1] for i in range(1, len(A_list3))
    ]
    print("86 R_list:", R_list[-1])
    print("86 A_list:", A_list[-1])
    print("86 C_list:", C_list[-1])
    print(model.A_eff(R_list[-1]))
    plt.figure(figsize=(10, 8))
    plt.plot(A_list, label='Leaf Area (cm²) High N')
    plt.plot(A_list2, label='Leaf Area (cm²) Med N')
    plt.plot(A_list3, label='Leaf Area (cm²) Low N')
    plt.title('Growth Simulation Results')
    plt.xlabel('Time Steps')
    plt.ylabel('Values')
    plt.ylim(0,450)
    plt.legend()
    plt.grid()
    plt.show()
    plt.figure(figsize=(10, 8))

    plt.title('Relative Growth Rate of Leaf Area')
    plt.plot(relative_growth_rate_A, label='High N', color='blue')
    plt.plot(relative_growth_rate_A2, label='Med N', color='orange')
    plt.plot(relative_growth_rate_A3, label='Low N', color='green')
    plt.xlabel('Time Steps')
    plt.ylabel('Relative Growth Rate')
    plt.legend()
    plt.grid()
    plt.show()


if __name__ == "__main__":
    main()
