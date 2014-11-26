

__author__ = 'Eric'
import sys
sys.path.append("../")
from kivy.app import App
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import NumericProperty, ObjectProperty
from drivers import Driver
from controls import DriverControl
import Logon_Client
import message
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen
from PasswordScreen import PasswordScreen
from NameScreen import NameScreen
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
#from chips import MCP23017

from kivy.lang import Builder
Builder.load_file('PasswordScreen.kv', rulesonly=True)
Builder.load_file('NameScreen.kv', rulesonly=True)

class Drivers_Screen(Screen):
    pass

class Rename_Screen(Screen):
    pass



#base widget to be passed to App, responsible for linking control classes with .kv layout and each other
class DriversPanel(BoxLayout):
    #for linking the python widget code with the .kv Markup, establish object property here link in .kv where widgets
    #will actually be initialize

    def __init__(self, **kwargs):
        super(DriversPanel, self).__init__(**kwargs)
        print "initializing root widget"
        print "driver control added"








class DriverInfoWidget(BoxLayout):
    total_drivers_label = ObjectProperty(None)
    total_drivers_on_label = ObjectProperty(None)
    max_drivers_label = ObjectProperty(None)
    remaining_label = ObjectProperty(None)

    total_drivers = NumericProperty(0)
    total_drivers_on = NumericProperty(0)
    max_drivers_on = NumericProperty(0)

    def update(self, newtotal):
        self.total_drivers_on_label.text = 'Total On: {i}'.format(i=newtotal)
        if(newtotal == self.max_drivers_on):
            self.remaining_label.text = 'Remaining: AT LIMIT'
        else:
            self.remaining_label.text = 'Remaining: {i}'.format(i=self.max_drivers_on - newtotal)

class ServerNavBar(BoxLayout):
    pass

class ServerButton(Button):
    name = StringProperty()
    status = StringProperty()









class DriverWidget(BoxLayout):
    name = StringProperty('')
    state = StringProperty('')
    toggle_btn = ObjectProperty(None)
    rename_btn = ObjectProperty(None)
    time_widget = ObjectProperty(None)

    def __init__(self, driverid, name, state, state_time, *args, **kwargs):
        super(DriverWidget,self).__init__(**kwargs)
        print "linking driver widget and driver"
        self.name = name
        self.state = state
        self.driverid = driverid
        self.state_time = state_time

    def on_state(self, instance, value):
        print instance, value
        ON_COLOR = [0, 1, 0, 1] #GREEN
        OFF_COLOR = [1,0,0,1] #RED
        #   [red, green, blue, alpha]
        if self.state=='On':
            self.rbtn.background_color = ON_COLOR
        elif self.state == 'Off':
            self.rbtn.background_color = OFF_COLOR
        else:
            print 'unknown driver state'
            raise Exception

    def update_time(self):
        if self.state == 'Off':
            self.time_widget.text = '00:00:00'
        else:
            self.time_widget.text = self.state_time









class KivyClientApp(App):

    def build(self):
        #non_update_message boolean is checked by scheduled send_request in order to decide whether to simply request
        #an update on the state of the drivers or to send an actual event request(turn on/off, rename, etc)
        self.non_update_message = False
        self.sm = ScreenManager()
        self.password_screen = PasswordScreen(name='PASSWORD_SCREEN')
        self.sm.add_widget(self.password_screen)
        self.drivers_screen = Drivers_Screen(name='DRIVERS_SCREEN')
        self.name_screen = NameScreen(name='NAME_SCREEN')

        self.client = GUI_Client()

        self.drivers_panel = DriversPanel()
        #request update to initialize widgets for driver board

        return self.sm

    def _toggle_event(self, driverid):
        self.non_update_message = True
        self.request = message.Message('toggle', [driverid])

    def _name_event(self, driverid, new_name):
        self.non_update_message = True
        self.request = message.Message('name', [driverid, new_name])

    def request_server_info(self, dt):
        if self.non_update_message:
            print self.request
            self.client.send(self.request)
            self.request = None
            self.non_update_message = False
        else:
            self.client.send(message.Message('update', ['update info']))
        new_driver_info = self.client.receive()
        assert new_driver_info.type == 'motor_response', 'unrecognized response type %s' % new_driver_info.type
        self._update_GUI(new_driver_info.data)

    def _update_GUI(self, new_info):

        widget_driver_pairs = zip(self.widget_drivers, new_info)
        #each driver is a flattened representation with fields (id, name, state, state_time)
        for widget, driver in widget_driver_pairs:
            assert widget.driverid == driver[0], 'widgetid %d driverid %d' % (widget.driverid, driver[0])
            widget.name = driver[1]
            widget.state = driver[2]
            widget.state_time = driver[3]

    def _update_times(self, dt):
        for driver in self.widget_drivers:
            driver.update_time()

    def _generate_drivers_screen(self):
        self.client.send(message.Message('update', ['update info']))
        print 'requested server info'
        #each driver in driver_info is a tuple (id, name, state, state_time) representing a driver on the server side
        for driver in self.client.receive().data:
            print driver
            self.drivers_panel.add_widget(DriverWidget(*driver))

        #must reverse children list, since it is in order of last widget added(id 7) to first(id 0) where the update
        #info is the other way around when matching up with the new driver information received by the servers
        self.widget_drivers = self.drivers_panel.children[:]
        self.widget_drivers.reverse()
        self.drivers_screen.add_widget(self.drivers_panel)

        Clock.schedule_interval(self.request_server_info, 0.1)
        Clock.schedule_interval(self._update_times, 1.0)
        self.sm.switch_to(self.drivers_screen)

    def login(self, username, password):
        response = self.client.login(username, password)
        if (response == 's'):
            self._generate_drivers_screen()
        elif(response == 'u'):
            self.password_screen.invalid_user()
        elif(response == 'p'):
            self.password_screen.invalid_password()
        else:
            pass


    def change_name(self, driverid, name):
        self.name_screen.old_name = name
        self.name_screen.new_name.focus = True
        self.name_screen.identifier = driverid
        self.sm.switch_to(self.name_screen, direction='right')


    def back_to_main(self):
        self.sm.switch_to(self.drivers_screen, direction='left')


class GUI_Client(Logon_Client.Logon_Client):

    def __init__(self):
        super(GUI_Client, self).__init__()
        self.send

    def login(self, username, password):
        #return True #uncomment if you want to just bypass the login screen

            self.send(message.Message('login', [username, password]))


            response = self.receive()
            return response.data[0]






KivyClientApp().run()
