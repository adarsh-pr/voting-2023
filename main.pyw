import os
from tkinter import *
from tkinter import messagebox

window = Tk()
window.title('VOTING SYSTEM LOGIN')
window.geometry("480x480")
window.resizable(False,False)
window.configure(background='#181818')

window.option_add("*Font", ("Consolas Bold",12))
window.option_add("*Background", "#181818")
window.option_add("*Button.Background", "#404040")
window.option_add("*Button.foreground", "White")
window.option_add("*Label.foreground", "White")
window.option_add("*Text.foreground", "White")
window.option_add("*OptionMenu.foreground", "White")
window.option_add("*Entry.foreground", "White")


code =1080

namevariable = StringVar()
passvariable = IntVar()

label= Label(window,text="VOTING SYSTEM LOGIN")
label.configure(font=("Britannic",20))
label.pack(side = "top",pady=20)

top = Frame(window)
top.pack()
def client():
    window.destroy()
    os.system('Client_side.pyw')

client_b = Button(master = top, command = client,height = 2, width = 15,text = "CLIENT LOGIN").pack(pady=20)

def admin():

    def login():
        pas = passvariable.get()
        if pas == code:
            window.destroy()
            os.system('ADMIN_control.pyw')
        else:
            e2.delete("0","end")
            messagebox.showerror('Passcode invalid','Check passcode !')

    Label(window, text='Enter your Passcode').pack()
    e2 = Entry(window,textvariable = passvariable,show='*')
    e2.delete("0","end")
    e2.pack(pady=10)

    login_b=Button(window,command=login,height = 2, width = 15,text = "LOGIN").pack(pady=20)

    top.destroy()

admn_login_b = Button(master = top, command = admin,height = 2, width = 15,text = "ADMIN LOGIN").pack(pady=20)

top.mainloop()
window.mainloop()