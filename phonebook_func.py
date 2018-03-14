import os
from tkinter import *
from tkinter import messagebox
import sqlite3


# pass in tkinter frame (master) reference, plus width and height
def center_window(self, w, h):
    # get user's screen width and height
    screen_width = self.master.winfo_screenwidth()
    screen_height = self.master.winfo_screenheight()
    # calculate coords to center app on user's screen
    x = int((screen_width / 2) - (w / 2))
    y = int((screen_height / 2) - (h / 2))
    centerGeo = self.master.geometry('{}x{}+{}+{}'.format(w, h, x, y))
    return centerGeo


# confirm close if user Xs out
def ask_quit(self):
    if messagebox.askokcancel("Quit Phonebook?", "Are you sure you want to quit?"):
        # close program to prevent memory leak
        self.master.destroy()
        os._exit(0)


def create_db(self):
    conn = sqlite3.connect('phonebook.db')
    with conn:
        cur = conn.cursor()
        cur.execute("CREATE TABLE if not exists tbl_phonebook( \
            ID INTEGER PRIMARY KEY AUTOINCREMENT, \
            col_fname TEXT, \
            col_lname TEXT, \
            col_fullname TEXT, \
            col_phone TEXT, \
            col_email TEXT \
            );")
        # commit to save changes and close dB connection
        conn.commit()
    conn.close()
    first_run(self)


def first_run(self):
    data = ('John', 'Doe', 'John Doe', '111-111-1111', 'jdoe@gmail.com')
    conn = sqlite3.connect('phonebook.db')
    with conn:
        cur = conn.cursor()
        cur, count = count_records(cur)
        if count < 1:
            cur.execute(
                """INSERT INTO tbl_phonebook (col_fname,col_lname,col_fullname,col_phone,col_email) VALUES (?,?,?,?,?)""",
                data)
            conn.commit()
    conn.close()


def count_records(cur):
    cur.execute("""SELECT COUNT(*) FROM tbl_phonebook""")
    count = cur.fetchone()[0]
    return cur, count


# select item from Listbox
def onSelect(self, event):
    # self.list is the widget calling event
    varList = event.widget
    select = varList.curselection()[0]
    value = varList.get(select)
    conn = sqlite3.connect('phonebook.db')
    with conn:
        cursor = conn.cursor()
        cursor.execute("""SELECT col_fname,col_lname,col_phone,col_email FROM tbl_phonebook WHERE col_fullname = (?)""",
                       [value])
        varBody = cursor.fetchall()
        # returns a tuple to split into 4 parts using data[] during iteration
        for data in varBody:
            self.text_fname.delete(0, END)
            self.text_fname.insert(0, data[0])
            self.text_lname.delete(0, END)
            self.text_lname.insert(0, data[1])
            self.text_phone.delete(0, END)
            self.text_phone.insert(0, data[2])
            self.text_email.delete(0, END)
            self.text_email.insert(0, data[3])


def addToList(self):
    var_fname = self.text_fname.get()
    var_lname = self.text_lname.get()
    # normalize data for dB consistency, removing blank space and capitalizing first letters
    var_fname = var_fname.strip()
    var_lname = var_lname.strip()
    var_fname = var_fname.title()
    var_lname = var_lname.title()
    var_fullname = ("{} {}".format(var_fname, var_lname))  # combine normalized names into a fullname
    print("var_fullname: {}".format(var_fullname))
    var_phone = self.text_phone.get().strip()
    var_email = self.text_email.get().strip()
    # require all forms filled
    if (len(var_fname) > 0) and (len(var_lname) > 0) and (len(var_phone) > 0) and (
            len(var_email) > 0):
        # require properly formatted email address
        if not "@" or not "." in var_email:
            messagebox.showerror("ERROR: Bad Email", "Please enter a properly formatted email address.")
        else:
            conn = sqlite3.connect('phonebook.db')
            with conn:
                cursor = conn.cursor()
                # disregard duplicate fullname entries and alert user, apologies to the John Smiths of the world
                cursor.execute(
                    """SELECT COUNT(col_fullname) FROM tbl_phonebook WHERE col_fullname = '{}'""".format(var_fullname))
                count = cursor.fetchone()[0]
                chkName = count
                if chkName == 0:
                    print("chkName: {}".format(chkName))
                    cursor.execute(
                        """INSERT INTO tbl_phonebook (col_fname,col_lname,col_fullname,col_phone,col_email) VALUES (?,?,?,?,?)""",
                        (var_fname, var_lname, var_fullname, var_phone, var_email))
                    self.list.insert(END, var_fullname)  # update listbox with new fullname
                    onClear(self)  # call function to clear all textboxes
                else:
                    messagebox.showerror("ERROR: Duplicate Name", "{} already exists in the database.".format(var_fullname))
                    onClear(self)
            conn.commit()
            conn.close()
    else:
        messagebox.showerror("ERROR: Missing Input", "Please fill in all four fields.")


def onDelete(self):
    try:
        index = self.list.curselection()[0]
        self.list.get(index)
    except IndexError:
        messagebox.showinfo("ERROR: Missing Selection", "No name was selected from the list.")
        return
    var_select = self.list.get(self.list.curselection())
    conn = sqlite3.connect('phonebook.db')
    with conn:
        cur = conn.cursor()
        # prevent user from deleting last record in the dB
        cur.execute("""SELECT COUNT(*) FROM tbl_phonebook""")
        count = cur.fetchone()[0]
        if count > 1:
            confirm = messagebox.askokcancel("Confirm Deletion?",
                                             "Are you sure you want to delete {}?".format(var_select))
            if confirm:
                conn = sqlite3.connect('phonebook.db')
                with conn:
                    cursor = conn.cursor()
                    cursor.execute("""DELETE FROM tbl_phonebook WHERE col_fullname = '{}'""".format(var_select))
                    onDeleted(self)  # call function to clear textboxes and selected index of listbox
                    conn.commit()
        else:
            messagebox.showerror("ERROR: Final Record",
                                           "{} is the final record in the database and cannot be deleted at this time.".format(
                                               var_select))
        conn.close()

def onDeleted(self):
    # clear text in textboxes and remove entry from listbox
    onClear(self)
    index = self.list.curselection()[0]
    self.list.delete(index)

def onClear(self):
    # clear text in textboxes
    self.text_fname.delete(0, END)
    self.text_lname.delete(0, END)
    self.text_phone.delete(0, END)
    self.text_email.delete(0, END)


# repopulate listbox to coincide with dB
def onRefresh(self):
    self.list.delete(0, END)
    conn = sqlite3.connect('phonebook.db')
    with conn:
        cursor = conn.cursor()
        cursor.execute("""SELECT COUNT(*) FROM tbl_phonebook""")
        count = cursor.fetchone()[0]
        i = 0
        while i < count:
            cursor.execute("""SELECT col_fullname FROM tbl_phonebook""")
            varList = cursor.fetchall()[i]
            for item in varList:
                self.list.insert(0, str(item))
                i = i + 1
    conn.close()


def onUpdate(self):
    try:
        var_select = self.list.curselection()[0]  # i of list selection
        var_value = self.list.get(var_select)  # list selection's text value
    except IndexError:
        messagebox.showinfo("ERROR: Missing Selection", "No name was selected from the list.")
        return
    # the user can only update phones and emails, not names
    var_phone = self.text_phone.get().strip()
    var_email = self.text_email.get().strip()
    if (len(var_phone) > 0) and (len(var_email) > 0):
        conn = sqlite3.connect('phonebook.db')
        with conn:
            cur = conn.cursor()
            # count records to see if user changes are already in the dB
            cur.execute("""SELECT COUNT(col_phone) FROM tbl_phonebook WHERE col_phone = '{}'""".format(var_phone))
            count = cur.fetchone()[0]
            print(count)
            cur.execute("""SELECT COUNT(col_email) FROM tbl_phonebook WHERE col_email = '{}'""".format(var_email))
            count2 = cur.fetchone()[0]
            print(count2)
            if count == 0 or count2 == 0:
                response = messagebox.askokcancel("Update Selection",
                                                  "The following changes will be implemented for {}:\n\nPhone Number: {}\nEmail: {}\n\nProceed?".format(
                                                      var_value, var_phone, var_email))
                print(response)
                if response:
                    with conn:
                        cursor = conn.cursor()
                        cursor.execute(
                            """UPDATE tbl_phonebook SET col_phone = '{0}',col_email = '{1}' WHERE col_fullname = '{2}'""".format(
                                var_phone, var_email, var_value))
                        onClear(self)
                        conn.commit()
                else:
                    messagebox.showinfo("ERROR: Invalid Update", "No changes have been made to {}.".format(var_value))
            else:
                messagebox.showinfo("ERROR: Invalid Update",
                                    "{} already has:\n\nPhone Number: {}\nEmail: {}\n\nYou cannot change the name of a contact.".format(var_value, var_phone,
                                                                                            var_email))
            onClear(self)


if __name__ == "__main__":
    pass
