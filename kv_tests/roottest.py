__author__ = 'Eric'

from kivy.lang import Builder
from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.widget import Widget

Builder.load_string("""
Screen:
    testWidget:

<testWidget>:
    Button:
        on_press: root.button_pressed()

""")

class testWidget(Widget):

    def button_pressed(self):
        print 'pressed'

class testapp(App):

    def build(self):
        return testWidget()

if __name__ =='__main__':
    testapp().run()