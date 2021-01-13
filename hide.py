import os
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
# from kivy.core.window import Window
from stegano import lsb, exifHeader  # Stegano Library {lsb -> png, exifHeader -> jpg/jpeg}


# Window.size = (850, 550)  # Sets the GUI size to start with


class SelectScreen(Screen):  # A class to initialise the screen to choose between encode and decode
    pass


class EncodeScreen(Screen):  # A class to initialise the encode screen

    def set_text(self):  # Fn to get file path

        try:
            self.ids.encode_image_path.text = EncodeScreen.file_path  # this value is obtained from the select encode screen
        except:
            self.ids.encode_image_path.text = "No image selected"

    def encode_txt_img(self):  # Fn to encode our txt to image

        sel_image = self.ids.encode_image_path.text  # getting the file location
        user_text = self.ids.user_text.text  # text to be encoded

        slash_count = sel_image.count("\\")  # getting the file location

        img_name = sel_image.split("\\", slash_count)[slash_count].split(".", 1)[0]  # selecting only the file name with no extension
        img_type = sel_image.split("\\", slash_count)[slash_count].split(".", 1)[1]  # selecting only the file extension

        # Checking if the required folder exists
        if os.path.exists(r"C:\Secret TXT"):
            pass
        else:  # if not creating it
            os.makedirs(r"C:\Secret TXT")

        try:
            # checking the type of file first

            # for png types
            if img_type == "png":
                secret_img = f"C:\\Secret TXT\\{img_name} [Encoded].{img_type}"  # setting the location to save the encoded images

                # lsb is used for png
                # hide is used to encode the image
                # it's parameters are selected image, the text to be encoded
                lsb.hide(sel_image, message=user_text).save(secret_img)  # save is used to save the image to the required location

                self.ids.encode_result.text = "Encoding was successful"

            # for jpg/jpeg types
            elif img_type == "jpg" or img_type == "jpeg":
                secret_img = f"C:\\Secret TXT\\{img_name} [Encoded].{img_type}"

                # exifHeader is used for jpg/jpeg
                # hide is used to encode the image
                # it's parameters are selected image, location to be saved, and the text to be encoded
                exifHeader.hide(sel_image, secret_img, secret_message=user_text)

                self.ids.encode_result.text = "Encoding was successful"

            # if type is not supported
            else:
                self.ids.encode_result.text = "Type not supported"
        except:

            # fail-safe
            self.ids.encode_result.text = "Encoding has failed"

    def clear_text(self):  # Fn to clear screen on leaving the screen
        self.ids.encode_image_path.text = ""
        self.ids.user_text.text = ""
        self.ids.encode_result.text = ""


class SelectFileEncode(Screen):  # A class to select a file

    def get_source_encode(self, filePath):
        # Getting the file path
        try:
            self.ids.image.source = filePath[0]
            EncodeScreen.file_path = filePath[0]

        except:
            EncodeScreen.file_path = "No path"


class DecodeScreen(Screen):  # A class to initalise the decode screen

    def set_text(self):  # Fn to get file path
        try:
            self.ids.decode_image_path.text = DecodeScreen.file_path  # this value is obtained from the select decode screen
        except:
            self.ids.decode_image_path.text = "No image selected"

    def decode_img_txt(self):  # Fn to decode our txt from our image

        sel_image = self.ids.decode_image_path.text  # getting the file location

        slash_count = sel_image.count("\\")  # getting the file location
        img_type = sel_image.split("\\", slash_count)[slash_count].split(".", 1)[1]  # selecting only the file type with extension

        try:
            # checking the type of file first
            hidden_text = ""  # initializing a variable

            # img type is png
            if img_type == "png":

                # lsb for png
                # reveal is used to decode
                # it's parameter is the selected image
                hidden_text = lsb.reveal(sel_image)

            # img type is jpg/jpeg
            elif img_type == "jpg" or img_type == "jpeg":

                # exifHeader for jpg/jpeg
                # reveal is used to decode
                # it's parameter is the selected image
                hidden_text = exifHeader.reveal(sel_image)

            # checking if there is anything to be decoded
            if hidden_text is not "":

                self.ids.text_decoded.text = hidden_text
                self.ids.decode_result.text = "Decoding was successful"

            else:

                self.ids.text_decoded.text = ""  # setting the text as empty if there is nothing to decode
                self.ids.decode_result.text = "Nothing to Decode"
        except:

            # fail-safe
            self.ids.text_decoded.text = ""
            self.ids.decode_result.text = "Decoding has failed"

    def clear_text(self):  # Fn to clear screen on leaving the screen

        self.ids.decode_image_path.text = ""
        self.ids.text_decoded.text = ""
        self.ids.decode_result.text = ""


class SelectFileDecode(Screen):  # A class to select a file

    def get_source_decode(self, file_path):
        # Getting the file path
        try:
            self.ids.image.source = file_path[0]
            DecodeScreen.file_path = file_path[0]

        except:
            DecodeScreen.file_path = "No path"


class WindowManger(ScreenManager):  # A class to switch between different screens
    pass


kv = Builder.load_file("layout.kv")  # kv stores the layout file


class SecretTextApp(App):  # A base class of this app

    def build(self):  # In the Livy lifecycle the build() is executed after run()
        return kv


if __name__ == '__main__':  # used to ensure only "main" is run
    SecretTextApp().run()  # run() is used to start this app
