import tkinter as tk
from tkinter import ttk
from reportlab.lib.styles import ParagraphStyle 
from objects import *
from style_utils import *
from default_settings import *
from functools import partial
import toml
import re

def load_styles(style_dict,*argv):
    for style_file in argv:
        styles_toml = toml.load(style_file)
        for style_name in styles_toml:
            #If two style names are equal put a (number) after the name
            updated_style_name = style_name
            if style_name in list(style_dict.keys()):
                updated_style_name = f"{style_name}({list(style_dict.keys()).count(style_name)})"
            #style_dict is a dictionary which at each style name in the file uploaded associate the style and the settings dictionaries
            style_dict[updated_style_name] = {"style": styles_toml[style_name]["style"], 
                                              "settings": styles_toml[style_name]["settings"],
                                              "file": style_file}
            if updated_style_name == style_name:
                style_dict[updated_style_name]["renamed"] = False
            else:
                style_dict[updated_style_name]["renamed"] = True

    return style_dict

def refresh(event, new_stringvar, style_dict, style_widget_dict):
    for name,widget in style_widget_dict["style"].items():
        init_widget(widget, name, style_dict[new_stringvar]["style"])

    for name,widget in style_widget_dict["settings"].items():
        init_widget(widget, name, style_dict[new_stringvar]["settings"],default_settings)
    
def export(name, style_config_dict, settings_config_dict):
    style_dict = {}
    default_style = ParagraphStyle(name='dummy')
    for entry in style_config_dict:
        if str(style_config_dict[entry].get()) != str(getattr(default_style, entry, None)):
            style_dict[entry] = style_config_dict[entry].get()

    settings_dict = {}
    for entry in settings_config_dict:
        settings_dict[entry] = settings_config_dict[entry].get()

    toml_dict = { name: {}, f"{name}": { 'style': style_dict, 'settings': settings_dict } }
    with open(f"styles/{name}.toml","w") as toml_file:
        toml.dump(toml_dict,toml_file)

def make_font_list(font_file):
    font_toml=toml.load(font_file)
    font_list = []
    font_list.append(ParagraphStyle(name='dummy').fontName)
    for font in font_toml:
        font_list.append(font_toml[font]['default']['name'])
    return font_list

def create_tab(notebook):

    def on_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))
    def on_mousewheel(event): 
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")
            
    def check_if_int(newval):
        return re.match('^[0-9]*$', newval) is not None
    
    #styles_dict, settings_dict = load_styles_settings({},{},'styles.toml','styles/poetry.toml')
    style_dict = load_styles({},'styles.toml','styles/poetry.toml')
    
    frame = ttk.Frame(notebook)
    frame.columnconfigure(0,weight=1)
    frame.columnconfigure(1,weight=1)
    frame.rowconfigure(0,weight=0)
    frame.rowconfigure(1,weight=1)
    notebook.add(frame, text='Style')
    style_notebook = ttk.Notebook(frame)
    style_tab = ttk.Frame(style_notebook)
    style_notebook.add(style_tab, text="Style")
    settings_tab = ttk.Frame(style_notebook)
    style_notebook.add(settings_tab, text="Settings")
    style_notebook.grid(row=1,column=0,sticky="nsew")

    ##########################################################################################
    #### STYLE MANAGER #######################################################################
    ##########################################################################################

    selected_style_stringvar = tk.StringVar()
    selected_style_stringvar.set(list(style_dict.keys())[0])
    style_selector = ttk.Combobox(frame, textvariable=selected_style_stringvar)
    style_selector.state(["readonly"])
    style_selector.bind("<<ComboboxSelected>>",lambda event: refresh(event,selected_style_stringvar.get(), style_dict, style_widget_dict))
    style_selector['values'] = list(style_dict.keys())
    style_selector.grid(row=0, column=1, sticky='w')

    newStyleButton = ttk.Button(frame,text="add",command=lambda: print(selected_style_stringvar.get()))
    #newStylwButton = ttk.Button(frame,text="New",command=lambda: refresh(selected_style_stringvar.get(), styles_dict, settings_dict, info_dict, settings_info_dict))
    newStyleButton.grid(row=1,column=1, sticky='nw')

    ##########################################################################################
    #### STYLE AND SETTINGS NOTEBOOK #########################################################
    ##########################################################################################

    canvas = tk.Canvas(style_tab) 
    canvas.pack(side='left', fill='both', expand= True)
    
    scrollbar = ttk.Scrollbar(style_tab, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right",fill="y")

    canvas.configure(yscrollcommand=scrollbar.set)

    labels_frame = ttk.Frame(canvas)
    canvas.create_window((0,0), window=labels_frame, anchor="nw")

    def pass_event_to_canvas(event):
        canvas.event_generate("<MouseWheel>", delta=event.delta)
        return "break"
    
    ######################### STYLE TAB #######################################################

    #style_widget_dict is a dictionary that holds the widget associated to each ParagraphStyle and settings properties
    #the structure is independent from the selected style, in this loop the values are initialized to the starting style
    style_widget_dict = {"style":{},"settings":{}}
    dummy_paragraph = ParagraphStyle(name="default")
    label_name_list = list(vars(dummy_paragraph).keys())
    #Iterate over the properties of ParagraphStyle
    for name,idx in zip(label_name_list,range(len(label_name_list))):
        
        #Skip the parent property
        if name in ['parent']:
            continue

        ttk.Label(labels_frame, text=name).grid(row=idx,column=0,sticky='w')
        
        #for each loop define some functions with aggregated parameters, enhance the readibilty of the code that
        #initialize the widget
        init_entry = partial(mkEntry, 
                             frame=labels_frame,
                             style=style_dict[selected_style_stringvar.get()]['style'],
                             row=idx,column=1,sticky='we')
        
        init_comb = partial(mkComb, 
                            frame=labels_frame, 
                            style=style_dict[selected_style_stringvar.get()]['style'],
                            scroll_event=pass_event_to_canvas, 
                            row=idx,column=1,sticky='we')

        init_checkbox = partial(mkCheckbox, 
                                frame = labels_frame, 
                                style=style_dict[selected_style_stringvar.get()]['style'],
                                row=idx,column=1,sticky='we')

        init_colorpicker = partial(mkColorpicker,
                                   frame = labels_frame,
                                   style=style_dict[selected_style_stringvar.get()]['style'],
                                   row=idx,column=1,sticky='we')

        init_multiinsert = partial(mkMultiinsert,
                                   frame = labels_frame,
                                   style=style_dict[selected_style_stringvar.get()]['style'],
                                   row = idx, column = 1, sticky='we')

        init_entryselctor = partial(mkEntryselctor,
                                     frame = labels_frame,
                                     style=style_dict[selected_style_stringvar.get()]['style'],
                                     row = idx, column = 1, sticky = 'we')

        if name in ['name','endDots']:
            style_widget_dict["style"][name] = init_entry(property_name=name)
        
        #DA METTERE CONDIZIONI SULL'INPUT
        elif name in ['borderRadius','spaceShrinkage','hyphenationLang','uriWasteReduce','underlineGap','strikeGap']:
            style_widget_dict["style"][name] = init_entry(property_name=name)
        
        elif name in ['underlineWidth','underlineOffset','strikeWidth','strikeOffset']:
            style_widget_dict["style"][name] = init_entryselctor(property_name=name, val_list=('P','L','f','F',''))

        elif name in ['fontName', 'bulletFontName']:           
            style_widget_dict["style"][name]=init_comb(property_name=name, val_list=make_font_list('fonts.toml'))

        elif name in ['alignment']:
            style_widget_dict["style"][name]=init_comb(property_name=name, val_list=(0,1,2,4))
        
        elif name in ['textTransform']:
            style_widget_dict["style"][name]=init_comb(property_name=name, val_list=('None','lowercase','uppercase','capitalize'))
        
        elif name in ['bulletAnchor']:
            style_widget_dict["style"][name]=init_comb(property_name=name, val_list=('start','middle','end','numeric'))
        
        elif name in ['wordWrap']:
            style_widget_dict["style"][name]=init_comb(property_name=name, val_list=('None','CJK'))

        elif name in ['fontSize','leading', 'leftIndent','rightIndent', 'firstLineIndent', 'spaceBefore', 'spaceAfter', 'bulletFontSize', 'bulletIndent', 'borderWidth']:
            style_widget_dict["style"][name] = init_entry(property_name=name, condition=check_if_int)
        
        elif name in ['borderPadding']:
            style_widget_dict["style"][name] = init_multiinsert(property_name=name, n_entries=4)

        elif name in ['splitLongWords','allowWidows','allowOrphans','justifyLastLine', 'justifyBreaks','linkUnderline','embeddedHyphenation']:
            style_widget_dict["style"][name] = init_checkbox(property_name=name)
        
        elif name in ['textColor','backColor','borderColor','underlineColor','strikeColor']:
            style_widget_dict["style"][name] = init_colorpicker(property_name=name)

    ######################### SETTINGS TAB #######################################################

    label_settings_list = list(default_settings.keys())
    for name,idx in zip(label_settings_list, range(len(label_settings_list))):
        ttk.Label(settings_tab, text=name).grid(row=idx,column=0,sticky='w')

        init_entry = partial(mkEntry, 
                             frame=settings_tab,
                             style=style_dict[selected_style_stringvar.get()]["settings"],
                             default = default_settings,
                             row=idx,column=1,sticky='we')
        
        init_checkbox = partial(mkCheckbox, 
                                frame = settings_tab,
                                style=style_dict[selected_style_stringvar.get()]["settings"], 
                                default = default_settings,
                                row=idx,column=1,sticky='we')

        if name in ['newPageBefore', 'newPageAfter', 'newParagraphOnEndline']:
            style_widget_dict['settings'][name] = init_checkbox(property_name=name)

        elif name in ['blockSpaceBefore', 'blockSpaceAfter']:
            style_widget_dict['settings'][name] = init_entry(property_name=name, condition=check_if_int)

    ttk.Button(settings_tab, text="button", command=lambda : print(style_widget_dict["style"]['newPageBefore'].get())) #BUTTON NEEDED SOMEHOW TO INITIALIZE CORRECTLY WIDGETS ON STYLE TAB
    labels_frame.bind("<Configure>", on_configure)
    canvas.bind_all("<MouseWheel>", on_mousewheel)

    ##########################################################################################
    #### NAME AND EXPORT BUTTON ##############################################################
    ##########################################################################################

    button = ttk.Button(frame, text="Save", command=lambda : export(selected_style_stringvar.get(), style_widget_dict['style'], style_widget_dict['settings']))
    button.grid(row=0,column=0,sticky='w')


    return style_tab