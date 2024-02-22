
### Press F5 to run for user input or another method ###
### Do not need to adjust any code below             ###

# Importing libraries and functions
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

## Asking for user input ##
print("Below are the approximate run times for 2000 stationary avalanche occurances and grid size")
print("Computer Specs: Intel i5 (4 cores) - 8GB ram")
print("10x10 Grid ~ 5 seconds.")
print("20x20 Grid ~ 30 seconds.")
print("30x30 Grid ~ 120 seconds.")
print("")
while True:
    Q1 = input("How many stationary state avalanche occurances do you need between 1000 and 2000?: ")
    if (int(Q1) < 1000) or (int(Q1) > 2000):
        print("Incorrect input, try again.")
        continue
    else:
        break
print("")
while True:
    Q2 = input("Choose length of sandpile grid between 10 and 30: ")
    if (int(Q2) < 10) or (int(Q2) > 30):
        print("Incorrect input, try again.")
        continue
    else:
        break
print("")
while True:
    print('Choose initial condition.')
    Q3 = input("Randomized Configuration (0) or Level Configuration (1)? Enter 0 or 1: ")
    if int(Q3) not in [0,1]:
        print("Incorrect input, try again.")
        continue
    else:
        break
if int(Q3) == 1:
    while True:
        print("")
        Q4 = input("Choose level configuration between 0,1,2,3: ")
        if int(Q4) not in [0,1,2,3]:
            print("Incorrect input, try again.")
        else:
            break
data_needed = int(Q1)
N = int(Q2)
print("")
print('Processing...')

# Defining some properties we want to plot over time
sandgrains = []
ratio0 = []; ratio1 = []; ratio2 = []; ratio3 = []                        # Proportion of grid with values {0, 1, 2, 3}
Topples_Freq = dict.fromkeys(range(0,math.floor(N**2)), 0)                # Number of topples of avalanche
Loss_Freq = dict.fromkeys(range(0,2*N), 0)                                # Sand grains lost to boundary from avalanche
Area_Freq = dict.fromkeys(range(0,N**2), 0)                               # Area of avalanche
Length_Freq = dict.fromkeys(range(0,math.ceil(math.sqrt(2*N**2))), 0)     # Length of avalanche (we use L2 norm)
Time_Freq = dict.fromkeys(range(1, 20), 0)                                # Times between avalanches

# Initializing grid (randomized or uniform)
if int(Q3) == 1:
    grid = np.full((N, N), int(Q4), dtype=int)
else:
    grid = np.random.randint(4, size = (N, N))
sandgrains.append(np.average(grid))

# Stationary State Indicator (mean grain sand per site) (We use this to know when to start recording stationary state avalanche data)
if  10 <= N < 15:
    SSI = 2.02
else:
    SSI = 2.06

## Main avalanche loop (Each step is the addition of a sand grain on a random site) ##
number_avalanche = 0  # Start number of avalanche
time_avalanche = 1    # Start time of avalanche
stationary = 0        # Stationary state dummie variable

while number_avalanche <= data_needed:

    "Choosing to place the sand grain based on uniform distribution over the possible sites"
    x_coord = secrets.choice([i for i in range(1,N+1)])
    y_coord = secrets.choice([i for i in range(1,N+1)])
    placement = [x_coord, y_coord]

    "Updating grid with new sand grain"
    grid[placement[0]-1, placement[1]-1] += 1

    "Running avalanche script if there is a critical site (ie, site with 4 or more grains)"
    if grid.max() > 3:
        number_avalanche += 1

         ## Run avalanche here ##

        'Defining Properties'
        Topples = 0; Area = 0 ; Loss = 0; Length = 0; UniqueSitesToppled = []

        "defining intitial unstable configuration of avalanche"
        grid_start = []
        for row in grid.tolist():
            bracket = []
            for column in grid.tolist():
                bracket.append(column)
            grid_start.append(bracket)

        "Toppling sites while configuration unstable"
        while grid.max() > 3:
            newgrid = topple(grid) # Topple function from Functions.py file
            grid = newgrid[0]
            Topples += 1
            Loss += newgrid[2]

            'Updating unique sites toppled'
            if newgrid[1] not in UniqueSitesToppled:
                UniqueSitesToppled.append(newgrid[1])



        'Updating Property: Area'
        Area = len(UniqueSitesToppled)

        'Updating Property: Length = floor( sup( { d(x,y) | x,y toppled in avalanche} ) where d is the L2-norm )'
        for a in UniqueSitesToppled:
            for b in UniqueSitesToppled:
                if L2norm(a,b) > Length:
                    Length = math.floor(L2norm(a,b))

        "Updating avalanche properties, avalanche times and site value frequencies once system is stationary"
        if np.average(grid) >= SSI:
            stationary = 1

        if stationary == 1:

            ratio0.append(grid_ratio(grid, 0))  # Update grid proportion frequency value 0
            ratio1.append(grid_ratio(grid, 1))  # Update grid proportion frequency value 1
            ratio2.append(grid_ratio(grid, 2))  # Update grid proportion frequency value 2
            ratio3.append(grid_ratio(grid, 3))  # Update grid proportion frequency value 3

            try:
                Topples_Freq[Topples] += 1          # Update Topples frequency dictionary
            except:
                pass
            try:
                Loss_Freq[Loss] += 1                # Update Loss frequency dictionary
            except:
                pass
            try:
                Area_Freq[Area] += 1                # Update Area frequency dictionary
            except:
                pass
            try:
                Length_Freq[Length] += 1            # Update Length frequency dictionary
            except:
                pass
            try:
                Time_Freq[time_avalanche] += 1      # Update Avalanche Time frequency dictionary
            except:
                pass

        "Updating mean number of sand grains time"
        sandgrains.append(np.average(grid))
        time_avalanche = 1


    else:
        "No site with 4 or more sand grains so we go to next time step"
        time_avalanche += 1
        sandgrains.append(np.average(grid))



## Below we plot our data ##

# Plotting distribution of grain heights on lattice
index = 1
for ratio in [ratio0, ratio1, ratio2, ratio3]:
    mu, std = norm.fit(ratio)
    if ratio == ratio3:
        mean3 = mu
    plt.subplot(2,2, index)
    plt.hist(ratio, bins=5, density=True, stacked=True, color='peru')
    xmin, xmax = plt.xlim()
    x = np.linspace(xmin, xmax, 100)
    p = norm.pdf(x, mu, std)
    plt.plot(x, p, 'k-', linewidth=2)
    plt.xlabel("")
    plt.ylabel("Frequency")
    plt.title("Distribution " + str(index - 1) + " value site , mean = " + str(round(mu,4)) + ", var = " + str(round(std,4)))
    index += 1
plt.show()

# Plotting Mean Sandgrains on Lattice Site over Time [Stationary/Transient State indicator graph]
x = [i for i in range(len(sandgrains))]
plt.subplot(1,2,1)
plt.plot(x,sandgrains, 'k')
plt.title("Sandgrains on lattice over time")
plt.ylabel('Mean number of sand grains')
plt.xlabel("Time")
plt.grid()

# Plotting times between avalanches in Stationary State against Geometric Distribution with rate given by mean of hight 3 distribution
plt.subplot(1,2,2)
x = [i for i in range(1,len(list(Time_Freq.values()))+1)]
geom_pd = geom.pmf(x,mean3)
plt.plot(x, geom_pd, 'k.', ms=8, label='Geometric('+str(round(mean3,4))+') density')
Fcount = sum(Time_Freq.values())
for key,value in Time_Freq.items():
    Time_Freq[key] = value/Fcount
"Getting max abs error between simulated probability and geo(0.415) probability"
maxerr = 0
for i in range(1, len(geom_pd)+1):
    error = abs(geom_pd[i-1] - Time_Freq[i])
    if error > maxerr:
        maxerr = error

plt.plot(x,list(Time_Freq.values()), 'r.', label='simulated result')
plt.title("Times between avalanches in Stationary state, Max Error = "+str(round(maxerr,5)))
plt.xlabel("Time")
plt.ylabel("Probability")
plt.grid()
plt.legend(loc="upper right")
plt.show()


# Plotting avalanche data (Topples, Loss, Area, Length) with power law relationship
index = 1
for property in [(Topples_Freq, "Topples"), (Loss_Freq, "Loss"), (Area_Freq, "Area"), (Length_Freq, "Length")]:

    x_axis = [x for x in list(property[0].keys())]
    y_axis = [y for y in list(property[0].values())]

    "Getting powerlaw fit"
    X = [x+1 for x in x_axis]
    Y = [y+1 for y in y_axis]
    logx = np.log(X)
    logy = np.log(Y)
    coeffs = np.polyfit(logx,logy,deg=1)
    poly = np.poly1d(coeffs)
    yfit = lambda X: np.exp(poly(np.log(X)))

    "Plotting loglog of data and powerlaw curve"
    plt.subplot(2,2,index)
    plt.loglog(X,yfit(X), 'r:')
    plt.loglog(x_axis, y_axis, 'k.')
    plt.title(property[1] + " loglog plot with powerlaw = " + str(round(coeffs[0], 3)))
    plt.ylabel("Frequency")
    plt.grid()
    index += 1
plt.show()
