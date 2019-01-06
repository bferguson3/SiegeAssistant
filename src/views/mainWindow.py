from src.views import rootView, basicInfoFrame
from src.models import charData
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox


class MainWindow(rootView.RootView):

    def __init__(self, tkroot):
        self.__root = tkroot
        self.__root.protocol("WM_DELETE_WINDOW", self.__windowDeleteCallback)
        style = ttk.Style()
        print(style.theme_names())
        style.theme_use(themename='clam')

        # init data
        self.charData = [charData.CharData()]
        rootView.RootView.dataChanged = False

        # setup the menu bar
        __menubar = tk.Menu(self.__root)
        __filemenu = tk.Menu(__menubar, tearoff=0)

        # start the file cascade
        __filemenu.add_command(label="New", command=self.newCharacter)
        __filemenu.add_command(label="Open...", command=self.doNothing)
        __filemenu.add_command(label="Save", command=self.doNothing)
        __filemenu.add_command(label="Save As...", command=self.doNothing)
        __filemenu.add_separator()
        __filemenu.add_command(label="Exit", command=self.doNothing)

        __menubar.add_cascade(label="File", menu=__filemenu)

        self.__root.config(menu=__menubar)

        # make the base frame
        __frame = ttk.Frame(self.__root)
        __frame.master.title('Siege Assistant')

        # start the tabs
        __nb = ttk.Notebook(__frame)

        __fBasic = ttk.Frame(__nb)

        self.basicInfoFrame = basicInfoFrame.BasicInfoFrame(__fBasic, self.charData)

        __nb.add(__fBasic, text="Basic Info")

        __fAttrib = ttk.Frame(__nb)
        # stuff here
        __nb.add(__fAttrib, text="Attributes")

        # pack that stuff or it won't appear.
        __nb.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
        __nb.pack(fill=tk.BOTH, expand=1)
        __frame.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
        __frame.pack(fill=tk.BOTH, expand=1)

    def doYouWantToSave(self):
        pass

    def newCharacter(self):
        if rootView.RootView.dataChanged:
            self.doYouWantToSave()
        self.charData[0] = charData.CharData()
        self.updateAll()

    def updateAll(self):
        self.basicInfoFrame.updateAll()
    def doNothing(self):
        pass

    def __windowDeleteCallback(self):
        self.__root.destroy()  # if messagebox.askokcancel("Quit", "Do you really wish to quit?"):
        # self.__root.destroy()
        # Yea, we need to do more here.
        # alot more
