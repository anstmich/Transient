from kivy.uix.widget import Widget

class DAQWidget(Widget):
	def on_touch_down(self, touch):
		if(self.collide_point(touch.x, touch.y)):
			print self.id