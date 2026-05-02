# Camera Fundamentals: Intrinsics, Extrinsics & Projection

> "The real world is 3D. Screens and sensors are 2D. Everything in camera calibration is about making that translation accurate."

---

## The Core Problem

Every time an AR headset places a virtual object on a real table, something had to answer:

> *"Given where this camera is in the world, and given this 3D point in space — where exactly on the screen do I draw it?"*

To answer that, every camera needs to know two things: **where it is** and **how its lens works**.

---

## Extrinsics — "Where is the camera?"

Extrinsics describe the camera's **position and orientation** in the world. Two components:

- **Rotation** — which way is the camera facing? (roll, pitch, yaw)
- **Translation** — where is it sitting? (X, Y, Z in world space)

> 💡 Think of it like a camera crew on a stage: extrinsics tell you where they're standing and which direction they're pointing.

Extrinsics define the transformation from **World Space → Camera Space**.

---

## Intrinsics — "How does this lens see?"

Intrinsics describe the **fixed optical properties** of a specific lens — independent of where the camera is pointing.

| Parameter | What it means |
|-----------|--------------|
| `fx` | Focal length in the horizontal direction (pixels) |
| `fy` | Focal length in the vertical direction (pixels) |
| `cx` | Principal point X — horizontal center of the image |
| `cy` | Principal point Y — vertical center of the image |

> 💡 Think of intrinsics as the prescription of the camera's glasses — fixed to that lens regardless of where it's pointing.

**Why two focal lengths?** Ideally `fx == fy` (square pixels), but manufacturing imperfections can make pixels slightly rectangular. In precision optical work, both are measured separately.

### The Camera Matrix

These four values are packaged into a 3×3 matrix:

```
K = | fx   0   cx |
    |  0  fy   cy |
    |  0   0    1 |
```

This is what calibration teams measure, validate, and store per device.

---

## Projection — "How do we go from 3D to 2D?"

This is the "squishing" step. It uses the **pinhole camera model**.

### The core insight: divide by Z

The further away something is, the smaller it appears on screen. That's captured by dividing by Z (depth):

```
screen_x = (X / Z) * fx + cx
screen_y = (Y / Z) * fy + cy
```

That's it. **Divide by Z, multiply by focal length, shift by principal point.**

### Concrete example

Point in camera space: **(X=2, Y=0, Z=4)**, focal length f=100, screen 1920×1080

```
screen_x = (2 / 4) * 100 + 960 = 50 + 960 = 1010
screen_y = (0 / 4) * 100 + 540 = 0  + 540 = 540
```

The point lands just slightly right of center. ✅

### Why does distance matter?

Same point, twice as far (Z=8):
```
screen_x = (2 / 8) * 100 + 960 = 25 + 960 = 985
```
Twice as far → appears half as far from center. That's perspective.

---

## The Full Pipeline

```
World Space → [Extrinsics] → Camera Space → [Intrinsics] → Screen Space
```

| Stage | What happens |
|-------|-------------|
| **World Space** | Where the point actually is in the real world |
| **Camera Space** | Where the point is relative to the camera (still 3D) |
| **Screen Space** | Where the point gets drawn on the 2D screen |

> ⚠️ If extrinsics are wrong, points are in the wrong place *before* projection. If intrinsics are wrong, they land on the wrong pixel. Both errors look similar on screen but have completely different fixes.

---

## Why This Matters for AR/VR 

In AR, virtual objects must align precisely with the real world. If the camera matrix `K` is even slightly off, **every single rendered point** inherits that error. There's no isolated failure — a bad calibration contaminates the entire scene.

In defense and industrial contexts, that misalignment isn't just annoying — it can be dangerous. That's why calibration teams exist: to measure, validate, and correct these parameters per device, per environment, per use case.

---

## Quick Reference

```
Extrinsics  = rotation + translation       (where is the camera?)
Intrinsics  = fx, fy, cx, cy              (how does the lens work?)
Projection  = screen_x = (X/Z)*fx + cx   (how do we draw it?)
Camera matrix K = 3×3 matrix of intrinsics
```

Next >> [Camera Extrinsics](camera-extrinsics.md)