# 3D Convex Hull Generator

A Python implementation of an **incremental 3D Convex Hull algorithm** that constructs a convex hull from a set of 3D points and exports the result as an **STL mesh file**.

---

## Overview

Given a set of 3D points, this project builds the smallest convex polyhedron that contains all of them — the convex hull. It starts by forming an initial tetrahedron from four non-coplanar points, then incrementally adds each remaining point, updating the hull's faces, edges, and vertices as needed. The final hull is exported as `polyhedron.stl`, ready for use in 3D modelling or printing software.

---

## Repository Structure

```
3D-Convex-Hull/
│
├── Main.py               # Entry point — runs the full pipeline
├── Utils.py              # Core geometric primitives: face, edge, signed volume, centroid
├── point_generator.py    # Random 3D point generator
└── Exporter.py           # Converts hull faces/vertices to STL mesh and saves
```

### File Descriptions

| File | Purpose |
|------|---------|
| `Main.py` | Defines the `Convex_Hull` class; handles initialization, incremental point insertion, and cleanup |
| `Utils.py` | Defines `face` and `edge` data structures, `signed_volume` (orientation test), and `centroid` |
| `point_generator.py` | Generates a list of random 3D `vertex` namedtuples within a configurable range |
| `Exporter.py` | Takes hull vertices and faces, builds a `numpy-stl` mesh, and writes `polyhedron.stl` |

---

## Requirements

- Python 3.8+
- Dependencies:

```bash
pip install numpy numpy-stl
```

| Package | Purpose |
|---------|---------|
| `numpy` | Matrix operations, determinant for signed volume |
| `numpy-stl` | STL mesh creation and file export |

---

## How to Run

```bash
python Main.py
```

The script will:
1. Generate 20 random 3D points in the range `(-30, 30)`
2. Build the initial tetrahedron from the first 4 non-coplanar points
3. Incrementally add each remaining point, updating the hull
4. Clean up any interior vertices
5. Save the result as **`polyhedron.stl`** in the working directory

---

## Configuration

In `point_generator.py`, the random point set can be adjusted:

```python
random_point_generator(Range=(-30, 30), count=20)
```

| Parameter | Default | Description |
|-----------|---------|-------------|
| `Range` | `(-30, 30)` | Integer range for x, y, z coordinates |
| `count` | `20` | Number of random points to generate |

---

## Algorithm

The implementation follows the **incremental convex hull** algorithm:

1. **Initialisation** — find 4 non-coplanar points and form a tetrahedron. The centroid of the tetrahedron is used as a guaranteed interior reference point throughout
2. **Interior test** — for each new point, check if it lies inside all existing faces using `signed_volume`. If interior, skip it
3. **Visible face detection** — find all faces visible from the new exterior point (negative signed volume)
4. **Boundary edge detection** — find edges on the boundary between visible and non-visible faces
5. **Update** — remove visible faces, edges, and vertices; connect the new point to all boundary edges to form new faces and edges
6. **Cleanup** — remove any vertices that became interior after the full incremental pass
7. **Export** — convert faces and vertices to an STL mesh

---

## Output

- **`polyhedron.stl`** — binary STL file of the convex hull, importable into any 3D software (Blender, MeshLab, FreeCAD, etc.)

---

## Key Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `count` | `20` | Number of input points |
| `Range` | `(-30, 30)` | Coordinate range for random points |
| `signed_volume` threshold | `0` | Used to determine face orientation and point visibility |

---

## References

- de Berg et al. — *Computational Geometry: Algorithms and Applications* (Chapter 11)
- Incremental convex hull construction algorithm
