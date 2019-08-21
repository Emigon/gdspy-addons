import gdspy
import numpy as np

def invert(direction):
    if direction[0] == '+':
        return '-' + direction[1]
    else:
        return '+' + direction[1]

def corner_correction(self, direction):
    self.extend_shadow(self.impedance_ratio*self.width/2, direction)
    self.extend_shadow(self.impedance_ratio*self.width/2, invert(direction))

    self.centre_line.segment(self.width/2, direction)
    self.centre_line.segment(self.width/2, invert(direction))

class CoplanarWG(object):
    def __init__(self, width, impedance_ratio = 2, simple = False):
        """ initialises a coplanar waveguide with centre line width and gap ratio

        Args:
            width:              centre line width
            impedance_ratio:    shadow_width = impedance_ratio*width
                                -> defines characteristic impedence of CPW
            simple:             use orthogonal turns instead of circular arcs.
                                useful for sonnet simulations
        """
        self.impedance_ratio = impedance_ratio
        self.simple = simple
        self.length = 0
        self.width = width

        self.centre_line = gdspy.Path(width = width)
        self.shadow = gdspy.Path(width = self.impedance_ratio*width)

    def extend_shadow(self, L, direction, **kwargs):
        self.shadow.segment(L, direction, **kwargs)
        return self # for operation stacking

    def translate_shadow(self, x, y, **kwargs):
        self.shadow.translate(x, y, **kwargs)
        return self # for operation stacking

    def segment(self, L, direction, **kwargs):
        if self.simple and 'final_width' in kwargs:
            self.centre_line.segment(0, direction, **kwargs)
        self.centre_line.segment(L, direction, **kwargs)

        if 'final_width' in kwargs:
            self.width = kwargs['final_width']
            kwargs['final_width'] *= self.impedance_ratio

        if self.simple and 'final_width' in kwargs:
            self.extend_shadow(self.width, direction)
            self.shadow.segment(0, direction, **kwargs)
            self.shadow.segment(L - self.width, direction, **kwargs)
        else:
            self.shadow.segment(L, direction, **kwargs)

        self.length += L

        return self # for operation stacking

    def turn(self, radius, direction):
        if self.simple:
            if direction in ['ll', 'rr']:
                d = self.direction
                self.segment(radius*(np.pi - 2)/2, d)
                corner_correction(self, d)
                self.segment(2*radius, '+y')
                corner_correction(self, '+y')
                self.segment(radius*(np.pi - 2)/2, invert(d))
            else:
                self.segment(radius*(.5*np.pi - 1), self.direction)
                corner_correction(self, self.direction)
                self.segment(radius, '+y')
        else:
            self.centre_line.turn(radius, direction)
            self.shadow.turn(radius, direction)

            if direction in ['ll', 'rr']:
                self.length += np.pi*radius
            else:
                self.length += .5*np.pi*radius

        return self # for operation stacking

    def translate(self, x, y):
        self.centre_line.translate(x, y)
        self.shadow.translate(x, y)

        return self # for operation stacking

    @property
    def x(self):
        return self.centre_line.x

    @property
    def y(self):
        return self.centre_line.y

    @property
    def direction(self):
        return self.centre_line.direction

    @property
    def etch(self):
        return gdspy.boolean(self.shadow, self.centre_line, 'not')
