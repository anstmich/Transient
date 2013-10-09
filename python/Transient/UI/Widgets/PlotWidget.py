from Transient.UI.DAQWidget import DAQWidget, Identifiable
from kivy.uix.widget import Widget
from kivy.uix.stencilview import StencilView
from kivy.graphics.texture import Texture
from kivy.graphics import Line, Color, Rectangle, Ellipse, Bezier, Point
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.uix.layout import Layout
from kivy.uix.scatter import Scatter
from kivy.core.window import Window
from math import sin, pi
from random import random

import Transient.Utilities as Utils
from Transient.Utilities import set_pos, set_size
from Transient.UI.Colors import UIColors, ColorQueue
from Transient.DataRep import OneVector, TwoVector

# c++ modules
from Transient.Utils.DAQWidget_Utils import calculate_points

class Plot(DAQWidget):
	pass
