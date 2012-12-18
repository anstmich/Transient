from kivy.uix.widget import Widget
from kivy.graphics.texture import Texture
class DAQWidget(Widget):

	def __init__(self, **kwargs):

		self.gradient = Texture.create(size=(1,2))
		buf = [255,255,255,100,255,255,255,255]
		buf = ''.join(map(chr, buf))
		self.gradient.blit_buffer(buf, colorfmt='rgba', bufferfmt='ubyte')

		# define area useable by sub widgets
		self.vis_width = 0
		self.vis_height = 0
		self.vis_pos = [0,0]

		super(DAQWidget, self).__init__(**kwargs)
		

	def on_touch_down(self, touch):
		if(self.collide_point(touch.x, touch.y)):
			print self.id

	def on_size(self, instance, new_size):
		self.vis_width = new_size[0]
		self.vis_height = new_size[1]

	def on_pos(self, instance, new_pos):
		self.vis_pos[0] = new_pos[0] + 5
		self.vis_pos[1] = new_pos[1] + 5