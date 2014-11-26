__author__ = 'Eric'
from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.uix.widget import Widget
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
class NameScreen(RelativeLayout):
    new_name = ObjectProperty(None)

    def set_name(self, new_name):
        print 'hi'

class NameScreenApp(App):

    def build(self):

        return NameScreen()

NameScreenApp().run()