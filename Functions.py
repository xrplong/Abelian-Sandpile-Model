### Below are functions used for the sandpile.py and wildfire.py files ###

# Importing Libraries
import numpy as np
import secrets
import math
from scipy.stats import bernoulli

def L2norm(a,b):
    "Computes the L2-norm distance between tuples a,b"
    return round(float(math.sqrt((b[0]-a[0])**2 + (b[1]-a[1])**2)), 3)

def grid_ratio(grid, index):
    "Assumes as input a NxN numpy grid with integer values on {0, 1, 2, 3}"
    "Index number in {0, 1, 2, 3}"
    "Gives ratio of index in grid"
    lattice = grid.tolist()
    size = len(lattice)**2
    index_count = 0
    for row in lattice:
        for column in row:
            if column == index:
                index_count += 1
    return round(float(index_count/size), 2)

def grid_max(grid):
    max = np.max(grid)
    max_sites = np.argwhere(grid == max)
    return max_sites.tolist()

def topple(input_grid):
    "Function Input"
    "2 dimensional numpy non-negative integer array representing an unstable configuration"

    "Function Output"
    "[A, B, C]"

    "A = Updated 2 dimensional numpy non-negative integer array representing configuration after toppling an unstable site"
    "B = Coordinate of site toppled"
    "C = Number of sand grains deleted from system"

    grid = input_grid
    deleted = 0

    "Choosing to collapse the site with most sandpiles, if multiple then choose uniformly randomly"
    "This choice is not important because of the Abelian property of the model ie; different topple sequences have the same ending configuration"
    update_location = secrets.choice(grid_max(grid))

    "updating chosen unstable site"
    grid[update_location[0], update_location[1]] -= 4

    "updating above site"
    try:
        grid[update_location[0] - 1, update_location[1]] += 1
    except:
        deleted += 1
        pass

    "updating below site"
    try:
        grid[update_location[0] + 1, update_location[1]] += 1
    except:
        deleted += 1
        pass

    "updating left of site"
    try:
        grid[update_location[0], update_location[1] - 1] += 1
    except:
        deleted += 1
        pass

    "updating right of site"
    try:
        grid[update_location[0], update_location[1] + 1] += 1
    except:
        deleted += 1
        pass

    return[grid, update_location, deleted]


## Below are two functions used in the wildfire.py file ##

# Function 1 (update_wildfire)  --> Takes as input a grid and returns an updated grid after 1 iteration of wildfire
def update_wildfire(grid, Wind_Dir, Pg, Pf, Pe, f):
    "__FunctionInput__"
    "2 dimensional numpy non-negative integer array representing an grid with fire"

    "__FunctionOutput__"
    "Outputs the bounary sites of the fire of input grid with each site being marked with a 0 or 1"
    "0 means not in direction of wind with respect to fire"
    '1 means in direction of wind with respect to fire'

    Ignite_locations = []

    "Updating lattice with trees burning out first"
    for i,j in np.ndindex(grid.shape):
        if grid[i][j] == 2:
             RV= bernoulli.rvs(Pe)
             if RV == 1:
                grid[i,j] = 0

    "Updating lattice with growing trees second"
    for i,j in np.ndindex(grid.shape):
        if grid[i][j] == 0:
            RV= bernoulli.rvs(Pg)
            if RV == 1:
                grid[i,j] = 1

    "Updating lattice with igniting trees by lighting"
    for i,j in np.ndindex(grid.shape):
        if grid[i][j] == 1:
            RV= bernoulli.rvs(f)
            if RV == 1:
                grid[i,j] = 2

    "Updating lattice with trees next to fire catching fire"
    "Trees next to fire in direction of wind will catch fire more frequently"
    if Wind_Dir == 99:
        for i,j in np.ndindex(grid.shape):
            if grid[i][j] == 2:
                RV= bernoulli.rvs(Pf)
                if (RV == 1):
                    try:
                        grid[i][j+1] = 2
                    except:
                        pass
                    try:
                        grid[i][j-1] = 2
                    except:
                        pass
                    try:
                       grid[i+1][j] = 2
                    except:
                       pass
                    try:
                        grid[i-1][j] = 2
                    except:
                        pass

    else:
        for i,j in np.ndindex(grid.shape):
            if grid[i][j] == 2 and (1 < i < grid.shape[0]-1) and (1 < j < grid.shape[0]-1):
                RV_DirectionOfWind= bernoulli.rvs(Pf)
                RV_AgainstWind= bernoulli.rvs(Pf/100)
                RV_SideofWind= bernoulli.rvs(Pf/10)
                if Wind_Dir == 'N':
                    if RV_DirectionOfWind == 1:
                        try:
                            grid[i-1][j] = 2
                        except:
                            pass
                    if RV_SideofWind == 1:
                        try:
                            grid[i][j+1] = 2
                        except:
                            pass
                        try:
                            grid[i][j-1] = 2
                        except:
                            pass
                    if RV_AgainstWind == 1:
                        try:
                            grid[i+1][j] = 2
                        except:
                            pass
                if Wind_Dir == 'S':
                    if RV_DirectionOfWind == 1:
                        try:
                            grid[i+1][j] = 2
                        except:
                            pass
                    if RV_SideofWind == 1:
                        try:
                            grid[i][j+1] = 2
                        except:
                            pass
                        try:
                            grid[i][j-1] = 2
                        except:
                            pass
                    if RV_AgainstWind == 1:
                        try:
                            grid[i-1][j] = 2
                        except:
                            pass
                if Wind_Dir == 'E':
                    if RV_DirectionOfWind == 1:
                        try:
                            grid[i][j+1] = 2
                        except:
                            pass
                    if RV_SideofWind == 1:
                        try:
                            grid[i+1][j] = 2
                        except:
                            pass
                        try:
                            grid[i-1][j] = 2
                        except:
                            pass
                    if RV_AgainstWind == 1:
                        try:
                            grid[i][j-1] = 2
                        except:
                            pass

                if Wind_Dir == 'W':
                    if RV_DirectionOfWind == 1:
                        try:
                            grid[i][j-1] = 2
                        except:
                            pass
                    if RV_SideofWind == 1:
                        try:
                            grid[i+1][j] = 2
                        except:
                            pass
                        try:
                            grid[i-1][j] = 2
                        except:
                            pass
                    if RV_AgainstWind == 1:
                        try:
                            grid[i][j+1] = 2
                        except:
                            pass

    newgrid = np.copy(grid)
    return newgrid

# Function 2 (wildfire_metrics) --> Returns proportion of input grid on fire, tree or empty.
def wildfire_metrics(grid):
    "__Function Input__"
    "2 dimensional numpy non-negative integer array"

    "__Function Output__"
    "List with three entries"
    "First entry:  Proportion of input grid with value 2 (site on fire)"
    "Second entry: Proportion of input grid with value 1 (site on with tree)"
    "Third  entry: Proportion of input grid with value 0 (empty site)"

    Proportion_Fire = 0
    Proportion_Tree = 0
    Proportion_Empty = 0
    for i,j in np.ndindex(grid.shape):
        if grid[i][j] == 2:
            Proportion_Fire += 1
        elif grid[i,j] == 1:
            Proportion_Tree += 1
        else:
            Proportion_Empty += 1
    size = (grid.shape[0])**2
    Proportion_Fire /= size
    Proportion_Tree  /= size
    Proportion_Empty /= size
    return[Proportion_Fire, Proportion_Tree, Proportion_Empty]
