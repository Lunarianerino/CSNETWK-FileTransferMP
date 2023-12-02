#import socket module
from socket import *
import sys # In order to terminate the program
import threading
import os
import argparse
import time
import select
class Client():
    def __init__(self, HOST = None, PORT = None):
        self.HOST = HOST
        self.PORT = PORT
        self.connection_flag = False
        self.message_thread = threading.Thread(target=self.run, daemon=True)
        self.kill_thread = False
        self.path = os.getcwd()
        
        self.handle = None
        
        if(self.path.split('\\')[-1] != "Client"):
            self.path = self.path + "\\Client"
        #self.start()

    def connect(self, HOST, PORT):
        self.HOST = HOST
        self.PORT = PORT
        self.clientEndpoint = socket()
        try:
            self.clientEndpoint.connect((self.HOST, int(self.PORT)))
        except Exception as e:
            self.HOST = None
            self.PORT = None
            return False
        self.buffer_size = 1024
        self.timeout = 5
        self.connection_flag = True

        return True

    def run(self):
        while self.connection_flag:
            #print("Waiting for reply...")
            try:
                ready = select.select([self.clientEndpoint], [], [], 0.1)
                if ready[0]:
                    reply = self.clientEndpoint.recv(self.buffer_size).decode()
                    self.HandleStatus(reply)
            except Exception as e:
                print(e)
                break  

            if self.kill_thread:
                break
    def start_message_thread(self):
        if not self.message_thread.is_alive() and self.connection_flag:
            self.message_thread = threading.Thread(target=self.run, daemon=True)
            self.kill_thread = False
            self.message_thread.start()
            print("Message thread started")
    def kill_message_thread(self):
        if self.message_thread.is_alive() and self.connection_flag:
            self.kill_thread = True
            self.message_thread.join()
            print("Message thread has been killed.")
    def sendMessage(self, *args):
        message = " ".join(args)
        print(message)
        self.clientEndpoint.send(message.encode())
    def close(self):
        self.clientEndpoint.close()
        self.buffer_size = 0
        self.connection_flag = False
        
    def HandleStatus(self, status):
        status, message = status.split("|", 1)
        if status == "444 CONNECTION_CLOSED":
            self.connection_flag = False
            self.HOST = None
            self.PORT = None
        #print(status)
        print(message)
        return status, message
    def commandHandler(self, command, *args):
        commands = ["/join", "/register", "/leave", "/store", "/dir", "/get", "/broadcast", "/?", "/msg"]
        if command not in commands:
            print("Error: Command not found. Please use /? to view all commands.")
            return
        if command != "/broadcast":
            self.kill_message_thread()

        if command == "/join":

            #check if args is greater than 2
            if len(args[0]) != 2:
                print("Error: Command parameters do not match or is not allowed.")
                return
            
            print("Joining...")
            #print(args)
            if self.connect(args[0][0], args[0][1]):
                status, message = self.HandleStatus(self.clientEndpoint.recv(self.buffer_size).decode())
            else:
                print("Error: Connection to the Server has failed! Please check IP Address and Port Number.")
        elif command == "/register":
            if len(args[0]) < 1:
                print("Error: Command parameters do not match or is not allowed.")
                return
            if self.connection_flag is False:
                print("Error: Registration failed. Please connect to the server first.")
                return
            handle = " ".join(args[0])
            self.handle = handle
            self.sendMessage(command, handle)
            status, message = self.HandleStatus(self.clientEndpoint.recv(self.buffer_size).decode())
        elif command == "/leave":
            if len(args[0]) > 0:
                print("Error: Command parameters do not match or is not allowed.")
                return
            if self.connection_flag is False:
                print("Error: Disconnection failed. Please connect to the server first.")
            else:
                self.sendMessage(command)
                reply = self.clientEndpoint.recv(self.buffer_size).decode()
                self.HandleStatus(reply)
        elif command == "/?":
            if len(args[0]) > 0:
                print("Error: Command parameters do not match or is not allowed.")
                return
            if self.connection_flag is False:
                print("Client Commands: \n/join <IP Address> <Port Number> - Connect to the server application")
                print("/? - Request command help to output all Input Syntax commands for references")
                print("More commands will be available once connected to the server application")
            else:
                print("File Transfer Commands:")
                print("/leave - Disconnect to the server application")
                print('/register <handle> - Register a handle to the server')
                print("/store <filename> - Send file to server")
                print("/dir - Request directory file list from a server")
                print("/get <filename> - Request file from server")
                print("/? - Request command help to output all Input Syntax commands for references")
                
        elif command == "/store":
            if len(args[0]) < 1:
                print("Error: Command parameters do not match or is not allowed.")
                return
            if self.connection_flag is False:
                print("Error: Command failed. Please connect to the server first.")
                return
            filename = " ".join(args[0])
            print(f"Sending file {filename}...")
            if os.path.exists(filename):
                print("File exists.")
                self.sendMessage(command, filename)
                status, message = self.HandleStatus(self.clientEndpoint.recv(self.buffer_size).decode())
                if status == "200 OK":
                    self.sendMessage(str(os.path.getsize(filename)))
                    status, message = self.HandleStatus(self.clientEndpoint.recv(self.buffer_size).decode())
                    f = open(filename, 'rb')
                    data = f.read()
                    self.clientEndpoint.send(data)
                    f.close()
                    status, message = self.HandleStatus(self.clientEndpoint.recv(self.buffer_size).decode())
            else:
                print("Error: File not found.")
        elif command == "/get":
            if len(args[0]) < 1:
                print("Error: Command parameters do not match or is not allowed.")
                return
            if self.connection_flag is False:
                print("Error: Command failed. Please connect to the server first.")
                return
            filename = " ".join(args[0])
            print(f"Getting file {filename}...")
            self.sendMessage(command, filename)
            status, message = self.HandleStatus(self.clientEndpoint.recv(self.buffer_size).decode())
            if status == "200 OK":
                filesize = int(message)
                self.sendMessage("200 OK|File size received")
                i = 1
                if os.path.exists(f"{self.path}/Downloads/{filename}"): #aaron pic.jpg
                    ext = filename.split(".")[-1] #.jpg
                    filename = ".".join(filename.split(".")[:-1]) #aaron pic
                    while os.path.exists(f"{self.path}/Downloads/{filename}({i}).{ext}"): #aaron pic(1).jpg
                        i+=1
                    filename = f"{filename}({i})" + "." + str(ext)


                open(f"{self.path}/Downloads/{filename}", 'x')
                f = open(f"{self.path}/Downloads/{filename}", 'wb')

                totalRecv = 0

                try:
                    while totalRecv < filesize:
                        data = self.clientEndpoint.recv(self.buffer_size)
                        totalRecv += len(data)
                        f.write(data)
                        print(f"Progress: {totalRecv/filesize*100}%")
                    f.close()
                    self.clientEndpoint.send("200 OK|File transfer complete".encode())
                except Exception as e:
                    print(e)
                    self.clientEndpoint.send("409 CONFLICT|File transfer failed".encode())
                    print("Error: File transfer failed.")
                    return
                
                status, message = self.HandleStatus(self.clientEndpoint.recv(self.buffer_size).decode())
        elif command == "/dir":
            if len(args[0]) > 0:
                print("Error: Command parameters do not match or is not allowed.")
                return
            if self.connection_flag is False:
                print("Error: Command failed. Please connect to the server first.")
                return
            self.sendMessage(command)
            status, message = self.HandleStatus(self.clientEndpoint.recv(self.buffer_size).decode())

        else:
            self.sendMessage(command, " ".join(args[0]))
            reply = self.clientEndpoint.recv(self.buffer_size).decode()
            self.HandleStatus(reply)
            # self.sendMessage(args[0][0])
            # self.sendFile(args[0][0])
        
        self.start_message_thread()
            
if __name__ == "__main__":
    client = Client()
    while True:
        try:
            text = input(">> ")
            if text[0] == '/':
                command = text.split()
                client.commandHandler(command[0], command[1:])
            else:
                #if client != None:
                #    client.sendMessage(text)
                print("Error: Command not found. Please use /? to view all commands.")
        except KeyboardInterrupt:
            print("Closing connection...")
            break
            #TODO: might have to implement a list of errors for easy error messages in GUI
        except Exception as e:
            print (e)
    print("Process interrupted")
    try:
        exit(0)
    except SystemExit:
        os._exit(0)

        
