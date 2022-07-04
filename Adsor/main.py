import adsor

spring = [0]  # [60, 120, 240, 480, 960]  # [60, 120, 480, 960]
n = [1]  # , 2, 3, 4, 5
for j in n:
    for i in spring:
        file_path = "D:/study/00课题/05移动接触角/03液滴/adsor/3.2/TW3-rigid/ar-ya-%s-100-0.1890-%s.profile" % (j, i) if i != 0 \
            else "D:/study/00课题/05移动接触角/03液滴/adsor/3.2/Void-csld/ar-yb-%s-100-0.1890.profile " % j

        layers = [0, 5] if 'ya' in file_path.split('-') else [0, 13]
        frequency = 1400  # 3200  # 2200  # 1400  # 2200  # 1400
        equilibrium = 200  # 200
        adsor.surface(file_path, layers, frequency, equilibrium)

