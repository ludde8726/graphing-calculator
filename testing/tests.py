import numpy as np
import matplotlib.pyplot as plt
import time

def implicit_func(x, y, r):
    return (x**2 + y**2 - 1)**3 - (x**2) * (y**3)

r = 1.5

# Define the range of x and y values
x = np.linspace(-r, r, 1000)
y = np.linspace(-r, r, 1000)

# Create a grid of points
x, y = np.meshgrid(x, y)

# Calculate the function value at each point
z = implicit_func(x, y, r)

# Use a contour plot to visualize the function
a = time.perf_counter()
plt.contour(x, y, z, levels=[0], colors='r')
print(time.perf_counter()-a)
plt.show()
