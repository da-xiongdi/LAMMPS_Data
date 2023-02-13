import numpy as np

import shape
from Adsor import adsor

frequency = 300  # 2200  # 3200  # 2200  # 1400  # 2200  # 1400
equilibrium = 0  # 200  # 200
drop_type = 4  #

sl_types = [0.1260, 0.1449, 0.1890, 0.1575, 0.2520]  # Ture for volatile F for nonvolatile
vl_types = 0.15
sv_types = 0.3465
rho = 1.5 if drop_type > 2 else 1.28  # 1.28 for vle; 1.5 for nonvolatile 0.3606; 1.5 for polymer
interface = 0.5  # 0.9 for nonvolatile; 0.5 for volatile; 0.1 0.3 for polymer
ylo = 20  # 16.36  # 13.86+ 2.475 =16.335
ad_layers = [0, 5]  # [0, 13]  # [0, 5]  # [0, 135]  #

# for i in np.arange(1, 4):
root_path = 'D:/study/00课题/05移动接触角/03液滴/stage8.2.6/NH'
square_path = '%s/ar-square-160-%.4f-%s-%.4f.profile' % (root_path, sl_types[drop_type], vl_types, sv_types)
y_path = '%s/ar-y-160-%.4f-%s-%.4f.profile' % (root_path, sl_types[drop_type], vl_types, sv_types)

# ylos = [16, 24]
# for ylo in ylos:
shape.radium(square_path, rho, interface, ylo, equilibrium)
adsor.surface(y_path, ad_layers, frequency, equilibrium)
# shape.ca(square_path, frequency, interface, ylo, equilibrium)
