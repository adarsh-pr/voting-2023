import os
from tkinter import *
from tkinter import messagebox
import mysql.connector
import matplotlib.pyplot as plt
import csv
from tkinter.filedialog import asksaveasfile
import random
from tkinter.filedialog import askopenfile
import shutil
import socket


def admin():
    mydb=mysql.connector.connect(host='localhost',user='root',passwd='tiger')
    mycursor=mydb.cursor()


    curr_dir = os.getcwd()
    final_dir = os.path.join(curr_dir, r'appCache')

    if not os.path.exists(final_dir):
        os.makedirs(final_dir,mode = 0o666)

    hostname = socket.gethostname()
    IP = socket.gethostbyname(hostname)
    f=open("appCache/server details.txt","w")
    f.write(IP)
    f.close()

    try:
        mycursor.execute("use PROJECTX")
    except:
        mycursor.execute("Create database PROJECTX")
        mycursor.execute("use PROJECTX")

    window = Tk()
    window.title('ADMIN_CONTROL')
    window.geometry("1080x720")
    window.resizable(False,False)
    window.configure(background='#181818')
    window.attributes('-fullscreen', True)
    window.option_add("*Font", ("Consolas Bold",14))
    window.option_add("*Background", "#181818")
    window.option_add("*Button.Background", "#404040")
    window.option_add("*Button.foreground", "White")
    window.option_add("*Label.foreground", "White")
    window.option_add("*Text.foreground", "White")
    window.option_add("*OptionMenu.foreground", "White")
    window.option_add("*Entry.foreground", "White")

    text1 = StringVar()
    cand1 = StringVar()


    def rand(l):
        col=[]
        for i in range(l):
            color = "#"+''.join([random.choice('ABCDEF0123456789') for i in range(6)])
            col.append(color)
        return col

    def add():
        top=Toplevel()
        top.title('Create')
        top.geometry('480x480')
        top.lift(window)

        topframe=Frame(top)
        topframe.pack(padx=10,pady=10,ipadx=10)   


        name_post_l = Label(master=topframe , text="NAME OF THE POST").pack(pady = 10)
        name_post_e = Entry(master = topframe,textvariable=text1 ).pack(pady = 10)


        def Create():
            name_post = text1.get()
            name_post_sl= name_post.replace(" ","_")
            namepost=name_post_sl.upper()
            post_table=("create table {} (name char(75),CID char(5) primary key,vote int(3))")
            post_assign=post_table.format(namepost)
            try:
                mycursor.execute(post_assign)
            except:
                messagebox.showerror('Error, Try again',"Couldn't create post!")

            else:
                topp=Toplevel()
                titl=name_post.title()
                topp.title(titl)
                topp.geometry('480x480')
                top.lower(window)
                ch=titl.lower()
                chg=ch.replace(" ","_")
                can_name=""
                def select():
                    cand_name=cand1.get()
                    cand_name=cand_name.upper()
                    global can_name
                    can_name=cand_name
                    if cand_name:
                        files = [('Png Files', '*.png'), 
                        ('All Files', '*.*')]
                        fil = askopenfile(filetypes = files, defaultextension = '.png',title='Candidate Symbol')
                        topp.lift(window)
                        if fil:
                            source=fil.name
                            fil.close()
                            nonlocal count
                            dest="appCache/{}{}.png".format(chg,str(count))
                            shutil.copy(source,dest)
                            next_b.config(text='Add',state='normal')
                            symbo.config(text='Symbol Uploaded !',state='disabled')
                        else:
                            messagebox.showerror('Error, Try again',"Select A Candidate Symbol")
                            topp.lift(window)
                    else:
                        messagebox.showerror('Error, Try again',"Type Candidate name")
                        topp.lift(window)

                postlist=[] 
                count=0
                cand_id = 'CID'+ str(count)
                curr_vote=0
                cand_name_l = Label(master=topp , text="NAME OF THE CANDIDATE").pack(pady = 10)
                cand_name_e = Entry(master = topp,textvariable=cand1 ).pack(pady = 10)
                symbo = Button(master = topp, relief='flat',command = select,height = 1, width = 23,font=("Consolas Bold",12),text = "Select Candidate Symbol")
                symbo.pack(padx = 60,pady=10)

                def nex():
                    nonlocal count
                    count = count+1
                    cand_id = 'CID'+ str(count)
                    symbo.config(text="Select Candidate Symbol",state='normal')
                    next_b.config(text="Candidate Added !",state='disabled')
                    global can_name
                    if count>1:
                        submit_b.config(state='normal')
                    name_p=name_post.replace(" ","_")
                    value_table="insert into {} values('{}','{}',{});".format(name_p,can_name,cand_id,curr_vote)
                    mycursor.execute(value_table)
                    postlist.append([can_name,cand_id,curr_vote])

                def reset():
                    for widget in topp.winfo_children():
                        if isinstance(widget, Entry):
                            widget.delete(0,'end')

                def lift():
                    top.lift(window)
                
                next_b = Button(master = topp,relief='flat',command =lambda: [nex(),reset()],state='disabled', height =1 , width = 25,text = "Add")
                next_b.pack(pady = 10)
                submit_b = Button(master = topp,relief='flat',command =lambda: [topp.destroy(),lift()],state='disabled', height = 1, width = 25,text = "Proceed to next post")
                submit_b.pack(pady = 10)
                finish_b.config(state='normal')
                topp.mainloop()
                
        
        bottomframe=Frame(top)
        bottomframe.pack(padx=10,pady=10,ipadx=10,ipady=50)

        create_b = Button(master = bottomframe, relief='flat',command = Create,height = 1, width = 10,text = "Create post")
        create_b.pack(side = LEFT,padx = 60)
        finish_b = Button(master = bottomframe, relief='flat',command = top.destroy,state='disabled',height = 1, width = 00,text = "Finish")
        finish_b.pack(side = LEFT,padx = 60)
        
        topframe.mainloop()
        bottomframe.mainloop()
        top.mainloop()
        mydb.commit()


    def result():
        mycursor.execute("use projectx;")
        mycursor.execute("Show tables;")
        postname=[]
        for i in mycursor:
            postname.append(i[0])

        if postname!=[]:
            s_last=[]
            s_vote=[]

            fla = 0

            for j in postname:
                a="Select * from {};".format(j)
                mycursor.execute(a)
                result=mycursor.fetchall()
                s1_last=[]
                vote1=[]

                for i in result:
                    s1_last.append(i[0])
                    vote1.append(i[2])

                s_last.append(s1_last)
                s_vote.append(vote1)

            x=0
            i=0
            spot = Toplevel()
            spot.geometry('480x480')
            spot.title('Results')

            clicked = StringVar()
            clicked.set( "Select Post Name" )
            drop = OptionMenu( spot , clicked , *postname )
            drop.configure(foreground='White')
            drop["menu"].config(foreground="White")
            drop.pack(pady = 10)


            def nex():
                de=clicked.get()
                it=0
                for m in postname:
                    if m == de:
                        nu=it
                        it=it+1
                    else:
                        it=it+1
                nonlocal i
                nonlocal fla
                i=nu
                fla = 0
                for h in s_vote[i]:
                    if h != 0:
                        fla = 1
                        break
                    else:
                        fla = 0

            def pot():
                nonlocal s_vote
                nonlocal s_last
                nonlocal postname
                nonlocal i
                nonlocal fla
                if fla == 1:
                    x = s_last[i]
                    y = s_vote[i]
                    plt.barh(x, y)
                    
                    for index, value in enumerate(y):
                        plt.text(value, index,
                                str(value))
                    plt.show()
                else:
                    messagebox.showerror('No votes recorded','No records found !')


            def pie():
                nonlocal i
                nonlocal fla
                if fla == 1:
                    l=len(s_last[i])
                    colV=rand(l) 
                    plt.pie(s_vote[i], labels=s_last[i], colors=colV,
                    autopct='%1.1f%%', shadow=True, startangle=140)
                    plt.title(postname[i], bbox={'facecolor':'0.8', 'pad':5})
                    plt.show()
                else:
                    messagebox.showerror('No votes recorded','No records found !')

            button = Button( spot , relief='flat',text = "OK" , command = nex ).pack(pady=10)
            graph_b = Button(master = spot, relief='flat',command = pot,text = "Bar Graph").pack()
            pie_b = Button(master = spot, relief='flat',command = pie,text = "Pie Chart").pack()

            spot.mainloop()

        else:
            messagebox.showerror('No votes recorded','No records found !')


    def show_vl():
        try:
            mycursor.execute("use voters_list;")
            mycursor.execute("select * from list group by admn_number;")
            lis=[]
            for i in mycursor:
                lis.append(i)

            s_vl = Toplevel()
            s_vl.geometry('480x480')
            s_vl.title('VOTERS LIST')
            scrollbar = Scrollbar(s_vl)
            scrollbar.pack( side = RIGHT, fill = Y )
            my=Text(s_vl,yscrollcommand=scrollbar.set)
            for v in lis:
                my.insert(END,v)
                my.insert(END,'\n')
            my.pack(ipadx =150,ipady=120,)
            my.config(state='disabled')
            scrollbar.config(command = my.yview )
        except:
            messagebox.showerror('No votes recorded','No records found !')
        
        


    def modify():
        mod = Toplevel()
        mod.geometry('480x480')
        mod.title('MODIFY DETAILS')


        def d_post():
            mycursor.execute("use projectx;")
            mycursor.execute("Show tables;")
            postname=[]
            for i in mycursor:
                postname.append(i[0])
            if postname != []:
                clicked = StringVar()
                clicked.set( "Select Post Name" )
                drop = OptionMenu( mod , clicked , *postname )
                drop.configure(foreground='White')
                drop["menu"].config(foreground="White")
                drop.pack(pady = 10)

                def nex():
                    de=clicked.get()
                    sg_box = messagebox.askquestion('Delete message', 'Are you sure you want to remove the post?',
                                                        icon='warning')
                    if sg_box == 'yes':
                        mycursor.execute("use projectx;")
                        query="drop table {} ;".format(de)
                        mycursor.execute(query)
                        messagebox.showinfo('Delete message','Post deleted!')
                        mod.destroy()
                    else:
                        mod.destroy()

                button = Button( mod ,relief='flat', text = "Confirm" , command = nex ).pack(pady=10)
            else:
                mod.destroy()
                messagebox.showerror('Delete error','No Data found!')

        def d_datb():
            sg_box = messagebox.askquestion('Delete message', 'Are you sure you want to delete this database?',
                                                icon='warning')
            if sg_box == 'yes':
                try:
                    mycursor.execute("use projectx;")
                    query="drop database projectx;"
                    mycursor.execute(query)
                    shutil.rmtree(final_dir)
                    messagebox.showinfo('Database deleted','Please Restart the Application')
                    window.destroy()
                except:
                    messagebox.showerror('Delete error','No Database found!')
                    mod.destroy()


        def d_vsl():
            try:
                mycursor.execute("use voters_list;")
            except:
                mod.destroy()
                messagebox.showerror('Delete message','No records found!')
            else:
                query="drop database voters_list;"
                sg_box = messagebox.askquestion('Delete message', 'Are you sure you want to delete Voters list?',
                                                    icon='warning')
                if sg_box == 'yes':
                    mycursor.execute(query)
                    messagebox.showinfo('List deleted!','Please Restart the Application')
                    window.destroy()
                else:
                    mod.destroy()



        del_post = Button(master = mod, relief='flat',command = d_post,height = 2, width = 25,text = "REMOVE POST").pack(pady=10)
        del_datab = Button(master = mod, relief='flat',command = d_datb,height = 2, width = 25,text = "DELETE EXISTING DATABASE").pack(pady=10)
        del_vsl = Button(master = mod, relief='flat',command = d_vsl,height = 2, width = 25,text = "DELETE VOTERS LIST").pack(pady=10)


    def save():
        sa = Toplevel()
        sa.geometry('480x480')
        sa.title('SAVE FILES')

        def s_vsl():
            try:
                mycursor.execute("use voters_list;")
            except:
                messagebox.showerror('Save error','No records found!')
                sa.destroy()
            else:
                files = [('csv Files', '*.csv'), 
                    ('All Files', '*.*')]
                fil = asksaveasfile(filetypes = files, defaultextension = csv,title = 'Voters List')
                if fil:
                    filename=fil.name
                    f = open(filename,"w")
                    mycursor.execute("use voters_list;")
                    mycursor.execute("select * from list;")
                    lis=[]
                    for i in mycursor:
                        lis.append(i)
                    c=csv.writer(f)
                    c.writerow(["Name","Admn_no"])
                    for j in lis:
                        c.writerow(j)
                    f.close()
                    sa.destroy()
                else:
                    sa.destroy()

        def s_post():
            try:
                mycursor.execute("use projectx;")
            except:
                messagebox.showerror('Save error','No records found!')
                sa.destroy()
            else:
                files = [('csv Files', '*.csv'), 
                    ('All Files', '*.*')]
                fil = asksaveasfile(filetypes = files, defaultextension = '.csv',title='Election results')
                if fil:
                    filename=fil.name
                    f = open(filename,"w")
                    mycursor.execute("use projectx;")
                    mycursor.execute("show tables;")
                    postname=[]
                    for i in mycursor:
                        postname.append(i[0])
                    lis = []
                    for j in postname:
                        s_list=[]
                        s_list.append(j)
                        query="select * from {} order by 'votes';".format(j)
                        mycursor.execute(query)
                        temp=[]
                        for k in mycursor:
                            temp.append(k)
                        s_list.append(temp)
                        lis.append(s_list)

                    c=csv.writer(f)
                    for i in lis:
                        c.writerow(["Details for the post :",i[0]])
                        c.writerow(["Name","Candidate_ID","Votes"])
                        for j in i[1]:
                            c.writerow(j)
                    f.close()
                    sa.destroy()
                else:
                    sa.destroy()
                

        sa_post = Button(master = sa, relief='flat',command = s_post,height = 2, width = 35,text = "SAVE ELECTION RESULTS AS CSV FILE").pack(pady = 10)
        sa_vsl = Button(master = sa, relief='flat',command = s_vsl,height = 2, width = 30,text = "SAVE VOTERS LIST AS CSV FILE").pack(pady = 10)


    def window_destroy():
        window.destroy()



    def realtime():
        current = []
        try:
            mycursor.execute("use voters_list;")
            query="select * from list;"
            mycursor.execute(query)
        except:
            tex1.delete("1.0","end")
            tex2.delete("1.0","end")
            tex3.delete("1.0","end")       
            tex1.insert(END,"No Voters Database")
            tex2.insert(END,"No Voters Database")
            tex3.insert(END,0)
        else:
            files=mycursor.fetchall()
            temp=[]
            try:
                tex1.delete("1.0","end")
                tex2.delete("1.0","end")
                tex3.delete("1.0","end")
            except:
                pass

            for i in files:
                if i[2] == 0:
                    current.append(i[1])
                else:
                    temp.append(i)
            m=1
            for j in reversed(temp):
                if m<6:
                    tex2.insert(END,j[1])
                    tex2.insert(END,'\n')
                    m=m+1

            if current != []:
                for i in current:
                    tex1.insert(END,i)
                    tex1.insert(END,'\n')
            else:
                tex1.insert(END,"No Running Session")

            no=len(files)
            tex3.insert(END,str(no))


    title = Label(master=window , text="ELECTION VOTING SYSTEM")
    title.pack(pady = 10)
    title.configure(font =("Queental",25))
    subtitle = Label(master=window , text="ADMIN CONTROL")
    subtitle.pack(pady = 10)
    subtitle.configure(font =("Queental",20))

    subframe1=Frame(window,highlightbackground="#1B1212",highlightthickness=10)
    subframe1.pack(padx=10,pady=10,expand=True,side=LEFT,fill='both')

    subframe2=Frame(window,highlightbackground="#1B1212",highlightthickness=10)
    subframe2.pack(padx=10,pady=10,expand=False,side=LEFT,fill='both')

    buttonframe1 =Frame(subframe1)
    buttonframe1.pack(padx=25,pady=100)

    heading =Frame(subframe2)
    heading.pack(padx=10,pady=10,fill='both')

    rframe =Frame(subframe2)
    rframe.pack(padx=10,pady=10,expand=True,fill='both')

    subbutton1 =Frame(rframe)
    subbutton1.pack(padx=10,pady=25,side=RIGHT,expand=True,fill='both')

    subbutton2 =Frame(rframe)
    subbutton2.pack(padx=10,pady=25,side=RIGHT,expand=True,fill='both')

    cred =Frame(subframe2)
    cred.pack(padx=10,pady=10,side=BOTTOM)

    realt=Label(heading,text="Realtime View")
    realt.pack(pady=10)
    realt.configure(font =("Queental",18))


    add_b = Button(master = buttonframe1, command = add,relief='flat',height = 2, width = 25,text = "Create").pack(padx=25,pady = 10)
    result_b = Button(master = buttonframe1, command = result,relief='flat',height = 2, width = 25,text = "Result").pack(padx=25,pady = 10)
    show_vl_b = Button(master = buttonframe1, command = show_vl,relief='flat',height = 2, width = 25,text = "Show Voters List").pack(padx=25,pady = 10)
    modify_b = Button(master = buttonframe1, command = modify,relief='flat',height = 2, width = 25,text = "Modify").pack(padx=25,pady = 10)
    save_b = Button(master = buttonframe1, command = save,relief='flat',height = 2, width = 25,text = "Save as csv").pack(padx=25,pady = 10)
    exit_b = Button(master = buttonframe1, command = window_destroy,relief='flat',height = 2, width = 25,text = "Close").pack(padx=25,pady = 10)


    lab=Label(subbutton1,text="Current Sessions").pack(pady=10)
    tex1=Text(subbutton1,height=8,width=20)
    tex1.pack(pady=10)


    vl=Label(subbutton2,text="Last voters").pack(pady=10)
    tex2=Text(subbutton2,height=9,width=20)
    tex2.pack(pady=10)


    n_votes=Label(subbutton1,text="Total Number Of Votes").pack(pady=10)
    tex3=Text(subbutton1,height=1,width=10)
    tex3.pack()

    refresh_b = Button(master = subbutton2, command = realtime,relief='flat',height = 1, width = 10,text = "Refresh").pack(pady = 15)

    credit=Label(cred,text='''Project Done By: ADARSH PR, KARTHIK KRISHNA, RIYA RAJESH
                                KENDRIYA VIDYALAYA KALPETTA
                                            Year : 2022-2023''')
    credit.pack(side='right',anchor='e')


    window.mainloop()




window = Tk()
window.title('VOTING SYSTEM LOGIN')
window.geometry("480x480")
img=b'iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAYAAACqaXHeAAAACXBIWXMAAAsTAAALEwEAmpwYAAAEdUlEQVR4nO2aS4gVRxSGPxUno8KEQBBFo5jFQEAFXTi+XSWCSCQRsjVkEUQk6G5ABRU1I+pCXZhkE9wEQiDRhVGzSEAjQgjkJWrQXRwFB/EFKjLacuTvULbdfbv7dnX3jPeH4vatOt116u86p+qcauigA5/oAvYC14GghnIP+B7opSYM1DTwaLkFTK+DgEEpsLii/r5Tfz8CbwHTgBOq+5YaEKhUhdvqz33b01V3h1eAgCChv6r1yNVxXnvO8qys9d7RIYCOCdDxAVSHxvqAoOKSpEflCDoEUCrzrd5kY2dA1QQU2UN4QbRjiw4/V4xwQ5FiVxvPaxwB44B5wGdOYBK0iA6NEN8m4A3dwDJgC3ASuNuCeTc6XKrrazEDSLq/dgJeB1YBe4CzwKMYZa8AXwOfpBCwVMQFqvNNQGFTmAp8BBwC/gSGIw96ovpDkpvaQqG6TCAXAROBrcDlmBvtjf8qpVdpRuRRuEskDCpNNuDJCRa59zneAP5whO/Kts3Gl8vmR8IyWFiXbyT0AFgjr94OmkDAeOCA07ZfdS/B8mdPI4nEPTF2XUThqosLd/Bh2Ren7Ptq/Bc4F7F78+pzRigBQ87Ks0TXN+OUXa3Gn/R/kTYzoee32XEaeBcYk5OAshA+z3Tqc+r7IitUmg6JOvWq4b9I/Sx56zvOzX8Bn2Zwir4IsHIJmAC8BlxImQGZCRirkxRrnJywQvQ7m5lA1/1qS1O47Fjgon73qrh1SQSkmcn/OKPGlSTDFF6nWRA+7L42Q29HZH1thMIp75a+Mgg4qEZ7q1lg/uCUs3oMy28sSiCgzFggfPPhTIjrL64ulYB1BY+RZgM/R5Q+5zkW8ELAXCegyYvzuveU9hBBw0wg6f8LsB3SQ03pHrIjnM5DiiUmARs9xgJFnGDS/5fwmwRWkB3Hdc/2ipfB7jKXwRBfSmAT2dCrsNhmzpSKCLApv8Cpnw88LouA9RI4mlGpryR/JEXhqktbBCyQwD8ZBj9ZkaP5jHdGCwHdmk7Dcmhp2KmH/ZDQ7ssE8rTnJsDwt4RcO4tiohNpWZQ1qgg4KiHzB0nYIJnzDTwXaJuATRKyFSEOlim6Kpm1ORSqIylaiIDlErI9QRzWqv1qi7RZE84FChHQI8/+MCF/Fm57zQwoQECV5wKFCEDxQKD4IG3by2g0ARQRmuDHvIhjqrclsBWacC5QmIB+CVqOILrtfRSz7S2icF5USsB7ErQsUTRO+KIkhRtNwJtOumtshm1vmkJVl1IIQBniQFN/h67NBzACCUiTSUT4kcO2yAFDEmYCHwK7lRlqkgkUImC1hJ/GbHtnRAY71G5nTfMBIQ47N9nS9buOluIGelOnybuADxoSC4QfcfSoBKrLDNvqbna+xQ/LkN78bg12RkM3Qr/E5A8tg50blidYqFzhzIIK1xELJGWQK0FTvhGKO0OoBE0wgXD2hm15v3JpCyPuG6Gy0YRl0JcumeDafBlIG0ScT6kdAymOzVfJ41O8w7V53wMfLOBTOuBVxzPzpNeMcCaEUgAAAABJRU5ErkJggg=='
icon=PhotoImage(data=img)
window.iconphoto(False,icon)
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

def login():
    pas = passvariable.get()
    if pas == code:
        window.destroy()
        admin()
    else:
        e2.delete("0","end")
        messagebox.showerror('Passcode invalid','Check passcode !')

Label(window, text='Enter your Passcode').pack()
e2 = Entry(window,textvariable = passvariable,show='*')
e2.delete("0","end")
e2.pack(pady=10)

login_b=Button(window,command=login,height = 2, width = 15,text = "LOGIN").pack(pady=20)
window.mainloop()




