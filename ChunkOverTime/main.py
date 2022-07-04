import DataAve
from Adsor import adsor

frequency = 2200  # 3200  # 2200  # 1400  # 2200  # 1400
ts = 10.5e6  # 200
te = 11e6

square_paths = ['D:/study/00课题/05移动接触角/03液滴/stage5/Void-NH/ar-square-100-0.1260.profile',
                'D:/study/00课题/05移动接触角/03液滴/stage5/Void-LGV/ar-square-100-0.1260.profile']
y_path = 'D:/study/00课题/05移动接触角/03液滴/stage5/NH-Void/ar-y-100-0.1890.profile'

for square_path in square_paths:
    DataAve.ave_time_space(square_path, frequency, ts, te, [6])
