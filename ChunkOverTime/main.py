import DataAve
from Adsor import adsor

frequency = 2000  # 3200  # 2200  # 1400  # 2200  # 1400
ts = 9e4  # 200
te = 1.1e5

# square_paths = ['D:/study/00课题/05移动接触角/03液滴/stage5/Void-LGV/nonzero/ar-square-100-0.1890.profile',
#                 'D:/study/00课题/05移动接触角/03液滴/stage5/Void-LGV/ar-square-100-0.1890.profile']
# y_path = 'D:/study/00课题/05移动接触角/03液滴/stage5/NH-Void/ar-y-100-0.1890.profile'
#
# for square_path in square_paths:
#     DataAve.ave_time_space(square_path, frequency, ts, te, [6])

square_path = 'D:/document/00Study/01接触角摩擦力/计算/液滴/stage13/TW/ar-square-100-0.1260.profile'
DataAve.ave_time_space(square_path, ts, te, [9, 10, 11])
