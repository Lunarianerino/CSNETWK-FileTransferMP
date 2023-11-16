#import socket module
from socket import *
import sys # In order to terminate the program
import threading
import time
import os
class SocketThread(threading.Thread):
    def __init__(self, connection):
        threading.Thread.__init__(self)
        self.connectionSocket = connection["Socket"]
        self.addr = connection["Addr"]
        self.server = connection["Server"]
        self.start()
        self.Names = list()
    def run(self):
        i = 0
        while True:
            #self.connectionSocket.send(f"This is a test {i}".encode())
            try:
                text = self.connectionSocket.recv(1024).decode()
            except Exception as e:
                print(e)
                break
            
            if len(text) > 0:
                print(text)
                if text[0] == '/':
                    self.commandHandler(text[1:].split()[0], text[1:].split()[1:])
                    #self.commandHandler(text[1:].split())
                else:
                    self.commandHandler("broadcast", text)
            #self.server.broadcast(text)
            #i += 1
    def send(self, message):
        self.connectionSocket.send(message.encode())
    def commandHandler(self, command, *args):
        print(command)
        if command == "leave":
            self.connectionSocket.send("444 CONNECTION_CLOSED".encode())
            self.connectionSocket.close()
            self.server.ActiveConnections.remove(self)
            
        elif command == "broadcast":
            self.server.broadcast(args[0])
            self.connectionSocket.send("200 OK".encode())

        elif command == "register":
            name = {
                "Name": args[0],
                "Socket": self.connectionSocket
            }
            self.server.addName(name)
            self.connectionSocket.send("200 OK".encode())
            self.connectionSocket.send(f"Welcome {args[0]}".encode())
            print(self.server.getNames())

        elif command == "?":
            self.connectionSocket.send("200 OK".encode())
            self.connectionSocket.send("Commands:\n/join <server_ip_add> <port>\n/leave\n/register <handle>\n/store <filename>\n/dir\n/get <filename>\n/?".encode())

        elif command == "dir":
            #get the list of files in /Server/Files
            directory = './Server/Files'
            files = os.listdir(directory)
            file_list = [] #list of dicts for each file
            for f in files:
                #tokenize file name with this format [Date][Time][Uploader][File Name including extension]
                #example: [2023-11-17][16-48-05][John][Hello World]
                tokens = f.replace('[', '').replace(']', '\n').split('\n')
                file = { #dict might be used for GUI but apparently CLI only needs to display file name and I may have overdone things
                    "Date": tokens[0],
                    "Time": tokens[1].replace('-', ':'),
                    "Uploader": tokens[2],
                    "Name": ''.join(tokens[3:]),
                    "Size": str(os.path.getsize(directory + '/' + f)) + " Bytes"
                }
                file_list.append(file)
            print(file_list)
            self.connectionSocket.send("200 OK".encode())
            self.connectionSocket.send("Server Directory\n".encode())
            for filename in file_list: # TODO: change this to sending the entire object instead of just the name once GUI is implemented
                self.connectionSocket.send(f"{filename['Name']}\n".encode())
                
        #elif command == "msg":




class Server:
    def __init__(self, HOST, PORT):
        self.PORT = PORT
        self.HOST = HOST
        self.ActiveConnections = list()
        self.Names = list() #List of names of the clients

        self.ServerSocket = socket(AF_INET, SOCK_STREAM)
        self.ServerSocket.bind((self.HOST, self.PORT))

    def run(self):
        try:
            while True:
                self.ServerSocket.listen(1)
                print('CSNETWK Server is ready to serve...')
                connectionSocket, addr = self.ServerSocket.accept()
                print(f"Connected by {addr}")

                connection = dict()
                connection["Server"] = self
                connection["Socket"] = connectionSocket
                connection["Addr"] = addr[0]
                connection["Port"] = addr[1]

                self.ActiveConnections.append(SocketThread(connection))

                # for i in range(len(self.ActiveConnections)):
                #     self.ActiveConnections[i]["Socket"].send(f"Client {i} is connected".encode())
        except Exception as e:
            print(e)
            self.ServerSocket.close()

    def broadcast(self, message):
        for i in range(len(self.ActiveConnections)):
            self.ActiveConnections[i].send(message)
    def addName(self, name):
        self.Names.append(name)
        
    def getNames(self):
        return self.Names
if __name__ == "__main__":
    server = Server(sys.argv[1], int(sys.argv[2]))
    server.run()