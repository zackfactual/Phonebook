from tkinter import *
import tkinter as tk

# import other modules for access
import phonebook_func

def load_gui(self):

    self.label_fname = tk.Label(self.master,text='First Name:')
    self.label_fname.grid(row=0,column=0,padx=(27,0),pady=(10,0),sticky='nw')
    self.label_lname = tk.Label(self.master,text='Last Name:')
    self.label_lname.grid(row=2,column=0,padx=(27,0),pady=(10,0),sticky='nw')
    self.label_phone = tk.Label(self.master,text='Phone Number:')
    self.label_phone.grid(row=4,column=0,padx=(27,0),pady=(10,0),sticky='nw')
    self.label_email = tk.Label(self.master,text='Email Address:')
    self.label_email.grid(row=6,column=0,padx=(27,0),pady=(10,0),sticky='nw')
    self.label_info = tk.Label(self.master,text='Information:')
    self.label_info.grid(row=0,column=2,padx=(27,0),pady=(10,0),sticky='nw')

    self.text_fname = tk.Entry(self.master)
    self.text_fname.grid(row=1,column=0,columnspan=2,padx=(30,40),sticky='new')
    self.text_lname = tk.Entry(self.master)
    self.text_lname.grid(row=3,column=0,columnspan=2,padx=(30,40),sticky='new')
    self.text_phone = tk.Entry(self.master)
    self.text_phone.grid(row=5,column=0,columnspan=2,padx=(30,40),sticky='new')
    self.text_email = tk.Entry(self.master)
    self.text_email.grid(row=7,column=0,columnspan=2,padx=(30,40),sticky='new')

    # define listbox with scrollbar
    self.scrollbar = Scrollbar(self.master,orient=VERTICAL)
    self.list = Listbox(self.master,exportselection=0,yscrollcommand=self.scrollbar.set)
    self.list.bind('<<ListboxSelect>>', lambda event: phonebook_func.onSelect(self,event))
    self.scrollbar.config(command = self.list.yview)
    self.scrollbar.grid(row=1,column=5,rowspan=7,sticky='nes')
    self.list.grid(row=1,column=2,rowspan=7,columnspan=3,sticky='nesw')

    self.button_add = tk.Button(self.master,width=12,height=2,text='Add',command=lambda: phonebook_func.addToList(self))
    self.button_add.grid(row=8,column=0,padx=(25,0),pady=(45,10),sticky='w')
    self.button_update = tk.Button(self.master,width=12,height=2,text='Update',command=lambda: phonebook_func.onUpdate(self))
    self.button_update.grid(row=8,column=1,padx=(25,0),pady=(45,10),sticky='w')
    self.button_delete = tk.Button(self.master,width=12,height=2,text='Delete',command=lambda: phonebook_func.onDelete(self))
    self.button_delete.grid(row=8,column=2,padx=(25,0),pady=(45,10),sticky='w')
    self.button_close = tk.Button(self.master,width=12,height=2,text='Close',command=lambda: phonebook_func.ask_quit(self))
    self.button_close.grid(row=8,column=4,padx=(25,0),pady=(45,10),sticky='e')

    phonebook_func.create_db(self)
    phonebook_func.onRefresh(self)

if __name__ == "__main__":
    pass
