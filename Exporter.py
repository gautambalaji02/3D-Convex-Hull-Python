# -*- coding: utf-8 -*-
"""
Created on Thu Apr 13 12:38:56 2023

@author: Gautam Balaji
"""
# Libraries
# For converting to STL
from stl import mesh

# Numpy
import numpy as np

# Function
def mesh_converter(points, faces):
    
    # Variables
    f_index = []
    
    # Converting the faces into keys
    for face in faces:
        key = []
        for i in range(3):
            key.append(points.index(face[i]))
        f_index.append(key)
    
    # COnverting to numpy array
    f_index = np.array(f_index)
    points = np.array(points)
    
    # Create the mesh
    poly = mesh.Mesh(np.zeros(f_index.shape[0], dtype=mesh.Mesh.dtype))
    for i, f in enumerate(f_index):
        for j in range(3):
            poly.vectors[i][j] = points[f[j],:]
            
    # Write the mesh to file "polyhedron.stl"
    poly.save('polyhedron.stl')
            
