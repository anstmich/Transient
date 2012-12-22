from kivy.app import App
from kivy.config import Config
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout

from Transient.UI.DAQWidget import DAQWidget
from Transient.UI.Container import Container,  FlexContainer

class TransientApp(App):
	def build(self):
		Builder.load_file('python/Transient/UI/Transient_UI.kv')
		
		layout = FlexContainer(3, padding=10)
		dwidget1 = DAQWidget()
		dwidget1.header_text = 'Widget 1'
		dwidget2 = DAQWidget()
		dwidget2.header_text = 'Widget 2'
		dwidget3 = DAQWidget()
		dwidget3.header_text = 'Widget 3'
		dwidget1.size = [300,200]
		layout.add_widget(dwidget1)
		layout.add_widget(dwidget2)
		layout.add_widget(dwidget3)
	
		return layout


if __name__ == "__main__":

	disp_w, disp_h = [1280,720]

	Config.set('kivy', 'log_enable', 0)
	Config.set('input', 'mouse', 'mouse,disable_multitouch')
	#Config.set('graphics', 'width', disp_w)
	#Config.set('graphics', 'height', disp_h)
	#Config.set('graphics', 'fullscreen', 'auto') # auto seems broken with gnome 3

	transient = TransientApp()

	transient.run()
