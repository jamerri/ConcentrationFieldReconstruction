import numpy as np
import math
import time
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.colors as col
import matplotlib.cm as cm
from matplotlib.ticker import MultipleLocator, FuncFormatter

start = datetime.now()

def time_stamp():
    ct = time.time()
    local_time = time.localtime(ct)
    data_head = time.strftime("%Y-%m-%d-%H-%M-%S", local_time)
    time_stamp = "%s" % data_head
    return time_stamp

pi = math.pi

def exp(n):
    answer = math.exp(n)
    return answer

def cos(n):
    answer = math.cos(n)
    return answer

def sin(n):
    answer = math.sin(n)
    return answer

'''1.File Reading'''
f = open("E:\\Desktop\\data\\5 percent random sampling data\\displacement ventilation\\DM_VW+_5.txt", 'r', encoding='utf-8')
measurement_data = f.readlines()
measurement_data = measurement_data[0:len(measurement_data)]
for i in range(len(measurement_data)):
    msg = measurement_data[i].strip('\n').split()
    for j in range(len(msg)):
        msg[j] = float(msg[j])
    measurement_data[i] = msg
np.set_printoptions(suppress=True)
measurement_data = np.array(measurement_data)

'''2.Algorithm Parameter Setting'''
radius_multiple = 3
kernel_size = 0.4
confidence_scale = 1
wind_speed_factor = 0.3

'''3.TXT Data Processing'''
position_x_line = 0
position_y_line = 1
alco_concentration_line = 2
wind_speed_line = 3
wind_dir_line = 4
sample_x_raw = measurement_data[:, position_x_line]
sample_y_raw = measurement_data[:, position_y_line]
sample_x = sample_x_raw
sample_y = sample_y_raw
for i in range(len(measurement_data)):
    if measurement_data[i, wind_dir_line] <= 180:
        measurement_data[i, wind_dir_line] = 180 - measurement_data[i, wind_dir_line]
    else:
        measurement_data[i, wind_dir_line] = 540 - measurement_data[i, wind_dir_line]
alco_concentration = measurement_data[:, alco_concentration_line]
wind_speed = measurement_data[:, wind_speed_line]
wind_dir = measurement_data[:, wind_dir_line]

'''4.Mesh Generation'''
cell_size_x = 0.05
cell_size_y = 0.05
# displacement ventilation：x*y=4.91*4.31；mixing ventilation：x*y=6*4.5；
temp_position_x = np.arange(0, 4.91 + cell_size_x, 0.05)
temp_position_y = np.arange(0, 4.31 + cell_size_y, 0.05)
position_x, position_y = np.meshgrid(temp_position_x, temp_position_y)
position_x = position_x.flatten()
position_y = position_y.flatten()
sample_num = len(sample_x)
grid_num = len(position_x)

'''5.Core algorithm calculation'''
weight = np.zeros(np.shape(position_x))
weight_concentration = np.zeros(np.shape(position_x))
r0 = sum(alco_concentration) / len(alco_concentration)
for i in range(grid_num):
    single_weight = []
    single_weight_concentration = []
    for j in range(sample_num):
        wind_dir_rad = np.deg2rad(wind_dir[j])
        rotation_sample_x = sample_x[j] * cos(wind_dir_rad) + sample_y[j] * sin(wind_dir_rad)
        rotation_sample_y = sample_y[j] * cos(wind_dir_rad) - sample_x[j] * sin(wind_dir_rad)
        rotation_position_x = position_x[i] * cos(wind_dir_rad) + position_y[i] * sin(wind_dir_rad)
        rotation_position_y = position_y[i] * cos(wind_dir_rad) - position_x[i] * sin(wind_dir_rad)
        distance = pow((rotation_sample_x - rotation_position_x), 2) + pow((rotation_sample_y - rotation_position_y), 2)
        if distance > pow((radius_multiple * kernel_size), 2):
            single_weight.append(0)
        elif distance == 0:
            coefficient_part = 1 / (((2 * pi) ** 0.5) * kernel_size)
            index_part = distance / (2 * pow(kernel_size, 2))
            temp_weight = coefficient_part * exp(index_part)
            temp_weight_concentration = temp_weight * alco_concentration[j]
            single_weight.append(temp_weight)
            single_weight_concentration.append(temp_weight_concentration)
        else:
            sqrt_distance = np.sqrt(distance)
            c_angle = (rotation_sample_x - rotation_position_x) / sqrt_distance
            coefficient_part = 1 / (((2 * pi) ** 0.5) * kernel_size)
            index_part = -0.5 * distance / (2 * pow(kernel_size, 2))
            temp_weight = coefficient_part * exp(index_part) * (1 + wind_speed_factor * wind_speed[j] * c_angle)
            temp_weight_concentration = temp_weight * alco_concentration[j]
            single_weight.append(temp_weight)
            single_weight_concentration.append(temp_weight_concentration)
    weight[i] = sum(single_weight)
    weight_concentration[i] = sum(single_weight_concentration)
confidence = np.zeros(np.shape(position_x))
mean_value = np.zeros(np.shape(position_x))
sigma_omega = confidence_scale * (1 / pow((2 * pi), 0.5) * kernel_size)
for i in range(len(weight)):
    confidence[i] = 1 - exp(-(weight[i] / (sigma_omega * sigma_omega)))
    mean_value[i] = confidence[i] * weight_concentration[i] / weight[i] + (1 - confidence[i]) * r0

min_val = np.min(mean_value)
max_val = np.max(mean_value)
normalized_value = (mean_value - min_val) / (max_val - min_val)

'''6、Data saving'''
desktop_path = "E:\\Desktop\\Concentration field reconstruction results\\Kernel_DMVW+\\"
file_path = desktop_path + '2D_KernelDMVW+_' + time_stamp() + '.txt'
with open(file_path, 'w') as file:
    for i in range(len(position_x)):
        file.write(f"{position_x[i]}\t{position_y[i]}\t{mean_value[i]}\n")
print(f"mean_value saved: {file_path}")

normalized_file_path = desktop_path + '2D_KernelDMVW+_normalize_' + time_stamp() + '.txt'
with open(normalized_file_path, 'w') as file:
    for i in range(len(position_x)):
        file.write(f"{position_x[i]}\t{position_y[i]}\t{normalized_value[i]}\n")
print(f"normalized_value saved: {normalized_file_path}")

'''7. Map Painting'''
cmap = col.LinearSegmentedColormap.from_list('own', ['#0000CD', '#00FFFF', '#00ff00', '#ffff00', '#ff0000'])
cm.register_cmap(cmap=cmap)
fig, ax = plt.subplots(figsize=(8, 10))
ax.set_aspect('equal')
grid_shape_x = len(np.unique(temp_position_x))
grid_shape_y = len(np.unique(temp_position_y))
Z = normalized_value.reshape(grid_shape_y, grid_shape_x)
contour = ax.contourf(temp_position_x, temp_position_y, Z, cmap='own', levels=80)
cax = ax.inset_axes([0, 1.1, 1, 0.04], transform=ax.transAxes)
cbar = fig.colorbar(contour, cax=cax, orientation='horizontal', ticks=np.linspace(normalized_value.min(), normalized_value.max()-0.1, 10))
cbar.ax.xaxis.set_ticks_position('bottom')
cbar.ax.xaxis.set_label_position('top')
cbar.ax.tick_params(labelsize=10)
def format_func(value, tick_number):
    return f'{value:.1f}'
ax.xaxis.set_major_formatter(FuncFormatter(format_func))
ax.yaxis.set_major_formatter(FuncFormatter(format_func))
ax.xaxis.set_major_locator(MultipleLocator(1.0))
ax.yaxis.set_major_locator(MultipleLocator(1.0))
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.set_xlim(temp_position_x.min(), temp_position_x.max())
ax.set_ylim(temp_position_y.min(), temp_position_y.max())
plt.rcParams['font.family'] = 'Times New Roman'
ax.tick_params(axis='both', which='major', labelsize=10)
ax.set_xlabel('X/m', fontsize=12, fontfamily='Times New Roman')
ax.set_ylabel('Y/m', fontsize=12, fontfamily='Times New Roman')
plt.show()

end = datetime.now()
print("running time：" + str((end - start)))
