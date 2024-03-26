import matplotlib.pyplot as plt
import numpy as np

def generate_random_rectangle():
    x = np.random.rand(2)  # Random x-coordinates
    y = np.random.rand(2)  # Random y-coordinates
    width = abs(x[1] - x[0])  # Width of the rectangle
    height = abs(y[1] - y[0])  # Height of the rectangle
    return x[0], y[0], width, height

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

# Plot bounding rectangle
bounding_rect = plt.Rectangle((min_x, min_y), max_x - min_x, max_y - min_y, edgecolor='red', facecolor='none')
ax.add_patch(bounding_rect)

# Set limits and display
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
plt.gca().set_aspect('equal', adjustable='box')
plt.show()
