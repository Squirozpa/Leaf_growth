import numpy as np
class GrowthModel:
    def __init__(self):
        # Constants
        self.PR = 69.12  # Photosynthetic rate umol/cm²d
        self.SNAR = 3360.96  # Specific nitrogen assimilation rate umol/gd
        
        self.P = 12 #Photoperiod in hours
        self.starch = 0.6 #starch coefficient
        
        self.alpha_leaf = 12.024  # Maintenance leaf respiration rate (carbon) umol/cm2d
        self.alpha_root = 1382.4  # Maintenance root respiration rate (carbon) umol/gd
        self.alpha_stem = 604.8  # Maintenance stem respiration rate (carbon) umol/gd

        self.beta_leaf = 8660  # Growth leaf respiration rate (carbon) umol/g
        self.beta_root = 10824 # Growth root respiration rate (carbon) umol/g
        self.beta_stem = 14200 # Growth stem respiration rate (carbon) umol/g

        self.Km = 400  # Michaelis-Menten constant for nitrogen uptake umol/cm²d

        self.gamma_leaf = 0.20  # Nitrogen allocation to leaf
        self.gamma_root = 0.19  # Nitrogen allocation to root
        self.gamma_stem = 0.61  # Nitrogen allocation to stem

        self.rho_resp = 0.101  # Leaf nitrogen allocation to respiration
        self.rho_photo = 0.453  # Leaf nitrogen allocation to photosynthesis
        self.rho_struct = 0.08  # Leaf nitrogen allocation to growth
        self.rho_store = 0.438  # Leaf nitrogen allocation to storage

        self.Kg = 0.6  # Carbon availability factor for growth
        self._Kl = 0.75  # Carbon availability factor for leaf growth

        self.sigma = 37500  # Biomass allocation factor umol/g

        self.r_rwr = 8.3  # Leaf to root ratio
        self.r_swr = 12.5  # Leaf to shoot ratio

        self.LMA = 0.00267  # Leaf mass per area (g/cm²

        self.current_leaf_weight = 0.05  # Initial leaf weight in grams
        self.dt = 1  # Time step in days
        self.current_t = 0  # Current time in days
    @property
    def Kl(self):
        """
        Calculate the carbon availability factor for leaf growth.
        """
        kl_early = np.linspace(0.75, 0.70, 45*self.dt)  
        kl_late = np.linspace(0.70, 0.32, 20*self.dt)
        if self.current_t < 45:
            return kl_early[int(self.current_t)]
        elif self.current_t < 65:
            return kl_late[int(self.current_t - 45)]
        else:
            return 0.32
    @Kl.setter
    def Kl(self, value):
        """
        Set the carbon availability factor for leaf growth.
        """
        self._Kl = value

    def A_eff(self, leaf_weight):
        leaf_area = leaf_weight / self.LMA
        # self-shading correction: max full-light area is 100 cm²
        full_light_area = min(leaf_area, 85)
        shaded_area = max(leaf_area - 85, 0)
        effective_area = full_light_area + 0.1 * shaded_area  # shaded contributes 10%
        return effective_area
    
    def A(self, leaf_weight):
        """
        Calculate the photosynthetic rate based on leaf area.
        """
        return leaf_weight/ self.LMA
    
    def RW(self, leaf_weight):
        """
        Calculate the root weight based on leaf weight.
        """
        return leaf_weight / self.r_rwr
    
    def SW(self, leaf_weight):
        """
        Calculate the shoot weight based on leaf weight.
        """
        return leaf_weight / self.r_swr
    
    def maintenance_respiration_day(self, leaf_weight):
        """
        Calculate the maintenance respiration based on leaf weight during the day.
        """
        print(f"Leaf Weight: {leaf_weight}")
        print(f"Alpha Leaf: {self.alpha_leaf*(self.A(leaf_weight))}, Alpha Root: {self.alpha_root*self.RW(leaf_weight)}, Alpha Stem: {self.alpha_stem*self.SW(leaf_weight)}")
        return (self.alpha_root * self.RW(leaf_weight) + self.alpha_stem * self.SW(leaf_weight))
    
    def maintenance_respiration_night(self, leaf_weight):
        """
        Calculate the maintenance respiration based on leaf weight.
        """
        A = self.A(leaf_weight)
        return (self.alpha_leaf * A + self.alpha_root * self.RW(leaf_weight) + self.alpha_stem * self.SW(leaf_weight))
    
    def net_carbon_assimilation(self, leaf_weight) :
        """
        Calculate the net carbon assimilation based on leaf weight.
        """
        A = self.A_eff(leaf_weight)
        net_day = (A * self.PR*(1-self.starch) - (self.maintenance_respiration_day(leaf_weight))) * (self.P / 24)
        starch = A * self.PR * self.starch * (self.P / 24)
        net_night = (starch/((24-self.P)) - (self.maintenance_respiration_night(leaf_weight))) * ((24 - self.P) / 24)
        return net_day + net_night
    
    def growth_net(self, leaf_weight):
        """
        Calculate the net growth based on leaf weight.
        """
        A = self.A(leaf_weight)
        carbon = self.net_carbon_assimilation(leaf_weight)*self.Kl
        carbon_consumption = (self.beta_leaf + self.sigma)
        print(f"Carbon: {carbon}, Carbon Consumption: {carbon_consumption}")
        new_growth = carbon / carbon_consumption
        print(f"New Growth: {new_growth}")
        return new_growth
    
    def simulate_growth_euler(self, initial_leaf_weight, soil_nitrogen, initial_carbon, time_steps, dt):
        """
        Simulate growth using Euler's method.
        """
        A_list = [self.A(initial_leaf_weight)]
        R_list = [initial_leaf_weight]
        C_list = [self.net_carbon_assimilation(initial_leaf_weight)]

        for t in range(1, time_steps):
            print(f"Time step {t}:")
            
            growth = self.growth_net(R_list[-1])
            new_leaf_weight = R_list[-1] + growth * dt

            A_list.append(self.A(new_leaf_weight))
            R_list.append(new_leaf_weight)
            C_list.append(self.net_carbon_assimilation(new_leaf_weight))

            self.current_leaf_weight = new_leaf_weight
            self.current_t += dt
        return A_list, R_list, C_list

class GrowthModelNitrogen(GrowthModel):
    def __init__(self):
        super().__init__()
        self._PR = 69.12  # Photosynthetic rate umol/cm²d
        self._rwr = 8.3  # Leaf to root ratio
        self._swr = 12.5
        self._LMA = 0.00267
        self._SNAR = 3360.96  # Specific nitrogen assimilation rate umol/gd
        self._PR = 69.12  # Photosynthetic rate umol/cm²d
        self._Kl= 0.55  # Carbon availability factor for leaf growth
        self.soil_nitrogen = 10

    def SNAR_adjusted(self):
        """
        Calculate the nitrogen uptake based on soil nitrogen.
        """
        return self.soil_nitrogen * self._SNAR / (self.Km + self.soil_nitrogen)
    @property
    def r_rwr(self):
        """
        Calculate the root weight based on leaf weight.
        """
        L_R = 1.9 + self._rwr * self.SNAR_adjusted() / (1100 + self.SNAR_adjusted())
        return L_R
    
    @r_rwr.setter
    def r_rwr(self, value):
        """
        Set the leaf to root ratio.
        """
        self._rwr = value
    
    @property
    def PR(self):
        """
        Calculate the shoot weight based on leaf weight.
        """
        A = self.A(self.current_leaf_weight)
        print(f"Current root weight: {self.RW(self.current_leaf_weight)}, SNAR adjusted: {self.SNAR_adjusted()}, A: {A}")
        concentration_leaf = self.RW(self.current_leaf_weight)*self.SNAR_adjusted() / A
        print(f"Concentration Leaf: {concentration_leaf}")
        print(f"Photosynthetic Rate: {84.9*(concentration_leaf - 0.25)**0.7 + 1}")
        return 84.9*(concentration_leaf - 0.25)**0.7 + 1

    @PR.setter
    def PR(self, value):
        """
        Set the photosynthetic rate.
        """
        self._PR = value
        
test = GrowthModelNitrogen()
test.soil_nitrogen = 3400
initial_leaf_weight = 150
test.current_leaf_weight = initial_leaf_weight
print(test.PR)
        