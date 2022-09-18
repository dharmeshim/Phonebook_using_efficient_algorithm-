from ast import Name
from email.iterators import typed_subpart_iterator
from msilib.schema import Icon
from tkinter import *
import sqlite3
import tkinter.ttk as ttk
import tkinter.messagebox as tkMessageBox
from turtle import update
from unicodedata import name
from xml.dom.expatbuilder import Namespaces

root = Tk()
root.title("PHONEBOOK USING HASHING")
width = 850
height = 400
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width / 2) - (width / 2)
y = (screen_height / 2) - (height / 2)
root.geometry("%dx%d+%d+%d" % (width, height, x, y))
#root.resizable(0, 0)
root.config(bg="white")

 
#VARIABLES

NAME = StringVar()
AGE = StringVar()
ADDRESS = StringVar()
CONTACT = StringVar()

contacts= ["aarav","aniruth","bargavv","binu","dhanush","vector"]

#METHODS

def Database():
    conn = sqlite3.connect("pythontut.db")
    cursor = conn.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS `member` (mem_id INTEGER NOT NULL  PRIMARY KEY AUTOINCREMENT, name TEXT, age TEXT, address TEXT, contact TEXT)")
    cursor.execute("SELECT * FROM `member` ORDER BY `name` ASC")
    fetch = cursor.fetchall()
    for data in fetch:
        tree.insert('', 'end', values=(data))
    cursor.close()
    conn.close()

def SubmitData():
    if NAME.get() == ""  or AGE.get() == "" or ADDRESS.get() == "" or CONTACT.get() == "":
        result = tkMessageBox.showwarning('', 'Please Complete The Required Field', icon="warning")
        AddNewWindow()
    else:
        tree.delete(*tree.get_children())
        conn = sqlite3.connect("pythontut.db")
        cursor = conn.cursor()
        cursor.execute("Select name from 'member'")
        fetch = cursor.fetchall()
        temp = 1
        for i in fetch:
            if(i[0].lower() == NAME.get().lower()):    
                temp = 0
                result = tkMessageBox.showwarning('', 'Name Already Exist', icon="warning")
                AddNewWindow()
                break
            else:
                temp = 1
        if(temp):
            cursor.execute(
                "INSERT INTO `member` (name, age, address, contact) VALUES(?, ?, ?, ?)", (
                str(NAME.get()), int(AGE.get()), str(ADDRESS.get()),
                str(CONTACT.get())))
            conn.commit()
            cursor.execute("SELECT * FROM `member` ORDER BY `name` ASC")
            fetch = cursor.fetchall()
            for data in fetch:
                tree.insert('', 'end', values=(data))
            cursor.close()
            conn.close()
            NAME.set("")
            AGE.set("")
            ADDRESS.set("")
            CONTACT.set("")
            result = tkMessageBox.showwarning('', 'contact saved!', icon='info')
def UpdateData():
        tree.delete(*tree.get_children())
        conn = sqlite3.connect("pythontut.db")
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE `member` SET `name` = ?, `age` = ?,  `address` = ?, `contact` = ? WHERE `mem_id` = ?",
            (str(NAME.get()), str(AGE.get()), str(ADDRESS.get()),
             str(CONTACT.get()), int(mem_id)))
        conn.commit()
        cursor.execute("SELECT * FROM `member` ORDER BY `name` ASC")
        fetch = cursor.fetchall()
        for data in fetch:
            tree.insert('', 'end', values=(data))
        cursor.close()
        conn.close()
        NAME.set("")
        AGE.set("")
        ADDRESS.set("")
        CONTACT.set("")

def getnam():
    str(NAME.get())

def OnSelected(event):
    global mem_id, UpdateWindow
    curItem = tree.focus()
    contents = (tree.item(curItem))
    selecteditem = contents['values']
    mem_id = selecteditem[0]
    NAME.set("")
    AGE.set("")
    ADDRESS.set("")
    CONTACT.set("")
    NAME.set(selecteditem[1])
    AGE.set(selecteditem[4])
    ADDRESS.set(selecteditem[5])
    CONTACT.set(selecteditem[6])
    UpdateWindow = Toplevel()
    UpdateWindow.title("Contact List")
    width = 850
    height = 400
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = ((screen_width / 2)) - (width / 2)
    y = ((screen_height / 2)) - (height/2)
    UpdateWindow.resizable(0, 0)
    UpdateWindow.geometry("%dx%d+%d+%d" % (width, height, x, y))
    if 'NewWindow' in globals():
        NewWindow.destroy()


    #FRAMES

    FormTitle = Frame(UpdateWindow)
    FormTitle.pack(side=TOP)
    ContactForm = Frame(UpdateWindow)
    ContactForm.pack(side=TOP, pady=10)
    RadioGroup = Frame(ContactForm)
  
    #LABELS

    lbl_title = Label(FormTitle, text="Update Contact", font=('arial bold italic', 25), bg="orange", width=300)
    lbl_title.pack(fill=X)
    lbl_firstname = Label(ContactForm, text="name", font=('times', 20), bd=5)
    lbl_firstname.grid(row=0, sticky=W)
    lbl_age = Label(ContactForm, text="Age", font=('times', 20), bd=5)
    lbl_age.grid(row=3, sticky=W)
    lbl_address = Label(ContactForm, text="Address", font=('times', 20), bd=5)
    lbl_address.grid(row=4, sticky=W)
    lbl_contact = Label(ContactForm, text="Contact", font=('times', 20), bd=5)
    lbl_contact.grid(row=5, sticky=W)

    #ENTRY

    name = Entry(ContactForm, textvariable=NAME, font=('times', 17))
    name.grid(row=0, column=1)
    RadioGroup.grid(row=2, column=1)
    age = Entry(ContactForm, textvariable=AGE, font=('times', 17))
    age.grid(row=3, column=1)
    address = Entry(ContactForm, textvariable=ADDRESS, font=('times', 17))
    address.grid(row=4, column=1)
    contact = Entry(ContactForm, textvariable=CONTACT, font=('times', 17))
    contact.grid(row=5, column=1)

    #BUTTONS

    btn_updatecon = Button(ContactForm, text="UPDATE", width=50,font=('arial bold italic', 10), bg= "orange", command=UpdateData)
    btn_updatecon.grid(row=6, columnspan=2, pady=10)

def DeleteData():
    if not tree.selection():
        result = tkMessageBox.showwarning('', 'Please Select Something First!', icon="warning")
    else:
        result = tkMessageBox.askquestion('', 'Are you sure you want to delete this record?', icon="warning")
        if result == 'yes':
            curItem = tree.focus()
            contents = (tree.item(curItem))
            selecteditem = contents['values']
            tree.delete(curItem)
            conn = sqlite3.connect("pythontut.db")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM `member` WHERE `mem_id` = %d" % selecteditem[0])
            conn.commit()
            cursor.close()
            conn.close()

def AddNewWindow():
    global NewWindow
    NAME.set("")
    AGE.set("")
    ADDRESS.set("")
    CONTACT.set("")
    NewWindow = Toplevel()
    NewWindow.title("Contact List")
    width = 850
    height = 400
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = ((screen_width / 2)) - (width /2)
    y = ((screen_height / 2) ) - (height / 2)
    NewWindow.resizable(0, 0)
    NewWindow.geometry("%dx%d+%d+%d" % (width, height, x, y))
    if 'UpdateWindow' in globals():
        UpdateWindow.destroy()



    #FRAMES

    FormTitle = Frame(NewWindow)
    FormTitle.pack(side=TOP)
    ContactForm = Frame(NewWindow)
    ContactForm.pack(side=TOP, pady=10)
    #RadioGroup = Frame(ContactForm)
    
    #LABELS

    lbl_title = Label(FormTitle, text="Add New Contact", font=('arial bold italic', 25), bg="Sky blue", width=400)
    lbl_title.pack(fill=X)
    lbl_name = Label(ContactForm, text="Name", font=('times', 20), bd=5)
    lbl_name.grid(row=0, sticky=W)
    lbl_age = Label(ContactForm, text="Age", font=('times', 20), bd=5)
    lbl_age.grid(row=3, sticky=W)
    lbl_address = Label(ContactForm, text="Address", font=('times', 20), bd=5)
    lbl_address.grid(row=4, sticky=W)
    lbl_contact = Label(ContactForm, text="Contact", font=('times', 20), bd=5)
    lbl_contact.grid(row=5, sticky=W)

    #ENTRY

    name = Entry(ContactForm, textvariable=NAME, font=('times', 17))
    name.grid(row=0, column=1)
    #RadioGroup.grid(row=2, column=1)
    age = Entry(ContactForm, textvariable=AGE, font=('times', 17))
    age.grid(row=3, column=1)
    address = Entry(ContactForm, textvariable=ADDRESS, font=('times', 17))
    address.grid(row=4, column=1)
    contact = Entry(ContactForm, textvariable=CONTACT, font=('times', 17))
    contact.grid(row=5, column=1)

    #BUTTONS

    btn_addcon = Button(ContactForm, text="SAVE", font=('arial bold italic', 10), width=50, bg= "sky blue", command=SubmitData)
    btn_addcon.grid(row=6, columnspan=2, pady=10)

#FRAMES

Top = Frame(root, width=500, bd=1, relief=SOLID)
Top.pack(side=TOP)
Bottom = Frame(root, width=500, bd=1, relief=SOLID)
Bottom.pack(side=BOTTOM)
Mid = Frame(root, width=500, bg="white")
Mid.pack(side=BOTTOM)
MidLeft = Frame(Bottom, width=100)
MidLeft.pack(side=LEFT)
MidLeftPadding = Frame(Bottom, width=500, bg="white")
MidLeftPadding.pack(side=LEFT)
MidRight = Frame(Bottom, width=100)
MidRight.pack(side=RIGHT)
TableMargin = Frame(root, width=500)
TableMargin.pack(side=TOP)

#LABELS

lbl_title = Label(Top, text="PHONE BOOK", font=('arial bold italic', 40), bg="Light grey", width=500)
lbl_title.pack(fill=X)

#search

def update(data):
    my_list.delete(0,END)
    for i in data:
        my_list.insert(END,i)

def fillout(event):
    my_entry.delete(0,END)
    my_entry.insert(0,my_list.get(ACTIVE))

def check(event):
    typed = my_entry.get()
    data = []
    conn = sqlite3.connect("pythontut.db")
    cursor = conn.cursor()
    conn.commit()
    if typed =='':
        cursor.execute("SELECT * FROM `member`")
    else:
        #cursor.execute("SELECT * FROM `member` where name = '" + typed +"'")
        cursor.execute("SELECT * FROM `member` where name ='" + typed +"'")
    fetch = cursor.fetchall()
    tree.delete(*tree.get_children())
    for zee in fetch:
        tree.insert('', 'end', values=(zee))
    for i in fetch:
        data.append(i[1])
    update(data)
    


my_entry = Entry(Top, font=("helvetica",20),width=40)
my_entry.pack(pady=40)

'''btn_add1 = Button(Top,text="SEARCH", font=('arial bold italic', 15),  bg="sky blue", )
btn_add1.pack(ipady=4,ipadx=4)
btn_add2 = Button(Top,text="SEARCH", font=('arial bold italic', 15),  bg="sky blue")
btn_add2.pack(ipadx=5,ipady=6,fill='both',side='left')
btn_add3 = Button(Top,text="SEARCH", font=('arial bold italic', 15),  bg="sky blue")
btn_add3.pack(ipadx=5,ipady=6,fill='both',side='left')'''





my_list= Listbox(Top,width=100)
'''my_list.pack(pady=40)'''

update(contacts)
my_list.bind("<<ListboxSelect>>", fillout)
my_entry.bind("<KeyRelease>",check)

# BUTTONS

btn_add = Button(MidLeft, text="ADD NEW", font=('arial bold italic', 15),  bg="sky blue", command=AddNewWindow)
btn_add.pack(side=BOTTOM)
btn_delete = Button(MidRight, text="DELETE",font=('arial bold italic', 15),  bg="sky blue", command=DeleteData)
btn_delete.pack(side=BOTTOM)

#TABLES

scrollbarx = Scrollbar(TableMargin, orient=HORIZONTAL)
scrollbary = Scrollbar(TableMargin, orient=VERTICAL)
tree = ttk.Treeview(TableMargin, columns=("ID", "NAME", "AGE", "ADDRESS", "CONTACT",),
                    height=200, selectmode="extended", yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
scrollbary.config(command=tree.yview)
scrollbary.pack(side=RIGHT, fill=Y)
scrollbarx.config(command=tree.xview)
scrollbarx.pack(side=BOTTOM, fill=X)
#tree.heading('ID', text="ID", anchor=W)
tree.heading('NAME', text="NAME", anchor=W)
tree.heading('AGE', text="AGE", anchor=W)
tree.heading('ADDRESS', text="ADDRESS", anchor=W)
tree.heading('CONTACT', text="CONTACT", anchor=W)
tree.column('#0', stretch=NO, minwidth=0, width=0)
tree.column('#1', stretch=NO, minwidth=0, width=80)
tree.column('#3', stretch=NO, minwidth=0, width=120)
tree.column('#4', stretch=NO, minwidth=0, width=90)
#tree.column('#5', stretch=NO, minwidth=0, width=80)


tree.pack()
tree.bind('<Double-Button-1>', OnSelected)

#INITIALIZATION
if __name__ == '__main__':
    Database()
    root.mainloop()
