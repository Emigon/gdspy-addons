import gdspy
import numpy as np

from .utils import *

def wf_stitch(geometry, wf_size, overlap = 5, extent = 10e3):
    """ create the write field stitching layer for input geometry

    Args:
        geometry:       gdspy object to define writefield stitches for. the
                        position of this object should be consistent with
                        the desired coordinate system
        wf_size:        write field size in the same units as geometry
        overlap:        the width of the stitch in the same units as geometry
        extent:         defines the square of size 2*extent x 2*extent. the
                        geometry must be entirely contained within this square
                        for the intersection to work correctly
    """
    h_intersect = []
    v_intersect = []
    for x in np.arange(-extent, extent, wf_size):
        horz = gdspy.Rectangle((-extent, x - overlap/2), (extent, x + overlap/2))
        vert = gdspy.Rectangle((x - overlap/2, -extent), (x + overlap/2, extent))
        h_intersect.append(gdspy.boolean(geometry, horz, 'and'))
        v_intersect.append(gdspy.boolean(geometry, vert, 'and'))

    stitches = []

    notnone = lambda x : x is not None

    for polygons in filter(notnone, h_intersect):
        for p in polygons.polygons:
            stitches.append(gdspy.Polygon(p).scale(0.9, 1.0, np.mean(p, axis = 0)))

    for polygons in filter(notnone, v_intersect):
        for p in polygons.polygons:
            stitches.append(gdspy.Polygon(p).scale(1.0, 0.9, np.mean(p, axis = 0)))

    return union(stitches)
