import numpy as np
import pygad
import plotly.graph_objects as go
import math

# Define function to generate random rectangles
def generate_random_rectangle():
    x = np.random.rand(2)  # Random x-coordinates
    y = np.random.rand(2)  # Random y-coordinates
    width = abs(x[1] - x[0])  # Width of the rectangle
    height = abs(y[1] - y[0])  # Height of the rectangle
    return x[0], y[0], width, height

# Number of rectangles to generate
num_rectangles = 5

# Generate random rectangles
rect_coords = []
for _ in range(num_rectangles):
    x, y, width, height = generate_random_rectangle()
    rect_coords.append((x, y, width, height))

# Calculate bounding rectangle
min_x = min(rect_coords, key=lambda r: r[0])[0]
min_y = min(rect_coords, key=lambda r: r[1])[1]
max_x = max(rect_coords, key=lambda r: r[0] + r[2])[0] + max(rect_coords, key=lambda r: r[2])[2]
max_y = max(rect_coords, key=lambda r: r[1] + r[3])[1] + max(rect_coords, key=lambda r: r[3])[3]

# Define resolution (number of points per unit length)
resolution = 10

# Generate grid points within the bounding rectangle
x_grid = np.linspace(min_x, max_x, int((max_x - min_x) * resolution))
y_grid = np.linspace(min_y, max_y, int((max_y - min_y) * resolution))
grid_points = [(x, y) for x in x_grid for y in y_grid]

# Filter out grid points within random rectangles
points_outside_rectangles = []
for point in grid_points:
    x_point, y_point = point
    is_inside = False
    for rect_coord in rect_coords:
        x_rect, y_rect, width_rect, height_rect = rect_coord
        if x_point >= x_rect and x_point <= x_rect + width_rect and \
           y_point >= y_rect and y_point <= y_rect + height_rect:
            is_inside = True
            break
    if not is_inside:
        points_outside_rectangles.append(point)

# Define the fitness function
"""
def fitness_func(ga_instance, solution, solution_idx):
    circle_x, circle_y, radius = solution
    # Check if the circle is within the bounding rectangle
    if (circle_x - radius < min_x) or (circle_x + radius > max_x) or (circle_y - radius < min_y) or (circle_y + radius > max_y):
        return 0  # Return 0 fitness if circle is outside the bounding rectangle
    # Check if the circle intersects with any of the random rectangles
    for rect_coord in rect_coords:
        x_rect, y_rect, width_rect, height_rect = rect_coord
        if (circle_x - x_rect)**2 + (circle_y - y_rect)**2 <= (radius + max(width_rect, height_rect))**2:
            return 0  # Return 0 fitness if circle intersects with a rectangle
    # Return fitness based on the radius of the circle, scaled to amplify larger radii
    scaled_radius = radius**3  # You can adjust the scaling factor as needed
    return scaled_radius
"""

def fitness_func(ga_instance,solution,solution_idx):
    point_index,radius = solution
    point = points_outside_rectangles[int(point_index)]
    if (point[0] - radius < min_x) or (point[0] + radius > max_x) or (point[1] - radius < min_y) or (point[1] + radius > max_y):
        return 0
    for rect_coord in rect_coords:
        x_rect, y_rect, width_rect, height_rect = rect_coord
        if (point[0] - x_rect)**2 + (point[1] - y_rect)**2 <= (radius + max(width_rect, height_rect))**2:
            return 0
    scaled_radius = radius**5
    return scaled_radius

# Define the gene space using points_outside_rectangles and radius
#num_genes = len(points_outside_rectangles[0]) + 1
num_genes = 2

#gene_space = [{'low': min(point[0] for point in points_outside_rectangles), 'high': max(point[0] for point in points_outside_rectangles)},
#              {'low': min(point[1] for point in points_outside_rectangles), 'high': max(point[1] for point in points_outside_rectangles)},
#              {'low': 0, 'high': max(max_x - min_x, max_y - min_y) / 2}]  # Radius

gene_space = [range(len(points_outside_rectangles)), [0, max(max_x - min_x, max_y - min_y) / 2]]  # Radius


# Create the PyGAD instance
ga_instance = pygad.GA(num_generations=50,
                       num_parents_mating=4,
                       sol_per_pop=8,
                       mutation_percent_genes=50,
                       num_genes=num_genes,
                       gene_space=gene_space,
                       fitness_func=fitness_func)

# Run the optimization
ga_instance.run()

# Get the best solution
solution, solution_fitness, solution_idx = ga_instance.best_solution()

# Extract the coordinates of the best circle center and its radius
best_center, best_radius = solution

best_center = points_outside_rectangles[int(best_center)]

print (f"Best center: {best_center}")
print (f"Best radius: {best_radius}")


# Create the bounding rectangle shape
bounding_rect_shape = {
    'type': 'rect',
    'x0': min_x,
    'y0': min_y,
    'x1': max_x,
    'y1': max_y,
    'line': {'color': 'red'},
    'fillcolor': 'rgba(0,0,0,0)'
}


# Create the random rectangles shapes
rect_shapes = []
for rect_coord in rect_coords:
    x_rect, y_rect, width_rect, height_rect = rect_coord
    rect_shape = {
        'type': 'rect',
        'x0': x_rect,
        'y0': y_rect,
        'x1': x_rect + width_rect,
        'y1': y_rect + height_rect,
        'line': {'color': 'black'},
        'fillcolor': 'rgba(0,0,0,0)'
    }
    rect_shapes.append(rect_shape)

# Create the points outside rectangles scatter trace
points_outside_trace = go.Scatter(
    x=[point[0] for point in points_outside_rectangles],
    y=[point[1] for point in points_outside_rectangles],
    mode='markers',
    marker=dict(color='blue'),
)

# Create the largest circle shape
circle_shape = {
    'type': 'circle',
    'x0': best_center[0] - best_radius,
    'y0': best_center[1] - best_radius,
    'x1': best_center[0] + best_radius,
    'y1': best_center[1] + best_radius,
    'line': {'color': 'green'},
    'fillcolor': 'rgba(0,0,0,0)'
}

# Create figure
fig = go.Figure()

# Add bounding rectangle shape
fig.add_shape(bounding_rect_shape)

# Add random rectangles shapes
for rect_shape in rect_shapes:
    fig.add_shape(rect_shape)

# Add points outside rectangles trace
fig.add_trace(points_outside_trace)

# Add largest circle shape
fig.add_shape(circle_shape)

# Set layout
fig.update_layout(
    xaxis=dict(range=[0, 2], scaleanchor='y', scaleratio=1),
    yaxis=dict(range=[0, 2]),
)

# Show plot
fig.show()
