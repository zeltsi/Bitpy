import tkinter

from Manager import core_manager

root = tkinter.Tk()

top_label = tkinter.Label(root, text="Created by Shlomi Zeltsinger and Alexis Gallepe")
top_label.grid(row=0)

send_menu = tkinter.Menu(root)
root.config(menu=send_menu)

send_menu_sub = tkinter.Menu(send_menu)
send_menu.add_cascade(label="Choose package to send", menu=send_menu_sub)
send_menu_sub.add_command(label="0-version", command=core_manager.send_version_msg())
send_menu_sub.add_command(label="1-verAck", command=core_manager.send_verack_msg())
send_menu_sub.add_command(label="2-getAddr", command=core_manager.send_getAddr_msg())
send_menu_sub.add_command(label="3-ping", command=core_manager.send_ping_msg())
send_menu_sub.add_command(label="4-getBlocks", command=core_manager.send_getBlocks_msg())

root.mainloop()