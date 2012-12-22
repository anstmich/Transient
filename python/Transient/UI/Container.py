from kivy.uix.layout import Layout
from kivy.clock import Clock

from Transient.UI.DAQWidget import DAQWidget

class Container(Layout):

	def __init__(self, **kwargs):
		kwargs.setdefault('size', (1,1))
		super(Container, self).__init__(**kwargs)
		self.bind(
			children=self._trigger_layout,
			pos=self._trigger_layout,
			pos_hint=self._trigger_layout,
			size_hint=self._trigger_layout,
			size=self._trigger_layout)

		self.emph_widget = None
		self.emph_view = False
		self.premph_pos = (0,0)
		self.premph_size = (0,0)

	# implement in child class
	def do_layout(self, *largs):
		pass

	def add_widget(self, widget, index=0):
		return super(Layout, self).add_widget(widget, index)


	def remove_widget(self, widget):
		return super(Layout, self).remove_widget(widget)

	def on_touch_down(self, event):
		if(not self.emph_view):
			for c in self.children:
				if(c.collide_point(event.x, event.y)):
					self.emph_widget = c
					self.emph_view = True
					self.premph_size = c.size
					self.premph_pos = c.pos

	def on_touch_up(self, event):
		if(self.emph_view):
			if(self.emph_widget.collide_point(event.x, event.y)):
				c = self.emph_widget
				e_size = c.get_emph_size(self.width, self.height)
				c.size = e_size
				c.pos = [self.pos[0] + (self.width - e_size[0])/2.0, self.pos[1] + (self.height - e_size[1])/2.0]

			else:
				self._trigger_layout()
				self.emph_widget = None
				self.emph_view = False

class FlexContainer(Container):
	def __init__(self, nbox, padding=10, orientation='horizontal', **kwargs):
		super(FlexContainer, self).__init__(**kwargs)
		self.nbox = nbox
		self.padding = padding
		self.orientation = orientation

		if(orientation != 'horizontal' and orientation != 'vertical'):
			raise Exception('Invalid orientation chosen for container object')
		if(nbox < 1):
			raise Exception('Must have at least one box.')

		self.box_size = []

		for i in xrange(nbox):
			self.box_size.append(1.0/nbox)

	def set_box_size(self, sizes):
		if(len(sizes) < self.nbox):
			raise Warning('Not enough sizes to describe FlexContainer contents.')
		elif(sum(sizes) != 1.0):
			raise Warning('Sizes do not add to one.')

		self.box_size = sizes

	def do_layout(self, *largs):
		if(self.size == [1,1]):
			return 

		sw = self.width
		sh = self.height
		sx = self.pos[0]
		sy = self.pos[1]
		spad = self.padding
		perim_pad = self.padding/2.0
		nbox = self.nbox
		bsizes = self.box_size

		# calculations for horizontal and vertical orientation must be separated
		if(self.orientation is 'horizontal'):
			# determine total height of all boxes:
			bh = (sh - (nbox-1)*spad - 2*perim_pad)*1.0

			# determine width of each box
			bw = (sw - 2*perim_pad)

			# initial point (top left-ish)
			bx = sx + perim_pad
			by = sy + sh - perim_pad - bh*bsizes[0]

			i = 0
			for c in self.children:
				c.size = [bw, bh*bsizes[i]]
				c.pos = [bx, by]

				by -= spad + c.size[1]
				i+=1




