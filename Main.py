# Libraries 
# For permutations and combinations
import itertools

# For exiting the code
import os

# Custom Modules
# To create a random set of points
import point_generator

# To create face or edge with the desired vertices
from Utils import face, edge, signed_volume, centroid

# To export as an stl file
from Exporter import mesh_converter

# Class to create the convex hull, initialisation and incremental
class Convex_Hull():
    def __init__(self, points):
        self.edges = []
        self.faces = []
        self.vertices = None
        print('\nHull initialized')
        print(points)
        self.init_hull(points)
    
    # Creating the initial tetrahedron with 4 vertices
    def init_hull(self, points):
        print('\nCreating initial hull')
        # Assigning the first initial vertices to form a tetrahrdron
        init_vertices = None
        for i in range((len(points) - 4)):
            init_vertices = points[i: i+4]
            if signed_volume(init_vertices[0], init_vertices[1], init_vertices[2], init_vertices[3]) == 0:
                init_vertices = None
                continue
            else:
                break
            
        # The below condition arises when all points are coplanar
        if not init_vertices:
            print('All the points are coplanar, hence no 3D hull exists')
            os._exit(1)
            
        # The vertices of tetrahedron are initially part of the convex hull
        print('initial vertices created')
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
        print('Initial hull faces created')
        # Add the edges to the hull
        face_comb = itertools.combinations(self.faces, 2)
        for f in face_comb:
            intersect = set.intersection(set(f[0]), set(f[1]))
            if len(intersect) == 2:
                intersect =  list(intersect)
                self.edges.append(edge(intersect[0], intersect[1], f[0], f[1]))
            else:
                print(f'faces {f[0]} and {f[1]} dont intersect or coincide\n')
        print('Initial hull edges created')
        # Removing the 4 tetrahedron vertices from the list of points
        for p in init_vertices:
            points.pop(points.index(p))
        print('tetrahedron hull vertices removed from points set')   
        
        # Features of the hull
        #print(f'\nTetrahedron vertices:\n{self.vertices}')
        #print(f'\nTetrahedron faces:\n{self.faces}')
        #for i in range(len(self.edges)):
        #    Edge = self.edges[i]
        #    print(f'\nEdge {i+1}:')
        #    Edge.edge_features()
        
    # To check whether point is an interior point
    def interior(self, p):
        for Face in self.faces:
            f = list(Face) 
            vol = signed_volume(f[0], f[1], f[2], p)
            if  vol <= 0:
                if vol == 0:
                    print(f'{p} is a surface point')
                return False
            
        return True
    
    # Add faces
    def add_face(self, v1, v2, v3, v4):
        # Normal facing outwards
        if signed_volume(v1, v2, v3, v4) > 0:
            self.faces.append(face(v1, v2, v3))
            #print(face(v1, v2, v3))
            return face(v1, v2, v3)
        # Normal facing inwards
        elif signed_volume(v1, v2, v3, v4) < 0:
            self.faces.append(face(v1, v3, v2))
            #print(face(v1, v3, v2))
            return face(v1, v3, v2)
        # Points happen to be collinear
        else:
            print(f'given points: {v1}, {v2}, {v3} are collinear\n')
    
    # Check whether point is exterior, and add if exterior to hull
    def add_point(self, p):
        # Algorithm
        # Check if point is interior or not
        
        int_point = self.interior(p)
        
        if int_point:
            print(f'point {p} is an interior point of the hull\n')
            return None
        print(f'{p} is an exterior point')
        # Variables
        visible_faces = []
        new_faces = []
        
        boundary_edges = []
        visible_edges = []
        new_edges = []
        
        visible_vertices = []
        boundary_vertices = []
        
        center = centroid(self.vertices[0], self.vertices[1], self.vertices[2], self.vertices[3])
        
        # Find visible faces - for an exterior point
        print('\nFinding visible faces:\n')
        for Face in self.faces:
            f = list(Face) 
            vol = signed_volume(f[0], f[1], f[2], p)
            if vol < 0:
                visible_faces.append(Face)
                print(f'visible face: {Face}')
        
        # Check for boundary edges
        print('\nFinding boundary and visible edges')
        for i in range(len(self.edges)):
            Edge = self.edges[i]
            #print(f'\nEdge {i+1}:')
            #Edge.edge_features()
            
            # Conditions for invisible, boundary and visible edge
            q = set.intersection(set(Edge.adj_faces), set(visible_faces))
            if len(q) == 1:
                #print('Boundary edge features:')
                #Edge.edge_features()
                # Finding the visible face and adding it to list of visible faces
                vis_face = set.intersection(set(Edge.adj_faces), set(visible_faces))
                visible_faces = list(set.union(set(visible_faces), set(vis_face)))       
                
                # Finding the visible vertex and adding to list of visible vertices
                vis_vertex = set.intersection(set(Edge.vertices), set(vis_face))
                if vis_vertex:
                    #print(f'\nvisible vertex: {vis_vertex}')
                    visible_vertices = list(set.union(set(visible_vertices), vis_vertex))
        
                # Removing the visible face from the edge and adding it to list of boundary edges
                Edge.adj_faces.pop(Edge.adj_faces.index(list(vis_face)[0]))
                boundary_edges.append(Edge)
                
                # Adding the boundary vertices to the list 
                boundary_vertices = list(set.union(set(boundary_vertices), set(Edge.vertices)))
                #print(f'\nboundary vertices:\n{boundary_vertices}\n')
            elif len(q) == 2:
                # Adding the edge from the list of visible edges
                #print('Visible edge features:')
                #Edge.edge_features()
                visible_edges.append(Edge)
                
                # Adding the visible adjacent faces to visible faces
                visible_faces = list(set.union(set(visible_faces), set(Edge.adj_faces[0])))      
                visible_faces = list(set.union(set(visible_faces), set(Edge.adj_faces[1])))  
                #print(f'\nVisible faces: {visible_faces}')
                # Adding the edge vertices to the visible vertices list
                visible_vertices = list(set.union(set(visible_vertices), Edge.vertices[0]))
                visible_vertices = list(set.union(set(visible_vertices), Edge.vertices[1]))
                
        # Avoiding repeating of edges       
        visible_edges = list(set(visible_edges))
        boundary_edges = list(set(boundary_edges))
        
        # Checking if there are common points in boundary and visible vertices list
        visible_vertices = list(set(visible_vertices).difference(set(boundary_vertices)))
                
        # Remove visible faces, edges and vertices from the convex hull
        self.faces = list(set(self.faces).difference(set(visible_faces)))
        self.vertices = list(set(self.vertices).difference(set(visible_vertices)))
        self.edges = list(set(self.edges).difference(set(visible_edges)))
            
        # Add new faces and edges and vertices
        # New vertex 
        self.vertices.append(p)
        
        # New Face
        print('\nCreating new faces')
        for Edge in boundary_edges:
            v1, v2 = Edge.vertices[0], Edge.vertices[1]            
            f = self.add_face(v1, v2, p, center)
            Edge.adj_faces.append(f)
            new_faces.append(f)
            #print(f'\nNew faces:\n{new_faces}')
        
        # Add new edges to the hull
        print('\nCreating new edges')
        face_comb = itertools.combinations(new_faces, 2)
        for f in face_comb:
            intersect = set.intersection(set(f[0]), set(f[1]))
            if len(intersect) == 2:
                intersect =  list(intersect)
                e = edge(intersect[0], intersect[1], f[0], f[1])
                new_edges.append(e)
                self.edges.append(e)
            else:
                print(f'faces {f[0]} and {f[1]} dont intersect or coincide\n')
        #print('\nNew edges:')
        for i in range(len(new_edges)):
            Edge = new_edges[i]
            #print(f'Edge {i+1}:')
            #Edge.edge_features()
    def cleanup(self, p):
        if self.interior(p) and set.intersection(set(p), set(self.vertices)):
            self.vertices.pop(self.vertices.index(p))
            
         
if __name__ == '__main__':
    
    # Variables
    vertices = point_generator.random_point_generator()
    vtxs_1 = vertices.copy()
    vtxs_2 = vertices.copy()
    CHull = Convex_Hull(vertices)
    
    # Adding every point
    for point in vtxs_1:
       print(f'\n---------------------------------\nnew vertex: {point}\n---------------------------------')
       CHull.add_point(point)
    
    # Cleanup of vertices    
    print('\n---------------------------------\nCleanup\n---------------------------------\n')

    for point in vtxs_2:
        CHull.cleanup(point)
    
    # Convertig to mesh
    mesh_converter(CHull.vertices, CHull.faces)
    
       
            

            
        
        
        
            



