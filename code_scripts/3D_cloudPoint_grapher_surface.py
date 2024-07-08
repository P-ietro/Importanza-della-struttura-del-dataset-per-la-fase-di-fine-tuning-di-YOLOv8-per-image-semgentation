# Questo script serve a plottare su un grafico 3D le informazioni definite in un file xlsx
# IMPORTANTE: potrebbe essere necessario modificare il path di cartelle e file.

import matplotlib.pyplot as plt
from scipy import interpolate
from matplotlib.ticker import LinearLocator
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import pandas as pd

fx = pd.read_excel('.\\totals\\_train_seg_loss.xlsx', usecols="A,B,C", dtype={'X':np.string_, 'Y':np.string_, 'Z':np.float32})

data = fx.to_numpy()
x = np.array(data[:, 0])
y = np.array(data[:, 1])
z = np.array(data[:, 2])

tmp = []
for el in x :
    tmp.append(int(el.replace("test_", "")))
x = np.array(tmp)

step = 1 / 6
tmp = []
for el in y :
    l = el.split("_")
    s = int(l[0].replace("s", ""))
    if s == 300:
        tmp.append(0)
    elif s == 100 :
        tmp.append(1)
    elif s == 95:
        tmp.append(2)
    elif s == 280:
        tmp.append(3)
    elif s == 90:
        tmp.append(4)
    elif s == 80:
        tmp.append(5)
y = np.array(tmp)

ordered = sorted(zip(x, y, z))
x = np.unique(np.array([e[0] for e in ordered]))
y = np.unique(np.array([e[1] for e in ordered]))
z = np.array([e[2] for e in ordered]).reshape((4, 6))

f_z = interpolate.RectBivariateSpline(x=x, y=y, z=z)

ref = np.linspace(0, len(x) - 1, len(x), dtype=int)
f_x = interpolate.interp1d(ref, x, kind='cubic')
ref = np.linspace(0, len(y) - 1, len(y), dtype=int)
f_y = interpolate.interp1d(ref, y, kind='cubic')

x = np.arange(0, 3.1, (1/5))
y = np.arange(0, 5.1, (1/3))
x = f_x(x)
y = f_y(y)

X, Y = np.meshgrid(x, y)
Z = f_z(x, y)

# Create a figure
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm, linewidth=0, antialiased=False)

# Set labels
ax.set_xlabel('Numbero of logos')
ax.set_ylabel('ratio real synth img', labelpad=14)
ax.set_zlabel('metric value')

ax.set_title('Train Segmentation Loss')

ax.set_yticks([0, 1, 2, 3, 4, 5])
ax.set_yticklabels(['S 300; R 0', 'S 100; R 0', 'S 95; R 5', 'S 280; R 20','S 90; R 10', 'S 80; R 20'])

# Add a color bar which maps values to colors.
fig.colorbar(surf, shrink=0.5, aspect=15, location='right', pad=0.15)

# Show the plot
plt.show()
