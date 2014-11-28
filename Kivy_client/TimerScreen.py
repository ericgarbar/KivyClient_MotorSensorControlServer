__author__ = 'Eric'
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty, StringProperty, NumericProperty, ListProperty
from kivy.app import App
from kivy.uix.textinput import TextInput
from kivy.lang import Builder


#Builder.load_file("TimerScreen.kv", rulesonly=True)

class TimerScreen(Screen):
    name = StringProperty('')
    driverid = NumericProperty(0)
    hours_input = ObjectProperty(None)
    minutes_input = ObjectProperty(None)
    seconds_input = ObjectProperty(None)

    def get_time(self, hours, minutes, seconds):
        total_seconds = 0
        if (len(hours) != 0):
            total_seconds += int(hours) * 3600
        if (len(minutes) != 0):
            total_seconds += int(minutes) * 60
        if (len(seconds) != 0):
            total_seconds += int(seconds)
        return total_seconds

    def reset_fields(self):
        self.hours_input.text = ''
        self.minutes_input.text = ''
        self.seconds_input.text = ''

class LimitTextInput(TextInput):
    max_char = NumericProperty(None)
    ranges = ListProperty()
    upper_limit = NumericProperty(0)

    def insert_text(self, substring, from_undo=False):
        if not from_undo:
            try:
                next_digit = int(substring)
                if (len(self.text) + len(substring) > self.max_char):
                    return #over max char length

                if (self.upper_limit != 0 and int(self.text + substring) > self.upper_limit):
                    return #upper limit exceeded even if within numerical bounds

            except ValueError: return
        super(LimitTextInput, self).insert_text(substring, from_undo)






class TimerScreenApp(App):

    def build(self):


        return TimerScreen()

if __name__ == '__main__':
    TimerScreenApp().run()

