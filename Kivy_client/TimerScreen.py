__author__ = 'Eric'
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty, StringProperty, NumericProperty, ListProperty
from kivy.app import App
from kivy.uix.textinput import TextInput
from kivy.lang import Builder


#Builder.load_file("TimerScreen.kv", rulesonly=True)

class TimerScreen(Screen):
    driver_name = StringProperty('')

    def get_time(self, hours, minutes, seconds):
        if ()


class LimitTextInput(TextInput):
    max_char = NumericProperty(None)
    ranges = ListProperty(None)
    upper_limit = NumericProperty(0)

    def insert_text(self, substring, from_undo=False):
        if not from_undo:
            try:
                next_digit = int(substring)
                if (len(self.text) + len(substring) > self.max_char):
                    return #over max char length

                range = self.ranges[len(self.text)] #get ranges from next digit
                if (next_digit < range[0] or next_digit > range[1]):
                    return #next_digit out of range
                if (self.upper_limit != 0 and int(self.text + substring) > self.upper_limit):
                    return #upper limit exceeded even if within numerical bounds

            except ValueError: return
        super(LimitTextInput, self).insert_text(substring, from_undo)






class TimerScreenApp(App):

    def build(self):


        return TimerScreen()

if __name__ == '__main__':
    TimerScreenApp().run()

