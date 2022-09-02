import shape
from Adsor import adsor

frequency = 2200  # 2200  # 3200  # 2200  # 1400  # 2200  # 1400
equilibrium = 200  # 200
interface = 0.1  # 0.1
ylo = 20  # 16.36  # 13.86+ 2.475 =16.335
ad_layers = [0, 5]  # [0, 13]  # [0, 5]  # [0, 135]  #

square_path = 'D:/study/00课题/05移动接触角/03液滴/stage7/NH-Void/ar-square-100-0.3686.profile'
y_path = 'D:/study/00课题/05移动接触角/03液滴/stage7/NH-Void/ar-y-100-0.3686.profile'

shape.radium(square_path, frequency, interface, ylo, equilibrium)
adsor.surface(y_path, ad_layers, frequency, equilibrium)
# shape.ca(square_path, frequency, interface, ylo, equilibrium)
