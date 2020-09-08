from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.graphics import Color, Rectangle
from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.behaviors import ToggleButtonBehavior
from main import Crypto

Builder.load_file('./Tucil-1.kv')

class FileChoosePopup(Popup):
    load = ObjectProperty()

class RootWidget(ToggleButtonBehavior, FloatLayout):
    def __init__(self,**kwargs):
        super(RootWidget, self).__init__(**kwargs)

        self.popup = ObjectProperty(None)
        self.file_path = ''
        self.radio_selected = 0

    def handleChooseFile(self):
        self.popup = FileChoosePopup(load=self.load)
        self.popup.open()

    def handleSave(self):
        pass

    # NEED HANDLE ENCRYPTION
    def handleEncrypt(self, input_text, key):
        if self.radio_selected == 0:
            pass
        elif self.radio_selected == 1:
            pass
        elif self.radio_selected == 2:
            pass
        elif self.radio_selected == 3:
            pass
        elif self.radio_selected == 4:
            self.ids.result_text.text = Crypto().PlayfairCipherEncrypt(input_text,key)
        elif self.radio_selected == 5:
            pass
        elif self.radio_selected == 6:
            pass
        elif self.radio_selected == 7:
            self.ids.result_text.text = Crypto().HillCipherEncrypt(input_text,key)

    def handleDecrypt(self, input_text, key):
        if self.radio_selected == 0:
            pass
        elif self.radio_selected == 1:
            pass
        elif self.radio_selected == 2:
            pass
        elif self.radio_selected == 3:
            pass
        elif self.radio_selected == 4:
            self.ids.result_text.text = Crypto().PlayfairCipherDecrypt(input_text,key)
        elif self.radio_selected == 5:
            pass
        elif self.radio_selected == 6:
            pass
        elif self.radio_selected == 7:
            self.ids.result_text.text = Crypto().HillCipherDecrypt(input_text,key)
    
    def handleRadio(self, current):
        if self.radio_selected != current:
            self.radio_selected = current
        else:
            # STANDARD VIGENERE CIPHER
            if current == 0:
                self.ids.radio_0.state = 'down'
            # FULL VIGENERE CIPHER
            elif current == 1:
                self.ids.radio_1.state = 'down'
            # AUTO-KEY VIGENERE CIPHER
            elif current == 2:
                self.ids.radio_2.state = 'down'
            # EXTENDED VIGENERE CIPHER
            elif current == 3:
                self.ids.radio_3.state = 'down'
            # PLAYFAIR CIPHER
            elif current == 4:
                self.ids.radio_4.state = 'down'
            # SUPER ENCRYPT
            elif current == 5:
                self.ids.radio_5.state = 'down'
            # AFFINE CIPHER
            elif current == 6:
                self.ids.radio_6.state = 'down'
            # HILL CIPHER
            elif current == 7:
                self.ids.radio_7.state = 'down'

    # NEED HANDLE LOAD FILE USING FILE_PATH
    # AFTER, CHANGE INPUT TEXT AND ENCRYPT IT
    def load(self, selection):
        self.file_path = str(selection[0])
        self.popup.dismiss()
        self.ids.file_path.text = self.file_path
        
        f = open(self.file_path)
        [content,key] = f.readlines()
        self.ids.input_text.text = content
        self.ids.key_text.text = key
        self.handleEncrypt(content,key)

class MyApp(App):
    def build(self):
        return RootWidget()

if __name__ == '__main__':
    MyApp().run()