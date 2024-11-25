import tkinter as tk
from tkinter import ttk
from reportlab.lib.styles import ParagraphStyle 
from objects import *

def init_widget(widget, property_name, selected, default=None):
    if property_name in selected.keys():
        widget.set(selected[property_name])
    elif default == None:
        widget.set(str(getattr(ParagraphStyle(name='dummy'), property_name, None)))
    else:
        widget.set(default[property_name])

def mkEntry(frame, property_name, style, default=None, condition=None, **kwargs):
    var_name = tk.StringVar()
    init_widget(var_name, property_name,style,default=default)
    if condition == None:
        entry = ttk.Entry(frame, textvariable=var_name)
    else:
        wrapper = (frame.register(condition), '%P')
        entry = ttk.Entry(frame, textvariable=var_name, validate='key', validatecommand=wrapper)
    entry.grid(**kwargs)
    return var_name

def mkComb(frame,property_name, style, val_list, scroll_event,default=None, state='readonly', **kwargs):
    comb = ttk.Combobox(frame)
    comb['values'] = val_list
    comb.state([state])
    comb.bind("<MouseWheel>", scroll_event)
    init_widget(comb,property_name,style,default=default)
    comb.grid(**kwargs)
    return comb

def mkCheckbox(frame, property_name, style, default=None,**kwargs):
    var_name = tk.IntVar()
    init_widget(var_name, property_name,style,default=default)
    checkbox = ttk.Checkbutton(frame, variable=var_name)
    checkbox.grid(**kwargs)
    return var_name

def mkColorpicker(frame,property_name,style,default=None,**kwargs):
    var_name = tk.StringVar()
    init_widget(var_name, property_name,style,default=default)
    picker = ColorPicker(frame,var_name)
    picker.grid(**kwargs)
    return picker

def mkMultiinsert(frame, property_name, style, n_entries, default=None,**kwargs):
    default_tuple = (0,)*n_entries
    multi = MultipleInsert(frame, n_entries, default_tuple)
    init_widget(multi, property_name,style,default=default)
    multi.grid(**kwargs)
    return multi

def mkEntryselctor(frame, property_name,style, val_list, default=None,**kwargs):
    selector = EntryWithSelector(frame, val_list, "")
    init_widget(selector, property_name,style,default=default)
    selector.grid(**kwargs)
    return selector