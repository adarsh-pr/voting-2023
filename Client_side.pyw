import mysql.connector
from tkinter import *
from tkinter import messagebox
import winsound

mydb=mysql.connector.connect(host='localhost',user='root',passwd='tiger')
mycursor=mydb.cursor()

canvas=Tk()
canvas.title("Voting")
canvas.geometry("480x480")
img=b'iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAYAAACqaXHeAAAACXBIWXMAAAsTAAALEwEAmpwYAAAEdUlEQVR4nO2aS4gVRxSGPxUno8KEQBBFo5jFQEAFXTi+XSWCSCQRsjVkEUQk6G5ABRU1I+pCXZhkE9wEQiDRhVGzSEAjQgjkJWrQXRwFB/EFKjLacuTvULbdfbv7dnX3jPeH4vatOt116u86p+qcauigA5/oAvYC14GghnIP+B7opSYM1DTwaLkFTK+DgEEpsLii/r5Tfz8CbwHTgBOq+5YaEKhUhdvqz33b01V3h1eAgCChv6r1yNVxXnvO8qys9d7RIYCOCdDxAVSHxvqAoOKSpEflCDoEUCrzrd5kY2dA1QQU2UN4QbRjiw4/V4xwQ5FiVxvPaxwB44B5wGdOYBK0iA6NEN8m4A3dwDJgC3ASuNuCeTc6XKrrazEDSLq/dgJeB1YBe4CzwKMYZa8AXwOfpBCwVMQFqvNNQGFTmAp8BBwC/gSGIw96ovpDkpvaQqG6TCAXAROBrcDlmBvtjf8qpVdpRuRRuEskDCpNNuDJCRa59zneAP5whO/Kts3Gl8vmR8IyWFiXbyT0AFgjr94OmkDAeOCA07ZfdS/B8mdPI4nEPTF2XUThqosLd/Bh2Ren7Ptq/Bc4F7F78+pzRigBQ87Ks0TXN+OUXa3Gn/R/kTYzoee32XEaeBcYk5OAshA+z3Tqc+r7IitUmg6JOvWq4b9I/Sx56zvOzX8Bn2Zwir4IsHIJmAC8BlxImQGZCRirkxRrnJywQvQ7m5lA1/1qS1O47Fjgon73qrh1SQSkmcn/OKPGlSTDFF6nWRA+7L42Q29HZH1thMIp75a+Mgg4qEZ7q1lg/uCUs3oMy28sSiCgzFggfPPhTIjrL64ulYB1BY+RZgM/R5Q+5zkW8ELAXCegyYvzuveU9hBBw0wg6f8LsB3SQ03pHrIjnM5DiiUmARs9xgJFnGDS/5fwmwRWkB3Hdc/2ipfB7jKXwRBfSmAT2dCrsNhmzpSKCLApv8Cpnw88LouA9RI4mlGpryR/JEXhqktbBCyQwD8ZBj9ZkaP5jHdGCwHdmk7Dcmhp2KmH/ZDQ7ssE8rTnJsDwt4RcO4tiohNpWZQ1qgg4KiHzB0nYIJnzDTwXaJuATRKyFSEOlim6Kpm1ORSqIylaiIDlErI9QRzWqv1qi7RZE84FChHQI8/+MCF/Fm57zQwoQECV5wKFCEDxQKD4IG3by2g0ARQRmuDHvIhjqrclsBWacC5QmIB+CVqOILrtfRSz7S2icF5USsB7ErQsUTRO+KIkhRtNwJtOumtshm1vmkJVl1IIQBniQFN/h67NBzACCUiTSUT4kcO2yAFDEmYCHwK7lRlqkgkUImC1hJ/GbHtnRAY71G5nTfMBIQ47N9nS9buOluIGelOnybuADxoSC4QfcfSoBKrLDNvqbna+xQ/LkN78bg12RkM3Qr/E5A8tg50blidYqFzhzIIK1xELJGWQK0FTvhGKO0OoBE0wgXD2hm15v3JpCyPuG6Gy0YRl0JcumeDafBlIG0ScT6kdAymOzVfJ41O8w7V53wMfLOBTOuBVxzPzpNeMcCaEUgAAAABJRU5ErkJggg=='
icon=PhotoImage(data=img)
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
                winsound.Beep(1000,3000)
                messagebox.showinfo('SORRY','YOU HAVE ALREADY VOTED')
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
    fla=False
    if flag == 0:
        fig = Toplevel()
        fig.geometry('720x720')
        fig.title('SESSION')
        img=b'iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAYAAACqaXHeAAAACXBIWXMAAAsTAAALEwEAmpwYAAAEdUlEQVR4nO2aS4gVRxSGPxUno8KEQBBFo5jFQEAFXTi+XSWCSCQRsjVkEUQk6G5ABRU1I+pCXZhkE9wEQiDRhVGzSEAjQgjkJWrQXRwFB/EFKjLacuTvULbdfbv7dnX3jPeH4vatOt116u86p+qcauigA5/oAvYC14GghnIP+B7opSYM1DTwaLkFTK+DgEEpsLii/r5Tfz8CbwHTgBOq+5YaEKhUhdvqz33b01V3h1eAgCChv6r1yNVxXnvO8qys9d7RIYCOCdDxAVSHxvqAoOKSpEflCDoEUCrzrd5kY2dA1QQU2UN4QbRjiw4/V4xwQ5FiVxvPaxwB44B5wGdOYBK0iA6NEN8m4A3dwDJgC3ASuNuCeTc6XKrrazEDSLq/dgJeB1YBe4CzwKMYZa8AXwOfpBCwVMQFqvNNQGFTmAp8BBwC/gSGIw96ovpDkpvaQqG6TCAXAROBrcDlmBvtjf8qpVdpRuRRuEskDCpNNuDJCRa59zneAP5whO/Kts3Gl8vmR8IyWFiXbyT0AFgjr94OmkDAeOCA07ZfdS/B8mdPI4nEPTF2XUThqosLd/Bh2Ren7Ptq/Bc4F7F78+pzRigBQ87Ks0TXN+OUXa3Gn/R/kTYzoee32XEaeBcYk5OAshA+z3Tqc+r7IitUmg6JOvWq4b9I/Sx56zvOzX8Bn2Zwir4IsHIJmAC8BlxImQGZCRirkxRrnJywQvQ7m5lA1/1qS1O47Fjgon73qrh1SQSkmcn/OKPGlSTDFF6nWRA+7L42Q29HZH1thMIp75a+Mgg4qEZ7q1lg/uCUs3oMy28sSiCgzFggfPPhTIjrL64ulYB1BY+RZgM/R5Q+5zkW8ELAXCegyYvzuveU9hBBw0wg6f8LsB3SQ03pHrIjnM5DiiUmARs9xgJFnGDS/5fwmwRWkB3Hdc/2ipfB7jKXwRBfSmAT2dCrsNhmzpSKCLApv8Cpnw88LouA9RI4mlGpryR/JEXhqktbBCyQwD8ZBj9ZkaP5jHdGCwHdmk7Dcmhp2KmH/ZDQ7ssE8rTnJsDwt4RcO4tiohNpWZQ1qgg4KiHzB0nYIJnzDTwXaJuATRKyFSEOlim6Kpm1ORSqIylaiIDlErI9QRzWqv1qi7RZE84FChHQI8/+MCF/Fm57zQwoQECV5wKFCEDxQKD4IG3by2g0ARQRmuDHvIhjqrclsBWacC5QmIB+CVqOILrtfRSz7S2icF5USsB7ErQsUTRO+KIkhRtNwJtOumtshm1vmkJVl1IIQBniQFN/h67NBzACCUiTSUT4kcO2yAFDEmYCHwK7lRlqkgkUImC1hJ/GbHtnRAY71G5nTfMBIQ47N9nS9buOluIGelOnybuADxoSC4QfcfSoBKrLDNvqbna+xQ/LkN78bg12RkM3Qr/E5A8tg50blidYqFzhzIIK1xELJGWQK0FTvhGKO0OoBE0wgXD2hm15v3JpCyPuG6Gy0YRl0JcumeDafBlIG0ScT6kdAymOzVfJ41O8w7V53wMfLOBTOuBVxzPzpNeMcCaEUgAAAABJRU5ErkJggg=='
        icon=PhotoImage(data=img)
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
                nonlocal fla
                fla=True
                global votelist
                votelist=[]

        def retrieve():
                opt=opted.get()
                global votelist
                votelist.append(opt)
                mycursor.execute("use projectx;")
                query = "update {} set vote = vote + 1 where name = '{}'".format(str(last[i][0]),str(votelist[i]))
                mycursor.execute(query)
                mydb.commit()
                nonlocal fla
                if fla == True:
                    messagebox.showinfo('Session Closed','Thank You :)')
                
        a=namevariable.get()
        na=a.capitalize()
        name='Current Session : '+na
        session_label =Label(fig,text=name,font=("Candara light",12))
        next_b = Button(master = fig, command = lambda : [retrieve(),reset(),nex(),op()],height = 2, width = 10,text = "NEXT")
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