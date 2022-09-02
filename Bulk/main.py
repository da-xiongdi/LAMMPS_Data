import walker

frequency = 5000  # 3200  # 2200  # 1400  # 2200  # 1400
equilibrium = 360  # 360 2ns for vis  # 1800 2ns for diff 360 200
repeat = 1

# paths = 'D:/study/00课题/05移动接触角/03液滴/bulk/LGV/nonvolatile'
paths = '//192.168.1.90/01接触角摩擦力/计算/液滴/bulk/trans/LGV/nonvolatile'
# diff_paths, vis_paths = walker.file_walker(paths)[:2]
# fluc_path = walker.file_walker(paths)[2]
# print(fluc_path)
# walker.calculate_walker(diff_paths, equilibrium)
# walker.calculate_walker(vis_paths, equilibrium)
for path in walker.file_walker(paths):
    if path:
        walker.calculate_walker(path, equilibrium)
