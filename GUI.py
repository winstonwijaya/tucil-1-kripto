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
from crypto import Crypto

Builder.load_file('./GUI.kv')

class FileChoosePopup(Popup):
    load = ObjectProperty()

class RootWidget(ToggleButtonBehavior, FloatLayout):
    def __init__(self,**kwargs):
        super(RootWidget, self).__init__(**kwargs)

        self.popup = ObjectProperty(None)
        self.file_path = ''
        self.radio_selected = 0
        self.cipher_result = 0

    def handleChooseFile(self):
        self.popup = FileChoosePopup(load=self.load)
        self.popup.open()

    def handleSave(self):
        pass

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

    # ENCRYPT
    def handleEncrypt(self, input_text, key):
        result = ''

        # STANDARD VIGENERE CIPHER
        if self.radio_selected == 0:
            result = Crypto().vigenere_standard(input_text,key,0)

        # FULL VIGENERE CIPHER
        elif self.radio_selected == 1:
            result = Crypto().vigenere_full(input_text,key,0)

        # AUTO-KEY VIGENERE CIPHER
        elif self.radio_selected == 2:
            result = Crypto().auto_key_vigenere(input_text,key,0)

        # EXTENDED VIGENERE CIPHER
        elif self.radio_selected == 3:
            result = Crypto().extended_vigenere_encrypt(input_text,key)

        # PLAYFAIR CIPHER
        elif self.radio_selected == 4:
            result = Crypto().playfair_encrypt(input_text,key)

        # SUPER ENCRYPT
        elif self.radio_selected == 5:
            result = Crypto().super_encrypt(input_text,key,0)

        # AFFINE CIPHER
        elif self.radio_selected == 6:
            result = Crypto().affine_cipher(input_text,key,0)

        # HILL CIPHER
        elif self.radio_selected == 7:
            result = Crypto().hill_encrypt(input_text,key)
        
        # SET RESULT
        if self.cipher_result == 1:
            result = Crypto().string_add_seperator(result,5)
        self.ids.result_text.text = result

    # DECRYPT
    def handleDecrypt(self, input_text, key):
        result = ''

        # STANDARD VIGENERE CIPHER
        if self.radio_selected == 0:
            result = Crypto().vigenere_standard(input_text,key,1)

        # FULL VIGENERE CIPHER
        elif self.radio_selected == 1:
            result = Crypto().vigenere_full(input_text,key,1)

        # AUTO-KEY VIGENERE CIPHER
        elif self.radio_selected == 2:
            result = Crypto().auto_key_vigenere(input_text,key,1)

        # EXTENDED VIGENERE CIPHER
        elif self.radio_selected == 3:
            result = Crypto().extended_vigenere_decrypt(input_text,key)

        # PLAYFAIR CIPHER
        elif self.radio_selected == 4:
            result = Crypto().playfair_decrypt(input_text,key)

        # SUPER ENCRYPT
        elif self.radio_selected == 5:
            result = Crypto().super_encrypt(input_text,key,1)

        # AFFINE CIPHER
        elif self.radio_selected == 6:
            result = Crypto().affine_cipher(input_text,key,1)

        # HILL CIPHER
        elif self.radio_selected == 7:
            result = Crypto().hill_decrypt(input_text,key)

        # SET RESULT
        if self.cipher_result == 1:
            result = Crypto().string_add_seperator(result,5)
        self.ids.result_text.text = result
    
    def handleCipherResult(self, current):
        if self.cipher_result != current:
            self.cipher_result = current
        else:
            # RESULT NO SPACE
            if current == 0:
                self.ids.cipher_result_0.state = 'down'
            # RESULT WITH SPACE
            elif current == 1:
                self.ids.cipher_result_1.state = 'down'

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

class MyApp(App):
    def build(self):
        return RootWidget()

if __name__ == '__main__':
    MyApp().run()