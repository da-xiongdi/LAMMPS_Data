import shape
from Adsor import adsor

frequency = 2200  # 3200  # 2200  # 1400  # 2200  # 1400
equilibrium = 200  # 200
liquid_type = False  # Ture for volatile F for nonvolatile
rho = 1.5  # 1.28 for vle; 1.5 for nonvolatile 0.3606
interface = 0.9
ylo = 20  # 16.36  # 13.86+ 2.475 =16.335
ad_layers = [0, 5]  # [0, 13]  # [0, 5]  # [0, 135]  #

square_path = 'D:/document/00Study/01接触角摩擦力/计算/液滴/stage7/TF-NH-local/ar-square-100-0.3686.profile'
y_path = 'D:/document/00Study/01接触角摩擦力/计算/液滴/stage7/TF-NH-local/ar-y-100-0.3686.profile'

shape.radium(square_path, frequency, rho, interface, ylo, equilibrium, liquid_type)
adsor.surface(y_path, ad_layers, frequency, equilibrium)
# shape.ca(square_path, frequency, interface, ylo, equilibrium)
