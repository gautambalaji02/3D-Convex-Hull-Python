# 3D Convex Hull
The **Incremental Algorithm** was used to generate the convex hull 

## Requirements
1. python 3.0 +: This includes the default packages it comes with
2. An IDE (eg: spyder, VSC)
3. numpy-stl module

## Files Description
1. **Main.py**:

This file contains the code for the convex hull, and uses certain functions from the other python files. It contains the code for initialising and adding points to the convex hull as per the incremental algorithm

2. **Utils.py**

Contains useful functions used by the main.py function in order to simplify several calculations

3. **point_generator.py**

Used to generate set of points in 3D space, without the user's intervention

4. **Exporter.py**

Given the list of points and faces as input, it converts the set into a mesh (a .stl file), to be run on any compatible softwares (Eg: Blender)
