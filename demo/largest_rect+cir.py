import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import minimize
import pygad

pygad.GA()

def generate_random_rectangle():
    x = np.random.rand(2)  # Random x-coordinates
    y = np.random.rand(2)  # Random y-coordinates
    width = abs(x[1] - x[0])  # Width of the rectangle
    height = abs(y[1] - y[0])  # Height of the rectangle
    return x[0], y[0], width, height

def is_circle_inside_rectangles(cx, cy, r, rect_coords):
    for x, y, width, height in rect_coords:
        # Calculate distance between circle center and rectangle center
        dx = abs(cx - (x + width / 2))
        dy = abs(cy - (y + height / 2))

        # Calculate distances along the edges of the rectangle
        if dx > width / 2 + r:
            closest_x = x + width
        elif cx < x:
            closest_x = x
        else:
            closest_x = cx

        if dy > height / 2 + r:
            closest_y = y + height
        elif cy < y:
            closest_y = y
        else:
            closest_y = cy

        # Check if distance to closest point is less than or equal to the radius
        if (closest_x - cx) ** 2 + (closest_y - cy) ** 2 <= r ** 2:
            return False  # Circle intersects with rectangle
    return True  # Circle doesn't intersect with any rectangle

def objective(r):
    return -r  # We maximize radius, hence the negative

# Define constraint functions for optimization
def constraint1(r):
    return r

def constraint2(r):
    return bounding_rect[2] - 2 * r

def constraint3(r):
    return bounding_rect[3] - 2 * r

def constraint4(r):
    cx = (min_x + max_x) / 2  # x-coordinate of the center of the bounding rectangle
    cy = (min_y + max_y) / 2  # y-coordinate of the center of the bounding rectangle
    if is_circle_inside_rectangles(cx, cy, r, rect_coords):
        print("no intersection")
        return 10  # Constraint satisfied if circle doesn't intersect with any rectangle
    else:
        print("intersection")
        return -100  # Constraint violated if circle intersects with any rectangle




# Number of rectangles to generate
num_rectangles = 5

# Create a figure and axis
fig, ax = plt.subplots()

# Generate and plot random rectangles
rect_coords = []
for _ in range(num_rectangles):
    x, y, width, height = generate_random_rectangle()
    rect = plt.Rectangle((x, y), width, height, edgecolor='black', facecolor='none')
    ax.add_patch(rect)
    rect_coords.append((x, y, width, height))

# Calculate bounding rectangle
min_x = min(rect_coords, key=lambda r: r[0])[0]
min_y = min(rect_coords, key=lambda r: r[1])[1]
max_x = max(rect_coords, key=lambda r: r[0] + r[2])[0] + max(rect_coords, key=lambda r: r[0] + r[2])[2]
max_y = max(rect_coords, key=lambda r: r[1] + r[3])[1] + max(rect_coords, key=lambda r: r[1] + r[3])[3]
bounding_rect = (min_x, min_y, max_x - min_x, max_y - min_y)

# Plot bounding rectangle
bounding_rect_patch = plt.Rectangle((min_x, min_y), max_x - min_x, max_y - min_y, edgecolor='red', facecolor='none')
ax.add_patch(bounding_rect_patch)

# Set up constraints for optimization
constraints = [{'type': 'ineq', 'fun': constraint1},  # Radius must be positive
               {'type': 'ineq', 'fun': constraint2},  # Circle must fit in x-direction
               {'type': 'ineq', 'fun': constraint3}]  # Circle must fit in y-direction

# Add the new constraint to the list of constraints
constraints.append({'type': 'ineq', 'fun': constraint4})

# Find the largest circle radius
initial_guess = min(bounding_rect[2], bounding_rect[3]) / 4
result = minimize(objective, initial_guess, constraints=constraints, method='SLSQP')

print (result)

# Plot the largest circle
largest_radius = result.x
cx = (min_x + max_x) / 2  # x-coordinate of the center of the bounding rectangle
cy = (min_y + max_y) / 2  # y-coordinate of the center of the bounding rectangle
circle = plt.Circle((cx, cy), largest_radius, edgecolor='blue', facecolor='none')
ax.add_patch(circle)

# Set limits and display
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
plt.gca().set_aspect('equal', adjustable='box')
plt.show()

print(rect_coords)