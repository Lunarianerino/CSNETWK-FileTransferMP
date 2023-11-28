import re
import tkinter as tk
from tkinter import ttk

import sys
sys.path.append('./Client')
from Client import Client


class View(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.login_view()


    def login_view(self):
        #remove all widgets
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
        #remove all widgets
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

    def error_view(self, error):
        #remove all widgets
        for widget in self.winfo_children():
            widget.destroy()

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
        self.files_table = ttk.Treeview(self, columns=('Name', 'Size', 'Type', 'Date Added', 'Uploader'))

        # Set the headings
        self.files_table.heading('Name', text='Name')
        self.files_table.heading('Size', text='Size')
        self.files_table.heading('Type', text='Type')
        self.files_table.heading('Date Added', text='Date Added')
        self.files_table.heading('Uploader', text='Uploader')


        #fill up table with 5 random data to be removed
        #TODO: replace with a function from the model that would return these values.
        self.files_table.insert(parent='', index='end', iid=0, text='0', values=('File1', '1MB', 'txt', '2020-01-01', 'John Doe'))
        self.files_table.insert(parent='', index='end', iid=1, text='1', values=('File2', '2MB', 'txt', '2020-01-02', 'Luis Razon'))
        self.files_table.insert(parent='', index='end', iid=2, text='2', values=('File3', '3MB', 'txt', '2020-01-03', 'Joe Bama'))
        self.files_table.insert(parent='', index='end', iid=3, text='3', values=('File4', '4MB', 'txt', '2020-01-04', 'Austin Natividad'))
        self.files_table.insert(parent='', index='end', iid=4, text='4', values=('File5', '5MB', 'txt', '2020-01-05', 'Bob'))
        self.files_table.grid(row=1, column=0)

        self.button_area = tk.Frame()

        #Download button
        self.download_button = ttk.Button(self.button_area, text='Download')
        
        #Upload button
        self.upload_button = ttk.Button(self.button_area, text='Upload')

        #Disconnect button
        self.disconnect_button = ttk.Button(self.button_area, text='Disconnect')

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
        """
        Show a success message
        :param message:
        :return:
        """
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


class Controller:
    def __init__(self, client, view):
        self.view = view

    def join(self, ip_add, host):
        try:
            #create a client instance
            client = Client(ip_add, host)
            client.connect(client.HOST, client.PORT)

            #show a success message
            self.view.show_success(f'Connection to the File Exchange Server is successful!')
            self.view.register_view()
            print(f'Connection: {ip_add}:{host}')

            #switch to the next window

        except ValueError as error: #FIXME: change the exception
            #TODO: Show an error message
            print(error)


    def register_view(self):
        #change the window to the register page
        self.view.show_register()  

    def register(self, handle):
        try:
            self.model.handle = handle

            #TODO: INSERT CLIENT CODE HERE

            self.view.show_success(f'Successful Registration! Redirecting to Main Window')
            self.view.files_view(handle)
            print(f"Handle: {handle}")
        except ValueError as error:
            print(error)

    def close(self):
        #close all windows and exit
        self.view.quit()


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('FTP Server')
        # create a client instance
        self.client = None

        # create a view and place it on the root window
        view = View(self)
        view.grid(row=0, column=0, padx=10, pady=10)

        # create a controller
        controller = Controller(self.client, view)

        # set the controller to view
        view.set_controller(controller)


if __name__ == '__main__':
    app = App()
    app.mainloop()            