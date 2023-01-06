from tkinter import *      
root = Tk()
root.option_add("*Background", "#181818")
canvas = Canvas(root, width = 300, height = 300)      
canvas.pack()      
img = PhotoImage(file="appCache\spl1.png")      
canvas.create_image(20,20, anchor=NW, image=img)      
mainloop() 