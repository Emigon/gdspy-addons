#!/usr/bin/python

import gdspy
from gdspy_addons import *

# define a meandering CPW
Wr = 5
L = 2500
Lc = 200
Wc = 10
H = 50
K = .8 
C = 2.0 
wf_width = 500
margin = 25.0
simple = False
Wt = 3*Wc + 2*C*Wc

cpw = CoplanarWG(width = Wc, impedance_ratio = C, simple = simple)

cpw.extend_shadow(Wc*(C - 1)/2, '+x').shadow.translate(-Wc*(C - 1)/2, 0) # end cap
cpw.segment(K*Lc, '+x').segment((1 - K)*Lc, '+x', final_width = Wr) # coupler + taper

segment_length = wf_width - 2*margin - H
cpw.turn(H, 'll').segment(segment_length - H/2, cpw.direction)
x, y = cpw.x, cpw.y # for later repositioning
cpw.turn(H/2, 'rr')

while cpw.length < L:
    d = 'l' if cpw.direction == '+x' else 'r'
    if (L - cpw.length) - segment_length > 3*np.pi*H/4:
        cpw.segment(segment_length, cpw.direction).turn(H/2, 2*d)
    else:
        if (L - np.pi*H/4) - cpw.length > segment_length:
            cpw.segment(segment_length, cpw.direction).turn(H/2, d)
            cpw.segment(L - cpw.length, '+y')
        else:
            cpw.segment((L - np.pi*H/4) - cpw.length, cpw.direction).turn(H/2, d)

# position with respect to the indended writefield
cpw.translate(margin + H/2 - x, 2*H + (1.5 + C)*Wc - y + 100 - 1.5*Wc)

parts = []
parts.append(cpw.etch)
change_layer(parts[0], 2)

bondpad_size = 200
w_feedline = 100

ext = bondpad_size*(C - 1)/2

feedline = CoplanarWG(bondpad_size)\
            .segment(bondpad_size, '+x')\
            .extend_shadow(-ext, '-x')\
            .translate_shadow(-ext, 0)\
            .segment(wf_width - (bondpad_size + ext), '+x', final_width = w_feedline)\
            .segment(1.5*wf_width - margin, '+x')

feedline.translate(-feedline.x + margin, 0)

parts.append(feedline.etch)
parts.append(feedline.etch.mirror((0,1)))

# create gds file and define coordinate system
device = gdspy.Cell('DEVICE')
for p in parts:
    device.add(p.translate(1.5*wf_width, wf_width))

full = union(parts)
stitches = wf_stitch(full, wf_width)
change_layer(stitches, 1)
device.add(stitches)
device.add(dose_test(full, wf_width).translate(0, 2*wf_width))

gdspy.write_gds('lambda_on_4.gds')
