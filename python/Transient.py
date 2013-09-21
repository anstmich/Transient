from kivy.app import App
from kivy.config import Config
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle

from Transient.UI.DAQWidget import DAQWidget, MyWidget, NumericalDisplay
from Transient.UI.Container import Stage, Container, BoxContainer
from Transient.UI.Widgets.PlotWidget import Grid, Plot, PlotBehavior
from Transient.UI.Widgets.PositionTracker import PositionTracker
from Transient.UI.Widgets.TextInput import TInput
from Transient.Backend import SerialDevice, Backend
from Transient.ParseHelper import AsciiFormat
from math import sin, cos, pi
from random import random

class test_rect(Widget):
	def get_emph_size(self, max_w, max_h):
		return (max_w*0.9, max_h*0.9)


class TransientApp(App):

	backend = None
	parser = None
	device = None

	def test_num_display(self, dt):

		lon = []
		lat = []
		speed = []
		erpm = []
		b3 = []
		time = []
		wrpm = []
		TransientApp.backend.get_doubles('long', lon)
		TransientApp.backend.get_doubles('lat', lat)
		TransientApp.backend.get_doubles('speed', speed)
		TransientApp.backend.get_doubles('erpm', erpm)
		TransientApp.backend.get_doubles('wrpm', wrpm)
		TransientApp.backend.get_doubles('b3', b3)
		TransientApp.backend.get_doubles('utc', time)
		if(len(lon) > 0 and len(lat) > 0 and len(speed) > 0 and len(erpm) > 0 and len(b3) > 0):
			spd = speed[-1]
			self.posTrack.update_pos([lon[-1], lat[-1]], spd)
			self.erpm.set_value(erpm[-1])
			self.speed.set_value(spd)
			self.emerg.set_value(b3[-1])
			self.fout.write(str(time[-1]) + ',' + str(spd) + "," + str(erpm[-1]) + "," + str(wrpm[-1]) + "\n")
			print time[-1], spd, erpm[-1], lon[-1], lat[-1], wrpm[-1]

			if(spd > self.maxspeed):
				self.maxspeed = spd
				self.topspeed.set_value(self.maxspeed)
		
		if(self.tinp.mqueued):
			text = self.tinp.get_text()
			TransientApp.backend.send(str( '$' + text + '&'))
			self.tinp.mqueued = False

	def build(self):
		self.count = 0
		self.maxspeed = 0

		self.fout = open('log.dat', 'w')

		Builder.load_file('python/Transient/UI/Transient_UI.kv')
		
		mainlayout = Stage()
		box1 = BoxContainer(2, orientation='vertical')
		box2 = BoxContainer(5)

		button = test_rect()

		box1.set_box_sizes([0.75,0.25])
		box2.set_box_sizes([0.2,0.2,0.2,0.2,0.2])

		self.erpm = NumericalDisplay()
		self.erpm.header_text = 'Engine RPM'
		self.erpm.set_units('RPM')
		self.erpm.set_value(0)
		
		self.speed = NumericalDisplay()
		self.speed.header_text = 'Speed'
		self.speed.set_units('MPH')
		self.speed.set_value(0)

		self.emerg = NumericalDisplay()
		self.emerg.header_text = 'Emergency Button'
		self.emerg.set_units('State')
		self.emerg.set_value(0)

		self.posTrack = PositionTracker()
		self.posTrack.header_text = 'GPS Tracking'

		self.topspeed = NumericalDisplay()
		self.topspeed.header_text = 'Top Speed'
		self.topspeed.set_units('MPH')
		self.topspeed.set_value(0)

		self.tinp = TInput()
		self.tinp.header_text = 'Send a Message'

		box2.add_member(self.speed)
		box2.add_member(self.topspeed)
		box2.add_member(self.erpm)
		box2.add_member(self.emerg)
		box2.add_member(self.tinp)
		box1.add_member(self.posTrack)
		box1.add_member(box2)

        # set up  the backend
		TransientApp.backend = Backend()
		TransientApp.device = SerialDevice('/dev/pts/5', 9600)
		tp = AsciiFormat('<START=$><utc=NUMBER>,<long=NUMBER>,<longdir=UCHAR>, \
				<lat=NUMBER>,<latdir=UCHAR>,<hdop=NUMBER>,<status=UCHAR>,<speed=NUMBER>, \
				<heading=NUMBER>,<erpm=NUMBER>, <wrpm=NUMBER>,<b1=NUMBER>,<b2=NUMBER>,<b3=NUMBER><END=\n>')  
		TransientApp.parser = tp.parser

		TransientApp.backend.set_parser(TransientApp.parser)
		TransientApp.backend.set_device(TransientApp.device)

		mainlayout.add_container(box1)
		self.num = 0
		
		Clock.schedule_interval(self.test_num_display, 1.0/4.0)

		# start the backend
		TransientApp.backend.start()

		return mainlayout

if __name__ == "__main__":

	disp_w, disp_h = [1280,720]

	Config.set('kivy', 'log_enable', 0)
	Config.set('kivy', 'log_level', 'warning')
	Config.set('input', 'mouse', 'mouse,disable_multitouch')
	#Config.set('graphics', 'width', disp_w)
	#Config.set('graphics', 'height', disp_h)
	#Config.set('graphics', 'fullscreen', 'auto') # auto seems broken with gnome 3
	Config.set('graphics', 'fullscreen', 'off')
	Config.set('graphics', 'multisamples', '8')
	transient = TransientApp()

	transient.run()
	transient.backend.stop()
	transient.fout.close()
	#transient.backend.finish()
