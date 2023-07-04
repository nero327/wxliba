import subprocess
import time
import tkinter as tk
from tkinter import filedialog
import shutil
import os
import ctypes, sys
import tinyaes

class ReplaceApp:
    def __init__(self, master):
        self.master = master
        self.master.title("转换器")
        self.master.geometry("400x200")

        self.file_path = tk.StringVar()
        self.id_value = tk.StringVar()
        self.password_value = tk.StringVar()
        self.ime_value = self.imeg()
        self.max_vvalue = tk.StringVar()
        self.var = tk.IntVar()
        self.check_value = "book"
        self.create_widgets()

    def create_widgets(self):
        checkbox = tk.Checkbutton(self.master, text="入坐", variable=self.var, command=self.get_selection)
        checkbox.grid(row=1, column=2)
        tk.Label(self.master, text="文件路径:").grid(row=0, column=0)
        tk.Entry(self.master, textvariable=self.file_path, width=30).grid(row=0, column=1)
        tk.Button(self.master, text="浏览", command=self.browse_file).grid(row=0, column=2)

        tk.Label(self.master, text="学号:").grid(row=1, column=0)
        tk.Entry(self.master, textvariable=self.id_value, width=30).grid(row=1, column=1)

        tk.Label(self.master, text="密码:").grid(row=2, column=0)
        tk.Entry(self.master, textvariable=self.password_value, width=30).grid(row=2, column=1)

        # tk.Label(self.master, text="IME Value:").grid(row=3, column=0)
        # tk.Entry(self.master, textvariable=self.ime_value, width=30).grid(row=3, column=1)

        tk.Label(self.master, text="时长:").grid(row=4, column=0)
        tk.Entry(self.master, textvariable=self.max_vvalue, width=30).grid(row=4, column=1)

        tk.Button(self.master, text="转换", command=self.replace_text).grid(row=5, column=1)
        tk.Button(self.master, text="exe", command=self.to_exe).grid(row=6, column=1)

    def get_selection(self):
        if self.var.get() == 1:
            self.check_value = "check"
        else:
            self.check_value = "book"

    def is_admin(self):
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False

    def to_exe(self):
        command = "pyinstaller -p venv\Lib\site-packages -F -i {b}/icon.png {a}{id_value}.py --key 'ddcnb'".format(b=os.getcwd(),
                                                                                                     a=self.check_value,
                                                                                                     id_value=self.id_value.get())
        # os.system(comand)
        # subprocess.run(['powershell', '-Command', f'Start-Process "{command}" -Verb RunAs'])
        if self.is_admin():
            recode = subprocess.Popen(
                command,
                shell=True)
        else:
            if sys.version_info[0] == 3:
                ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
            else:  # in python2.x
                ctypes.windll.shell32.ShellExecuteW(None, u"runas", unicode(sys.executable), unicode(__file__), None, 1)

    def browse_file(self):
        file_path = filedialog.askopenfilename()
        self.file_path.set(file_path)

    def imeg(self):
        imee = 56516602590020406 + int(time.time())
        return imee

    def maxday(self):
        maxd = int(self.max_vvalue.get()) * 86440 + int(time.time())
        return maxd

    def replace_text(self):
        file_path = self.file_path.get()
        id_value = self.id_value.get()
        password_value = self.password_value.get()
        ime_value = self.imeg()
        max_vvalue = self.maxday()

        # copy the file to a new location
        file_path = file_path
        new_file_path = os.getcwd() + '/{b}{id_value}.py'.format(b=self.check_value, id_value=self.id_value.get())
        # os.makedirs(os.path.dirname(new_file_path), exist_ok=True)
        # new_file_path = file_path
        shutil.copy2(file_path, new_file_path, )

        # replace the text in the new file
        with open(new_file_path, 'r', encoding='UTF-8') as f:
            text = f.read()

        text = text.replace('id = ""', f'id = "{id_value}"')
        text = text.replace('password = ""', f'password = "{password_value}"')
        text = text.replace('ime = ""', f'ime = "{ime_value}"')
        text = text.replace('max = ""', f'max = "{max_vvalue}"')

        with open(new_file_path, 'w', encoding='UTF-8') as f:
            f.write(text)

        tk.messagebox.showinfo("成功", "转换完成")


if __name__ == '__main__':
    root = tk.Tk()
    app = ReplaceApp(root)
    root.mainloop()
