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
from Transient.UI.Colors import UIColors
from Transient.DataRep import OneVector, TwoVector

from Transient.UI.Colors import ColorQueue

# c++ modules
from Transient.DAQWidget_Utils import calculate_points

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
		
class Grid(Widget, Identifiable):

	ID = 0

	def __init__(self, xdivs=10, ydivs=10, **kwargs):
		super(Grid, self).__init__(**kwargs)

		self.xdivs = xdivs
		self.ydivs = ydivs
		self.x_ticks = []
		self.y_ticks = []

		self.dx = 0
		self.dy = 0

		self.move_mode = False
		self.x_i = 0
		self.y_i = 0

		self.gfx_group = str(id(self))

		self.gen_grid()

		self.bind(pos=self.update_position, size=self.update_size)

	def gen_grid(self):
		xdivs = self.xdivs
		ydivs = self.ydivs

		with self.canvas:
			self.canvas.clear()

			Color(*UIColors.OUTLINE)
			self.outline = Rectangle(pos=self.pos, size=self.size, 
				group=self.gfx_group)

			Color(*UIColors.SHADOW)
			self.shadow = Rectangle(pos=[self.x+1, self.y+1], size=[self.width-2, self.height-2], 
				group=self.gfx_group)

			Color(*UIColors.AXES_BG)
			self.fg = Rectangle(pos=[self.x+2, self.y+2], size=[self.width-4, self.height-4], 
				group=self.gfx_group)

			Color(*UIColors.TICK_LINE)

			for i in xrange(0, xdivs):
				tick = Rectangle(pos=[self.x + i/xdivs * self.width, self.y], size=[1, self.height], 
					group=self.gfx_group)
				self.x_ticks.append(tick)

			for i in xrange(0, ydivs):
				tick = Rectangle(pos=[self.x, self.y + i/ydivs*self.height], size=[self.width, 1], 
					group=self.gfx_group)
				self.y_ticks.append(tick)

	def update_position(self, inst, value):
		set_pos(self.outline, *value)
		set_pos(self.shadow, value[0] + 1, value[1] + 1)
		set_pos(self.fg, value[0] + 2, value[1] + 2)

		x = value[0]
		y = value[1]
		xdivs = self.xdivs
		ydivs = self.ydivs
		width = self.width
		height = self.height
		x_ticks = self.x_ticks
		y_ticks = self.y_ticks

		self.update_ticks()

	def update_size(self, inst, value):
		set_size(self.outline, *value)
		set_size(self.shadow, value[0] - 2, value[1] - 2)
		set_size(self.fg, value[0] - 4, value[1] - 4)

		xdivs = self.xdivs
		ydivs = self.ydivs
		x_ticks = self.x_ticks
		y_ticks = self.y_ticks
		width = value[0]
		height = value[1]

		for i in xrange(0, xdivs):
			set_size(x_ticks[i-1], 1, height)
		for i in xrange(0, ydivs):
			set_size(y_ticks[i-1], width, 1)

		self.update_ticks()


	def update_ticks(self):
		x = self.x
		y = self.y
		xdivs = self.xdivs
		ydivs = self.ydivs
		width = self.width
		height = self.height
		x_ticks = self.x_ticks
		y_ticks = self.y_ticks

		if(self.dx == 0):
			set_pos(x_ticks[0], 1.0/xdivs * width + x, y)
		elif(self.dx < 0):
			set_pos(x_ticks[0], self.width + self.dx + x, y)
		else:
			set_pos(x_ticks[0], x + self.dx, y)
		for i in xrange(1, xdivs):
			set_pos(x_ticks[i], x + i*1.0/xdivs * width + self.dx, y)
		
		if(self.dy == 0):
			set_pos(y_ticks[0], x, 1.0/ydivs * height + y)
		elif(self.dy < 0):
			set_pos(y_ticks[0], x, self.height + self.dy + y)
		else:
			set_pos(y_ticks[0], x, y + self.dy)
		for i in xrange(1, ydivs):
			set_pos(y_ticks[i], x, y + i*1.0/ydivs * height + self.dy)

	def set_dx(self, dx):
		xdiv = self.width / self.xdivs
		self.dx = int(dx - int(dx/xdiv)*xdiv)

	def set_dy(self, dy):
		ydiv = self.height / self.ydivs
		self.dy = int(dy - int(dy/ydiv)*ydiv)

	def set_x_divs(self, xdivs):
		self.xdivs = xdivs
		self.x_ticks = [] 
		self.y_ticks = []
		self.gen_grid()

	def set_y_divs(self, ydivs):
		self.ydivs = ydivs
		self.x_ticks = []
		self.y_ticks = []
		self.gen_grid()

	def set_grid_size(self, xdivs, ydivs):
		self.xdivs = xdivs
		self.ydivs = ydivs
		self.x_ticks = []
		self.y_ticks = []
		self.gen_grid()

	def get_actual_pos(self):
		return [self.x + 2, self.y + 2]

	def get_actual_size(self):
		return [self.width - 4, self.height - 4]

class Axes(Widget, Identifiable):

	def __init__(self, xdivs=10, ydivs=10, xmin=0.0, xmax=1.15, 
		ymin=0.0, ymax=1.15, interactable=False, num_digits=5, **kwargs):

		super(Axes, self).__init__(**kwargs)

		self.interactable = interactable

		self.grid = Grid(xdivs, ydivs)
		self.add_widget(self.grid)

		self.xdivs = xdivs
		self.ydivs = ydivs
		self.xmin = xmin
		self.xmax = xmax
		self.ymin = ymin
		self.ymax = ymax
		self.num_digits = 5

		self.dx = 0
		self.dy = 0

		self.xnums = []
		self.ynums = []
		self.xlabel = None
		self.ylabel = None
		self.xlabel_text = ''
		self.ylabel_text = ''
		self.text_holder = Scatter(rotation=90, do_rotation=False, do_scale=False, do_translation=False)
		self.add_widget(self.text_holder)

		self.gfx_group = str(id(self))

		self.move_mode = False
		self.x_i = 0
		self.y_i = 0

		self.generate_labels()

		self.bind(pos=self.update_pos, size=self.update_size)

	def on_touch_down(self, event):
		if(not self.grid.collide_point(event.x, event.y) or not self.interactable):
			return False

		self.move_mode = True
		self.x_i = event.x
		self.y_i = event.y

		return True

	def on_touch_move(self, event):
		if(not self.move_mode):
			return False

		dx = event.x - self.x_i
		dy = event.y - self.y_i

		self.grid.set_dx(dx)
		self.grid.set_dy(dy)
		self.grid.update_ticks()
		self.update_labels()

		return True

	def on_touch_up(self, event):
		if(not self.move_mode):
			return False

		self.move_mode = False
		return True

	def update_pos(self, inst, pos):
		global AXES_PX, PADDING

		self.grid.x = pos[0] + self.num_digits*AXES_PX/2.0 + AXIS_LABEL + PADDING*3
		self.grid.y = pos[1] + AXES_PX + PADDING*2 + AXIS_LABEL

		self.update_labels()

	def update_size(self, inst, size):
		global AXES_PX, PADDING
		self.grid.width = size[0] - (self.num_digits*AXES_PX/2.0 + AXIS_LABEL + 3*PADDING)
		self.grid.height = size[1] - (AXES_PX + AXIS_LABEL + PADDING*2)

		self.update_labels()

	def generate_labels(self):
		global AXIS_LABEL

		x = self.x
		y = self.y
		xdivs = self.grid.xdivs
		ydivs = self.grid.ydivs
		xmin = self.xmin
		xmax = self.xmax
		ymin = self.ymin
		ymax = self.ymax

		xdiv = (xmax - xmin)/(xdivs)
		ydiv = (ymax - ymin)/(ydivs)

		for xn in self.xnums:
			self.remove_widget(xn)
		for yn in self.ynums:
			self.remove_widget(yn)

		if(self.xlabel is not None):
			self.remove_widget(self.xlabel)
		if(self.ylabel is not None):
			self.text_holder.remove_widget(self.ylabel)

		self.xnums = []
		self.ynums = []

		for i in xrange(1, xdivs):
			num = Label(text=Utils.num_to_str(xmin + xdiv*i, self.num_digits), 
				font_size=AXES_PX, group=self.gfx_group)
			self.add_widget(num)
			self.xnums.append(num)

		for i in xrange(1, ydivs):
			num = Label(text=Utils.num_to_str(ymin + ydiv*i, self.num_digits), 
				font_size=AXES_PX, group=self.gfx_group)
			self.add_widget(num)
			self.ynums.append(num)

		self.xlabel = Label(text=self.xlabel_text, 
			font_size=AXIS_LABEL, group=self.gfx_group)
		self.add_widget(self.xlabel)

		self.ylabel = Label(text=self.ylabel_text, font_size=AXIS_LABEL)
		self.text_holder.add_widget(self.ylabel)
		
	
	def update_labels(self):
		x = self.grid.x
		y = self.grid.y
		xdiv = self.grid.width*1.0/self.xdivs
		ydiv = self.grid.height*1.0/self.ydivs

		dx = self.grid.dx
		dy = self.grid.dy

		for i in xrange(0, len(self.xnums)):
			self.xnums[i].center_x = int(x + (i+1)*xdiv + dx)
			self.xnums[i].center_y = int(y - 2 - AXES_PX/2.0)

		for i in xrange(0, len(self.ynums)):
			self.ynums[i].center_x = int(x - (AXES_PX/4.0)*self.num_digits - PADDING)
			self.ynums[i].center_y = int(y + (i+1)*ydiv + dy)

		self.xlabel.center_x = int(self.grid.x + self.grid.width/2)
		self.xlabel.center_y = int(self.y + PADDING)

		self.text_holder.height = 50
		self.text_holder.x = self.x + PADDING
		self.text_holder.center_y = self.y + self.height/2


	def set_x_label(self, text):
		self.xlabel_text = text
		self.xlabel.text = text
		self.generate_labels()
		self.update_labels()

	def set_y_label(self, text):
		self.ylabel_text = text
		self.ylabel.text = text
		self.generate_labels()

	def set_x_divs(self, xdivs):
		self.grid.set_x_divs(xdivs)
		self.xdivs = xdivs
		self.generate_labels()
		self.update_labels()

	def set_y_divs(self, ydivs):
		self.grid.set_y_divs(ydivs)
		self.ydivs = ydivs
		self.generate_labels()
		self.update_labels()

	def set_grid_size(self, xdivs, ydivs):
		self.grid.set_grid_size(xdivs, ydivs)
		self.xdivs = xdivs
		self.ydivs = ydivs
		self.generate_labels()
		self.update_labels()

	def set_x_range(self, xmin, xmax):
		self.xmin = xmin
		self.xmax = xmax
		self.generate_labels()

	def set_y_range(self, ymin, ymax):
		self.ymin = ymin
		self.ymax = ymax
		self.generate_labels()

	# Get the point on grid corresponding to the x, y position on the screen
	def point_at(self, x, y):
		px = (x - self.grid.x)/self.grid.width * (self.xmax - self.xmin) + self.xmin
		py = (y - self.grid.y)/self.grid.height * (self.ymax - self.ymin) + self.ymin
		return (px, py)


class PlotBehavior:
	AUTOSCALED, FIXED, OSCILLOSCOPE = range(3)
	# OSCILLOSCOPE and FIXED not implemented

class PlotTrace2D(Widget, Identifiable):

	def __init__(self, behavior=PlotBehavior.AUTOSCALED, color=(1,0,0,1), **kwargs):
		super(PlotTrace2D, self).__init__(**kwargs)

		self.behavior = behavior
		self.rgb = color

		self.data = TwoVector()
		self.min_x = 0
		self.max_x = 1
		self.min_y = 0
		self.max_y = 1
		self.xlim = [0,1]
		self.ylim = [0,1]

		self.marker_size = 2
		self.trace_width = 1

		self.points = []
		self._points = []
		self.markers = []
		self.line = None
		self.color = None
		
		self.calc_points()
		self._gen_plot()
		
		self.bind(pos=self.update_pos, size=self.update_size)

	def _gen_plot(self):

		self.calc_points()
		del self.markers[:]

		self.canvas.clear()
		with self.canvas:

			self.color = Color(*self.rgb)
			
			for i in xrange(len(self._points)):
				circ = Rectangle(pos=[0,0], size=[self.marker_size, self.marker_size])
				self.markers.append(circ)
			
			self.line = Line(points=self.points, width=self.trace_width)

	def update_pos(self, inst, pos):
		self.calc_points()
		self.line.points = self.points
		self.update_markers()

	def update_size(self, inst, size):
		self.calc_points()
		self.line.points = self.points
		self.update_markers()

	def set_max_x(self, mx):
		self.max_x = mx

	def set_min_x(self, mx):
		self.min_x = mx

	def set_max_y(self, my):
		self.max_y = my

	def set_min_y(self, my):
		self.min_y = my

	def append_value(self, vx, vy):
		self.data.append_value(vx, vy)

		px = self.x + self.width * ((vx - self.min_x) / (self.max_x - self.min_x))
		py = self.y + self.height * ((vy - self.min_y) / (self.max_y - self.min_y))

		self.points.append(px)
		self.points.append(py)

		if(self.behavior == PlotBehavior.FIXED and px <= self.x + self.width and px >= self.x and py >= self.y and py <= self.y + self.width):
			self.line.points += [px, py]

		with self.canvas:
			mark = Rectangle(pos=[px,py], size=[self.marker_size, self.marker_size])
			self.markers.append(mark)

		if(vx < self.min_x):
			self.min_x = vx
		elif(vx > self.max_x):
			self.max_x = vx

		if(vy < self.min_y):
			self.min_y = vy
		elif(vy > self.max_y):
			self.max_y = vy

	def append_multiple(self, xs, ys):
		self.data.append_multiple(xs, ys)

		with self.canvas:
			for x, y in xs, ys:
				px = self.width * (vx/(self.max_x - self.min_x))
				py = self.height * (vy / (self.max_y - self.min_y))

				self.points.append(px)
				self.points.append(py)

				mark = Rectangle(pos=[px, py], size=[self.marker_size, self.marker_size])
				self.markers.append(mark)

		if(vx < self.min_x):
			self.min_x = vx
		elif(vx > self.max_x):
			self.max_x = vx

		if(vy < self.min_y):
			self.min_y = vy
		elif(vy > self.max_y):
			self.max_y = vy

	def autoscale(self):
		self.xlim = [self.min_x, self.max_x]
		self.ylim = [self.min_y, self.max_y]

	def on_touch_down(self, touch):
		return False

	def on_touch_move(self, touch):
		return False

	def on_touch_up(self, touch):
		return False

	def calc_points(self):
		if(self.behavior == PlotBehavior.AUTOSCALED):
			self.autoscale()

		x_range = self.xlim[1] - self.xlim[0]
		y_range = self.ylim[1] - self.ylim[0]

		min_x = self.xlim[0]
		min_y = self.ylim[0]

		del self.points[:]
		del self._points[:]

		calculate_points(self.data.x, self.data.y, len(self.data.x), self.points, self._points,
			self.x+2, self.y+2, x_range, y_range, min_x, min_y, self.width-4, self.height-4)

	def update_markers(self):

		#for m, p in zip(self.markers, self._points):
		#	m.pos = [p[0] - 1, p[1] - 1]
		i = 0
		j = 0
		l = len(self.markers)
		while(i < l):
			self.markers[i].pos = [self.points[j] - 1, self.points[j+1] - 1]
			i += 1
			j += 2

	# Unnecessary if FIXED plot behavior
	def refresh(self):
		if(self.behavior == PlotBehavior.AUTOSCALED):
			self.calc_points()
			self.line.points = self.points
			self.update_markers()
		elif(self.behavior == PlotBehavior.OSCILLOSCOPE):
			pass # TODO: Implement

	def set_color(self, color):
		if(len(color) is 3):
			self.color.rgb = color
			self.rgb = color
		elif(len(color) is 4):
			self.color.rgba = color
			self.rgb = color
		else:
			raise Warning(''.join(['Warning, trace color specified for 2D plot trace, ', self.get_id(), 'is invalid. Check that it is defined using either the rgb or rgba color format.']))


	def set_behavior(self, behavior):
		if(behavior != PlotBehavior.AUTOSCALED and behavior != PlotBehavior.FIXED and behavior != PlotBehavior.OSCILLOSCOPE):
			raise Exception(''.join(['Unknown plot behavior: ', str(behavior)]))

		self.behavior = behavior

	def set_x_range(self, xmin, xmax):
		self.min_x = xmin
		self.max_x = xmax
		self.xlim = [xmin, xmax]

	def set_y_range(self, ymin, ymax):
		self.min_y = ymin
		self.max_y = ymax
		self.ylim = [ymin, ymax]


class PointDisplay(Widget):

	def __init__(self, **kwargs):
		super(PointDisplay, self).__init__(**kwargs)
		#necessary in order to achieve proper sizing
		self.label.bind(texture_size=self.label.setter('size'))
		self.bind(size=self.size_changed)

	def size_changed(self, inst, value):
		self.size = self.label.size

	def set_point(self, x,y):
		self.x_label = Utils.num_to_str(x,4)
		self.y_label = Utils.num_to_str(y,4)


class Plot(Widget):

	def __init__(self, nplots=1, behavior=PlotBehavior.AUTOSCALED, **kwargs):
		super(Plot, self).__init__(**kwargs)

		self.colors = ColorQueue()

		self.nplots = nplots
		self.clip = StencilView(size_hint=(None, None))
		self.traces = []
		for i in xrange(nplots):
			trace = PlotTrace2D(color=self.colors.next_color())
			self.traces.append(trace)
			self.clip.add_widget(trace)
		
		self.axes = Axes()
		self.add_widget(self.axes)
		self.add_widget(self.clip)

		self.pdisplay = PointDisplay()
		self.pd_vis = False
		self.mouse_down = False
		
		# bind a custom mouse motion callback
		Window.bind(mouse_pos=self.on_motion)

	def on_pos(self, *largs):
		
		self.axes.pos = self.pos
		self.clip.pos = [self.axes.grid.x + 2, self.axes.grid.y + 2]
		for t in self.traces:
			t.pos = self.axes.grid.pos

		self.pdisplay.x = self.x + self.width - self.pdisplay.label.texture_size[0]
		self.pdisplay.y = self.y 

	def on_size(self, *largs):
		self.axes.size = self.size
		self.clip.size = [self.axes.grid.width - 4, self.axes.grid.height -4]
		for t in self.traces:
			t.size = self.axes.grid.size

		self.pdisplay.x = self.x + self.width - self.pdisplay.label.texture_size[0]
		self.pdisplay.y = self.y 

	def on_motion(self, inst, value):

		if(self.collide_point(*value)):
			if(not self.pd_vis):
				self.add_widget(self.pdisplay)
				self.pd_vis = True

			self.pdisplay.set_point(*self.axes.point_at(*value))
		elif(self.pd_vis):
			self.pd_vis = False
			self.remove_widget(self.pdisplay)

	def set_autoscale(self, trace, ascale=True):
		if(trace >= len(self.traces)):
			raise Exception('Trace selection for function \'set_autoscale\' exceeds total number of available traces.')
		self.traces[trace].set_autoscale(ascale)

	def set_color(self, color, trace):
		if(trace >= len(self.traces)):
			raise Exception('Trace selection for function \'set_color\' exceeds total number of available traces.')
		else:
			self.traces[trace].set_color(color)

	def append_value(self, x, y, trace):
		if(trace >= len(self.traces)):
			raise Exception('Trace selection for function \'append_value\' exceeds total number of available traces.')
		self.traces[trace].append_value(x,y)

	def refresh(self, trace):
		if(trace >= len(self.traces)):
			raise Exception('Trace selection for function \'refresh\' exceeds total number of available traces.')
		self.traces[trace].refresh()

	def set_xlabel(self, xlabel):
		self.axes.set_x_label(xlabel)

	def set_ylabel(self, ylabel):
		self.axes.set_y_label(ylabel)

	def set_x_range(self, xmin, xmax):
		for t in self.traces:
			t.set_x_range(xmin, xmax)
		
		self.axes.set_x_range(xmin, xmax)

	def set_y_range(self, ymin, ymax):
		for t in self.traces:
			t.set_y_range(ymin, ymax)
		
		self.axes.set_y_range(ymin, ymax)

	def set_behavior(self, behavior):
		for t in self.traces:
			t.set_behavior(behavior)