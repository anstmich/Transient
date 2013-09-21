from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from Transient.UI.DAQWidget import DAQWidget, Identifiable
import Transient.Utilities as Utils
from Transient.Utilities import set_pos, set_size
from Transient.UI.Colors import UIColors, ColorQueue, CMap
from Transient.DataRep import OneVector, TwoVector

class TInput(DAQWidget):

	def __init__(self, **kwargs):

		super(TInput, self).__init__(**kwargs)
		
		self.box = BoxLayout(orientation='vertical', padding=[5,10])
		self.button = Button(text='send!')
		self.inp = TextInput(multiline=False)
		self.box.add_widget(self.inp)
		self.box.add_widget(self.button)

		self.set_widget(self.box)

		self.button.bind(on_press=self.button_clicked)
		self.mqueued = False

		self.inp.bind(on_text_validate=self.on_enter)
		self.text = ''

	def on_touch_down(self, event):
		if(self.inp.collide_point(*event.pos)):
			self.inp.on_touch_down(event)
			return True
		elif(self.button.collide_point(*event.pos)):
			self.button.on_touch_down(event)
			return True
		return False

	def button_clicked(self, arg):
		self.mqueued = True
		self.text = self.inp.text
		self.inp.text = ''

	def get_text(self):
		return self.text

	def on_enter(self, val):
		self.mqueued = True
		self.text = self.inp.text
		self.inp.text = ''

