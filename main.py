import tkinter as tk
import tkinter.ttk as ttk
import style_tab

window = tk.Tk()
window.geometry("600x600")
window.title("Style creator")
window.configure(background="white")
window.columnconfigure(0,weight=1)
window.rowconfigure(0,weight=1)
#window.rowconfigure(1,weight=1)

notebook = ttk.Notebook(window)
text_tab = ttk.Frame(notebook)
regex_tab = ttk.Frame(notebook)
fonts_tab = ttk.Frame(notebook)
notebook.add(text_tab, text='Text')
style_tab.create_tab(notebook)
notebook.add(regex_tab, text='Regex')
notebook.add(fonts_tab, text='Fonts')
#notebook.pack(expand=1, fill='both')
notebook.grid(row=0,column=0,sticky='nsew')

if __name__ == "__main__":
    window.mainloop()