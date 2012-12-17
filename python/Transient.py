from kivy.app import App
from kivy.config import Config
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from Transient_UI_DAQWidget import DAQWidget

class TransientApp(App):
	def build(self):
		Builder.load_file('python/Transient_UI.kv')
		
		layout = BoxLayout(spacing=10, orientation='vertical')
		dwidget1 = DAQWidget()
		dwidget1.id = 'Widget 1'
		dwidget2 = DAQWidget()
		dwidget2.id = 'Widget 2'
		layout.add_widget(dwidget1)
		layout.add_widget(dwidget2)

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
