from tkinter import *
from tkinter.messagebox import *
import time

def askvalue(title='', msg='', arg=(0, 100)):
    tk = Tk()
    tk.title(title)
    tk.resizable(0, 0)
    # Tkinter
    if msg != '':
        Label(tk, text=msg).pack()
    if type(arg[0]) == type(0):
        sb = Spinbox(tk, from_=arg[0], to=arg[1], wrap=True)
    elif type(arg[0]) == type('0'):
        sb = Spinbox(tk, values=arg, wrap=True)
    else:
        raise TypeError('%s\'s items must be int or string')
    sb.pack()
    Button(tk, text='OK', command=tk.quit).pack()
    # Window
    tk.mainloop()
    # Mainloop
    get = sb.get()
    tk.destroy()
    return get
# Askvalue
def askitem(title='', msg='', items=[], number=1, normal=0):
    tk = Tk()
    tk.title(title)
    # Tkinter
    if msg != '':
        Label(tk, text=msg).place(relx=0.5, rely=0.05, relwidth=1, relheight=0.1, anchor='center')#, selectmode='multiple')
    lb = Listbox(tk)
    lb.place(relx=0.5, rely=0.5, relwidth=0.8, relheight=0.8, anchor='center')
    lb.selection_set(normal)
    Button(tk, text='OK', command=tk.quit).place(relx=0.5, rely=0.95, relwidth=1, relheight=0.1, anchor='center')
    # Window
    for x in range(0, len(items)):
        lb.insert('end', items[x])
    # Load
    tk.mainloop()
    # Mainloop
    finish = False
    get = []
    while not finish:
        tk.mainloop()
        for x in range(0, len(items)):
            if lb.selection_includes(x) == 1:
                get.append(x)
        # Get
        if len(get) == number:
            finish = True
        else:
            showinfo('', 'Choosen items must be %s item(s)' % number)
            get = []
    # Check & Get
    tk.destroy()
    return get
# Askitem
class AV:
    askyesnocancel_finish = ''
def askyesnocancel(title='', msg=''):
    askyesnocancel_tk = Tk()
    askyesnocancel_tk.title(title)
    askyesnocancel_tk.resizable(0, 0)
    # Tkinter
    if msg != '':
        Label(askyesnocancel_tk, text=msg).grid(column=0, row=0, columnspan=4)
    b1 = Button(askyesnocancel_tk, text='Cancel')
    b1.grid(column=0, row=1)
    b2 = Button(askyesnocancel_tk, text='No')
    b2.grid(column=2, row=1)
    b3 = Button(askyesnocancel_tk, text='Yes')
    b3.grid(column=3, row=1)
    # Tkinter
    b1.bind('<Button-1>', s1)
    b2.bind('<Button-1>', s2)
    b3.bind('<Button-1>', s3)
    # Bind
    while AV.askyesnocancel_finish == '':
        askyesnocancel_tk.update()
        time.sleep(0.01)
    # Mainloop
    askyesnocancel_tk.destroy()
    return AV.askyesnocancel_finish
def s1(event):
    AV.askyesnocancel_finish = None
def s2(event):
    AV.askyesnocancel_finish = False
def s3(event):
    AV.askyesnocancel_finish = True
# Askyesnocancel
def controlboard(title='', msg='', item=[('', 1, 100)]):
    tk = Tk()
    tk.title(title)
    tk.resizable(0, 0)
    # Tkinter
    if msg != '':
        Label(tk, text=msg).grid(column=0, row=0, columnspan=2)
    # Label
    window = []
    for x in item:
        window.append(Scale(tk, from_=x[1], to=x[2], orient='horizontal'))
    for x in range(0, len(item)):
        window[x].grid(column=1, row=x + 1)
        Label(tk, text=item[x][0]).grid(column=0, row=x + 1)
    # Scale
    a = len(tk.grid_slaves())
    a = int((a - 1) / 2 + 1)
    Button(tk, text='Finish', command=tk.quit).grid(column=0, row=a, columnspan=2)
    # Button
    # Window
    tk.mainloop()
    # Mainloop
    result = []
    for x in window:
        result.append(x.get())
    tk.destroy()
    return result
# Controlboard
def askanswer(title='', msg=''):
    tk = Tk()
    tk.title(title)
    tk.resizable(0, 0)
    # Tkinter
    if msg != '':
        Label(tk, text=msg).pack()
    entry = Entry(tk, width=30)
    entry.pack()
    Button(tk, text='Finish', command=tk.quit).pack()
    # Window
    tk.mainloop()
    # Mainloop
    get = entry.get()
    tk.destroy()
    return get
# Askanswer
def singlechoice(title='', msg='', arg=('a', 'b', 'c')):
    tk = Tk()
    tk.title(title)
    tk.resizable(0, 0)
    # Tkinter
    if msg != '':
        Label(tk, text=msg).pack()
    window = []
    v = StringVar()
    for x in arg:
        window.append(Checkbutton(tk, text=x, varible=v))
    for x in window:
        x.pack()
    Button(tk, text='Finish', command=tk.quit).pack()
    # Window
    tk.mainloop()
    # Mainloop
    get = v.get()
    tk.destroy()
    return get
# Singlechoice
def create(tkinter_attribute, mode='menu', arg=[('1', '<function>')]):
    tk = tkinter_attribute
    if mode == 'menu':
        a = Menu(tk)
        for x in arg:
            a.add_command(label=x[0], command=x[1])
        return a
    elif mode == 'option menu' and 1 != 1:     ##### Error : No Return
        v = StringVar()
        a = 'OptionMenu(tk, v, '
        for x in arg:
            a = a + x
            if x != arg[-1]:
                a = a + ', '
        a = a + ')'
        return exec(a)
# Create
