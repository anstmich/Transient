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

import timeit

# constants
PADDING = 5
HEADER_HEIGHT = 26

# Font stuff
AXES_PX = 11
AXIS_LABEL = 12

class Identifiable:
	def set_id(self, id):
		self.obj_id = id

	def get_id(self):
		return self.obj_id

class DAQWidget(Layout, Identifiable):

	def __init__(self, **kwargs):

		# define header gradient
		self.gradient = Texture.create(size=(1,2))
		buf = [255,255,255,100,255,255,255,255]
		buf = ''.join(map(chr, buf))
		self.gradient.blit_buffer(buf, colorfmt='rgba', bufferfmt='ubyte')

		super(DAQWidget, self).__init__(**kwargs)

		self.widget = None

	def on_touch_down(self, touch):
		if(self.widget is None):
			return False
		
		if(self.widget.collide_point(touch.x, touch.y)):
			return self.widget.on_touch_down(touch)

	def on_touch_up(self, touch):
		if(self.widget is None):
			return False

		if(self.widget.collide_point(touch.x, touch.y)):
			return self.widget.on_touch_up(touch)

	def get_emph_size(self, max_w, max_h):
		return (max_w*0.9, max_h*0.9)

	def set_widget(self, widget):
		self.widget = widget
		self.add_widget(widget)
		self.do_layout()

	# A DAQWidget is a special type of layout which houses a single visual display
	def do_layout(self, *largs):
		global PADDING, HEADER_HEIGHT

		c = self.widget
		if(c is not None):
			c.x = self.x + PADDING
			c.y = self.y + PADDING
			c.width = self.width - 2*PADDING
			c.height = self.height - 2*PADDING - HEADER_HEIGHT

class MyWidget(Widget, Identifiable):
	def get_emph_size(self, max_w, max_h):
		return (max_w*0.9, max_h*0.9)


class NumericalDisplay(DAQWidget):

	def __init__(self, init_text='NAN', digits=4, **kwargs):
		self.digits = digits

		super(NumericalDisplay, self).__init__(**kwargs)
		self.number_text = init_text

		self.scientific = False
		self.truncated = False

	def set_value(self, val):
		self.value = val
		self.number_text = Utils.num_to_str(val, 4, self.truncated, self.scientific)

	def set_units(self, units):
		self.units = units

	def set_scientific(self, sci=True):
		self.scientific = sci

	def set_truncated(self, trunc=False):
		self.truncated = trunc

	def get_emph_size(self, max_w, max_h):
		return (max_w*0.7, max_h*0.7)
