# Run this code to compare the convergence in mean grain sand in the time limit on different initial conditions
# No need to adjust anything - Just hit run and results will output
# Run time - Approximately 15 seconds

# Importing libraries and functions from Functions.py file
import math
import secrets
import statistics
import numpy as np
import matplotlib.pyplot as plt

from Functions import topple
from Functions import L2norm
from Functions import grid_ratio

from scipy.stats import norm
from scipy.stats import geom
from scipy.stats import linregress

time = 3000
N = 20
level = 0
meanDist = []  # Bucket for random initial configuration mean sand grain distribution
stationaryIndicator = 0

# Looping over each initial condition
for level in range(0,5):

    mean = []

    # Random initial condition if level == 4 else level initial condition at level value
    if level == 4:
        grid = np.random.randint(4, size = (N, N))
    else:
        grid = np.full((N, N), level, dtype=int)

    sandgrains = []
    sandgrains.append(np.average(grid))


    ## Main avalanche loop (Each step is the addition of a sand grain on a random site) ##
    number_avalanche = 0
    t = 0
    while t <= time:

        "Choosing to place the sand grain based on uniform distribution over the possible sites"
        x_coord = secrets.choice([i for i in range(1,N+1)])
        y_coord = secrets.choice([i for i in range(1,N+1)])
        placement = [x_coord, y_coord]

        "Updating grid with new sand grain"
        grid[placement[0]-1, placement[1]-1] += 1

        "Running avalanche script if there is a site with 4 or more grains"
        if grid.max() > 3:

            number_avalanche += 1

            "defining intitial unstable configuration of avalanche"
            grid_start = []
            for row in grid.tolist():
                bracket = []
                for column in grid.tolist():
                    bracket.append(column)
                grid_start.append(bracket)

            "Toppling sites while configuration unstable"
            while grid.max() > 3:
                newgrid = topple(grid)
                grid = newgrid[0]

            "defining final stable configuration of avalanche"
            grid_end = grid.tolist()

            sandgrains.append(np.average(grid))

        else:
            sandgrains.append(np.average(grid))
        t += 1

        if len(mean) < 500:
            mean.append(np.mean(grid))
        else:
            del mean[0]
            mean.append(np.mean(grid))

        if np.mean(grid) >= 2.06:
            stationaryIndicator = 1
        if level == 4 and np.mean(grid) > 1.95 and stationaryIndicator == 1:
            meanDist.append(np.mean(grid))


    # Mean Sandgrains on Lattice Site over Time [Stationary/Transient State indicator graph]
    x = [i for i in range(1, len(sandgrains)+1)]

    if level < 4:
        plt.plot(x,sandgrains, label="level "+str(level)+" Initial Condition, mean = " + str(round(statistics.mean(mean),4)))
    else:
        plt.plot(x,sandgrains, label="Randomized Initial Condition, mean = " + str(round(statistics.mean(mean), 4)))

# Plotting results
plt.xscale('log')
plt.title("Mean number of sand grains per site 20x20 lattice")
plt.ylabel('Mean number of sand grains per site')
plt.xlabel("Time")
plt.grid()
plt.legend(loc="upper right")
plt.show()

plt.hist(meanDist, bins=33, density=True, stacked=True, color='peru')
mu, std = norm.fit(meanDist)
xmin, xmax = plt.xlim()
x = np.linspace(xmin, xmax, 100)
p = norm.pdf(x, mu, std)
plt.plot(x, p, 'k-', linewidth=2)
plt.xlabel("mean sand grains per site")
plt.ylabel("Frequency")
plt.title("Distribution of Mean Number of sand grains, mean = " + str(round(mu,4)) + ", var = " + str(round(std,4)))
plt.show()
