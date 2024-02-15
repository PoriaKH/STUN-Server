import socket
import threading

STUNServerIP = "127.0.0.1"
STUNServerPORT = 5355

bufferSize = 1024

class STUNClient():
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    def start_here(self):
        t = threading.Thread(target=self.get_input)
        t.start()
        self.listen()

    def connect_to_client(self,message):
        global STUNServerPORT
        global STUNServerIP

        decoded_string = message.decode("utf-8")
        data = decoded_string.split("\n")
        target_ip = data[3].split(' ')[2]
        target_port = data[4].split(' ')[2]
        print("data = ", data)
        print("target_ip = ", target_ip)
        print("target_port = ", target_port)

        STUNServerIP = target_ip
        STUNServerPORT = int(target_port)
    def get_input(self):
        while True:
            value = input("Please enter a string:\n")
            self.sock.sendto(str.encode(value), (STUNServerIP, STUNServerPORT))


    def listen(self):
        flag = 0
        while True:
            msg = self.sock.recv(bufferSize)
            print(msg)
            if msg.startswith(b'Message from Server:\nYOUR_IP') and flag == 0:
                flag = 1
                self.connect_to_client(msg)
