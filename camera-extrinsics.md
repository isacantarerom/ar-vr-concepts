# Camera Extrinsics, Coordinate Systems & Unity

> "Rotating the camera right is the same as rotating the entire world left around you."

---

## Extrinsics — The Full Picture

Extrinsics answer: **where is the camera in the world, and which way is it facing?**

Two components:

- **R** — a 3×3 rotation matrix (orientation)
- **t** — a 3×1 translation vector (position)

Together they transform a point from World Space into Camera Space:

```
P_camera = R * P_world - t
```

**Order matters — rotation always comes before translation.**

---

## Rotation — R

Rotation re-aligns the world axes to match the camera's personal axes.

### The key insight

When you rotate the camera, your personal axes detach from the world axes:

| Before rotation | After 90° right turn |
|---|---|
| World X = your right | World X = your forward |
| World Z = your forward | World Z = your left |

> 💡 Moving in "world X" and moving in "your X" are only the same thing when your rotation is zero.

### Concrete example

Mug at world position **(3, 1, 5)**. Camera rotates 90° to the right:

- World Z=5 (was in front) → now to your left → becomes **X=-5**
- World X=3 (was to your right) → now in front → becomes **Z=3**
- Y=1 unchanged (horizontal rotation)

Result in camera space: **(-5, 1, 3)**

---

## Translation — t

Translation accounts for the camera's position in the world.

After accounting for rotation, subtract the camera's world position:

```
P_camera = R * P_world - t
```

### Concrete example

Camera moves 2 meters in world X (to the right). After the 90° rotation above, world X is now the camera's forward direction — so the mug gets **2 units closer in Z**, not X:

```
(-5, 1, 3) → (-5, 1, 1)
```

> ⚠️ This is the most common bug: assuming world axes and camera axes are aligned when they're not. Always rotate first, then translate.

---

## The Camera Matrix K — Why It's Shaped That Way

```
K = | fx   0   cx |
    |  0  fy   cy |
    |  0   0    1 |
```

Multiplying K by a point **(X, Y, Z)**:

```
| fx   0   cx |   | X |   | fx*X + cx*Z |
|  0  fy   cy | × | Y | = | fy*Y + cy*Z |
|  0   0    1 |   | Z |   |      Z      |
```

Divide everything by Z:

```
screen_x = fx*(X/Z) + cx  ✅
screen_y = fy*(Y/Z) + cy  ✅
```

**Why the zeros?** X only affects screen_x, Y only affects screen_y. No cross-contamination.

**Why (0, 0, 1) on the bottom?** It carries Z through unchanged so we can divide by it at the end.

**K never rotates** — it's a fixed property of the lens hardware. R rotates the world into camera space first, then K projects it onto the screen. Completely separate steps.

---

## FOV → Focal Length in Pixels

Camera specs usually give focal length as a **field of view angle** (degrees). The pipeline needs it in **pixels**.

```
fx = (image_width  / 2) / tan(fov / 2)
fy = (image_height / 2) / tan(fov / 2)
```

### Example — 60° FOV, 1920×1080 screen

```
fx = 960  / tan(30°) = 960  / 0.577 ≈ 1663 pixels
fy = 540  / tan(30°) = 540  / 0.577 ≈ 935  pixels
cx = 960   (half of 1920)
cy = 540   (half of 1080)
```

> 💡 Notice fx ≠ fy even with one focal length — because the screen isn't square. This is exactly why the camera matrix has two separate values.

---

## Coordinate System Mismatch — OpenCV vs Unity

This is the #1 source of bugs when bringing calibration data into Unity.

| | OpenCV (right-handed) | Unity (left-handed) |
|---|---|---|
| X | right | right |
| Y | **down** | **up** |
| Z | forward | forward |

> 💡 **Memory trick:** Unity is "human" — Y up, like a person standing. OpenCV is "camera on a tripod" — Y down.

### The fix

When converting a point from camera space to Unity space, flip Y:

```
Unity_x = Camera_x
Unity_y = -Camera_y    ← flip
Unity_z = Camera_z
```

---

## Unity's Camera Component

Unity does the full pipeline every frame under the hood. It just uses different names:

| What we call it | Unity calls it | How to access |
|---|---|---|
| Extrinsics (R and t) | **View Matrix** | `Camera.main.worldToCameraMatrix` |
| Intrinsics (K) | **Projection Matrix** | `Camera.main.projectionMatrix` |

```csharp
Matrix4x4 V = Camera.main.worldToCameraMatrix;  // Extrinsics
Matrix4x4 P = Camera.main.projectionMatrix;      // Intrinsics
```

---

## The Full Pipeline

```
World Space → [R, t] → Camera Space → [K] → Screen Space → [Flip Y] → Unity Space
```

### End-to-end example

Point **(1, 8, 2)** in camera space, 60° FOV, 1920×1080 screen:

```
fx ≈ 1663,  fy ≈ 935,  cx = 960,  cy = 540

screen_x = (1/2) * 1663 + 960 = 1791.5
screen_y = (8/2) * 935  + 540 = 4280       ← off screen! point is above FOV

Flip Y for Unity:
x = 1791.5
y = -4280
```

The Y result being off-screen tells us the point at Y=8 is way above the camera's field of view — which makes physical sense.

---

## Quick Reference

```
P_camera   = R * P_world - t          (extrinsics transform)
screen_x   = (X/Z) * fx + cx          (projection)
screen_y   = (Y/Z) * fy + cy
fx         = (width/2)  / tan(fov/2)  (FOV to pixels)
fy         = (height/2) / tan(fov/2)
Unity_y    = -Camera_y                 (coordinate flip)
```

<< Prev [Camera fundamentals](camera-fundamentals.md) | Next [] >>