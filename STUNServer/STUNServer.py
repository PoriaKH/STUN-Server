import logging
import socket
import threading

ServerIP = "127.0.0.1"   # Server IP
ServerPort = 5355        # Server Port

bufferSize = 1024

# There are 2 kind of instructions acceptable for the server
# first is the ID introduction  (first of all,you need to tell us your ID )
# after that you can start to communicate with others.
# first type commands : HELLOSERVER "Your ID", for example: HELLOSERVER 52
# second type commands : TALKTO "Client ID", for example: TALKTO 91

print("UDP server up and listening")

list = [] # Each element is an array with 3 items (IP,Port,ID)

class STUNServer():

    def __init__(self):
        logging.info('Initializing Broker')
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((ServerIP, ServerPort))
        self.clients_list = []

    def update_list(self, message, address):
        decoded_string = message.decode("utf-8")
        number = decoded_string[12:]
        try:
            ID_number = int(number)
        except ValueError:
            final_answer = b'Message from Server : Invalid Number\n'
            self.sock.sendto(final_answer, address)
            return


        for i in range(len(list)):
            x = list[i]
            if x[2] == ID_number:
                return -1 # ID already in use

        for i in range(len(list)):
            x = list[i]
            if x[0] == address[0] and x[1] == address[1]:
                new = [address[0],address[1],ID_number]

                list[i] = new
                return 0


        new = [address[0],address[1],ID_number]
        list.append(new)
        return 0

    def listen_clients(self):
        while True:
            msg, client = self.sock.recvfrom(1024)
            logging.info('Received data from client %s: %s', client, msg)
            t = threading.Thread(target=self.talk_to_client, args=(msg,client))
            t.start()
    def src_id_exists(self,message, address):    # source ID exists -> 1 else -> -1
        for i in range(len(list)):
            x = list[i]
            if (x[0] == address[0] and x[1] == address[1]):
                return x[2]
        return -1
    def dst_id_exists(self,message, address):    # destination ID exists -> 1 else -> -1
        #TODO
        decoded_string = message.decode("utf-8")
        number = decoded_string[7:]
        try:
            ID_number = int(number)
        except ValueError:
            return -1
        print("ID_number = ",ID_number)

        for i in range(len(list)):
            x = list[i]
            if x[2] == ID_number and address[1] != x[1]:   #TODO this works only for Local server.
            #if x[2] == ID_number and address[0] != x[0]:  #TODO use this in real server(global).
                return ID_number
        return -1
    def remove_list(self, ID_number):
        for i in range(len(list)):
            x = list[i]
            if x[2] == ID_number:
                address = (str(x[0]), str(x[1]))
                list.remove(x)
                return address
        return -1   # Something went wrong.
    def talk_to_client(self,message, address):

        print("bytesAddressPair = ", message)

        clientMsg = "Message from Client:{}".format(message)
        clientIP = "Client IP Address:{}".format(address)

        print(clientMsg)
        print(clientIP)

        # Sending a reply to client
        print(message.hex())
        print("")
        print("message = ", message)

        if message.startswith(b'HELLOSERVER '):
            print("were in HELLOSERVER")
            if self.update_list(message,address) == -1: # ID already in use
                final_answer = b'Message from Server : ID already in use, please choose another ID\n'
                self.sock.sendto(final_answer, address)

            return

        if(message.startswith(b'TALKTO ')):
            print("were in TALKTO")
            src_id = self.src_id_exists(message, address)
            if src_id >= 0:
                # source ID exists
                dst_id = self.dst_id_exists(message, address)
                if dst_id >= 0:
                    src_address = self.remove_list(src_id)
                    dst_address = self.remove_list(dst_id)
                    if src_address == -1 or dst_address == -1:
                        final_answer = b'Something went wrong !\n'
                        self.sock.sendto(final_answer, address)
                        return
                    final_answer_src = b'Message from Server:\nYOUR_IP = ' + str.encode(src_address[0]) + b'\nYOUR_PORT = ' + str.encode(src_address[1]) + b'\nTARGET_IP = ' + str.encode(dst_address[0]) + b'\nTARGET_PORT = ' + str.encode(dst_address[1]) + b'\n'
                    final_answer_dst = b'Message from Server:\nYOUR_IP = ' + str.encode(dst_address[0]) + b'\nYOUR_PORT = ' + str.encode(dst_address[1]) + b'\nTARGET_IP = ' + str.encode(src_address[0]) + b'\nTARGET_PORT = ' + str.encode(src_address[1]) + b'\n'

                    self.sock.sendto(final_answer_src, (src_address[0], int(src_address[1])))
                    self.sock.sendto(final_answer_dst, (dst_address[0], int(dst_address[1])))
                    return

                # destination ID doesn't exists
                final_answer = b'Message from Server : Invalid Destination ID\n'
                self.sock.sendto(final_answer, address)
                return

            # source ID doesn't exists
            final_answer = b'Message from Server : You have to Initialize your ID first:\nfirst type commands : HELLOSERVER \"Your ID\", for example: HELLOSERVER 52\n'
            self.sock.sendto(final_answer, address)
            return

        final_answer = b'# There are 2 kind of instructions acceptable for the server\n# first is the ID introduction  (first of all,you need to tell us your ID )\n# after that you can start to communicate with others.\n# first type commands : HELLOSERVER "Your ID", for example: HELLOSERVER 52\n# second type commands : TALKTO "Client ID", for example: TALKTO 91\n'
        self.sock.sendto(final_answer, address)
        print("List = ", list)
