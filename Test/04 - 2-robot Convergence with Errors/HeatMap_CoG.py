# Run with python, not pypy

import csv
import matplotlib.pyplot as plt
import numpy as np

from math import floor, ceil, pi

sectors = 100

max_err_d = 1
max_err_a = pi

Total = np.zeros([sectors,sectors])

max_d = np.zeros([sectors,sectors])
sum_d = np.zeros([sectors,sectors])
nb_d = np.zeros([sectors,sectors])

failed = np.zeros([sectors,sectors])

with open('results_FSYNC_CoG_err') as csv_file:
	csv_reader = csv.reader(csv_file, delimiter=',')
	for row in csv_reader:

		X = floor(float(row[0])*sectors/max_err_d)
		Y = floor(float(row[1])*sectors/max_err_a)
		
		Total[X,Y] += 1
		
		if row[2] == '-1':
			failed[X,Y] += 1
		else:
			if float(row[2]) > max_d[X,Y]:
				max_d[X,Y] = float(row[2])
			sum_d[X,Y] += float(row[2])
			nb_d[X,Y] += 1
		
avg_d = np.divide(sum_d,nb_d)
failed = np.divide(failed,Total)

x_ticks = [0,sectors/2,sectors-1]
x_label_list = ['0','$\dfrac{\pi}{2}$', '$\pi$'] # To be done manually

y_ticks = [0,sectors/2,sectors-1]
y_label_list = ['0',str(max_err_d/2), str(max_err_d)]


fig, ax = plt.subplots()
#im = ax.imshow(max_d,vmin=1, vmax=51) # For fixed color scale. Must be chosen properly 
im = ax.imshow(max_d,origin='lower')

ax.set_xticks(x_ticks)
ax.set_xticklabels(x_label_list)
ax.set_yticks(y_ticks)
ax.set_yticklabels(y_label_list)

ax.set_xlabel('Maximum Angular Error')
ax.set_ylabel('Maximum Distance Error', rotation=90, va="bottom")

cbar = ax.figure.colorbar(im, ax=ax)
cbar.ax.set_ylabel('Maximum Distance', rotation=-90, va="bottom")
fig.tight_layout()
plt.show()





fig, ax = plt.subplots()
#im = ax.imshow(avg_d,vmin=1, vmax=3.5) # For fixed color scale. Must be chosen properly 
im = ax.imshow(avg_d,origin='lower')

ax.set_xticks(x_ticks)
ax.set_xticklabels(x_label_list)
ax.set_yticks(y_ticks)
ax.set_yticklabels(y_label_list)

ax.set_xlabel('Maximum Angular Error')
ax.set_ylabel('Maximum Distance Error', rotation=90, va="bottom")

cbar = ax.figure.colorbar(im, ax=ax,)
cbar.ax.set_ylabel('Average Distance', rotation=-90, va="bottom")

fig.tight_layout()
plt.show()





fig, ax = plt.subplots()
#im = ax.imshow(avg_d,vmin=1, vmax=3.5) # For fixed color scale. Must be chosen properly 
im = ax.imshow(failed,origin='lower')

ax.set_xticks(x_ticks)
ax.set_xticklabels(x_label_list)
ax.set_yticks(y_ticks)
ax.set_yticklabels(y_label_list)

ax.set_xlabel('Maximum Angular Error')
ax.set_ylabel('Maximum Distance Error', rotation=90, va="bottom")

cbar = ax.figure.colorbar(im, ax=ax,)
cbar.ax.set_ylabel('Failed Convergence', rotation=-90, va="bottom")

fig.tight_layout()
plt.show()
