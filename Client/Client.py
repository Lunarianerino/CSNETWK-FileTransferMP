#import socket module
from socket import *
import sys # In order to terminate the program
import threading
class Client(threading.Thread):
    def __init__(self, HOST, PORT):
        threading.Thread.__init__(self)
        self.HOST = HOST
        self.PORT = PORT
        self.clientEndpoint = socket()
        self.clientEndpoint.connect((self.HOST, int(self.PORT)))
        self.buffer_size = 1024
        self.connection_flag = True
        self.start()

    def run(self):
        while self.connection_flag:
            try:
                reply = self.clientEndpoint.recv(self.buffer_size).decode()
                if not self.HandleStatus(reply):
                    print(reply)
            except Exception as e:
                print(e)
                break  

    def sendMessage(self, message):
        self.clientEndpoint.send(str(message).encode())
    def close(self):
        self.clientEndpoint.close()
        self.buffer_size = 0
        self.connection_flag = False
        
    def HandleStatus(self, status):
        if status == "444 CONNECTION_CLOSED":
            print("Connection closed. Thank you!")
            self.close()
            return True
        return False
if __name__ == "__main__":
    client = None
    while True:
        text = input(">> ")
        try:
            if text[0] == '/':
                command = text[1:].split()
                if command[0]== "join":
                    client = Client(command[1], command[2])
                elif client != None:
                    client.sendMessage(text)
            else:
                if client != None:
                    client.sendMessage(text)
        except Exception as e:
            #TODO: might have to implement a list of errors for easy error messages in GUI
            print("Connection to the Server has failed! Please check IP Address and Port Number.") 

        
