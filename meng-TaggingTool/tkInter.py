# coding: utf-8
from tkinter import *
from tkinter import ttk, font
import os
import sqlite3 as sql
from io import BytesIO
from PIL import Image, ImageTk
import configparser
import random


conn = sql.connect('./hard_labels.db')
cursor = conn.cursor()
cex = cursor.execute
cex('''PRAGMA TABLE_INFO (front)''')
if cursor.fetchone() is None:
    raise FileNotFoundError("input db not found")
cex('''PRAGMA TABLE_INFO (status)''')
if cursor.fetchone() is None:
    with conn:
        cex('''CREATE TABLE status (id TEXT PRIMARY KEY, info TEXT)''')
        cex('''INSERT OR IGNORE INTO status VALUES (?,?)''', (0, '0'))

if getattr(sys, 'frozen', False):
    curdir = os.path.dirname(sys.executable)
else:
    curdir = os.path.dirname(os.path.abspath(__file__))

TITLE = 'ultimate super very nice idcard label tools'
FONT='./simhei.ttf'
PERSON = {'any': ''}



def get_spec_files(path, ext='.jpg', fullpath=True, maxN=0):
    ''' get files in path with specific extension '''
    files = []
    for f in os.listdir(path):
        if os.path.splitext(f)[1] == ext:
            if fullpath:
                files.append(os.path.join(path, f))
            else:
                files.append(f)
            if maxN > 0 and len(files) >= maxN:
                break
    return files


def parse_front(s):
    content = s[:-4]
    front, orderno, content = content.split('_')
    content = content.split('-')
    name, birth, nation = content[0], content[1], content[2]
    idno = content[-1]
    address = '-'.join(content[3:-1])
    return name, birth, nation, address, idno


def parse_back(s):
    content = s[:-4]
    back, orderno, content = content.split('_')
    police, start, end = content.split('-')
    return police, start + '-' + end



##yl 2018/12/11
import cv2
import os
def save_img(img,img_name):
    root_path=r'c:/users/yelei/desktop/'
    path="{0}{1}{2}".format(str(root_path),str(img_name),".jpg")
    cv2.imwrite(path,img)
def delete_img(img_name):
    root_path = r'c:/users/yelei/desktop/'
    path = "{0}{1}{2}".format(str(root_path), str(img_name), ".png")
    if os.path.exists(path):
        os.remove(path)





class Cleaner:
    def __init__(self, root_widget, is_front, whom='any'):
        self.root_widget = root_widget
        if is_front:
            self.images = get_spec_files(r'/zqzn/chenxin/data/ocr/images/test_data/hard_id_card_image/front')
        else:
            # self.images = get_spec_files(os.path.join(curdir,'images/back'))
            self.images = get_spec_files(r'/zqzn/chenxin/data/ocr/images/test_data/hard_id_card_image/back')
        self.images.sort()
        self.is_front = is_front
        cex('''SELECT info FROM status''')
        self.prog = int(cursor.fetchone()[0])
        if self.prog >= len(self.images):
            self.prog = 0
            with conn:
                cex('''UPDATE status SET info=? WHERE id=0''', (str(self.prog),))
        self.whom = whom

        cfg = configparser.ConfigParser()
        cfg.read(os.path.join(curdir, 'config.ini'))
        self.fontsize = cfg['Gui']['fontsize']

        self.build_gui()
        self.set_task()
        if self.is_front:
            self.name_ety.focus()
        else:
            self.police_ety.focus()
        # for i in range(len(eggs)):
        #     eggs[i] = ImageTk.PhotoImage(eggs[i])

    def build_gui(self):
        self.root_widget.title('{}: {}/{}'.format(TITLE, self.prog + 1, len(self.images)))
        self.root_widget.geometry('800x600')
        self.root_widget.columnconfigure(0, weight=1)
        self.root_widget.rowconfigure(0, weight=1)
        self.frame = ttk.Frame(self.root_widget)
        self.frame.rowconfigure(0, weight=1)
        if self.is_front:
            self.frame.columnconfigure(0, weight=1)
            self.frame.columnconfigure(1, weight=100)
        else:
            self.frame.columnconfigure(0, weight=3)
            self.frame.columnconfigure(1, weight=4)
        self.canvas = Canvas(self.frame)

        self.frame.grid(row=0, column=0, sticky='nsew')
        self.canvas.grid(row=0, column=0, rowspan=2, columnspan=2, sticky='nsew')
        self.canvas.bind('<Configure>', self.event_resize)

        pad = 3
        if self.is_front:
            self.name_lbl = ttk.Label(self.frame, text='name', width=10, font='{} {}'.format(FONT, self.fontsize))
            self.name_var = StringVar()
            self.name_ety = ttk.Entry(self.frame, textvariable=self.name_var,
                                      font='{} {}'.format(FONT, self.fontsize))

            self.nation_lbl = ttk.Label(self.frame, text='nation', font='{} {}'.format(FONT, self.fontsize))
            self.nation_var = StringVar()
            self.nation_ety = ttk.Entry(self.frame, textvariable=self.nation_var,
                                        font='{} {}'.format(FONT, self.fontsize))

            self.address_lbl = ttk.Label(self.frame, text='address', font='{} {}'.format(FONT, self.fontsize))
            self.address_var = StringVar()
            self.address_ety = ttk.Entry(self.frame, textvariable=self.address_var,
                                         font='{} {}'.format(FONT, self.fontsize))

            self.idno_lbl = ttk.Label(self.frame, text='idno', font='{} {}'.format(FONT, self.fontsize))
            self.idno_var = StringVar()
            self.idno_ety = ttk.Entry(self.frame, textvariable=self.idno_var,
                                      font='{} {}'.format(FONT, self.fontsize))

            self.name_lbl.grid(row=10, column=0, sticky='sw', pady=pad, padx=pad)
            self.name_ety.grid(row=10, column=1, sticky='nsew', pady=pad, padx=pad)
            self.nation_lbl.grid(row=11, column=0, sticky='sw', pady=pad, padx=pad)
            self.nation_ety.grid(row=11, column=1, sticky='nsew', pady=pad, padx=pad)
            self.address_lbl.grid(row=12, column=0, sticky='sw', pady=pad, padx=pad)
            self.address_ety.grid(row=12, column=1, sticky='nsew', pady=pad, padx=pad)
            self.idno_lbl.grid(row=13, column=0, sticky='sw', pady=pad, padx=pad)
            self.idno_ety.grid(row=13, column=1, sticky='nsew', pady=pad, padx=pad)
        else:
            self.police_lbl = ttk.Label(self.frame, text='police', font='{} {}'.format(FONT, self.fontsize))
            self.police_var = StringVar()
            self.police_ety = ttk.Entry(self.frame, textvariable=self.police_var,
                                        font='{} {}'.format(FONT, self.fontsize))

            self.expiry_lbl = ttk.Label(self.frame, text='expiry', font='{} {}'.format(FONT, self.fontsize))
            self.expiry_var = StringVar()
            self.expiry_ety = ttk.Entry(self.frame, textvariable=self.expiry_var,
                                        font='{} {}'.format(FONT, self.fontsize))

            self.police_lbl.grid(row=10, column=0, sticky='sw', pady=pad, padx=pad)
            self.police_ety.grid(row=10, column=1, sticky='nsew', pady=pad, padx=pad)
            self.expiry_lbl.grid(row=11, column=0, sticky='sw', pady=pad, padx=pad)
            self.expiry_ety.grid(row=11, column=1, sticky='nsew', pady=pad, padx=pad)

        self.root_widget.bind('<Return>', self.event_enter)
        self.root_widget.bind('<Shift-Return>', self.event_shift_enter)
        self.root_widget.bind('<Control-Left>', self.event_rotate)
        self.root_widget.bind('<Control-Right>', self.event_rotate_anti)

    def _resize(self, width, height):
        h, w = self.img_ori.height, self.img_ori.width
        scale = min(width / w, height / h)
        width, height = int(w * scale + 0.5), int(h * scale + 0.5)
        resized = self.img_ori.resize((width, height), Image.ANTIALIAS)
        self.img_show = ImageTk.PhotoImage(resized)
        self.canvas.delete('IMG')
        self.canvas.create_image(0, 0, image=self.img_show, anchor='nw', tags='IMG')

    def event_resize(self, event):
        self._resize(event.width, event.height)

    def event_rotate(self, event):
        self.img_ori = self.img_ori.transpose(Image.ROTATE_90)
        self._resize(self.canvas.winfo_width(), self.canvas.winfo_height())

    def event_rotate_anti(self, event):
        self.img_ori = self.img_ori.transpose(Image.ROTATE_90)
        self.img_ori = self.img_ori.transpose(Image.ROTATE_90)
        self.img_ori = self.img_ori.transpose(Image.ROTATE_90)
        self._resize(self.canvas.winfo_width(), self.canvas.winfo_height())

    def msgbox(self, title, msg):
        top = Toplevel(self.root_widget)
        top.title(title)
        lbl = ttk.Label(top, text=msg)
        lbl.grid(row=0, column=0)
        btn = ttk.Button(top, text="^-^", command=top.destroy)
        btn.grid(row=1, column=0)
        screenwidth = top.winfo_screenwidth()
        screenheight = top.winfo_screenheight()
        top.geometry('+%s+%s' % (screenwidth // 2, screenheight // 2))
        top.focus()

    def save_current(self):
        if self.is_front:
            name, nation, address, idno = self.name_var.get(), self.nation_var.get(), \
                                          self.address_var.get(), self.idno_var.get()
            with conn:
                cex('''UPDATE front SET name=?,nation=?,address=?,idno=? WHERE fn=?''',
                    (name, nation, address, idno, self.fn))
        else:
            police, expiry = self.police_var.get(), self.expiry_var.get()
            with conn:
                cex('''UPDATE back SET police=?, expiry=? WHERE fn=?''',
                    (police, expiry, self.fn))
        # if self.prog % 500 >= 490 and random.uniform(0,1) < 0.2:
        # self.imgbox('辛苦啦，休息一下吧^-^'+PERSON[self.whom])

    def event_enter(self, event):
        self.save_current()
        self.prog += 1
        if self.prog >= len(self.images):
            self.prog -= 1
            self.msgbox('Yes ^-^ Yes', '完成了，欧耶')
        else:
            self.set_task()
            self._resize(self.canvas.winfo_width(), self.canvas.winfo_height())
        self.root_widget.title('{}: {}/{}'.format(TITLE, self.prog + 1, len(self.images)))
        with conn:
            cex('''UPDATE status SET info=? WHERE id=0''', (str(self.prog),))


    def event_shift_enter(self, event):
        self.save_current()
        self.prog -= 1
        if self.prog < 0:
            self.prog += 1
            self.msgbox('@-@', '天哪，竟然是第一张')
        else:
            self.set_task()
            self._resize(self.canvas.winfo_width(), self.canvas.winfo_height())
        self.root_widget.title('{}: {}/{}'.format(TITLE, self.prog + 1, len(self.images)))
        with conn:
            cex('''UPDATE status SET info=? WHERE id=0''', (str(self.prog),))

    def set_task(self):
        img = self.images[self.prog]
        self.img_ori = Image.open(img)
        self.img_show = ImageTk.PhotoImage(self.img_ori)
        self.canvas.create_image(0, 0, image=self.img_show, anchor='nw', tags='IMG')
        if self.is_front:
            print(os.path.split(img)[1])
            cex('''SELECT * FROM front WHERE fn=?''', (os.path.split(img)[1],))
            self.fn, name, sex, nation, birth, address, idno = cursor.fetchone()
            self.name_var.set(name)
            self.nation_var.set(nation)
            self.address_var.set(address)
            self.idno_var.set(idno)
            # name_, _, nation_, address_, idno_ = parse_front(self.fn)
            # self.name_ety['state'] = 'disable' if name == name_ else 'normal'
            # self.nation_ety['state'] = 'disable' if nation == nation_ else 'normal'
            # self.address_ety['state'] = 'disable' if address == address_ else 'normal'
            # self.idno_ety['state'] = 'disable' if idno == idno_ else 'normal'
        else:
            cex('''SELECT * FROM back WHERE fn=?''', (os.path.split(img)[1],))
            self.fn, police, expiry = cursor.fetchone()
            self.police_var.set(police)
            self.expiry_var.set(expiry)
            # police_, expiry_ = parse_back(self.fn)
            # self.police_ety['state'] = 'disable' if police == police_ else 'normal'
            # self.expiry_ety['state'] = 'disable' if expiry == expiry_ else 'normal'

        if self.img_ori.height > self.img_ori.width:
            self.event_rotate_anti(None)


if __name__ == '__main__':
    root_widget = Tk()
    cleaner = Cleaner(root_widget,is_front=False)
    root_widget.mainloop()
