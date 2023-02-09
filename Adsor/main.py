import adsor

spring = [0]  # np.arange(10) + 1  # [60, 120, 240, 480, 960]  # [60, 120, 480, 960]
n = [1]  # np.arange(10) + 1  # [1]  # , 2, 3, 4, 5
epsilon = [1.1, 1.2, 1.3, 1.4]
# for j in n:
#     for i in epsilon:
#         # if i != 3:
tdamp = [100, 500, 1000, 2000, 2500, 3000, 3500, 4000, 5000]
# for t in tdamp:
file_path = 'D:/document/00Study/01接触角摩擦力/计算/液滴/adsor/3.4/Void-NH/ar-ya-1-100-0.1449.profile' #% t
layers = [0, 5] if 'ya' in file_path.split('-') else [0, 13]
frequency = 1400  # 3200  # 2200  # 1400  # 2200  # 1400
equilibrium = 200  # 200
adsor.surface(file_path, layers, frequency, equilibrium)
