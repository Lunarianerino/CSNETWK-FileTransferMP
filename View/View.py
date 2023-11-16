import tkinter as tk
from tkinter import ttk

class View(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        #create a window with the label "Main Window"
        self.label = ttk.Label(self, text="Main Window")
        self.label.grid(row = 1, column = 0)

        # IP Addresss entry
        self.ip_address_label = ttk.Label(self, text="IP Address")
        self.ip_address_var = tk.StringVar()
        self.ip_address_entry = ttk.Entry(self, width=15, textvariable=self.ip_address_var)
        self.ip_address_entry.grid(row=1, column=1, sticky=tk.NSEW)


if __name__ == '__main__':
    root = tk.Tk()
    view = View(root)
    view.grid(row=0, column=0)
    root.mainloop()