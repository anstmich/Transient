from kivy.uix.layout import Layout
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle
from Transient.UI.DAQWidget import DAQWidget
from Transient.Utilities import raise_to_top

class EmphScreen(Widget):
	pass

class Stage(Layout):

	def __init__(self, **kwargs):
		kwargs.setdefault('size', (1,1))
		super(Stage, self).__init__(**kwargs)
		self.bind(
			children=self._trigger_layout,
			pos=self._trigger_layout,
			pos_hint=self._trigger_layout,
			size_hint=self._trigger_layout,
			size=self._trigger_layout)

		self.emph_widget = None

		self.down_event = False
		self.emph_view = False
		self.premph_pos = (0,0)
		self.premph_size = (0,0)
		self.ordered_children = []

		self.emph_screen = EmphScreen()

		self.scale_anim = None
		self.darken_anim = None

		self.container = None

	# dont touch this!
	def do_layout(self, *largs):

		if(not self.emph_view):
			self.container.pos = self.pos
			self.container.size = self.size
			self.container.do_layout(*largs)

	def add_container(self, container):
		container.set_parent_layout(self)
		self.container = container

	def add_widget(self, widget, index=0):
		return super(Layout, self).add_widget(widget, index)
		
	def remove_widget(self, widget):
		return super(Layout, self).remove_widget(widget)

	def on_touch_down(self, event):
		if(not self.emph_view):
			for c in self.children:
				if(c.collide_point(event.x, event.y)):
					self.emph_widget = c

					# pass event to child
					if(not c.on_touch_down(event)):
						self.down_event = True
					
					return True

		else:
			if(not self.emph_widget.collide_point(event.x, event.y)):
				self.down_event = True
				return True
			else:
				if(self.emph_widget.on_touch_down(event)):
					return True
		return False

	def on_touch_up(self, event):

		# pass event to children (they have priority)
		for c in self.children:
			if(c.collide_point(event.x, event.y) and c.on_touch_up(event)):
				return True

		c = self.emph_widget
		if(c is None):
			return False
			
		if(self.down_event):
			if(c.collide_point(event.x, event.y) and not self.emph_view):
		
					self.emph_view = True
					self.down_event = False

					self.add_widget(self.emph_screen)
					self.emph_screen.pos = self.pos
					self.emph_screen.size = self.size

					raise_to_top(self, c)
					
					width, height = self.size
					x, y = self.pos

					e_size = c.get_emph_size(width, height)

					e_pos = [x + (width - e_size[0])/2.0, y + (height - e_size[1])/2.0]
					self.scale_anim = Animation(pos=e_pos, size=e_size, duration=0.15, t='in_sine')
					self.emph_screen.opacity = 0
					self.darken_anim = Animation(opacity=1.0, duration=0.15, t='in_sine')
					
					self.scale_anim.start(c)
					self.darken_anim.start(self.emph_screen)

			elif(not c.collide_point(event.x, event.y)):
				self._trigger_layout()
				self.emph_widget = None
				self.emph_view = False
				self.remove_widget(self.emph_screen)

class Container(Widget):

	def __init__(self, **kwargs):
		self.parent_layout = None
		self.members = []

	def set_parent_layout(self, parent):

		self.parent_layout = parent

		for m in self.members:
			if(isinstance(m, Container)):
				m.set_parent_layout(parent)
			else:
				if(m.parent is None):
					parent.add_widget(m)
					

	def add_member(self, new_mem):
		self.members.append(new_mem)

		if(new_mem.parent is None and self.parent_layout is not None):
			self.parent_layout.add_widget(new_mem)

	def do_layout(self, *largs):
		pass


class BoxContainer(Container):
	def __init__(self, nbox, padding=6, orientation='horizontal', **kwargs):
		super(BoxContainer, self).__init__(**kwargs)
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

	def set_box_sizes(self, sizes):
		if(len(sizes) < self.nbox):
			raise Warning('Not enough sizes to describe FlexContainer contents.')
		elif(sum(sizes) != 1.0):
			raise Warning('Sizes do not add to one.')

		self.box_size = sizes

	def do_layout(self, *largs):

		if(self.size == [1,1]):
			return 

		sw, sh = self.size
		sx, sy = self.pos
		spad = self.padding
		nbox = self.nbox
		bsizes = self.box_size

		# calculations for horizontal and vertical orientation must be separated
		if(self.orientation is 'horizontal'):
			# determine total height of all boxes:
			bh = (sh - (nbox-1)*spad)*1.0

			# determine width of each box
			bw = sw

			# initial point (top left-ish)
			bx = sx
			by = sy + sh

			i = 0
			for m in self.members:
				m.size = [bw, bh*bsizes[i]]
				by -= m.size[1]
				m.pos = [bx, by]
				by -= spad

				
				i+=1

		elif(self.orientation is 'vertical'):
			# total height of each box
			bh = sh

			# total width occupied by all boxes
			bw = sw - (nbox - 1)*spad

			bx = sx
			by = sy

			i = 0
			for m in self.members:
				m.size = [bw*bsizes[i], bh]
				m.pos = [bx, by]

				bx += spad + m.size[0]
				i+=1

		for m in self.members:
			if(isinstance(m, Container)):
				m.do_layout(*largs)