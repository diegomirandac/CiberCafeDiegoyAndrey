import tkinter as tk
import time

def time():
    return time.strftime("%Y%m%dT%H%M%SZ",time.gmtime())

class Aplication(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.pack()
        self.createWidgets()
    def createWidgets(self):
        self.now = tk.StringVar()
        self.time = tk.Label(self, font=('Helvetica', 24))
        self.time.pack(side="top")
        self.time["textvariable"] = self.now
        self.QUIT = tk.Button(self, text="QUIT", fg="red",
                                            command=root.destroy)
        self.QUIT.pack(side="bottom")
        self.onUpdate()
        def onUpdate(self):
        self.now.set(current_iso8601())
        self.after(1000, self.onUpdate)
root = tk.Tk()
app = Application(master=root)
root.mainloop()