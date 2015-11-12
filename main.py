import sys
import os
import kivy
kivy.require('1.9.0')

__version__ = "0.0.1"

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.listview import ListView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label

from passgen import PassGen
from passdb import PassDb, AccountExistsError, AccountDoesNotExistError, DbLoadError, DbSaveError

class LoginScreen(GridLayout):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.cols = 2
        self.add_widget(Label(text="Passphrase"))
        self.passphrase = TextInput(password=True,multiline=False)
        self.add_widget(self.passphrase)

class PassManApp(App):
    def build(self):
        return LoginScreen()

if __name__ == '__main__':
    PassManApp().run()