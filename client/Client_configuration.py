import mysql.connector
from tkinter import *


canvas=Tk()
canvas.title("Voting")
canvas.geometry("480x480")
icon=PhotoImage(file="logo.png")
canvas.iconphoto(False,icon)
canvas.resizable(False,False)
canvas.configure(background='#181818')

namevariable=StringVar

title= Label(canvas, text="ELECTION VOTING SYSTEM")
title.pack(pady=25)
title.configure(font =("Queental",15))
label= Label(canvas, text="Client - Side Configuration")
label.pack(pady=15)
label.configure(font =("Queental",8))
Label(canvas, text='Enter Database Server IP-Address').pack(pady=10)
e1 = Entry(canvas,textvariable = namevariable,width=15)
e1.pack()

def enter():
    ip=e1.get()
    f=open("appCache/server details.txt","w")
    f.write(ip)
    f.close()



Enter_b = Button(master = canvas,activeforeground="black", command = enter,height = 2, width = 10,text = "Enter")
Enter_b.pack()



canvas.mainloop()