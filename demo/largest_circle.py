import numpy as np
from scipy.optimize import minimize
import matplotlib.pyplot as plt
from shapely.geometry import Polygon, Point

# Define the objective function to minimize (e.g., fitting error)
def objective(params, polyline):
    # params: (x_center, y_center, radius)
    x_center, y_center, radius = params
    # Create a circle object
    circle = Point(x_center, y_center).buffer(radius)
    # Create a polygon object from the polyline
    poly = Polygon(polyline)
    # Calculate fitting error (penalize points outside the polygon)
    error = poly.symmetric_difference(circle).area
    return error

# Example polyline (list of points)
polyline = [(0, 0), (0, 4), (4, 4), (4, 2), (7, 0), (0, 0)]  # Closing the polyline by adding the first point at the end

# Initial guess for circle parameters
# Center: centroid of polyline points
x_center_guess = np.mean([point[0] for point in polyline])
y_center_guess = np.mean([point[1] for point in polyline])
# Radius: half of the minimum distance between the centroid and any polyline point
radius_guess = min(np.sqrt((x - x_center_guess)**2 + (y - y_center_guess)**2) for x, y in polyline) / 2

# Define the initial guess for the circle
initial_guess = [x_center_guess, y_center_guess, radius_guess]

# Run optimization to ensure the circle remains within the polyline
result = minimize(objective, initial_guess, args=(polyline,), method='Nelder-Mead')

x_center, y_center, radius = result.x

# Plot polyline
polyline_x = [point[0] for point in polyline]
polyline_y = [point[1] for point in polyline]
plt.plot(polyline_x, polyline_y, 'b-', label='Polyline')

# Plot fitted circle
theta = np.linspace(0, 2*np.pi, 100)
circle_x = x_center + radius * np.cos(theta)
circle_y = y_center + radius * np.sin(theta)
plt.plot(circle_x, circle_y, 'r-', label='Fitted Circle')

plt.title('Fitted Circle within Polyline')
plt.xlabel('X')
plt.ylabel('Y')
plt.legend()
plt.grid(True)
plt.axis('equal')

plt.show()
