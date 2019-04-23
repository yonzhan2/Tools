import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

from scipy.interpolate import spline, BSpline
import scipy

data = {"time": [10, 20, 30, 40, 50, 60], "usage": [20, 40, 50, 35, 10, 60]}
df = pd.DataFrame(data)
print(df)

time = np.array([10, 20, 30, 40, 50, 60])
usage = np.array([10, 15, 5, 25, 40, 20])

xnew = np.linspace(time.min(), time.max(), 300)

power_smooth = spline(time, usage, xnew)
plt.plot(xnew, power_smooth)
plt.xlabel('Time(min)')
plt.ylabel('CPU')
plt.title("CPU Uage Histogram")
plt.savefig('cpu.png')
plt.show()
