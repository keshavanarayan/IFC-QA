import numpy as np
import pygad
import plotly.graph_objects as go

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

# Define the gene space using points_outside_rectangles and radius
num_genes = 2
gene_space = [np.arange(num_genes), np.linspace(0, max(max_x - min_x, max_y - min_y) / 2, num_genes)]

# Define the fitness function
def fitness_func(ga_instance, solution, solution_idx):
    point_index, radius = solution
    point = points_outside_rectangles[int(point_index)]
    if (point[0] - radius < min_x) or (point[0] + radius > max_x) or (point[1] - radius < min_y) or (point[1] + radius > max_y):
        return 0
    for rect_coord in rect_coords:
        x_rect, y_rect, width_rect, height_rect = rect_coord
        if (point[0] - x_rect)**2 + (point[1] - y_rect)**2 <= (radius + max(width_rect, height_rect))**2:
            return 0
    scaled_radius = radius**5
    return scaled_radius

# Create the PyGAD instance
ga_instance = pygad.GA(num_generations=50,
                       num_parents_mating=4,
                       sol_per_pop=8,
                       num_genes=num_genes,
                       gene_space=gene_space,
                       fitness_func=fitness_func)

# Run the optimization
ga_instance.run()

# Get the best solution
solution, solution_fitness, solution_idx = ga_instance.best_solution()

# Extract the index of the best point and its radius
best_point_index, best_radius = solution

# Extract the coordinates of the best point
best_point = points_outside_rectangles[int(best_point_index)]

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

# Create the point outside rectangles trace
best_point_trace = go.Scatter(
    x=[best_point[0]],
    y=[best_point[1]],
    mode='markers',
    marker=dict(color='blue', size=10),
    name='Best Point'
)

# Create the largest circle shape
circle_shape = {
    'type': 'circle',
    'x0': best_point[0] - best_radius,
    'y0': best_point[1] - best_radius,
    'x1': best_point[0] + best_radius,
    'y1': best_point[1] + best_radius,
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

# Add best point trace
fig.add_trace(best_point_trace)

# Add largest circle shape
fig.add_shape(circle_shape)

# Set layout
fig.update_layout(
    xaxis=dict(range=[min_x - 0.1, max_x + 0.1]),
    yaxis=dict(range=[min_y - 0.1, max_y + 0.1]),
    title="Optimized Largest Circle within Bounding Rectangle",
    xaxis_title="X",
    yaxis_title="Y",
)

# Show plot
fig.show()
