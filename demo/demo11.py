import numpy as np
from scipy.spatial import Voronoi, voronoi_plot_2d
import matplotlib.pyplot as plt

# Define your irregular closed polyline vertices
polyline_vertices = np.array([[0, 0], [2, 0], [2, 1], [1, 1.5], [0, 1]])

# Plot the polyline
plt.plot(polyline_vertices[:, 0], polyline_vertices[:, 1], 'ko-')

# Compute the Voronoi diagram
vor = Voronoi(polyline_vertices)

# Plot the Voronoi diagram (optional for visualization)
voronoi_plot_2d(vor)
plt.plot(polyline_vertices[:, 0], polyline_vertices[:, 1], 'ko')  # Plot the polyline vertices
plt.axis('equal')

# Extract the Voronoi vertices that correspond to the internal edges of the polyline
# These Voronoi vertices represent the median axis
median_axis_vertices = []
for ridge in vor.ridge_vertices:
    if -1 not in ridge:  # -1 indicates a ridge unbounded on one side
        median_axis_vertices.append(vor.vertices[ridge[0]])
        median_axis_vertices.append(vor.vertices[ridge[1]])

# Convert to numpy array for easier manipulation
median_axis_vertices = np.array(median_axis_vertices)

# Plot the median axis
plt.plot(median_axis_vertices[:, 0], median_axis_vertices[:, 1], 'r-')
plt.show()
