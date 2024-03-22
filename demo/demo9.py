import numpy as np

class Box3D:
    def __init__(self, points):
        self.points = np.array(points)
    
    def intersects(self, other_box):
        # Check for overlap along each axis
        for i in range(3):  # Check for each dimension (x, y, z)
            self_min = np.min(self.points[:, i])
            self_max = np.max(self.points[:, i])
            other_min = np.min(other_box.points[:, i])
            other_max = np.max(other_box.points[:, i])

            if self_max < other_min or self_min > other_max:
                return False

        return True

# Example usage
points_box1 = [(-2, -2, -2), (-2, -2, 2), (-2, 2, -2), (-2, 2, 2), (2, -2, -2), (2, -2, 2), (2, 2, -2), (2, 2, 2)]
points_box2 = [(-1, -1, -1), (-1, -1, 3), (-1, 3, -1), (-1, 3, 3), (3, -1, -1), (3, -1, 3), (3, 3, -1), (3, 3, 3)]

box1 = Box3D(points_box1)
box2 = Box3D(points_box2)

if box1.intersects(box2):
    print("Boxes intersect")
else:
    print("Boxes do not intersect")
