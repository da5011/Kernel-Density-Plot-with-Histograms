#Required Imports
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.ticker import NullFormatter

os.chdir(os.path.dirname(os.path.abspath(__file__))) #Sets Working Directory to script

df = pd.read_excel("sample_data.xlsx", header=0) #Reads data of interest into a dataframe. Can read from csv, txt, etc

#Objective: Find Extrema to make appropriate bounds
x_min = df.min(axis=0, numeric_only=True).tolist()[0]
x_max = df.max(axis=0, numeric_only=True).tolist()[0]
y_min = df.min(axis=1, numeric_only=True).tolist()[0]
y_max = df.max(axis=1, numeric_only=True).tolist()[0]

#Generate Continuous Colormap for KDP
custom_cmap = LinearSegmentedColormap.from_list('cmap', ['aliceblue','blue','yellow','red','darkred'], N=64)

#Define Graph Borders
left, width = 0.1, 0.65
bottom, height = 0.1, 0.65
bottom_h = left_h = left + width

#Define Graph Bounds
kdp_bounds = [left, bottom, width, height]
hist_x_bounds = [left, bottom_h, width, 0.2]
hist_y_bounds = [left_h, bottom, 0.2, height]

nBins_x = 100 #Defines how many bins are disired for the 1-D Histograms
nBins_y = 100

#Generate Matplotlib Figure Object, a Seaborn Axes Object for the KDP, and 2 MPL Axes Objects for the 1-D Histograms
fig = plt.figure(1, figsize=(8,8))
ax_kdp = plt.axes(kdp_bounds)
ax_hist_x = plt.axes(hist_x_bounds)
ax_hist_y = plt.axes(hist_y_bounds)

#Initialize Seaborn Kernel Density Plot
sb.kdeplot(x= df.iloc[0:, 0], y= df.iloc[0:, 1],
           bw_adjust= 1.3, cmap= custom_cmap, fill= True, ax= ax_kdp) #bw_adjust paramater can be changed to liking

#Calculate Binwidth for the 1-D Histograms
binwidth_x = (x_max-x_min)/nBins_x
binwidth_y = (y_max-y_min)/nBins_y

#Initialize 1-D Histograms
ax_hist_x.hist(x=df.iloc[0:, 0], bins= nBins_x, color="red", edgecolor= "black")
ax_hist_y.hist(x=df.iloc[0:, 1], bins= nBins_y, color="red", edgecolor= "black", orientation="horizontal")

#Axes Information. Enable/Disable at your Preference
ax_hist_x.xaxis.set_major_formatter(NullFormatter())
ax_hist_y.yaxis.set_major_formatter(NullFormatter())
ax_hist_x.set_xlim(ax_kdp.get_xlim())
ax_hist_y.set_ylim(ax_kdp.get_ylim())
ax_hist_x.axis('off')
ax_hist_y.axis('off')

ax_kdp.set_xlabel(df.columns[0])
ax_kdp.set_ylabel(df.columns[1])
fig.suptitle("My Plot", fontsize= 24)

plt.savefig(f"./myfigure.png", dpi= 500)
plt.show()
