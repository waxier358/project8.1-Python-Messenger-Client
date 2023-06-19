import tkinter
from tkinter import DISABLED, END, ttk, VERTICAL, ALL, PhotoImage, LEFT, NORMAL
import tkinter.scrolledtext as scrolled_text
from fonts_and_colors import font, background_color, text_color, client_name_font, chat_font
import Pmw


class ConnectionFrame(tkinter.Frame):
    """create a tkinter frame where user can:
       enter server ip address
       enter server port number
       enter his name
       choose color for his text
       choose his image for chat
       connect/disconnect to server
       receive information about his connection

       input main_window: tkinter to access frames from main_window"""

    def __init__(self, main_window):
        """initialization of ConnectionFrame
            create and place all widgets"""
        super().__init__()

        self.main_window = main_window
        self.configure(background=background_color)

        # create and place host_ip_label
        self.server_ip_label = tkinter.Label(self, text='Server IP:', font=font, background=background_color,
                                             foreground=text_color)
        self.server_ip_label.grid(row=0, column=0, pady=10, sticky='WE', padx=(20, 20))

        # create and place host_ip_entry
        self.server_ip_entry = tkinter.Entry(self, width=25, font=font, borderwidth=2)
        self.server_ip_entry.grid(row=0, column=1, padx=(0, 20))

        # create and place server_port_label
        self.server_port_number_label = tkinter.Label(self, text='Port Number: ', font=font, foreground=text_color,
                                                      background=background_color)
        self.server_port_number_label.grid(row=1, column=0, sticky='WE', pady=10, padx=(20, 20))

        # create and place server_port_entry
        self.server_port_number_entry = tkinter.Entry(self, width=25, font=font, borderwidth=2)
        self.server_port_number_entry.grid(row=1, column=1, padx=(0, 20))

        # create and place name_port_label
        self.name_label = tkinter.Label(self, text='Name: ', font=font, foreground=text_color,
                                        background=background_color)
        self.name_label.grid(row=2, column=0, sticky='WE', pady=10, padx=(20, 20))

        # create and place name_entry
        self.name_entry = tkinter.Entry(self, width=25, font=font, borderwidth=2)
        self.name_entry.grid(row=2, column=1, padx=(0, 20))

        # create and place text_color_label
        self.text_color_label = tkinter.Label(self, text='Text Color: ', font=font, foreground=text_color,
                                              background=background_color)
        self.text_color_label.grid(row=3, column=0, sticky='WE', pady=10, padx=(20, 20))

        # create option for all Combobox from this frame (font and justify)
        self.option_add("*TCombobox*Listbox*Font", font)
        self.option_add('*TCombobox*Listbox.Justify', 'center')

        # create and place text_color_combobox
        self.text_color_combobox = ttk.Combobox(self, values=['gray', 'rosybrown', 'red', 'sienna', 'tan', 'darkcyan',
                                                              'blue', 'plum', 'purple', 'slateblue'], width=22,
                                                justify='center', font=font)
        self.text_color_combobox.current(0)
        self.text_color_combobox.grid(row=3, column=1, pady=10, sticky='WE', padx=(0, 20))

        # create and place image_label
        self.image_text_label = tkinter.Label(self, text='Image: ', font=font, foreground=text_color,
                                              background=background_color)
        self.image_text_label.grid(row=4, column=0, sticky='WE', pady=10, padx=(20, 20))

        # create and place image_label
        self.image_button = tkinter.Button(self, font=font, foreground=text_color, background=background_color,
                                           borderwidth=0, activebackground=background_color)
        self.image_button.grid(row=4, column=1, padx=(0, 20))

        # display message when hovering over image_button
        self.message_tool = Pmw.Balloon(self)
        self.message_tool.bind(self.image_button, 'Click to chose another image!')
        self.message_tool.configure(relmouse='both', initwait=100)

        # create and place connect button
        self.connect_button = tkinter.Button(self, font=font, foreground=text_color, background=background_color,
                                             text='Connect', activebackground=background_color,
                                             activeforeground=text_color)
        self.connect_button.grid(row=5, column=0, columnspan=2, padx=(10, 10), ipadx=170, pady=10)

        # create and place connection label frame
        self.connection_label_frame = tkinter.LabelFrame(self, text='Connection Messages', bg=background_color,
                                                         foreground='white', font=font)
        self.connection_label_frame.grid(row=6, column=0, columnspan=2, padx=(10, 10))

        # create and place connection_messages text in connection_label_frame
        self.connection_messages = scrolled_text.ScrolledText(self.connection_label_frame, width=36, height=4,
                                                              font=font, state=DISABLED, wrap=tkinter.WORD)
        self.connection_messages.grid(row=0, column=0)


class ClientsFrame(tkinter.LabelFrame):
    """create a tkinter frame where user can:

       see info about his connection
       see clients connected to the server
       initiate a conversations with another connected client

       input main_window: tkinter to access frames from main_window"""

    def __init__(self, main_window):
        """initialization of ClientsFrame
            create and place all widgets"""
        super().__init__()

        self.main_window = main_window
        self.configure(text='Clients Connected:', bg=background_color, foreground='white', font=font, borderwidth=2)

        # create container frame
        self.container_frame = tkinter.Frame(self, bg='white')
        # create a canvas in above container_frame
        self.my_canvas = tkinter.Canvas(self.container_frame)
        # add a scroll_bar to above canvas
        self.y_scrollbar = ttk.Scrollbar(self.container_frame, orient=VERTICAL, command=self.my_canvas.yview, )
        self.my_canvas.configure(yscrollcommand=self.y_scrollbar.set, width=400, height=400)

        def on_mousewheel(event):
            """when mouse is above image display a message"""
            if str(event.widget.winfo_parent()) == '.!clientsframe.!frame.!canvas.!frame':
                self.my_canvas.yview_scroll(int(-1 * (event.delta / 60)), "units")

        # create scrollable frame in self.my_canvas
        self.scrollable_frame = tkinter.Frame(self.my_canvas, bg='white')
        self.my_canvas.bind("<Configure>", lambda e: self.my_canvas.configure(scrollregion=self.my_canvas.bbox(ALL)))
        self.my_canvas.bind_all("<MouseWheel>", on_mousewheel)
        self.my_canvas.create_window((0, 0), window=self.scrollable_frame, anchor='nw')

        self.container_frame.pack(fill='both', expand=True)
        self.my_canvas.pack(side='left', fill='both', expand=True)
        self.y_scrollbar.pack(side='right', fill='y')

        self.buttons = {}
        self.images = {}
        self.images_name = {}
        self.clients_connected = []
        self.clients_names = {}

    def create_buttons(self, message: dict):
        """
        create and place buttons on clients_frame based on dictionary received from server
        :param message: dict -> {'client1': {'name': 'Client1', 'color': 'red', 'image_name': 'image_1.png'}}
        :return: None
        """
        # create and add button in self.buttons dict
        for key in message.keys():
            if key not in self.clients_connected:
                self.clients_connected.append(key)
                self.images.update({f'image_{key}': PhotoImage(file=f'images/{message[f"{key}"]["image_name"]}')})
                self.images_name.update({f'{key}': message[f"{key}"]["image_name"]})
                name = message[f"{key}"]["name"]

                self.clients_names.update({f'{key}': name})

                color = message[f"{key}"]["color"]

                self.main_window.connection_frame.connection_messages.config(state=NORMAL)
                self.main_window.connection_frame.connection_messages.insert(END,
                                                                             f'Client {name} connected to server!\n',
                                                                             color)
                self.main_window.connection_frame.connection_messages.tag_config(color, foregroun=color)
                self.main_window.connection_frame.connection_messages.see(END)
                self.main_window.connection_frame.connection_messages.config(state=DISABLED)
                # play connect sound
                self.main_window.sounds.connect_sound.play()

                # extend_name
                while len(name) < 65:
                    name += ' '
                self.buttons.update({f'button_{key}': tkinter.Button(self.main_window.clients_frame.scrollable_frame,
                                                                     compound=LEFT,
                                                                     text=f' {name}', width=400,
                                                                     justify='left',
                                                                     height=50,
                                                                     activeforeground=color,
                                                                     borderwidth=2, fg=color, font=client_name_font,
                                                                     command=lambda current_name=key: self.main_window.
                                                                     functionality.open_message_window_at_button_press
                                                                     (current_name))})
                self.buttons[f'button_{key}'].configure(image=self.images[f'image_{key}'])
                self.buttons[f'button_{key}'].pack()
                # update GUI
                self.main_window.update()
                self.main_window.clients_frame.my_canvas.configure(scrollregion=self.my_canvas.bbox(ALL))

    def clear_all_buttons(self):
        """delete all buttons from clients_frame when current client disconnects from server"""

        for client_name in self.clients_connected:
            self.buttons[f'button_{client_name}'].destroy()
            self.main_window.update()
            self.main_window.clients_frame.my_canvas.configure(scrollregion=self.my_canvas.bbox(ALL))

        self.buttons.clear()
        self.images.clear()
        self.clients_connected.clear()
        self.images_name.clear()

    def update_clients(self, button_name: str):
        """delete associated button with a disconnected client"""
        client_name_to_delete = self.clients_names.get(f'{button_name}')
        # delete image of disconnected client
        self.images.pop(f'image_{button_name}')
        # delete image name from images_name
        self.images_name.pop(f'{button_name}')
        # delete client index of disconnected client
        self.clients_connected.remove(button_name)
        # delete client name from clients_names
        self.clients_names.pop(f'{button_name}')
        # delete button associated with disconnected client
        button_to_delete = self.buttons.pop(f'button_{button_name}')
        client_color_to_delete = button_to_delete['foreground']
        # destroy button
        button_to_delete.destroy()
        # update GUI based on above modification
        self.main_window.update()
        self.main_window.connection_frame.connection_messages.config(state=NORMAL)
        self.main_window.connection_frame.connection_messages.insert(END,
                                                                     f'Client {client_name_to_delete} disconnected '
                                                                     f'from server!\n',
                                                                     client_color_to_delete)
        self.main_window.connection_frame.connection_messages.tag_config(client_color_to_delete,
                                                                         foregroun=client_color_to_delete)
        self.main_window.connection_frame.connection_messages.see(END)
        self.main_window.connection_frame.connection_messages.config(state=DISABLED)
        # play disconnect sound
        self.main_window.sounds.disconnect_sound.play()


class MessageWindow(tkinter.Toplevel):
    """class MessageWindow creates a Message Window specific to each client
       main_window (parent window): tkinter.Tk()
       connection: Connection()"""

    def __init__(self, main_window, connection, current_name: str, destination_name: str, current_image_name: str,
                 destination_image_name: str, this_conversation_name: str, partner_name: str):
        super().__init__(main_window)

        self.main_window = main_window
        self.connection = connection

        self.destination_name = destination_name
        self.destination_image_name = destination_image_name

        self.title(f"Message from {current_name} to {self.destination_name}")
        self.geometry("467x680")
        self.configure(background=background_color)
        self.resizable(False, False)
        self.iconbitmap('icon/chat_icon.ico')

        self.this_conversation_name = this_conversation_name
        self.partner_name = partner_name

        if '/' in current_image_name:
            self.current_image = PhotoImage(file=f'{current_image_name}')
        else:
            self.current_image = PhotoImage(file=f'images/{current_image_name}')

        self.destination_image = PhotoImage(file=f'images/{self.destination_image_name}')

        self.image_label_1 = tkinter.Label(self, image=self.current_image, background=background_color)
        self.image_label_1.grid(row=0, column=0, padx=(10, 10), pady=10)
        self.to_label = tkinter.Label(self, text=' to ', font=client_name_font, foreground='white',
                                      background=background_color)
        self.to_label.grid(row=0, column=1, padx=30, pady=(0, 2))
        self.image_label_2 = tkinter.Label(self, image=self.destination_image, background=background_color)
        self.image_label_2.grid(row=0, column=2, padx=10, pady=10)
        self.chat_frame = tkinter.LabelFrame(self, text='Chat:', foreground='white', font=client_name_font,
                                             borderwidth=2, width=70, height=50, background=background_color)
        self.chat_frame.grid(row=1, column=0, columnspan=3, padx=5, pady=(0, 5))
        self.chat_text = scrolled_text.ScrolledText(self.chat_frame, width=47, height=17, wrap=tkinter.WORD,
                                                    font=chat_font, state=DISABLED)
        self.chat_text.grid(row=0, column=0, columnspan=3, padx=5)
        self.label_frame = tkinter.LabelFrame(self, text='Messages:', foreground='white',
                                              font=client_name_font, borderwidth=2, width=70, height=50,
                                              background=background_color)
        self.label_frame.grid(row=2, column=0, columnspan=3, padx=5)
        self.message_text = scrolled_text.ScrolledText(self.label_frame, width=47, height=5, wrap=tkinter.WORD,
                                                       font=chat_font)
        self.message_text.grid(row=0, column=0, columnspan=3, padx=5)
        self.send_button = tkinter.Button(self, font=font, foreground='white', background=background_color,
                                          text='Send', activebackground=background_color,
                                          activeforeground='white', command=lambda: self.main_window.functionality.
                                          send_message_from_window(self.partner_name, self.this_conversation_name))
        self.send_button.grid(row=3, column=0, columnspan=3, padx=5, ipadx=195, pady=(10, 5))

    def destroy(self):
        """action performed when message window is closed
           remove current_conversation
           destroy MessageWindow"""

        current_windows_name = self.this_conversation_name
        self.main_window.connection.conversations_open.remove(current_windows_name)
        self.main_window.connection.windows_opened.pop(current_windows_name)
        tkinter.Toplevel.destroy(self)
