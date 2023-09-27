# Python Chat Application via TCP Socket
This project is for the completion of the `Laboratory Exercise #1` and `Laboratory Exercise #2` for `IT 238 - Network and Client/Server Computing`.   

Simple Client-Server Chat application using Python TCP/IP Socket Programming.

## Exercise #1 
### Program Description: 
The server process runs on your Linux machine that waits for a client to establish a `TCP/IP connection`. The client may run on your laptop or any other client device with a network connection to your server. Once a connection is established, the client/server may send chat messages between each other. Display in a scrolling screen the exchange of messages. Messages are entered in a message entry box and are sent as a stream after pressing the `<enter>` key. Pressing `<ctrl-x>` will terminate the program.

## Exercise #2 
Multiple Client to one Server Chat application using UDP Broadcast

### Program Description: 
 Extend your simple client-server chat application in `Lab Exer 1` to allow multiple clients to join in the chat (or bulletin board). Clients establish a connection with the server by registering a name. The server receives text message streams from the client and sends a copy of the `message to all other clients by IP broadcast`. All chat screens must be the same for all clients and servers. 


## Dependencies
* python-tk
* customtkinter
* Pillow
* python-dotenv

## Starting the Application
```python
  python3 ./src/app/main.py
```

## Network Connection
To change the default connection from `TCP` to `UDP`, edit the configuration in `.env` file
```env
  CONNECTION_TYPE=TCP
```