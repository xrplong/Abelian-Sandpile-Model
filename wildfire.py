
### Adjust parameter values in choose input section below if you so wish ###
### Then press run                                                       ###
#__________________________________________________________________________________________________________________________
### Choose input parameters here ###

# Choose grid length dimension (Recommened 10 - 30)
N = 20

# Choose intial tree density (Recommened 0.5)
TreeDensity = 0.5

# Choose Wind direction
# 99 - No Wind, N - North, E - East, S - South, W - West
directions = [99, 'N', 'E', 'S', 'W']
Wind_Dir = directions[2] # Change number inside directions {0 == No Wind, 1 == North, 2 == East, 3 == South, 4 == West}

# Choose probability of site with no tree growing a tree (Recommended < 0.5)
Pg = 0.2

# Choose probability of tree catching fire if on boundary of fire (Recommended > 0.5)
Pf = 0.9

# Choose probability of tree on fire burning out and becoming an empty site (Recommended > 0.4)
Pe = 0.5

# Choose probability of a tree catching fire by lightning strike (Recommened < 0.01)
f  = 0.005

# Choose number of iterations (Recommened 200 - 400)
Iterations = 200

#__________________________________________________________________________________________________________________________
## DO NOT ADJUST ANYTHING BELOW, ONLY ABOVE ##

# Importing libraries and functions
import math
import secrets
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import bernoulli
from matplotlib import animation
from Functions import topple
from Functions import L2norm
from Functions import grid_ratio
from Functions import update_wildfire
from Functions import wildfire_metrics


# Setting up forest with tree density
grid = np.zeros((N,N), dtype = np.int64)
for i,j in np.ndindex(grid.shape):
    RV= bernoulli.rvs(TreeDensity)
    if RV == 1:
        grid[i,j] = 1

# Choosing centre of grid to start fire
grid[math.floor(N/2), math.floor(N/2)] = 2

# Simulating wildfire
gridlist = []
metriclist = []
gridlist.append(grid)

while len(gridlist) < Iterations:
    "Updating grid"
    grid = np.copy(update_wildfire(grid, Wind_Dir, Pg, Pf, Pe, f))
    gridlist.append(grid)
    bracket = []
    "Updating wildfire metrics"
    bracket.append(wildfire_metrics(grid)[0])
    bracket.append(wildfire_metrics(grid)[1])
    bracket.append(wildfire_metrics(grid)[2])
    metriclist.append(bracket)

# Plotting wildfire data
x_axis = [i for i in range(0,len(metriclist))]
y0_axis = [i[0] for i in metriclist]
y1_axis = [i[1] for i in metriclist]
y2_axis = [i[2] for i in metriclist]

plt.subplot(1,2,1)
plt.plot(x_axis, y0_axis, color='brown', label='Proportion: Tree on Fire.')
plt.plot(x_axis, y1_axis, color='seagreen', label='Proportion: Tree not on Fire.')
plt.plot(x_axis, y2_axis, color='k', label='Proportion: Empty Site.')
plt.title('Probability (Grow Tree) = ' + str(Pg) + ', Probability (Catch Fire) = ' + str(Pf) + '\n \
           Probability (Burn out) = ' + str(Pe) + ', Probability (Lighting strike) = ' + str(f))
plt.legend(loc='upper right')
plt.ylabel('Proportion')
plt.xlabel("Time")

plt.subplot(1,2,2)
plt.imshow(gridlist[-1], cmap='gray')
plt.title('Snap shot of fire on '+str(N)+' by '+str(N)+' grid \n white = fire, grey = tree, black = empty')

plt.show()


# Animation of wildfire
plt.rcParams["figure.figsize"] = [7.00, 3.50]
plt.rcParams["figure.autolayout"] = False

fig, ax = plt.subplots()

def update(i):
    im_normed = np.array(gridlist[i])
    ax.imshow(im_normed, cmap='gray')
    ax.set_axis_off()

anim = animation.FuncAnimation(fig, update, frames = Iterations, interval=200)

plt.show()
