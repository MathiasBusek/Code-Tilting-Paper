import pandas as pd
import numpy as np
import glob
import matplotlib.pyplot as plt
import easygui

path = easygui.diropenbox("Open Folder with CSV files") + '/'
filenames = glob.glob(path + '*.csv')
degrees = []
aspect_ratios = []
tilt = False

for files in filenames:
    data = pd.read_csv(files, delimiter=';')
    
    # Brightfield images does not contain aspect ratio data
    if 'aspect_ratio' in data.columns:
        aspect_ratios.extend(data.aspect_ratio)

        # If image is flipped, orientation needs to be corrected
        if tilt:
            for angle in data.Orientation:
                if (angle < 90):
                    degrees.append(angle + 90)
                else:
                    degrees.append(angle - 90)
        else:
            degrees.extend(data.Orientation)

    # Brightfield images: Orientation is +- 90 degree
    else:
        for angle in data.Orientation:
            degrees.append(angle + 90)
    
radians = np.deg2rad(degrees)

bin_size = 10
a , b=np.histogram(degrees, bins=np.arange(0, 360+bin_size, bin_size))
centers = np.deg2rad(np.ediff1d(b)//2 + b[:-1])

fig = plt.figure(figsize=(10,8))
ax = fig.add_subplot(111, projection='polar')
ax.bar(centers, a, width=np.deg2rad(bin_size), bottom=0.0, color='.8', edgecolor='k')
ax.set_theta_zero_location("N")
ax.set_theta_direction(-1)
ax.set_thetamax(180)
plt.savefig(path+'orientation.png')
plt.savefig(path+'orientation.pdf')
plt.show()
plt.hist(aspect_ratios, 10)
plt.savefig(path+'aspect_ratio.png')
plt.savefig(path+'aspect_ratio.pdf')
