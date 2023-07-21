# project8.1-Python-Messenger-Client
I created a Python Messenger using sockets.
This application works in hub and soke mode.
Server can be started with this GUI.
Owner of server can enter his local IP address (current version will get IP address from ethernet interface automatically) and port number for server and can also start or stop server.
All connected clients appear in first scrollable frame with name and avatar.
All information about client status and all messages sent by every client will appear in second scrollable frame.


![image](https://github.com/waxier358/project8.1-Python-Messenger-Client/assets/105735620/7764ade7-82bb-4b05-ab0f-a5cf9ee75288)



This is client’s  GUI.

![image](https://github.com/waxier358/project8.1-Python-Messenger-Client/assets/105735620/2548b15e-ddd2-4900-a151-baaccec787b8)


Clients can insert IP address and port number of server, name, color of messages and choose avatar image. Connection status and information about clients and server status appear in first scrollable frame from GUI. All connected clients with names and avatars appear in second scrollable frame.  
To send messages client should press the button associated with his partner’s name and a message window will appear.

![image](https://github.com/waxier358/project8.1-Python-Messenger-Client/assets/105735620/eb0a54af-e23a-46ec-85e8-76ff98e9756d)


If destination client doesn’t have an open window associated with the source (client that sent the message), a message window will automatically be displayed on destination side. If any of the clients has message window associated with other client in minimized mode, the message window will be displayed on top of the screen. 
Application works on LAN and WAN network. This is a capture of a communication made in LAN network.
![image](https://github.com/waxier358/project8.1-Python-Messenger-Client/assets/105735620/262d0bc8-b7d2-4cbc-aee4-cb8b62afa2be)
![image](https://github.com/waxier358/project8.1-Python-Messenger-Client/assets/105735620/1300f16f-ce8f-4580-a75e-867409928816)

WAN communication capture:
![image](https://github.com/waxier358/project8.1-Python-Messenger-Client/assets/105735620/11b39777-a2d0-4f6d-94a7-1ad75b894fa8)

![image](https://github.com/waxier358/project8.1-Python-Messenger-Client/assets/105735620/011b3229-3da1-454d-bc9e-b59b56d1856e)


!!! COMMUNICATION IS NOT ENCRYPTED !!!

If somebody converts hex values from above capture into a string, he will see the message:

Hex value:
7b22666c6167223a20224d455353414745222c202264617461223a207b226d657373616765223a202268656c6c6f212121215c6e222c2022706172746e65725f6e616d65223a2022636c69656e7431227d7d

string after conversion:

{"flag": "MESSAGE", "data": {"message": "hello!!!!\n", "partner_name": "client1"}}.

!!! IMPLEMENTATION !!!

If server is behind a NAT router, PORT FORWORDING must be implemented on router. On client and server site new rules must be implemented in FIREWALL.
Here is a link with more details: (https://stackoverflow.com/questions/29929107/python-3-using-sockets-over-the-internet)

!!! RECOMMENDATION !!!

For best GUI experience use a client name as short as possible.
All clients' names must have approximately the same length.
