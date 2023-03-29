import numpy as np
from collections import namedtuple
from point_generator import vertex

# For the polyhedron's sake, all the faces considered will be triangles
face = namedtuple('face', ['v1', 'v2', 'v3'])
'''
Edge: This is the feature that we will be working with the most. Since we will
add/remove faces to an edge

'''
class edge():
    def __init__(self, p1, p2, f1, f2):
        self.vertices = [p1, p2]
        self.adj_faces = [f1, f2]
    
    def edge_features(self):
        print(f'Vertices: {self.vertices[0]}, {self.vertices[1]}')
        print(f'Adjacent Faces: {self.adj_faces[0]}, {self.adj_faces[1]}')
        
def signed_volume(p1, p2, p3, p):     
    return np.linalg.det(np.concatenate([np.array([p1, p2, p3, p]), np.array([[1.0, 1.0, 1.0, 1.0]]).T], axis=1))

def centroid(p1, p2, p3, p4):
    centroid = (np.array(p1) + np.array(p2) + np.array(p3) + np.array(p4)) / 4
    centroid = vertex(centroid[0], centroid[1], centroid[2])
    return centroid
                            
                         
                         
                         