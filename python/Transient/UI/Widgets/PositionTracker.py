from Transient.UI.DAQWidget import DAQWidget, Identifiable
from kivy.uix.widget import Widget
from kivy.uix.layout import Layout
from kivy.properties import ListProperty

import Transient.Utilities as Utils
from Transient.Utilities import set_pos, set_size
from Transient.UI.Colors import UIColors, ColorQueue
from Transient.DataRep import OneVector, TwoVector


class Ball(Widget):
	color = ListProperty([0,1.0,0,1.0])

class PositionTracker(DAQWidget):
	trailoff = 50
	max_nodes = 1000

	def __init__(self, **kwargs):

		self.curr_x = 0; self.curr_y = 0
		self.ball = Ball()
		self.ball.pos = self.pos
		self.ball.size = [20,20]
		self.ball_w = 20; self.ball_h = 20
		
		super(PositionTracker, self).__init__(**kwargs)

		self.px = []
		self.py = []
		self.markers = []

		self.minx = self.maxx = 0
		self.miny = self.maxy = 0

		self.first = True

		self.add_widget(self.ball)

		self.manual_marks = []

		self.count = 0

	def update_pos(self, *pos):
		self.curr_x, self.curr_y = pos
		x,y = pos
		self.ball.pos = [self.pos[0]+self.curr_x, self.pos[1]+self.curr_y]

		if(self.first):
			self.first = False
			self.minx = x; self.maxx = x
			self.miny = y; self.maxy = y

		else:
			if(x < self.minx):
				self.minx = x
			elif(x > self.maxx):
				self.maxx = x

			if(y < self.miny):
				self.miny = y
			elif(y > self.maxy):
				self.maxy = y


		if(self.count > PositionTracker.max_nodes):
			self.px.pop()
			self.py.pop()
			end = self.markers.pop()
			self.remove_widget(end)

		self.count += 1
		self.px.insert(0,x)
		self.py.insert(0,y)

		marker = Ball()
		marker.color = [0,1.0,1.0,1.0]
		marker.size = [5,5]
		marker.pos = self.ball.pos
		self.add_widget(marker)
		self.markers.insert(0,marker)
		self.recalc_pos()

	def recalc_pos(self):

		width = self.size[0] - 10
		height = self.size[1] - 36

		w = (self.maxx - self.minx)*1.25
		h = (self.maxy - self.miny)*1.25

		if(w == 0 or h == 0):
			return

		ix = self.pos[0] + 5 + width*0.125
		iy = self.pos[1] + 5 + height*0.125
		
		trailoff = PositionTracker.trailoff
		j = 0
		for m,x,y in zip(self.markers,self.px,self.py):
			rx = (x-self.minx)/w
			ry = (y-self.miny)/h
			m.color = [0,1.0*(trailoff-j)/trailoff,1.0*j/trailoff,0.5 + 0.5*(trailoff-j)/trailoff]
			m.pos = [ix + rx*width, iy + ry*height]
			j += 1
			if(j > trailoff):
				j = trailoff

		rx = (self.curr_x - self.minx)/w
		ry = (self.curr_y - self.miny)/h
		self.ball.pos = [ix + rx*width - self.ball.width/2, iy + ry*height - self.ball.height/2]

	def on_move(self, *largs):
		self.recalc_pos()

	def on_touch_down(self, touch):
		"""
		if(self.in_active_region(*touch.pos)):
			if(touch.button == 'left'):
				mark = Ball()
				mark.color = [1.0,0,0,1.0]
				mark.size = [12,12]
				mark.pos = [touch.x - 6, touch.y - 6]
				self.add_widget(mark)
				self.manual_marks.append(mark)
			elif(touch.button == 'right'):
				mark = None
				for m in self.manual_marks:
					if(m.collide_point(*touch.pos)):
						mark = m
				if(mark != None):
					self.remove_widget(mark)
					self.manual_marks.remove(mark)
			
			return True
			"""
		return False
	def in_active_region(self, x, y):

		if(x > self.x + 10 and x < self.x + self.width - 20 and y > self.y + 10 and y < self.y + self.height - 46):
			return True

		return False
