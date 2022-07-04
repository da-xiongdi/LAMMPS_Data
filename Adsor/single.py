import adsor
import numpy as np

index = np.arange(0.7, 1.4, 0.1)
arrest = np.empty(len(index))
j = 0
for i in index:
    file_path = "D:/document/00Study/01接触角摩擦力/计算/液滴/stage4/test/adsor/7/V-NH/ar.100.0.1890.%.1f.profile" % i
    cutoff, base = 11.92, 13.8593

    arrest[j] = adsor.single(file_path, cutoff, base)
    j += 1

print(np.average(arrest), np.std(arrest))
