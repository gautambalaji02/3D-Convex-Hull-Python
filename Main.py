# Libraries 
# For permutations and combinations
import itertools

# Custom Modules
# To create a random set of points
import point_generator
# To create face or edge with the desired vertices
from Utils import face, edge, signed_volume, centroid

# Class to create the convex hull, initialisation and incremental
class Convex_Hull():
    def __init__(self, points):
        self.edges = []
        self.faces = []
        self.vertices = None
        
        print(points)
        self.init_hull(points)
        
    def init_hull(self, points):
        
        # Assigning the first initial vertices
        init_vertices = None
        for i in range((len(points) - 4)):
            init_vertices = points[i: i+4]
            if signed_volume(init_vertices[0], init_vertices[1], init_vertices[2], init_vertices[3]) == 0:
                continue
            else:
                break
        if not init_vertices:
            print('All the points are coplanar, hence no 3D hull exists')
            exit(0)
        self.vertices = init_vertices
        
        '''
        # Centroid
        This centroid point will always be an interior point of the convex hull
        '''
        center = centroid(init_vertices[0], init_vertices[1], init_vertices[2], init_vertices[3])
        
        # Add Faces to the hull
        self.add_face(init_vertices[0], init_vertices[1], init_vertices[2], center)
        self.add_face(init_vertices[0], init_vertices[1], init_vertices[3], center)
        self.add_face(init_vertices[1], init_vertices[2], init_vertices[3], center)
        self.add_face(init_vertices[0], init_vertices[2], init_vertices[3], center)
        
        # Add the edges to the hull
        face_comb = itertools.combinations(self.faces, 2)
        for f in face_comb:
            intersect = set.intersection(set(f[0]), set(f[1]))
            if len(intersect) == 2:
                intersect =  list(intersect)
                self.edges.append(edge(intersect[0], intersect[1], f[0], f[1]))
            else:
                print(f'faces {f[0]} and {f[1]} dont intersect or coincide')
       
        for p in init_vertices:
            points.pop(points.index(p))

        
    # Add faces
    def add_face(self, v1, v2, v3, v4):
        if signed_volume(v1, v2, v3, v4) > 0:
            self.faces.append(face(v1, v2, v3))
            print(face(v1, v2, v3))
            return face(v1, v2, v3)
        elif signed_volume(v1, v2, v3, v4) < 0:
            self.faces.append(face(v1, v3, v2))
            print(face(v1, v3, v2))
            return face(v1, v3, v2)
        else:
            print(f'given points: {v1}, {v2}, {v3} are collinear')
    
    # Check whether point is exterior, and add if exterior to hull
    def add_point(self, p):
        
        # Variables
        interior = True
        visible_faces = []
        boundary_edges = []
        boundary_vertices = []
        new_faces = []
        center = centroid(self.vertices[0], self.vertices[1], self.vertices[2], self.vertices[3])
        
        # Algorithm
        # Check if point is interior or not, add visbile faces
        for Face in self.faces:
            f = list(Face) 
            vol = signed_volume(f[0], f[1], f[2], p)
            if  vol < 0:
                interior = False
                visible_faces.append(Face)
        
        if interior:
            print(f'point {p} is an interior point of the hull')
            return None
        
        # Check for boundary edges
        for Edge in self.edges:
            # Conditions for invisible, boundary and visible edge
            if len(set.intersection(set(Edge.adj_faces), set(visible_faces))) == 1:
                vis_face = set.intersection(set(Edge.adj_faces), set(visible_faces))
        
                Edge.adj_faces.pop(Edge.adj_faces.index(list(vis_face)[0]))
                boundary_edges.append(Edge)
                boundary_vertices = list(set.union(set(boundary_vertices), set(Edge.vertices)))
                
            elif len(set.intersection(set(Edge.adj_faces), set(visible_faces))) == 2:
                self.edges.pop(self.edges.index(Edge))
                
        # Remove visible faces   
        for Face in visible_faces:
             self.faces.pop(self.faces.index(Face))
         
         # Add new faces and edges
        self.vertices.append(p)
         
        for Edge in boundary_edges:
            v1, v2 = Edge.vertices[0], Edge.vertices[1]
            f = self.add_face(v1, v2, p, center)
            new_faces.append(f)
        
        # Add new edges to the hull
        face_comb = itertools.combinations(new_faces, 2)
        for f in face_comb:
            intersect = set.intersection(set(f[0]), set(f[1]))
            if len(intersect) == 2:
                intersect =  list(intersect)
                self.edges.append(edge(intersect[0], intersect[1], f[0], f[1]))
            else:
                print(f'faces {f[0]} and {f[1]} dont intersect or coincide')
             
         
if __name__ == '__main__':
    
    # Variables
    vertices = point_generator.random_point_generator()
    CHull = Convex_Hull(vertices)
    
    vtxs = vertices.copy()
    
    # Adding every point
    for point in vtxs:
        CHull.add_point(point)
        
    
        
    
       
            

            
        
        
        
            



