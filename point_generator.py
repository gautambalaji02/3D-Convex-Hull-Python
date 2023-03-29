import random
from collections import namedtuple

# Defining a tuple called vertex. This definition of vertex will be used everywhere in all files
vertex = namedtuple('vertex', ['x', 'y', 'z'])

def random_point_generator( Range = (-30, 30), count = 20):
    Vertices = []
    for i in range(count):
        x = random.randint(Range[0], Range[1])
        y = random.randint(Range[0], Range[1])
        z = random.randint(Range[0], Range[1])
        p = vertex(x = x, y = y, z = z)
        Vertices.append(p)
    
    return Vertices

    