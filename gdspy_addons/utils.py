import gdspy

def union(parts_list):
    union = gdspy.PolygonSet([])
    for p in parts_list:
        union = gdspy.boolean(union, p, 'or')

    return union

def change_layer(geometry, layer):
    geometry.layers = len(geometry.layers)*[layer]
