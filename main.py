'''
Use Ubuntu Kivy VM with buildozer to build APK
'''
import sys
import os
import kivy
kivy.require('1.9.0')

__version__ = "0.0.1"

from kivy.app import App
from kivy.uix.button import Button

from passgen import PassGen
from passdb import PassDb, AccountExistsError, AccountDoesNotExistError, DbLoadError, DbSaveError

class TestApp(App):
    def build(self):
        return Button(text="Hello World")

if __name__ == '__main__':
    TestApp().run()