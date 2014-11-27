__author__ = 'Eric'
from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.widget import Widget
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button

class NameScreen(Screen):
    #old name is passed previous name to be printed on name screen
    old_name = StringProperty('')
    #identifier is used to tell the app, what widget's name is to be changed
    identifier = ObjectProperty(None)
    new_name = ObjectProperty(None)

class NameScreenApp(App):

    def build(self):

        return NameScreen()

if __name__ == '__main__':
    NameScreenApp().run()