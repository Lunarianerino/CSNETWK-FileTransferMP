import re
import tkinter as tk
from tkinter import ttk
import json
import tkinter.messagebox as messagebox

import sys
sys.path.append('./Client')
from Client import Client

import threading

class View(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.login_view()


    def login_view(self):
        #reset the window by removing all widgets, frames, etc.
        for widget in self.winfo_children():
            widget.destroy()

            

        
        # create widgets
        # IP label
        self.ip_label = ttk.Label(self, text='IP Address:')
        self.ip_label.grid(row=1, column=0)

        # IP entry
        self.ip_var = tk.StringVar()
        self.ip_entry = ttk.Entry(self, textvariable=self.ip_var, width=30)
        self.ip_entry.grid(row=1, column=1, sticky=tk.NSEW)

        # Host label
        self.host_label = ttk.Label(self, text='Host:')
        self.host_label.grid(row=3, column=0)

        # host entry
        self.host_var = tk.StringVar()
        self.host_entry = ttk.Entry(self, textvariable=self.host_var, width=30)
        self.host_entry.grid(row=3, column=1, sticky=tk.NSEW)

        # join button
        self.join_button = ttk.Button(self, text='Join', command=self.join_button_clicked)
        self.join_button.grid(row=8, column=1, sticky=tk.NSEW)

        # message
        self.message_label = ttk.Label(self, text='', foreground='red')
        self.message_label.grid(row=5, column=1, sticky=tk.W)

        # set the controller
        self.controller = None

    def register_view(self):
        #reinitialize the window
        for widget in self.winfo_children():
            widget.destroy()
            
        

        #create widgets
    
        #handle label
        self.handle_label = ttk.Label(self, text='Handle:')
        self.handle_label.grid(row=2, column=0)

        #handle entry
        self.handle_var = tk.StringVar()
        self.handle_entry = ttk.Entry(self, textvariable=self.handle_var, width=30)
        self.handle_entry.grid(row=2, column=1, sticky=tk.NSEW)
    
        #register button
        self.register_button = ttk.Button(self, text='Register', command=self.register_button_clicked)
        self.register_button.grid(row=9, column = 1, sticky=tk.NSEW)

        #message
        self.message_label = ttk.Label(self, text='', foreground='red')
        self.message_label.grid(row=3, column=1, sticky=tk.W)

    
    def download_view(self):
        #create a new window
        self.download_window = tk.Toplevel(self)
        self.download_window.title('Download')
        self.download_window.geometry('300x100')
        
        #create widgets
        #drop-down box for files
        self.file_list = self.getFileList()
        
        #extract all names for the drop-down box
        self.file_names = []
        for file in self.file_list:
            self.file_names.append(file['Name'])
            
            
        self.file_var = tk.StringVar()
        self.file_var.set(self.file_names[0])
        self.file_dropdown = ttk.OptionMenu(self.download_window, self.file_var, *self.file_names)
        
        #download button
        self.download_button = ttk.Button(self.download_window, text='Download', command=self.download_file)
        
        #pack widgets
        self.file_dropdown.pack()
        self.download_button.pack()
        
    
    
    def upload_view(self):
        self.upload_window = tk.Toplevel(self)
        self.upload_window.title('Upload')
        self.upload_window.geometry('300x100')
        
        #create widgets
        
        self.filename_label = ttk.Label(self.upload_window, text='Filename: ')
        self.file_var = tk.StringVar()
        self.handle_entry = ttk.Entry(self.upload_window, textvariable=self.file_var, width=30)
        
        self.upload_button = ttk.Button(self.upload_window, text='Upload', command=self.upload_file)
        
        #pack widgets
        self.filename_label.pack()
        self.handle_entry.pack()
        self.upload_button.pack()
        
        
        
    
    def upload_file(self):
        if self.controller:
            self.controller.upload(self.file_var.get())
            
    def upload_button_clicked(self):
        if self.controller:
            self.upload_view()
            

            
    
    
    
    def error_view(self, error):
        #remove all widgets
        for widget in self.winfo_children():
            widget.destroy()
            if isinstance(widget, tk.Frame): 
                for child in widget.winfo_children(): 
                    child.destroy()

        #create widgets
        #error label
        self.error_label = ttk.Label(self, text=error)
        self.error_label['foreground'] = 'red'
        self.error_label.grid(row=0, column=0)

        #close button
        self.close_button = ttk.Button(self, text='Close', command=self.close_button_clicked)
        self.close_button.grid(row=2, column=0)

    def close_button_clicked(self):
        self.controller.close()
        
        
    def getFileList(self):
        try:
            f = open("./Server/Storage/FileList.json", "r")
            file_list = json.load(f)
            f.close()
            
        except Exception as e:
            print(e)
        
        return file_list
        
    
    def files_view(self, handle):
        if handle == None or handle == '':
            self.error_view('Please register first!')
            return
        
        #actual code here

        #remove all widgets
        for widget in self.winfo_children():
            widget.destroy()

        #create widgets

        #heading
        self.heading_label = ttk.Label(self, text=f'Welcome, {handle} :)')
        self.heading_label.grid(row=0, column=0)

        #files table
        self.files_table = ttk.Treeview(self, columns=('Name', 'Size', 'DateTime', 'Uploader'))

        # Set the headings
        self.files_table.heading('Name', text='Name')
        self.files_table.heading('Size', text='Size')
        self.files_table.heading('DateTime', text='DateTime')
        self.files_table.heading('Uploader', text='Uploader')


        #TODO: replace with a function from the model that would return these values.
        
        file_list = self.getFileList()
        
        for file in file_list:
            self.files_table.insert('', 'end', text=str(file_list.index(file)+1), values=(file['Name'], file['Size'], file['DateTime'], file['Uploader']))
            
        self.files_table.grid(row=1, column=0)
        
        self.button_area = tk.Frame()

        #Download button
        self.download_button = ttk.Button(self.button_area, text='Download', command=self.download_button_clicked)
        
        #Upload button
        self.upload_button = ttk.Button(self.button_area, text='Upload', command=self.upload_button_clicked)

        #Disconnect button
        self.disconnect_button = ttk.Button(self.button_area, text='Disconnect', command=self.controller.close)

        #pack buttons
        self.download_button.pack(side=tk.LEFT)
        self.upload_button.pack(side=tk.LEFT)
        self.disconnect_button.pack(side=tk.LEFT)

        self.button_area.grid(row=2, column=0, pady=10)

    def set_controller(self, controller):
        """
        Set the controller
        :param controller:
        :return:
        """
        self.controller = controller

    def join_button_clicked(self):
        if self.controller:
            self.controller.join(self.ip_var.get(), self.host_var.get())

    def show_error(self, message):
        """
        Show an error message
        :param message:
        :return:
        """
        self.message_label['text'] = message
        self.message_label['foreground'] = 'red'
        self.message_label.after(3000, self.hide_message)

    def show_success(self, message):

        self.message_label['text'] = message
        self.message_label['foreground'] = 'green'
        self.message_label.after(3000, self.hide_message)

    def hide_message(self):
        """
        Hide the message
        :return:
        """
        self.message_label['text'] = ''       

    def register_button_clicked(self):
        if self.controller:
            self.controller.register(self.handle_var.get())
    
    
    def download_button_clicked(self):
        if self.controller:
            self.controller.download_view()
            
    def download_file(self):
        if self.controller:
            self.controller.download(self.file_var.get())
        


class Controller:
    def __init__(self, client, view):
        self.view = view
        self.client = client

    def join(self, ip_add, host):
        try:
            #create a client instance
            self.client.connect(ip_add, host)

            #switch to the register window
            self.view.register_view()
            messagebox.showinfo("Connected", "You have successfully connected to the server.")

        except ValueError as error: #FIXME: change the exception
            #TODO: Show an error message
            print(error)


    def register_view(self):
        #change the window to the register page
        self.view.show_register()  

    def register(self, handle):
        try:
            #TODO: INSERT CLIENT CODE HERE
            self.client.commandHandler("/register", [handle])


            self.view.files_view(handle)
            print(f"Handle: {handle}")
            messagebox.showinfo("Registered", f"You have successfully registered as {handle}.")
        except ValueError as error:
            print(error)
    
    
    def download_view(self):
        self.view.download_view()
        
    def download(self, filename):
        try:
            self.client.commandHandler("/get", [filename])
            
            #refresh the file list
            self.view.files_view(self.client.handle)
            
            #close the download window
            self.view.download_window.destroy()
            messagebox.showinfo("Download Complete", f"The file {filename} has been downloaded.")
            
            
        except ValueError as error:
            print(error)
            
    def upload(self, filename):
        try:
            self.client.commandHandler("/store", [filename])
            
            #refresh the file list
            self.view.files_view(self.client.handle)
            
            #close the upload window
            self.view.upload_window.destroy()
            messagebox.showinfo("Upload Complete", f"The file {filename} has been uploaded.")
            
        except ValueError as error:
            print(error)

    def close(self):
        #close client and exit
        self.client.commandHandler("/leave", [])
        messagebox.showinfo("Disconnected", "You have successfully disconnected from the server. Thank you for using the File Transfer Client.")
        #destroy all windows
        sys.exit(0)


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('File Transfer Client')
        # create a client instance
        self.client = Client()

        # create a view and place it on the root window
        view = View(self)
        view.grid(row=0, column=0, padx=10, pady=10)

        # create a controller
        controller = Controller(self.client, view)

        # set the controller to view
        view.set_controller(controller)
        
        self.thread = threading.Thread(target=self.mainloop())
        self.thread.start()

if __name__ == '__main__':
    app = App()
    app.mainloop()            