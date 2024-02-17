# STUN-Server
Its an STUN server using [User Datagram Protocol (UDP)](https://en.wikipedia.org/wiki/User_Datagram_Protocol) to communicate with clients which is used to solve the [UDP hole punching](https://en.wikipedia.org/wiki/UDP_hole_punching) problem and establish a connection between two devices behind [network address translation (NAT)](https://en.wikipedia.org/wiki/Network_address_translation).<br/>

### Usage
There are 2 kind of instructions acceptable for the server <br/>
first is the ID introduction  (first of all,you need to tell server your ID )
```
HELLOSERVER "Your ID"
```
For example:
```
HELLOSERVER 52
```
after that you can start to communicate with others by second type commands as bellow:<br/>
```
TALKTO "Client ID"
```
For example:
```
TALKTO 91
```
If the requested ID exists, the server will sent you the open port and ip address which the demanded client is listening to. after getting the details you can start the connection  directly to the client.<br/>
Server ip and port are defined by variables `ServerIP` and `ServerPort` in `./STUNServer/STUNServer.py`, you can change them to your own server ip, port.<br/>
<br/>
We have provided a sample of client written in python in `./STUNClient` for your comfort.

### Build
Use `make` to build the project. The executable file will be in the `dist` directory. <br/>
`make clean` to clean the artifacts. <br/>
