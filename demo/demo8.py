import numpy as np

def find_3d_box(origin, x_axis, extrusion_direction, length, width, height):
    # Normalize vectors
    x_axis = x_axis / np.linalg.norm(x_axis)
    #extrusion_direction = extrusion_direction / np.linalg.norm(extrusion_direction)

    # Calculate other axes
    z_axis = extrusion_direction / np.linalg.norm(extrusion_direction)
    y_axis = np.cross(z_axis, x_axis)

    length = abs(length)
    width = abs(width)
    height = abs(height)

    # Calculate vertices
    
    v0 = origin
    v1 = origin + length * x_axis
    v2 = origin + width * y_axis
    v3 = origin + height * extrusion_direction
    v4 = v1 + width * y_axis
    v5 = v1 + height * extrusion_direction
    v6 = v2 + length * x_axis
    v7 = v3 + length * x_axis

    print(x_axis,y_axis,z_axis)

    # Return vertices
    return np.array([v0, v1, v2, v3, v4, v5, v6, v7])



# Example usage:
origin1 = np.array([0, 0, 0])
x_axis1 = np.array([1, 0, 0])
extrusion_direction1 = np.array([0, 0, -1])
length1 = 1
width1 = 1
height1 = 1

origin2 = np.array([0.5, 0.5, 0.5])
x_axis2 = np.array([1, 0, 0])
extrusion_direction2 = np.array([0, 0, -1])
length2 = 1
width2 = 1
height2 = 1

box1_vertices = find_3d_box(origin1, x_axis1, extrusion_direction1, length1, width1, height1)
box2_vertices = find_3d_box(origin2, x_axis2, extrusion_direction2, length2, width2, height2)

print("Box 1 Vertices:")
print(box1_vertices)
print("Box 2 Vertices:")
print(box2_vertices)

if boxes_intersect(box1_vertices, box2_vertices):
    print("Boxes intersect.")
else:
    print("Boxes do not intersect.")
