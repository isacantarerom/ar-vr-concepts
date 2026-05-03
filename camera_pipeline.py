import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# ---------------------------------------------
# ---- Define our 3D point in world space  ----
# ---------------------------------------------

point_world = np.array([1,8,2]) #(x,y,z)

# ---------------------------------------------
# ----          Camera parameters          ----
# ---------------------------------------------

image_width     = 1920
image_height    = 1080
fov_degrees     = 60

# Camera position and rotation (Extrinsics) :
camera_position = np.array([0,0,0]) # where the camera sits in the world
rotation_degrees = 0    # rotation around y axis (left/right)


# ---------------------------------------------
# ----      Compute intrinsics from FOV    ----
# ---------------------------------------------


fov_rad = np.radians(fov_degrees) # convert degrees to radians
fx      = (image_width/2) / np.tan(fov_rad / 2)
fy      = (image_height/2) / np.tan(fov_rad/2)
cx      = image_width / 2
cy      = image_height / 2

print("======= INTRINSICS =======")
print(f"fx: {fx:.2f} -- fy: {fy:.2f}")
print(f"cx: {cx:.2f} -- cy: {cy:.2f}")


# ---------------------------------------------
# ----Build rotation matrix (around Y axis)----
# ---------------------------------------------

angle = np.radians(rotation_degrees)
R = np.array([
    [ np.cos(angle), 0, np.sin(angle)],
    [0, 1 , 0],
    [-np.sin(angle), 0, np.cos(angle)]
])

# ---------------------------------------------
# -- Apply extrinsics (world → camera space) --
# ---------------------------------------------

point_camera = R @ (point_world - camera_position)

print("\n=== EXTRINSICS ===")
print(f"Point in world space:  {point_world}")
print(f"Point in camera space: {point_camera}")

# ----------------------------------------
# Apply intrinsics (camera → screen space)
# ----------------------------------------

X, Y, Z = point_camera

if Z <= 0:
    print("Point is behind the camera — not visible!")
else: 
    screen_x = (X/Z) * fx + cx
    screen_y = (Y/Z) *fy + cy

    print("\n=== PROJECTION ===")
    print(f"Screen space (OpenCV): ({screen_x:.2f}, {screen_y:.2f})")

    # ---------------------------------------------
    # --             Flip Y for Unity           ---
    # ---------------------------------------------

    unity_x = screen_x
    unity_y = -screen_y

    print(f"Screen space (unity): ({unity_x:.2f}, {unity_y:.2f})")


    # ---------------------------------------------
    # --              Visualize                 ---
    # ---------------------------------------------
fig = plt.figure(figsize=(12, 5))

# --- Left plot: 3D world space ---
ax1 = fig.add_subplot(121, projection='3d')
ax1.scatter(*point_world, color='red', s=100, label='3D Point')
ax1.scatter(*camera_position, color='blue', s=100, marker='^', label='Camera')
ax1.plot(
    [camera_position[0], point_world[0]],
    [camera_position[1], point_world[1]],
    [camera_position[2], point_world[2]],
    'gray', linestyle='--'
)
ax1.set_xlabel('X')
ax1.set_ylabel('Y')
ax1.set_zlabel('Z')
ax1.set_title('World Space')
ax1.legend()

# --- Right plot: 2D screen space ---
ax2 = fig.add_subplot(122)
ax2.set_xlim(0, image_width)
ax2.set_ylim(-image_height, 0)  # Unity Y is flipped

ax2.set_facecolor('black')

ax2.scatter(unity_x, -unity_y, color='red', s=100, label='Projected Point')
ax2.axhline(-cy, color='gray', linestyle='--', linewidth=0.5)
ax2.axvline(cx, color='gray', linestyle='--', linewidth=0.5)

ax2.set_xlabel('Screen X')
ax2.set_ylabel('Screen Y')
ax2.set_title('Screen Space (Unity)')
ax2.legend()

plt.tight_layout()
plt.show()


    # ---------------------------------------------
    # --   Dot and Cross Product exercises      ---
    # ---------------------------------------------

A = np.array([3,2,1])
B = np.array([1,4,2])

dot = np.dot(A, B)
cross = np.cross(A, B)

print("\n=== DOT & CROSS PRODUCTS ===")
print(f"A = {A}")
print(f"B = {B}")
print(f"A · B (dot)   = {dot}")
print(f"A × B (cross) = {cross}")

print(f"\nAre A and B collinear? {np.all(cross == 0)}")

# ----------------------------------------
# COLLINEAR POINTS CHECK
# ----------------------------------------
P1 = np.array([0, 0, 0])
P2 = np.array([1, 1, 1])
P3 = np.array([2, 2, 2])

A = P2 - P1 # [1 1 1]
B = P3 - P1 # [2 2 2]

# cross: [0][0][0] == collinear

cross = np.cross(A, B)
collinear = np.all(cross == 0)

print("\n=== COLLINEAR CHECK ===")
print(f"P1={P1}, P2={P2}, P3={P3}")
print(f"Vector A (P2-P1) = {A}")
print(f"Vector B (P3-P1) = {B}")
print(f"Cross product    = {cross}")
print(f"Collinear?       = {collinear}")



#
# 
# anchor = points[0]
#for every other point P:
#   A = P2 - anchor   # first vector (fixed)
#    B = P  - anchor   # vector to current point   
#  if cross(A, B) != (0,0,0):
#        not on the same line
# 
# 
# #


# ----------------------------------------
# INTERVIEW SOLUTION — Max collinear points
# ----------------------------------------
def cross_product(a, b):
    return [
        a[1]*b[2] - a[2]*b[1],
        a[2]*b[0] - a[0]*b[2],
        a[0]*b[1] - a[1]*b[0]
    ]

def is_zero(v):
    return v[0] == 0 and v[1] == 0 and v[2] == 0

def subtract(a, b):
    return [a[0]-b[0], a[1]-b[1], a[2]-b[2]]

def max_collinear(points):
    n = len(points)
    if n <= 2:
        return n

    best = 2
    best_line = []

    for i in range(n):
        for j in range(i+1, n):
            ref = subtract(points[j], points[i])
            line = [points[i], points[j]]

            for k in range(n):
                if k == i or k == j:
                    continue
                vec = subtract(points[k], points[i])
                if is_zero(cross_product(ref, vec)):
                    line.append(points[k])

            if len(line) > best:
                best = len(line)
                best_line = line

    return best, best_line

# ----------------------------------------
#  POINTS 
# ----------------------------------------
points = [
    [1,0,0], [5,0,0],
    [8,0,0], [11,0,0],
    [3,5,6], [5,6,7]
]

count, line = max_collinear(points)

print("\n=== COLLINEAR CHECKER ===")
print(f"Total points:        {len(points)}")
print(f"Max collinear:       {count}")
print(f"Points on that line:")
for p in line:
    print(f"  {p}")
 


