# ConcentrationFieldReconstruction (CFR)
Code for "Enhanced method for concentration field reconstruction: Visualizing pollutant distribution in ventilated indoor environments", under reviewed by Journal of Clean Production.

# Kernel DM+V

The main parameter affecting the performance of this algorithm is kernel_size (Line 39). 
By modifying this parameter, the CFR (Concentration Field Reconstruction) results can be adjusted.

**Usage Instructions:**
The folders data\\10 percent random sampling data and data\\5 percent random sampling data contain the 10% and 5% sampling data, respectively.
On Line 26, enter the path to the sampling data, for example: "E:\\Desktop\\data\\10 percent random sampling data\\mixing ventilation\\DM_V_10.txt".
When using data from the mixing ventilation folder, modify Line 56 to set np.arange(0, X + cell_size_x, cell_size_x) where X = 6, and modify Line 57 to set np.arange(0, Y + cell_size_y, cell_size_y) where Y = 4.5.
When using data from the displacement ventilation folder, modify Line 56 to set np.arange(0, X + cell_size_x, cell_size_x) where X = 4.91, and modify Line 57 to set np.arange(0, Y + cell_size_y, cell_size_y) where Y = 4.31.
On Line 96, enter the path to save the results, such as: "E:\\Desktop\\Concentration field reconstruction results\\Kernel_DMV\\". This will save the calculation results of the Kernel_DM+V algorithm.

# Kernel DM+V/W

The main parameters affecting the performance of this algorithm are kernel_size (Line 47) and wind_scale (Line 49). 
By modifying these parameters, the CFR (Concentration Field Reconstruction) results can be adjusted.

**Usage Instructions:**
The folders data\\10 percent random sampling data and data\\5 percent random sampling data contain the 10% and 5% sampling data, respectively.
On Line 34, enter the path to the sampling data, for example: "E:\\Desktop\\data\\10 percent random sampling data\\mixing ventilation\\DM_VW_10.txt".
When using data from the mixing ventilation folder, modify Line 74 to set np.arange(0, X + cell_size_x, cell_size_x) where X = 6, and modify Line 75 to set np.arange(0, Y + cell_size_y, cell_size_y) where Y = 4.5.
When using data from the displacement ventilation folder, modify Line 74 to set np.arange(0, X + cell_size_x, cell_size_x) where X = 4.91, and modify Line 75 to set np.arange(0, Y + cell_size_y, cell_size_y) where Y = 4.31.
On Line 137, enter the path to save the results, such as: "E:\\Desktop\\Concentration field reconstruction results\\Kernel_DMV\\". This will save the calculation results of the Kernel_DM+V/W algorithm.

# Kernel DM+V/W+

The main parameters affecting the performance of this algorithm are kernel_size (Line 47) and wind_speed_factor (Line 49).
By modifying these parameters, the CFR (Concentration Field Reconstruction) results can be adjusted.

**Usage Instructions:**
The folders data\\10 percent random sampling data and data\\5 percent random sampling data contain the 10% and 5% sampling data, respectively.
On Line 34, enter the path to the sampling data, for example: "E:\\Desktop\\data\\10 percent random sampling data\\mixing ventilation\\DM_VW+_10.txt".
When using data from the mixing ventilation folder, modify Line 74 to set np.arange(0, X + cell_size_x, cell_size_x) where X = 6, and modify Line 75 to set np.arange(0, Y + cell_size_y, cell_size_y) where Y = 4.5.
When using data from the displacement ventilation folder, modify Line 74 to set np.arange(0, X + cell_size_x, cell_size_x) where X = 4.91, and modify Line 75 to set np.arange(0, Y + cell_size_y, cell_size_y) where Y = 4.31.
On Line 128, enter the path to save the results, such as: "E:\\Desktop\\Concentration field reconstruction results\\Kernel_DMV\\". This will save the calculation results of the Kernel_DM+V/W+ algorithm.
