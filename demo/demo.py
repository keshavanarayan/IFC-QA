import numpy as np
import plotly.graph_objs as go
from shapely.geometry import Polygon, Point
from shapely.ops import unary_union

def generate_random_points_within_polygon(polygon, num_points):
    min_x, min_y, max_x, max_y = polygon.bounds

    random_points = []
    while len(random_points) < num_points:
        point = Point(np.random.uniform(min_x, max_x), np.random.uniform(min_y, max_y))
        if polygon.contains(point):
            random_points.append([point.x, point.y])

    return np.array(random_points)

# Example polyline
polyline = np.array([[1, 1], [3, 6], [7, 8], [10, 4], [1, 1]])  # Close the polyline with the first point

# Create a shapely polygon from the polyline
polygon = Polygon(polyline)

# Compute the convex hull
convex_hull = polygon.convex_hull

# Offset the convex hull by 1 unit
offset_convex_hull = convex_hull.buffer(1)

# Generate random points within the offset convex hull
num_points = 100
random_points = generate_random_points_within_polygon(offset_convex_hull, num_points)

# Plot the polyline, convex hull, and random points
fig = go.Figure()

# Add polyline trace
fig.add_trace(go.Scatter(x=polyline[:, 0], y=polyline[:, 1], mode='lines', name='Polyline'))

# Add convex hull trace
hull_x, hull_y = offset_convex_hull.exterior.xy
fig.add_trace(go.Scatter(x=hull_x, y=hull_y, mode='lines', name='Convex Hull'))

# Add random points trace
fig.add_trace(go.Scatter(x=random_points[:, 0], y=random_points[:, 1], mode='markers', name='Random Points'))

# Set layout
fig.update_layout(title='Polyline with Convex Hull and Random Points', xaxis_title='X', yaxis_title='Y')

# Show plot
fig.show()
