'''
Last modified: 16.06.2020
here we define the ball class ...
'''

from graphics import *
from table import *
from textures import *

potted_stripes = 0
potted_solids = 0

class Ball:
    def __init__(self, _x, _y, _radius, _vx, _vy, _r, _g, _b, _m, _number):
        self.x = _x
        self.y = _y
        self.radius = _radius
        self.vx = _vx
        self.vy = _vy
        self.r = _r
        self.g = _g
        self.b = _b
        self.m = _m
        self.number = _number
        self.phi = 0.0
        
        '''
        self.shift = False ??
        '''

