import re
import tkinter as tk
from tkinter import ttk


class Model:
    def __init__(self, email):
        self.email = email

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, value):
        """
        Validate the email
        :param value:
        :return:
        """
        pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if re.fullmatch(pattern, value):
            self.__email = value
        else:
            raise ValueError(f'Invalid email address: {value}')

    def save(self):
        """
        Save the email into a file
        :return:
        """
        with open('emails.txt', 'a') as f:
            f.write(self.email + '\n')

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

        self.text_area = ttk.Frame()
        #add a tk.Text inside text_area
        self.message_box = tk.Text(self.text_area)
        self.message_box.pack(fill=tk.X, expand=True, padx=10, pady=10)
        self.message_box.bind('<Key>', self.cancel_event)
        
        self.message_box.insert('1.0', "Welcome to the Console. enter \"/h\" for the full list of commands.")


        self.text_area.grid(row=2, column=0, sticky=tk.NSEW)



        #handle entry
        self.input_area = ttk.Frame()

        self.handle_var = tk.StringVar()
        self.handle_entry = ttk.Entry(self.input_area, textvariable=self.handle_var, width=30)
        
        self.input_submit_button = ttk.Button(self.input_area, text='Submit', command=self.register_button_clicked)
        
        self.handle_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10, pady=10)
        self.input_submit_button.pack(side=tk.LEFT, fill=tk.X, padx=10, pady=10)

        self.input_area.grid(row=3, column=0, sticky=tk.NSEW)
    

    def cancel_event(self, event):
        return "break"

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
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def join(self, ip_add, host):
        try:
            self.model.ip_add = ip_add
            self.model.host = host

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

        # create a model
        model = Model('hello@pythontutorial.net')

        # create a view and place it on the root window
        view = View(self)
        view.grid(row=0, column=0, padx=10, pady=10)

        # create a controller
        controller = Controller(model, view)

        # set the controller to view
        view.set_controller(controller)


if __name__ == '__main__':
    app = App()
    app.mainloop()            