#import socket module
from socket import *
import sys # In order to terminate the program
import threading
import time
import os
import json
class SocketThread(threading.Thread):
    def __init__(self, connection):
        threading.Thread.__init__(self)
        self.connectionSocket = connection["Socket"]
        self.addr = connection["Addr"]
        self.server = connection["Server"]
        self.start()
        self.Names = list()
        self.timeout = 5 #seconds
        self.connectionSocket.send("200 OK|Connection to the File Exchange Server is successful!".encode())
        self.path = os.getcwd()
        
        if(self.path.split('\\')[-1] != "Server"):
            self.path = self.path + "\\Server"
            
            
        print(self.path)
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


    #function to check if a socket is in the list of names
    def checkHandle(self, port):
        for name in self.server.getNames():
            if str(name["Port"]) == str(port):
                return name["Name"]
        return None
    
    def checkIfRegistered(self, port):
        for name in self.server.getNames():
            if str(name["Port"]) == str(port):
                return True
        return False
    
    def statusHandler(self, status):
        status, message = status.split("|", 1)
        print(status)
        print(message)
        return status, message
    
    def commandHandler(self, command, *args):
        print(command)
        if command == "leave":
            print("Closing connection...")
            self.connectionSocket.send("444 CONNECTION_CLOSED|Connection closed. Thank you!".encode())
            sys.exit() #close thread
            #self.server.ActiveConnections.remove(self)
            
        elif command == "broadcast":
            #check first if user is registered
            if(self.checkIfRegistered(self.connectionSocket.getpeername()[1]) == False):
                self.connectionSocket.send("401 UNAUTHORIZED|You must first use /register to access this command. Enter /? for more details.".encode())
                return

            self.server.broadcast(args[0])

        elif command == "register":
            #check if args[0] exists
            str_name = " ".join(args[0])
            if len(str_name) == 0:
                self.connectionSocket.send("400 BAD REQUEST|No handle provided.".encode())
                return

            #check if str_name is already in use
            for name in self.server.getNames():
                if name["Name"] == str_name:
                    self.connectionSocket.send("409 CONFLICT|Error: Registration failed. Handle or alias already exists.".encode())
                    return
            
            name = {
                "Name": str_name,
                "Port": self.connectionSocket.getpeername()[1]
            }

            self.server.addName(name)
            self.connectionSocket.send(f"200 OK|Welcome, {str_name}!".encode())
            print("Server Names: ")
            print(self.server.getNames())

        elif command == "dir":
            #check first if user is registered
            if(self.checkIfRegistered(self.connectionSocket.getpeername()[1]) == False):
                self.connectionSocket.send("401 UNAUTHORIZED|You must first use /register to access this command. Enter /? for more details.".encode())
                return
            #get the list of files in /Server/Files
            if len(args[0]) > 0:
                self.connectionSocket.send("400 BAD_REQUEST|Error: Command parameters do not match or is not allowed.".encode())
                return
            directory = self.path + r'/Files/'
            files = os.listdir(directory)
            self.file_list = [] #list of dicts for each file
            for f in files:
                file_list.append({"Name": f})
            print(file_list)
            string_to_send=""
            for filename in file_list: # TODO: change this to sending the entire object instead of just the name once GUI is implemented
                string_to_send = string_to_send + f"{filename['Name']}\n"
            
            self.connectionSocket.send(("200 OK|Server Directory: \n" + string_to_send).encode())
        
        elif command == "get":
            #check first if user is registered
            if(self.checkIfRegistered(self.connectionSocket.getpeername()[1]) == False):
                self.connectionSocket.send("401 UNAUTHORIZED|You must first use /register to access this command. Enter /? for more details.".encode())
                return
            filename = " ".join(args[0])
            
            directory = self.path + r'/Files/'
            files = os.listdir(directory)

            #if file exists, send file
            if filename in files:
                self.connectionSocket.send(f"200 OK|{str(os.path.getsize(directory+filename))}".encode())
                status, message = self.statusHandler(self.connectionSocket.recv(1024).decode())
                if status != "200 OK":
                    return
                f = open(directory + filename, 'rb')
                data = f.read()
                self.connectionSocket.send(data)
                f.close()
                status, message = self.statusHandler(self.connectionSocket.recv(1024).decode())
                if status == "200 OK":
                    self.connectionSocket.send(f"200 OK|File received from Server: {filename}".encode())
                else:
                    self.connectionSocket.send("409 CONFLICT|Something went wrong while transferring data...".encode())
            else:
                self.connectionSocket.send("404 NOT FOUND|Error: File not found in server".encode())

        elif command == "store":

            #TODO: insert check here if user has registered
            print(f"Checking user: {self.connectionSocket.getpeername()[1]}")
            user = self.checkHandle(self.connectionSocket.getpeername()[1])
            print(f"user: {user}")
            if user == None:
                self.connectionSocket.send("401 UNAUTHORIZED|You must first use /register to access this command. Enter /? for more details.".encode())
                return
            self.connectionSocket.send(f"200 OK|User {user} found.".encode())
        
            filename = " ".join(args[0])
            filename = filename.split("/")[-1]
            print(f"Receiving file {filename}...")

            curr_timeout = 0
            received = False
            try:
                while curr_timeout < self.timeout:
                    filesize = int(self.connectionSocket.recv(1024).decode())
                    if filesize > 0:
                        received = True
                        break
                    time.sleep(1)
            except Exception as e:
                print(e)
                self.connectionSocket.send("409 CONFLICT|Something went wrong while transferring data...".encode())
                return
            
            if received:
                curr_timeout = 0
                self.connectionSocket.send("200 OK|File Size Received".encode())
            else:
                self.connectionSocket.send("409 CONFLICT|File Size not received, aborting...".encode())
                return
            
            print(f"Filesize: {filesize}")



            # #self.connectionSocket.send("File has been uploaded".encode())
            # #checking for duplicate files
            i = 1
            if os.path.exists(self.path + f"/Files/{filename}"): #aaron pic.jpg
                ext = filename.split(".")[-1] #.jpg
                filename = ".".join(filename.split(".")[:-1]) #aaron pic
                while os.path.exists(self.path + f"/Files/{filename}({i}).{ext}"): #aaron pic(1).jpg
                    i+=1
                filename = f"{filename}({i})" + "." + str(ext)

            file = {
                "Name": filename,
                "Uploader": user,
                "DateTime" : time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                "Size": filesize
            }

            try:
                open(self.path + f"/Files/{filename}", 'x')
                f = open(self.path + f"/Files/{filename}", 'wb')

                totalRecv = 0

                while totalRecv < filesize:
                    curr_timeout = 0
                    while curr_timeout < self.timeout:
                        data = self.connectionSocket.recv(1024)
                        curr_timeout += 1
                        if len(data) > 0:
                            break
                        
                        time.sleep(1)
                    totalRecv += len(data)
                    f.write(data)
                
                print("Download Complete!")
                f.close()
            except Exception as e:
                print(e)
                self.connectionSocket.send("409 CONFLICT|Something went wrong while receiving data...".encode())
                return
            
            self.server.broadcast(f"200 OK|{file['Uploader']} <{file['DateTime']}>: Uploaded {file['Name']}".encode())
            #FIXME: CHANGE TO BROADCAST (SHOULD BE SEEN BY ALL CLIENTS)

            #append file to FileList.json (Will be used for GUI)
            try:
                with open(self.path + '/Storage/FileList.json', 'r') as f:
                    data = json.load(f)
            except json.decoder.JSONDecodeError:
                data = []
            data.append(file)
            with open(self.path + '/Storage/FileList.json', 'w') as f:
                json.dump(data, f)
        elif command == "msg":
            print(f"Checking user: {self.connectionSocket.getpeername()[1]}")
            user = self.checkHandle(self.connectionSocket.getpeername()[1])
            print(f"user: {user}")
            if user == None:
                self.connectionSocket.send("401 UNAUTHORIZED|You must first use /register to access this command. Enter /? for more details.".encode())
                return
            
            query = " ".join(args[0])
            query = query.split("|")

            if len(query) < 2:
                self.connectionSocket.send("400 BAD REQUEST|Error: Command parameters do not match or is not allowed.".encode())
                return

            recipient = query[0]
            message = query[1]

            if (not any(name["Name"] == recipient for name in self.server.getNames())):
                self.connectionSocket.send("404 NOT FOUND|Error: Recipient not found.".encode())
                return

            for name in self.server.getNames():
                if name["Name"] == recipient:
                    port = name["Port"]
                    break
            
            for connection in self.server.ActiveConnections:
                if connection.connectionSocket.getpeername()[1] == port:
                    connection.send(f"200 OK|{user} <{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}>: {message}")
                    break
        else:
            self.connectionSocket.send("400 BAD REQUEST|Error: Command not found.".encode())
            return




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

    def broadcast(self, *args):
        for i in range(len(self.ActiveConnections)):
            self.ActiveConnections[i].send("209 BROADCAST|"+" ".join(args[0]))
    def addName(self, name):
        self.Names.append(name)
        
    def getNames(self):
        return self.Names
if __name__ == "__main__":
    try:
        server = Server(sys.argv[1], int(sys.argv[2]))
        server.run()
    except KeyboardInterrupt:
        print("Server is closing...")
        server.ServerSocket.close()
        sys.exit()





