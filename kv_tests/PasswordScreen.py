__author__ = 'Eric'

from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.gridlayout import GridLayout
from kivy.properties import ObjectProperty
from kivy.core.window import Window

class PasswordScreen(Screen):
    user_label = ObjectProperty(None)
    pl = ObjectProperty(None)
    password_input = ObjectProperty(None)
    user_input = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(PasswordScreen, self).__init__(**kwargs)

    #keyboard is the keyboard instance used to generate the event
    #keycode is a tuple of the (code, 'key')
    #text is repr version of char i.e u/'x'
    #modifers represent ctrl, shift etc
    def _switch(self, instance):
            print instance
            print 'hi'
            self.focus = False
            self.root.password_input.focus = True


    def login_request(self):
        pass





class DriversScreen(Screen):
    pass
class PasswordScreenApp(App):

    def build(self):
        sm = ScreenManager()

        PASSWORD_SCREEN = 'PASSWORD_SCREEN'
        DRIVERS_SCREEN = 'DRIVERS_SCREEN'

        sm.add_widget(PasswordScreen(name=PASSWORD_SCREEN))
        sm.add_widget(DriversScreen(name=DRIVERS_SCREEN))


        return sm

if __name__ == '__main__':
    PasswordScreenApp().run()