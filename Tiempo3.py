from tkinter import *
import time
tk=Tk()
def clock():
    t=time.strftime('%I:%M:%S',time.localtime())
    if t!='':
        label1.config(text=t,font='times 25')
    tk.after(100,clock)
label1=Label(tk,justify='center')
label1.pack()
clock()
tk.mainloop()