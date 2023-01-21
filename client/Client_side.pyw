import mysql.connector
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
import winsound

with open("appCache/server details.txt","r") as f:
    ip=f.read()


mydb=mysql.connector.connect(host=ip,user='root',passwd='tiger')
mycursor=mydb.cursor()

canvas=Tk()
canvas.title("Voting")
canvas.geometry("480x480")
icon=PhotoImage(file="logo.png")
canvas.iconphoto(False,icon)
canvas.resizable(False,False)
canvas.configure(background='#181818')


canvas.option_add("*Font", ("Consolas Bold",13))
canvas.option_add("*Background", "#181818")
canvas.option_add("*Button.Background", "#404040")
canvas.option_add("*Button.foreground", "White")
canvas.option_add("*Label.foreground", "White")
canvas.option_add("*Text.foreground", "White")
canvas.option_add("*Radiobutton.foreground", "White")
canvas.option_add("*Entry.foreground", "White")

try:
    mycursor.execute("use voters_list;")
except:
    mycursor.execute("Create database voters_list;")
    mycursor.execute("use voters_list;")

try:
    query="create table list (ADMN_NUMBER INT(50) primary key,NAME char(75),Status INT(1));"
    mycursor.execute(query)
    mydb.commit()
except:
    pass

mycursor.execute("use projectx;")
mycursor.execute("Show tables;")
postname=[]
for i in mycursor:
    postname.append(i[0])

if postname == []:
    canvas.destroy()
    messagebox.showerror('No database','Contact Administartor for more information')

m=len(postname)
s_last=[]

for j in postname:
    a="Select * from {};".format(j)
    mycursor.execute(a)
    result=mycursor.fetchall()
    s1_last=[]

    for i in result:
        s1_last.append(i[0])
    s_last.append(s1_last)

last=[]
for i in range (len(postname)):
    last.append([postname[i],s_last[i]])


opted=StringVar()
votelist=[]
namevariable = StringVar()
admnvariable = StringVar()

flag =0
name =""
def name_admn():
    global name
    name = namevariable.get()
    global flag
    if name:
        name=name.upper()
        admn = admnvariable.get()
        if admn.isdigit():
            mycursor.execute("use voters_list;")
            try:
                insert="insert into list values('{}','{}','{}');".format(admn,name,0)
                mycursor.execute(insert)
                mydb.commit()
            except:
                flag=1
                messagebox.showinfo('SORRY','YOU HAVE ALREADY VOTED')
                winsound.Beep(1000,1000)
        else:
            flag=1
            winsound.Beep(1000,1000)
            messagebox.showerror('Entry error','Invalid admission number')
    else:
        flag=1
        winsound.Beep(1000,1000)
        messagebox.showerror('Name error','Enter your details')
def value():
    mycursor.execute("use voters_list;")
    update="update list set Status = 1 where name = '{}'".format(name)
    mycursor.execute(update)
    mydb.commit()

def start():
    if flag == 0:
        fig = Toplevel()
        fig.geometry('720x720')
        fig.title('SESSION')
        icon=PhotoImage(file="logo.png")
        fig.iconphoto(False,icon)
        post_n=last[0][0]
        post_nn=post_n.upper()
        post_name_l = Label(master=fig , text=post_nn,)
        post_name_l.pack(pady=10)
        post_name_l.configure(font=("Consolas Bold",15))
        buttons = Frame(fig)
        buttons.pack()
        count=0
        for v in last[0][1]:
            dire="appCache\{}{}.png".format(post_n,count)
            option=Frame(buttons,highlightbackground='#1B1212',highlightthickness=2)
            option.pack(expand=True,fill="x",pady=3)
            radio=Radiobutton(option, text=v,variable=opted,value=v)
            radio.pack(side=LEFT,expand=True,fill="both")
            img = PhotoImage(file=dire)
            img.config(height=100,width=100)
            label=Label(option,text="image",image=img)
            label.image=img
            label.pack(padx=5,side=LEFT)
            count=count+1
        def reset():
            for widget in fig.winfo_children():
                if not isinstance(widget, Button):
                    widget.destroy()
        def op():
            global i
            try:
                a=namevariable.get()
                na=a.capitalize()
                name='Current Session : '+na
                session_label =Label(fig,text=name,font=("Candara light",12))
                session_label.pack(side="top",anchor=W)
                datframe=Frame(fig)
                post_n=last[i][0]
                post_nn=post_n.upper()
                post_name_l = Label(master=fig, text=post_nn)
                post_name_l.pack(pady=10)
                post_name_l.configure(font=("Consolas Bold",15))
                datframe.pack()
                count=0
                for v in last[i][1]:
                    dire="appCache\{}{}.png".format(post_n,count)
                    option=Frame(datframe,highlightbackground='#1B1212',highlightthickness=2)
                    option.pack(expand=True,fill="x",pady=3)
                    radio=Radiobutton(option, text=v,variable=opted,value=v)
                    radio.pack(side=LEFT,expand=True,fill="both")
                    img = PhotoImage(file=dire)
                    img.config(height=100,width=100)
                    label=Label(option,text="image",image=img)
                    label.image=img
                    label.pack(padx=5,side=LEFT)
                    count=count+1

            except:
                value()
                i = 0
                e1.delete("0","end")
                e2.delete("0","end")
                winsound.Beep(1000,500)
                fig.destroy()
                messagebox.showinfo('Session Closed','Thank You :)')

        def retrieve():
                opt=opted.get()
                global votelist
                votelist.append(opt)
                mycursor.execute("use projectx;")
                query = "update {} set vote = vote + 1 where name = '{}'".format(str(last[i-1][0]),str(votelist[i-1]))
                mycursor.execute(query)
                mydb.commit()
                
        a=namevariable.get()
        na=a.capitalize()
        name='Current Session : '+na
        session_label =Label(fig,text=name,font=("Candara light",12))
        next_b = Button(master = fig, command = lambda : [reset(),nex(),op(),retrieve()],height = 2, width = 10,text = "NEXT")
        session_label.pack(side="bottom",anchor=W,padx=5,pady=5)
        next_b.pack(side='bottom',pady=5)
    else:
        pass


def chng_dbs():
    global flag
    flag = 0
    mycursor.execute("use projectx;")
        
def nex():
    global i
    i=i+1
i=0


label= Label(canvas, text="ELECTION VOTING SYSTEM")
label.pack(pady=40)
label.configure(font =("Queental",15))

dataframe = Frame(canvas)
dataframe.pack()

Label(dataframe, text='Name      ').grid(row=0,column=0,pady=10)
Label(dataframe, text='Admn No.  ').grid(row=1,column=0)
e1 = Entry(dataframe,textvariable = namevariable,width=15)
e2 = Entry(dataframe,textvariable = admnvariable,width=15)
e2.delete("0","end")
e1.grid(row=0,column=1)
e2.grid(row=1,column=1)

def on_enter(e):
   start_b.config(background='white', foreground= "#404040")

def on_leave(e):
   start_b.config(background= '#404040', foreground= 'White')

start_b = Button(master = canvas,activeforeground="black", command = lambda : [name_admn(),start(),chng_dbs()],height = 2, width = 10,text = "START")
start_b.pack(pady=40)
start_b.bind('<Enter>', on_enter)
start_b.bind('<Leave>', on_leave)

canvas.mainloop()