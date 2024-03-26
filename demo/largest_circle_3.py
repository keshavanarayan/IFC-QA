import numpy as np
import pygad
import plotly.graph_objects as go

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

# Define the fitness function
def fitness_func(ga_instance,solution, solution_idx):
    circle_x, circle_y, radius = solution
    # Check if the circle is within the bounding rectangle
    if (circle_x - radius < min_x) or (circle_x + radius > max_x) or (circle_y - radius < min_y) or (circle_y + radius > max_y):
        return 0  # Return 0 fitness if circle is outside the bounding rectangle
    # Check if the circle intersects with any of the random rectangles
    for rect_coord in rect_coords:
        x_rect, y_rect, width_rect, height_rect = rect_coord
        if (circle_x - x_rect)**2 + (circle_y - y_rect)**2 <= (radius + max(width_rect, height_rect))**2:
            return 0  # Return 0 fitness if circle intersects with a rectangle
    # Return fitness based on the radius of the circle
    return radius


# Define the search space
# Define the search space
num_genes = 3
max_radius = min(max_x - min_x, max_y - min_y) / 2  # Maximum radius is half of the minimum dimension of the bounding rectangle
gene_space = [{'low': min_x, 'high': max_x}, {'low': min_y, 'high': max_y}, {'low': 0, 'high': max_radius}]


# Create the PyGAD instance
ga_instance = pygad.GA(num_generations=50,
                       num_parents_mating=8,
                       mutation_percent_genes=50,
                       sol_per_pop=8,
                       num_genes=num_genes,
                       gene_space=gene_space,
                       fitness_func=fitness_func)

# Run the optimization
ga_instance.run()

# Get the best solution
solution, solution_fitness, solution_idx = ga_instance.best_solution()

# Extract the coordinates of the best circle center and its radius
best_circle_x, best_circle_y, best_radius = solution

# Create figure
fig = go.Figure()

# Add random rectangles to the plot
for rect_coord in rect_coords:
    x_rect, y_rect, width_rect, height_rect = rect_coord
    fig.add_shape(
        type="rect",
        x0=x_rect, y0=y_rect, x1=x_rect + width_rect, y1=y_rect + height_rect,
        line=dict(color="Black"),
    )

# Add bounding rectangle
fig.add_shape(
    type="rect",
    x0=min_x, y0=min_y, x1=max_x, y1=max_y,
    line=dict(color="Red"),
)

# Add largest circle
fig.add_shape(
    type="circle",
    x0=best_circle_x - best_radius, y0=best_circle_y - best_radius, x1=best_circle_x + best_radius, y1=best_circle_y + best_radius,
    line=dict(color="Green"),
)

# Set layout
# Set layout with 1:1 aspect ratio
fig.update_layout(
    xaxis=dict(range=[min_x, max_x], scaleanchor='y', scaleratio=1),
    yaxis=dict(range=[min_y, max_y]),
    showlegend=False
)

# Show plot
fig.show()
