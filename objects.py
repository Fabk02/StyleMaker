import tkinter as tk
from tkinter import ttk
from tkinter import colorchooser
import re

class ColorPicker:
    def __init__(self,parent,stringvar):
        self.stringvar = stringvar
        self.frame = ttk.Frame(parent)
        self.entry = tk.Entry(self.frame,textvariable=self.stringvar)
        self.entry.grid(row=0,column=0,sticky='we')
        self.entry.bind('<KeyRelease>', self.update_color)
        self.colorbutton = tk.Button(self.frame, command=self.choose_color)
        if re.match('^#[0-9]*$', self.stringvar.get()) is not None:
            self.colorbutton.config(background=self.stringvar.get())
        else:
            self.colorbutton.config(background="#000000")
        self.colorbutton.grid(row=0,column=1,sticky='we')
        self.checkvar = tk.IntVar()
        if self.stringvar.get() == "None":
            self.checkvar.set(1)
            self.entry.config(state='disabled')
            self.colorbutton.config(state="disabled")
        else:
            self.checkvar.set(0)
        self.checkbox = ttk.Checkbutton(self.frame, variable=self.checkvar, command=self.update_status)
        self.checkbox.grid(row=0,column=2,sticky='we')
        self.update_color("s")
        
    def grid(self, **kwargs):
        self.frame.grid(kwargs)

    def choose_color(self):
        color = colorchooser.askcolor(title="choose color")
        if color[1] is not None:
            self.stringvar.set(color[1])
            self.colorbutton.config(background = color[1])
    
    def update_color(self,event):
        if re.match('^#[0-9a-fA-F]*$', self.stringvar.get()) is not None and len(self.stringvar.get()) == 7:
            self.colorbutton.config(background=self.stringvar.get())
        elif self.stringvar.get() == "None":
            self.entry.config(state='disabled')
            self.colorbutton.config(state='disabled')
            if self.checkvar.get() == 0:
                self.checkvar.set(1)
        else:
            self.colorbutton.config(background='#000000')

    def update_status(self):
        if self.checkvar.get() == 0:
            self.stringvar.set(self.colorbutton.cget('bg'))
            self.entry.config(state='normal')
            self.colorbutton.config(state='normal')
        else:
            self.stringvar.set("None")
            self.entry.config(state='disabled')
            self.colorbutton.config(state='disabled')
    
    def set(self,colorvar):
        self.stringvar.set(colorvar)
        self.update_color("s")

    def get(self):
        if (re.match('^#[0-9a-fA-F]*$', self.stringvar.get()) is not None and len(self.stringvar.get()) == 7) or self.stringvar.get() == "None":
            return self.stringvar.get()
        else:
            return self.colorbutton.cget('bg')

class MultipleInsert:
    def __init__(self,parent, n_entries,arg_tuple, default=0):
        self.tuple = arg_tuple
        self.default = default
        self.frame = ttk.Frame(parent)
        self.entry_varlist = []

        total_width = 22
        entry_width = total_width // n_entries

        for idx in range(n_entries):
            self.frame.grid_columnconfigure(idx, weight=1,uniform="equal")
            var = tk.StringVar()
            if isinstance(self.tuple, tuple) or isinstance(self.tuple, list):
                if idx < len(self.tuple):
                    var.set(self.tuple[idx])
                else:
                    var.set(default)
            else:
                var.set(self.tuple)
            entry = ttk.Entry(self.frame, textvariable=var, width=entry_width)
            entry.grid(row=0,column=idx,sticky='nsew')
            self.entry_varlist.append(var)

    def grid(self, **kwargs):
        self.frame.grid(kwargs)
    
    def set(self, arg_tuple):
        for entry,idx in zip(self.entry_varlist,range(len(self.entry_varlist))):
            if isinstance(arg_tuple, tuple) or isinstance(arg_tuple, list):
                if idx < len(arg_tuple):
                    entry.set(arg_tuple[idx])
                else:
                    entry.set(self.default)
            else:
                entry.set(arg_tuple)
    
    def get(self):
        if len(set([x.get() for x in self.entry_varlist])) == 1:
            return (int(self.entry_varlist[0].get()))
        else:
            l=[]
            for entry in self.entry_varlist:
                l.append(int(entry.get()))
            return tuple(l)
    
class EntryWithSelector:
    def __init__(self,parent,args,string):
        self.frame = ttk.Frame(parent)
        self.args = args
        self.string = string
        self.comb = ttk.Combobox(self.frame,width=3)
        self.comb.state(['readonly'])
        self.comb['values'] = self.args
        self.stringvar = tk.StringVar()
        self.entry = ttk.Entry(self.frame, textvariable=self.stringvar,width=17)
        
        self.splitted_string = self.string.rsplit("*",1)
        if len(self.splitted_string) == 1:
            self.splitted_string.append(" ")

        self.comb.set(self.splitted_string[1])
        self.stringvar.set(self.splitted_string[0])

        self.entry.grid(row=0,column=0,sticky='we')
        ttk.Label(self.frame, text='*').grid(row=0,column=1)
        self.comb.grid(row=0,column=2,sticky='we')
    
    def grid(self, **kwargs):
        self.frame.grid(**kwargs)
    
    def set(self, string):
        self.splitted_string = string.rsplit("*",1)
        if len(self.splitted_string) == 1:
            self.splitted_string.append(" ")

        self.comb.set(self.splitted_string[1])
        self.stringvar.set(self.splitted_string[0])
    
    def get(self):
        if self.comb.get().strip(' ') == '':
            return self.stringvar.get()
        else:
            return (self.stringvar.get() + '*' + self.comb.get())


""" window = tk.Tk()
window.geometry("600x600")
window.title("Style creator")
window.configure(background="white")
frame = ttk.Frame(window)
frame.pack(expand=1,fill="both")
picker = ColorPicker(frame,tk.StringVar(value="#nano"))
picker.grid(row=0,column=0,sticky='we')
selector = MultipleInsert(frame, 4, (2,3))
selector.grid(row=1,column=0,columnspan=1)
seles = EntryWithSelector(frame, ('P','L','f','F'), "p*al*F")
seles.grid(row=2,column=0)
ttk.Button(frame, text="Palle", command=lambda: print(seles.get())).grid(row=0,column=1)

window.mainloop() """