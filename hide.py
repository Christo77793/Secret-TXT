from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.core.window import Window
from stegano import lsb  # Stegano Library

Window.size = (850, 550)  # Sets the GUI size to start with


class SelectScreen(Screen):  # A class to initialise the screen to choose between encode and decode
    pass


class EncodeScreen(Screen):  # A class to initalise the encode screen

    def set_text(self):  # Fn to get file path
        try:
            self.ids.encode_image_path.text = EncodeScreen.file_path
        except:
            self.ids.encode_image_path.text = "No image selected"

    def encode_txt_img(self):  # Fn to encode our txt to image
        try:
            sel_image = self.ids.encode_image_path.text
            user_text = self.ids.user_text.text
            secret_img = r"C:\Secret Text\encoded_img.png"

            try:
                lsb.hide(sel_image, message=user_text).save(secret_img)

                self.ids.encode_image_path.text = ""
                self.ids.user_text.text = ""

                self.ids.encode_result.text = "Encoding was successful"
            except:

                self.ids.encode_result.text = "Encoding has failed"
        except:

            self.ids.encode_result.text = "Encoding has failed"

    def clear_text(self):  # Fn to clear screen on leaving the screen
        self.ids.encode_image_path.text = ""
        self.ids.user_text.text = ""
        self.ids.encode_result.text = ""


class SelectFileEncode(Screen):  # A class to select a file

    def get_source_encode(self, filename):
        try:
            self.ids.image.source = filename[0]
            EncodeScreen.file_path = filename[0]

        except:
            EncodeScreen.file_path = "No path"


class DecodeScreen(Screen):  # A class to initalise the decode screen

    def set_text(self):  # Fn to get file path
        try:
            self.ids.decode_image_path.text = DecodeScreen.file_path
        except:
            self.ids.decode_image_path.text = "No image selected"

    def decode_img_txt(self):   # Fn to decode our txt from our image
        try:
            sel_image = self.ids.decode_image_path.text
            hidden_text = lsb.reveal(sel_image)
            try:
                self.ids.text_decoded.text = hidden_text

                self.ids.decode_result.text = "Decoding was successful"
            except:
                self.ids.decode_result.text = "Decoding has failed"
        except:
            self.ids.decode_result.text = "Decoding has failed"

    def clear_text(self):  # Fn to clear screen on leaving the screen
        self.ids.decode_image_path.text = ""
        self.ids.text_decoded.text = ""
        self.ids.decode_result.text = ""


class SelectFileDecode(Screen):  # A class to select a file

    def get_source_decode(self, filename):
        try:
            self.ids.image.source = filename[0]
            DecodeScreen.file_path = filename[0]

        except:
            DecodeScreen.file_path = "No path"


class WindowManger(ScreenManager):  # A class to manage between different screens
    pass


kv = Builder.load_file("layout.kv")


class SecretTextApp(App):

    def build(self):
        return kv


if __name__ == '__main__':
    SecretTextApp().run()
