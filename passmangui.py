import sys
import os
import kivy
kivy.require('1.9.0')

from kivy.app import App
from kivy.uix.button import Button

from passgen import PassGen
from passdb import PassDb, AccountExistsError, AccountDoesNotExistError, DbLoadError, DbSaveError

class TestApp(App):
    def build(self):
        return Button(text="Hello World")

if __name__ == '__main__':
    TestApp().run()