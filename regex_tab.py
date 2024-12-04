import tkinter as tk
from tkinter import ttk
import toml
import objects

def load_regex(regex_dict,*argv):
    for file in argv:
        regex_toml = toml.load(file)
        for og_regex_dict in regex_toml['regex']:
            regex_dict[og_regex_dict['find']] = {'replace': og_regex_dict['replace'],
                                                 'file': file,
                                                 'active': False}
    return regex_dict

def create_tab(notebook):
    frame = ttk.Frame(notebook)
    notebook.add(frame, text='Regex')

    top_frame_buttons = ttk.Frame(frame)
    top_frame_buttons.grid(row=0,column=0,sticky="w")

    regex_dict = load_regex({},"regex.toml")
    newButton = ttk.Button(top_frame_buttons, text="New", command=lambda: print("New"))
    newButton.grid(row=0,column=0)
    loadButton = ttk.Button(top_frame_buttons, text="Load", command=lambda: print("Load"))
    loadButton.grid(row=0, column=1)

    for match_regex,idx in zip(list(regex_dict.keys()), range(len(list(regex_dict.keys())))):
        objects.RegexEntry(frame, match_regex, regex_dict[match_regex]['replace'], regex_dict[match_regex]['active']).grid(row=idx+1,column=0)

    return frame