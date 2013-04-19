from kivy.app import App
from kivy.config import Config
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle

from Transient.UI.DAQWidget import DAQWidget, NumericalDisplay, Grid, Axes, PlotTrace2D, Plot, PlotBehavior
from Transient.UI.Container import Stage, Container, BoxContainer

from math import sin, cos
from random import random

class test_rect(Widget):
	def get_emph_size(self, max_w, max_h):
		return (max_w*0.9, max_h*0.9)


class TransientApp(App):

	def test_num_display(self, dt):
		self.num += 0.1

		self.numdisp.set_value(self.num)

		self._x += 2
		#self.plot.append_value(self._x/10.0, sin(self._x/10.0 + 0.1*random()), 0)
		#self.plot.append_value(self._x/10.0, sin(self._x/10.0 + 0.1*random())*cos(self._x/10.0 + 0.1*random()), 1)
		#self.tizzle.autoscale()
		#self.plot.refresh(0)
		#self.plot.refresh(1)

		self.count += 1
		if(self.count % 250 == 0):
			print self.count, Clock.get_rfps()

	def build(self):
		self.count = 0

		Builder.load_file('python/Transient/UI/Transient_UI.kv')
		
		mainlayout = Stage()
		box1 = BoxContainer(2)
		box2 = BoxContainer(2, orientation='vertical')
		box3 = BoxContainer(2)
		box4 = BoxContainer(2)

		button = test_rect()

		box1.set_box_sizes([0.6,0.4])

		dwidget1 = DAQWidget()
		dwidget1.header_text = 'Widget 1'
		dwidget2 = DAQWidget()
		dwidget2.header_text = 'Widget 2'
		dwidget3 = NumericalDisplay()
		dwidget3.set_units('Accel Time')
		dwidget3.header_text = 'Widget 3'
		dwidget4 = DAQWidget()
		dwidget4.header_text = 'Widget 4'

		self.num = 0
		self._x = 0
		self.numdisp = dwidget3

		self.plot = Plot(2)
		self.plot.set_xlabel('Time')
		self.plot.set_ylabel('RPM')
		self.plot.set_behavior(PlotBehavior.FIXED)
		self.plot.set_x_range(0, 50.0)
		self.plot.set_y_range(-1.0,1)

		dwidget1.set_widget(self.plot)

		grid2 = Plot(2)
		grid2.set_xlabel('Time')
		grid2.set_ylabel('Speed (mph)')
		grid2.set_behavior(PlotBehavior.FIXED)
		grid2.set_x_range(0, 50.0)
		grid2.set_y_range(-1.0,1)

		dwidget2.set_widget(grid2)

		box3.add_member(dwidget3)
		box3.add_member(dwidget4)

		box2.add_member(dwidget2)
		box2.add_member(box3)
		box2.set_box_sizes([0.7,0.3])

		box1.add_member(box2)
		box1.add_member(dwidget1)

		mainlayout.add_container(box1)

		Clock.schedule_interval(self.test_num_display, 1.0/30)
	
		return mainlayout

if __name__ == "__main__":

	disp_w, disp_h = [1280,720]

	Config.set('kivy', 'log_enable', 0)
	Config.set('kivy', 'log_level', 'warning')
	Config.set('input', 'mouse', 'mouse,disable_multitouch')
	#Config.set('graphics', 'width', disp_w)
	#Config.set('graphics', 'height', disp_h)
	#Config.set('graphics', 'fullscreen', 'auto') # auto seems broken with gnome 3
	Config.set('graphics', 'fullscreen', 'False')
	Config.set('graphics', 'multisamples', 0)
	transient = TransientApp()

	transient.run()
