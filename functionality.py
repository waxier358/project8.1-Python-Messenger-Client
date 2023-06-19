from tkinter import filedialog as fd
from tkinter import PhotoImage, DISABLED, END, NORMAL
import os
import socket
import json
import threading
import pygame
from fonts_and_colors import admin_color
from frames import MessageWindow


class Sounds:
    """Sounds class plays sounds"""
    def __init__(self, main_window):
        pygame.init()
        self.main_window = main_window

        self.connect_sound = pygame.mixer.Sound('sounds/connect_sound.mp3')
        self.disconnect_sound = pygame.mixer.Sound('sounds/disconnect_sound.mp3')
        self.receive_send_message_sound = pygame.mixer.Sound('sounds/receive_send_message_sound.mp3')
        self.error_sound = pygame.mixer.Sound('sounds/error_sound.mp3')


class Connection:
    """keep all information about connection"""

    def __init__(self, main_window):
        self.main_window = main_window

        self.encoder = 'utf-8'
        self.server_ip = str()
        self.server_port = int()
        self.name = str()
        self.client_color = str()
        self.client_image_name = os.getcwd() + '/images/image_1.png'
        self.client_image = PhotoImage(file='images/image_1.png')
        self.main_window.connection_frame.image_button.configure(image=self.client_image)
        self.packet_length = 10
        self.client_socket = socket.socket()
        self.conversations_open = []
        self.windows_opened = {}


class Functionality:
    """functionality of application"""

    def __init__(self, main_window):

        self.main_window = main_window
        self.client_is_connected = False

    def chose_another_picture(self, current_connection: Connection):
        """chose another pictures for client in GUI"""

        # get name of the current directory
        current_directory_name = os.getcwd()
        # select an image from image folder from current directory
        current_connection.client_image_name = fd.askopenfile(title='chose another image', filetypes=[(".png files",
                                                                                                       "*.png")],
                                                              initialdir=current_directory_name + '\images').name
        create_directory_name = "\\".join(current_connection.client_image_name.split('/')[:-1])
        if current_directory_name + '\images' != create_directory_name:
            self.main_window.connection_frame.connection_messages.config(state=NORMAL)
            self.main_window.connection_frame.connection_messages.insert(END, f'Your image must be from '
                                                                              f'/images folder!\n',
                                                                         admin_color)
            self.main_window.connection_frame.connection_messages.tag_config(admin_color, foregroun=admin_color)
            self.main_window.connection_frame.connection_messages.see(END)
            self.main_window.connection_frame.connection_messages.config(state=DISABLED)

        else:
            # create new_image
            current_connection.client_image = PhotoImage(file=current_connection.client_image_name)
            # place new_image in connection_frame.image_button
            self.main_window.connection_frame.image_button.configure(image=current_connection.client_image)

    def connect_disconnect(self, current_connection: Connection):
        """connect or disconnect client based on self.client_is_connected """
        if self.client_is_connected:
            self.disconnect_client(current_connection)
        else:
            self.connect_client(current_connection)

    def disconnect_client(self, current_connection: Connection):
        """disconnect client"""

        # send disconnect flag
        message_packet = self.create_message('DISCONNECT', 'Please disconnect me!!')
        message_json = json.dumps(message_packet)
        # calculate length
        packet_length = str(len(message_json))
        while len(packet_length) < 10:
            packet_length += ' '
        # send info request
        # send packet_length
        current_connection.client_socket.send(packet_length.encode(current_connection.encoder))
        # send packet
        current_connection.client_socket.send(message_json.encode(current_connection.encoder))
        # update gui
        # disconnect message
        self.main_window.connection_frame.connection_messages.config(state=NORMAL)
        self.main_window.connection_frame.connection_messages.insert(END, f'Client {current_connection.name} '
                                                                          f'disconnect from server...\n',
                                                                     current_connection.client_color)
        self.main_window.connection_frame.connection_messages.tag_config(current_connection.client_color,
                                                                         foregroun=current_connection.client_color)
        self.main_window.connection_frame.connection_messages.see(END)
        self.main_window.connection_frame.connection_messages.config(state=DISABLED)
        # clear all clients
        self.main_window.clients_frame.clear_all_buttons()
        # reset initial values
        self.reset_properties(current_connection)
        self.enable_gui()
        self.client_is_connected = False
        self.main_window.connection_frame.connect_button.configure(text='Connect')

        # play disconnect sound
        self.main_window.sounds.disconnect_sound.play()

        # close socket
        current_connection.client_socket.close()

    def connect_client(self, current_connection: Connection):
        """connect client"""
        current_connection.server_ip = self.main_window.connection_frame.server_ip_entry.get()

        try:
            current_connection.server_port = int(self.main_window.connection_frame.server_port_number_entry.get())
        except ValueError:
            self.main_window.connection_frame.connection_messages.config(state=NORMAL)
            self.main_window.connection_frame.connection_messages.insert(END, 'Port Number must be a number!\n',
                                                                         admin_color)
            self.main_window.connection_frame.connection_messages.tag_config(admin_color, foregroun=admin_color)
            self.main_window.connection_frame.connection_messages.see(END)
            self.main_window.connection_frame.connection_messages.config(state=DISABLED)
            # play error sound
            self.main_window.sounds.error_sound.play()

        else:
            current_connection.name = self.main_window.connection_frame.name_entry.get()
            current_connection.client_color = self.main_window.connection_frame.text_color_combobox.get()

            # create client socket
            current_connection.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # connect to server
            try:
                current_connection.client_socket.connect((current_connection.server_ip, current_connection.server_port))
            except OverflowError:
                self.main_window.connection_frame.connection_messages.config(state=NORMAL)
                self.main_window.connection_frame.connection_messages.insert(END,
                                                                             'Port Number must be between 1-65535!\n',
                                                                             admin_color)
                self.main_window.connection_frame.connection_messages.tag_config(admin_color, foregroun=admin_color)
                self.main_window.connection_frame.connection_messages.see(END)
                self.main_window.connection_frame.connection_messages.config(state=DISABLED)
                # play error sound
                self.main_window.sounds.error_sound.play()
            except socket.gaierror:
                self.main_window.connection_frame.connection_messages.config(state=NORMAL)
                self.main_window.connection_frame.connection_messages.insert(END,
                                                                             'You entered an incorrect IP address!\n',
                                                                             admin_color)
                self.main_window.connection_frame.connection_messages.tag_config(admin_color, foregroun=admin_color)
                self.main_window.connection_frame.connection_messages.see(END)
                self.main_window.connection_frame.connection_messages.config(state=DISABLED)
                # play error sound
                self.main_window.sounds.error_sound.play()
            except ConnectionRefusedError:
                self.main_window.connection_frame.connection_messages.config(state=NORMAL)
                self.main_window.connection_frame.connection_messages.insert(END,
                                                                             'Connection Refused, port'
                                                                             ' number incorrect or server is closed!\n',
                                                                             admin_color)
                self.main_window.connection_frame.connection_messages.tag_config(admin_color, foregroun=admin_color)
                self.main_window.connection_frame.connection_messages.see(END)
                self.main_window.connection_frame.connection_messages.config(state=DISABLED)
                # play error sound
                self.main_window.sounds.error_sound.play()
            except TimeoutError:
                self.main_window.connection_frame.connection_messages.config(state=NORMAL)
                self.main_window.connection_frame.connection_messages.insert(END,
                                                                             'Connection Timeout, IP address '
                                                                             'and/or port'
                                                                             ' number are incorrect!\n', admin_color)
                self.main_window.connection_frame.connection_messages.tag_config(admin_color, foregroun=admin_color)
                self.main_window.connection_frame.connection_messages.see(END)
                self.main_window.connection_frame.connection_messages.config(state=DISABLED)
                # play error sound
                self.main_window.sounds.error_sound.play()

            else:
                self.main_window.connection_frame.connection_messages.configure(state=NORMAL)
                self.main_window.connection_frame.connection_messages.insert(END, 'Connecting to the server...\n',
                                                                             admin_color)
                self.main_window.connection_frame.connection_messages.tag_config(admin_color, foregroun=admin_color)
                self.main_window.connection_frame.connection_messages.config(state=DISABLED)

                # receive packet_length from server
                packet_length = current_connection.client_socket.recv(current_connection.packet_length).\
                    decode(current_connection.encoder)
                # receive incoming message from server
                message_json = current_connection.client_socket.recv(int(packet_length))

                self.client_is_connected = True
                # update GUI
                self.disable_gui()
                self.main_window.connection_frame.connect_button.configure(text='Disconnect')

                self.process_message(message_json, current_connection)

    def disable_gui(self):
        """disable some widgets from GUI"""

        self.main_window.connection_frame.server_ip_entry.configure(state=DISABLED)
        self.main_window.connection_frame.server_port_number_entry.configure(state=DISABLED)
        self.main_window.connection_frame.name_entry.configure(state=DISABLED)
        self.main_window.connection_frame.text_color_combobox.configure(state=DISABLED)
        self.main_window.connection_frame.image_button.configure(state=DISABLED)

    def enable_gui(self):
        """enable some widgets from GUI"""

        self.main_window.connection_frame.server_ip_entry.configure(state=NORMAL)
        self.main_window.connection_frame.server_port_number_entry.configure(state=NORMAL)
        self.main_window.connection_frame.name_entry.configure(state=NORMAL)
        self.main_window.connection_frame.text_color_combobox.configure(state=NORMAL)
        self.main_window.connection_frame.image_button.configure(state=NORMAL)

    @staticmethod
    def reset_properties(current_connection: Connection):
        """reset attributes"""

        current_connection.server_ip = str()
        current_connection.server_port = int()
        current_connection.name = str()
        current_connection.client_color = str()
        current_connection.client_socket = socket.socket()

    def process_message(self, message_json: bytes, current_connection: Connection):
        """process message based on flag associated with it"""

        # decode and turn string in dict
        message_packet = json.loads(message_json)
        flag = message_packet['flag']
        data = message_packet['data']
        if flag == 'INFO':
            # server is asking about client information
            self.main_window.connection_frame.connection_messages.configure(state=NORMAL)
            self.main_window.connection_frame.connection_messages.insert(END, 'Sending information to the server...\n',
                                                                         admin_color)
            self.main_window.connection_frame.connection_messages.tag_config(admin_color, foregroun=admin_color)
            self.main_window.connection_frame.connection_messages.tag_config('green', foreground='green')
            self.main_window.connection_frame.connection_messages.see(END)
            self.main_window.connection_frame.connection_messages.config(state=DISABLED)

            # create image_name
            current_image_name = current_connection.client_image_name[::-1].split("/")[0][::-1]

            client_data = {'name': current_connection.name,
                           'color': current_connection.client_color,
                           'image_name': current_image_name}

            message_packet = self.create_message('INFO', client_data)
            message_json = json.dumps(message_packet)
            # calculate length
            packet_length = str(len(message_json))
            while len(packet_length) < 10:
                packet_length += ' '
            # send packet_length of info answer
            current_connection.client_socket.send(packet_length.encode(current_connection.encoder))
            # send packet info answer
            current_connection.client_socket.send(message_json.encode(current_connection.encoder))

            receive_thread = threading.Thread(target=self.receive_message, args=(current_connection,))
            receive_thread.start()

        elif flag == 'ALL CLIENTS':
            self.main_window.clients_frame.create_buttons(data)

        elif flag == 'DISCONNECT':
            button_for_delete = data
            self.main_window.clients_frame.update_clients(button_for_delete)

        elif flag == 'SERVER CLOSE':
            self.main_window.clients_frame.clear_all_buttons()
            # disconnect message
            self.main_window.connection_frame.connection_messages.config(state=NORMAL)
            self.main_window.connection_frame.connection_messages.insert(END, f'Server is closing...\n', 'red')
            self.main_window.connection_frame.connection_messages.tag_config('red', foregroun='red')
            self.main_window.connection_frame.connection_messages.see(END)
            self.main_window.connection_frame.connection_messages.config(state=DISABLED)
            # clear all clients
            self.main_window.clients_frame.clear_all_buttons()
            # close socket
            current_connection.client_socket.close()
            # reset initial values
            self.reset_properties(current_connection)
            self.enable_gui()
            self.client_is_connected = False
            self.main_window.connection_frame.connect_button.configure(text='Connect')

        elif flag == 'MESSAGE':
            # create name of button press windows generated name
            local_generated_window_name = f'{current_connection.name}to{message_packet["data"]["source_client"]}'
            remote_generated_windows_name = f'{message_packet["data"]["source_client"]}to{current_connection.name}'
            local_window_to_place_message = self.main_window.connection.windows_opened.get(local_generated_window_name)
            remote_window_to_place_message = self.main_window.connection.windows_opened.\
                get(remote_generated_windows_name)
            partner_name = self.main_window.clients_frame.clients_names.get(message_packet["data"]["source_client"])
            partner_color = self.main_window.clients_frame.buttons.get(f'button_{message_packet["data"]["source_client"]}')['fg']
            source_index = message_packet['data']['source_client']
            destination_index = message_packet['data']['partner_name']

            if local_window_to_place_message:
                if local_window_to_place_message.state() == 'iconic':
                    local_window_to_place_message.state('normal')
                local_window_to_place_message.chat_text.config(state=NORMAL)
                local_window_to_place_message.chat_text.insert(END, f"{partner_name}: {message_packet['data']['message']}", partner_color)
                local_window_to_place_message.chat_text.tag_config(partner_color, foreground=partner_color)
                local_window_to_place_message.chat_text.config(state=DISABLED)
                # play receive message sound
                self.main_window.sounds.receive_send_message_sound.play()
            elif remote_window_to_place_message:
                if remote_window_to_place_message.state() == 'iconic':
                    remote_window_to_place_message.state('normal')
                local_window_to_place_message.chat_text.config(state=NORMAL)
                remote_window_to_place_message.chat_text.insert(END,
                                                               f"{partner_name}: {message_packet['data']['message']}")
                remote_window_to_place_message.chat_text.tag_config(partner_color, foreground=partner_color)
                local_window_to_place_message.chat_text.config(state=DISABLED)
                # play receive message sound
                self.main_window.sounds.receive_send_message_sound.play()

            else:
                self.open_message_window_at_message(source_index, destination_index,
                                                    message=message_packet['data']['message'])

    @staticmethod
    def create_message(flag: str, data) -> dict:
        """data: dict or str"""

        return {'flag': flag,
                'data': data}

    def receive_message(self, current_connection: Connection):
        """receive continuously for message from server and pass received message to process_message"""

        while True:
            try:
                packet_length = current_connection.client_socket.recv(current_connection.packet_length)
                message_json = current_connection.client_socket.recv(int(packet_length))
                self.process_message(message_json, current_connection)
            except OSError:
                # Socket close
                break
            except ValueError:
                # receive empty string
                break

    def open_message_window_at_message(self, source_index: str, destination_index: str, message: str):
        """open new MessageWindow when receiving message with MESSAGE flag
           and MessageWindow doesn't exist"""

        # find source name
        source_name = self.main_window.clients_frame.clients_names.get(f'{source_index}')
        source_image_name = self.main_window.clients_frame.images_name.get(f'{source_index}')
        destination_name = self.main_window.clients_frame.clients_names.get(f'{destination_index}')
        destination_image_name = self.main_window.clients_frame.images_name.get(f'{destination_index}')
        conversation_name = f'{source_index}to{destination_name}'
        source_color = self.main_window.clients_frame.buttons.get(f'button_{source_index}')['fg']

        self.main_window.connection.conversations_open.append(conversation_name)
        self.message_window = MessageWindow(main_window=self.main_window, connection=self.main_window.connection,
                                            current_name=source_name, destination_name=destination_name,
                                            current_image_name=source_image_name,
                                            destination_image_name=destination_image_name,
                                            this_conversation_name=conversation_name, partner_name=source_index)

        self.message_window.chat_text.config(state=NORMAL)
        self.message_window.chat_text.insert(END, f'{source_name}: {message}', source_color)
        self.message_window.chat_text.tag_config(source_color, foreground=source_color)
        self.message_window.chat_text.config(state=DISABLED)

        self.main_window.connection.windows_opened.update({f'{conversation_name}': self.message_window})
        self.main_window.update()
        # play message sound
        self.main_window.sounds.receive_send_message_sound.play()

    def open_message_window_at_button_press(self, name: str):
        button_presses = self.main_window.clients_frame.buttons.get(f'button_{name}')
        destination_name = button_presses['text']
        destination_image = self.main_window.clients_frame.images_name.get(f'{name}')
        this_conversation_name = f'{self.main_window.connection.name}to{name}'
        if this_conversation_name not in self.main_window.connection.conversations_open:
            self.main_window.connection.conversations_open.append(this_conversation_name)
            message_window = MessageWindow(main_window=self.main_window, connection=self.main_window.connection,
                                           current_name=self.main_window.connection.name,
                                           destination_name=destination_name,
                                           current_image_name=self.main_window.connection.client_image_name,
                                           destination_image_name=destination_image,
                                           this_conversation_name=this_conversation_name,
                                           partner_name=name)
            self.main_window.connection.windows_opened.update({f'{this_conversation_name}': message_window})
            self.main_window.update()

    def send_message_from_window(self, partner_name: str, conversation_name: str):
        """send message when Send button from MessageWindow is pressed"""

        current_window = self.main_window.connection.windows_opened.get(conversation_name)
        current_color = self.main_window.connection.client_color
        text_to_send = current_window.message_text.get(1.0, END)
        # send text only if text exist
        # remove \n from the end
        if text_to_send[:-1] != '':
            text_to_send_length = len(text_to_send[:-1])
            while text_to_send[text_to_send_length - 1] == '\n':
                text_to_send_length -= 1

            current_window.chat_text.config(state=NORMAL)
            current_window.chat_text.insert(END, f'{self.main_window.connection.name}:'
                                                 f' {text_to_send[:text_to_send_length + 1]}', current_color)
            current_window.chat_text.tag_config(current_color, foreground=current_color)
            current_window.chat_text.config(state=DISABLED)

            current_window.message_text.delete(1.0, END)
            message_data = {'message': text_to_send[:text_to_send_length + 1],
                            'partner_name': partner_name}

            message_packet = self.create_message('MESSAGE', message_data)
            message_json = json.dumps(message_packet)
            # calculate length
            packet_length = str(len(message_json))
            while len(packet_length) < 10:
                packet_length += ' '
            # send packet_length of message packet
            self.main_window.connection.client_socket.send(packet_length.encode(self.main_window.connection.encoder))
            # send packet message packet
            self.main_window.connection.client_socket.send(message_json.encode(self.main_window.connection.encoder))
            # play send sound
            self.main_window.sounds.receive_send_message_sound.play()
