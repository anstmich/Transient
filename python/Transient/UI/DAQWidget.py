from kivy.uix.widget import Widget
from kivy.graphics.texture import Texture

class DAQWidget(Widget):

	def __init__(self, **kwargs):

		# define header gradient
		self.gradient = Texture.create(size=(1,2))
		buf = [255,255,255,100,255,255,255,255]
		buf = ''.join(map(chr, buf))
		self.gradient.blit_buffer(buf, colorfmt='rgba', bufferfmt='ubyte')

		super(DAQWidget, self).__init__(**kwargs)

	def on_touch_down(self, touch):
		if(self.collide_point(touch.x, touch.y)):
			print self.id

	def on_pos(self, instance, npos):
		self.diffpos = [10,100]

	def get_emph_size(self, max_w, max_h):
		return (max_w*0.9, max_h*0.9)