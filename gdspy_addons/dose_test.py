import gdspy
import numpy as np

from .utils import *

def dose_test(geometry, wf_size, biggest_feature = 0.1):
    """ generate a dose test for the given geometry 

    Args:
        geometry:           gdspy.PolygonSet
        wf_size:            target writefield size
        biggest_feature:    largest feature as a percentage of the writefield size
    """
    smlfeats = []

    for i, p in enumerate(geometry.polygons):
        if p.shape[0] == 4: # only use rectangular features
            X, Y = np.sort(p[:,0]), np.sort(p[:,1])
            smlfeats += [np.abs(X[-1] - X[0]), np.abs(Y[-1] - Y[0])]

    smallest_feature = np.min(smlfeats)

    N_tests = round(1.0/biggest_feature)
    tests = []
    for i in range(N_tests):
        test_atom = gdspy.Path(width = wf_size*biggest_feature)\
                        .segment(0.1*wf_size, '+y')\
                        .translate(wf_size*biggest_feature/2, 0)\
                        .segment(0.3*wf_size, '+y', final_width = smallest_feature)\
                        .segment(0.1*wf_size, '+y')\
                        .translate(i*wf_size/N_tests, 0)
        if i % 2:
            tests.append(test_atom.mirror((1,0)).translate(0, wf_size))
        else:
            tests.append(test_atom)

    pattern = union(tests)
    change_layer(pattern, 10)

    return pattern
