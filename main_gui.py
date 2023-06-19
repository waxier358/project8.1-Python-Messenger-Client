import tkinter
from tkinter import BOTH
from fonts_and_colors import background_color
from frames import ConnectionFrame, ClientsFrame
from functionality import Functionality, Connection, Sounds


class ChatClient(tkinter.Tk):
    """ChatClient class create and control ChatClient application """

    def __init__(self):
        super().__init__()

        self.title('Python Messenger Client')
        self.resizable(False, False)
        self.geometry('466x730')
        self.iconbitmap('icon/chat_icon.ico')
        self.configure(background=background_color)

        self.functionality = Functionality(self)

        self.connection_frame = ConnectionFrame(self)
        self.connection_frame.pack(fill=BOTH)

        self.functionality = Functionality(self)
        self.connection = Connection(self)

        self.clients_frame = ClientsFrame(self)
        self.clients_frame.pack(pady=20, padx=20)

        self.sounds = Sounds(self)

        # add functionality
        self.connection_frame.image_button.configure(command=lambda: self.functionality.chose_another_picture(self.connection))
        self.connection_frame.connect_button.configure(command=lambda: self.functionality.connect_disconnect(self.connection))

    def destroy(self) -> None:
        """action perform when main window is closed
           disconnect and destroy main_window
           input: tkinter.Tk
           return: None"""
        try:
            self.functionality.disconnect_client(self.connection)
        except OSError:
            print('socket is not connected')
        finally:
            tkinter.Tk.destroy(self)
