from tkinter import *
from tkinter import ttk
import os
import database
import main
import psycopg2
from dotenv import load_dotenv

load_dotenv()
database_url = os.environ["DATABASE_URL"]
connection = psycopg2.connect(database_url)
root = Tk()
root.title('password_manager')
root.geometry("500x600")

style = ttk.Style()

style.theme_use("clam")

style.configure("Treeview",
                background="white",
                foreground="black",
                rowheight=25,
                fieldbackground="white"
                )

style.map('Treeview', background=[('selected', 'blue')])

tree_frame = Frame(root)
tree_frame.pack(pady=20)

tree_scroll = Scrollbar(tree_frame)
tree_scroll.pack(side=RIGHT, fill=Y)

my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set)
my_tree.pack()

tree_scroll.config(command=my_tree.yview)

my_tree['columns'] = ("Name", "ID", "User-ID", "password")

my_tree.column("#0", width=0, stretch=NO)
my_tree.column("Name", anchor=W, width=140)
my_tree.column("ID", anchor=CENTER, width=100)
my_tree.column("User-ID", anchor=CENTER, width=100)
my_tree.column("password", anchor=W, width=140)

my_tree.heading("#0", text="", anchor=W)
my_tree.heading("Name", text="Name", anchor=W)
my_tree.heading("ID", text="ID", anchor=CENTER)
my_tree.heading("User-ID", text="User-ID", anchor=CENTER)
my_tree.heading("password", text="Password", anchor=W)


users = main.prompt_show_users(connection)

my_tree.tag_configure('oddrow', background="white")
my_tree.tag_configure('evenrow', background="lightblue")


global count
count = 0
for item in users:
    if count % 2 == 0:
        my_tree.insert(parent='', index='end', iid=count, text="", values=(item[1], count, item[0], item[2]),
                       tags=('evenrow',))
    else:
        my_tree.insert(parent='', index='end', iid=count, text="", values=(item[1], count, item[0], item[2]),
                       tags=('oddrow',))
    count += 1

add_frame = Frame(root)
add_frame.pack(pady=20)


nl = Label(add_frame, text="Name")
nl.grid(row=0, column=0)

tl = Label(add_frame, text="Password")
tl.grid(row=0, column=1)


name_box = Entry(add_frame)
name_box.grid(row=1, column=0)

password_box = Entry(add_frame)
password_box.grid(row=1, column=1)


def prompt_create_user():
    global count
    main.prompt_create_user(connection, name_box.get(), password_box.get())
    user = database.get_last_user(connection)
    if count % 2 == 0:
        my_tree.insert(parent='', index='end', iid=count, text="", values=(user[1], count, user[0], user[2]),
                       tags=('evenrow',))
    else:
        my_tree.insert(parent='', index='end', iid=count, text="", values=(user[1], count, user[0], user[2]),
                       tags=('oddrow',))
    count += 1


    name_box.delete(0, END)
    password_box.delete(0, END)


def prompt_remove_all_users():
    global count
    main.prompt_delete_all_users(connection)

    for item in my_tree.get_children():
        my_tree.delete(item)
    count = 0


def prompt_remove():
    x = my_tree.selection()
    for item in x :
        item_details = my_tree.item(item)
        _id = item_details.get("values")[2]
        print(_id)
        main.prompt_delete_user(connection, _id)
        my_tree.delete(item)


def prompt_update():
    pass

def prompt_select():
    pass


select_button = Button(root, text="Select User", command=prompt_select)
select_button.pack(pady=10)

update_button = Button(root, text="Update User", command=prompt_update)
update_button.pack(pady=10)


add_record = Button(root, text="Add User", command=prompt_create_user)
add_record.pack(pady=10)

remove_all = Button(root, text="Remove All Users", command=prompt_remove_all_users)
remove_all.pack(pady=10)

remove = Button(root, text="Remove", command=prompt_remove)
remove.pack(pady=10)

root.mainloop()