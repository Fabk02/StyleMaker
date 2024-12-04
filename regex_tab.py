import tkinter as tk
from tkinter import ttk
import toml

def load_regex(regex_list,*argv):
    for file in argv:
        regex_toml = toml.load(file)
        regex_list += regex_toml['regex']
        for regex_dict in regex_list:
            regex_dict['file'] = file
            regex_dict['active'] = False

def create_tab(notebook):
    frame = ttk.Frame(notebook)
    notebook.add(frame, text='Regex')

    top_frame_buttons = ttk.Frame(frame)
    top_frame_buttons.grid(row=0,column=0,sticky="w")
    newButton = ttk.Button(top_frame_buttons, text="New", command=lambda: load_regex([], "regex.toml"))
    newButton.grid(row=0,column=0)
    loadButton = ttk.Button(top_frame_buttons, text="Load", command=lambda: print("Load"))
    loadButton.grid(row=0, column=1)

    return frame