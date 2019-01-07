from src.views import rootView, basicInfoFrame
from src.models import charData
import tkinter as tk
import tkinter.ttk as ttk
import urllib.parse
import os
from tkinter import messagebox, filedialog
import xml.dom.minidom as md


class MainWindow(rootView.RootView):

    def __init__(self, tkroot):
        self.__root = tkroot
        self.__root.protocol("WM_DELETE_WINDOW", self.__windowDeleteCallback)
        style = ttk.Style()
        # print(style.theme_names())
        style.theme_use(themename='clam')

        # init data
        self.charData = [charData.CharData()]
        rootView.RootView.dataChanged = False
        self.hasCharFileName = False
        self.charFileName = ''

        self.workingDirectory = os.getcwd()
        # fp = tempfile.TemporaryFile()
        # I might need the tempfile later
        tmpPath = os.path.expanduser('~')
        tmpPathAddMe = 'SiegeAssistant'
        tmpPathSg = os.path.normpath(tmpPath + '/' + tmpPathAddMe)

        if os.path.exists(tmpPath):
            if os.path.exists(tmpPathSg):
                self.useThisSaveDirectory = tmpPathSg
            else:
                try:
                    os.mkdir(tmpPathSg, 0o755)
                    self.useThisSaveDirectory = tmpPathSg
                except:
                    messagebox.showerror("Oops", "Unable to create path: " + tmpPathSg)
                    self.useThisSaveDirectory = ''
        else:
            messagebox.showerror("Oops", "Unable to use path: " + tmpPathSg)
            self.useThisSaveDirectory = ''

        # print(os.path.expanduser('~'))
        # print(os.getcwd())

        # setup the menu bar
        __menubar = tk.Menu(self.__root)
        __filemenu = tk.Menu(__menubar, tearoff=0)

        # start the file cascade
        __filemenu.add_command(label="New", command=self.newCharacter)
        __filemenu.add_command(label="Open...", command=self.openCharacter)
        __filemenu.add_command(label="Save", command=self.saveCharacter)
        __filemenu.add_command(label="Save As...", command=self.saveAsCharacter)
        __filemenu.add_separator()
        __filemenu.add_command(label="Exit", command=self.__windowDeleteCallback)

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

        # final stuff
        rootView.RootView.dataChanged = False

    def doYouWantToSave(self):
        response = messagebox.askyesnocancel(title="Save Character?",
                                             message="Do you want to save the existing character?")
        if response:
            if self.saveCharacter():
                return True  # save worked, move on.
            else:
                return False  # save failed, don't delete the data
        elif response is None:
            return False  # meaning don't create a new character or open a character
        else:
            return True  # they don't want to save, but go ahead and make or load a new character

    def saveAsCharacter(self):
        useThisName = ''
        if self.hasCharFileName:
            useThisName = self.charFileName
        else:
            useThisName = self.makeFileNameSafe(self.charData[0].basicInfo.cname)
            # useThisName = self.charData[0].basicInfo.cname

            # useThisName = urllib.parse.quote(useThisName)

        response = filedialog.asksaveasfilename(parent=self.__root, initialfile=useThisName,
                                                initialdir=self.useThisSaveDirectory,
                                                title="Save As...",
                                                defaultextension='sec',
                                                filetypes=(("Siege Engine Characters", "*.sec"), ("all files", "*.*")))
        return self.saveCharacterStuff(response)

    def saveCharacter(self):
        if self.hasCharFileName:
            useThisName = self.charFileName
            checkpath = os.path.normpath(self.useThisSaveDirectory + '/' + useThisName)
            if os.path.exists(checkpath):
                return self.saveCharacterStuff(checkpath)
            else:
                return self.saveAsCharacter()
        else:
            return self.saveAsCharacter()

    def saveCharacterStuff(self, filePath):
        try:
            imp = md.getDOMImplementation()
            doc = imp.createDocument(None, "Siege Character", None)
            root = doc.documentElement
            ele = doc.createElement('Basic Info')
            self.basicInfoFrame.saveToXML(doc, ele)
            root.appendChild(ele)

            f = open(filePath, 'wb')
            f.write(doc.toprettyxml(indent='  ', encoding='utf-8'))
            f.close()

            # end with
            self.hasCharFileName = True
            self.useThisSaveDirectory, self.charFileName = os.path.split(filePath)
            rootView.RootView.dataChanged = False
            return True

        except Exception as e:
            messagebox.showerror("Oops", "Unable to save file at: " + filePath)
            print(e)
            return False

    def newCharacterStuff(self):
        self.charData[0] = charData.CharData()
        self.updateAll()

        # final stuff
        self.hasCharFileName = False
        rootView.RootView.dataChanged = False

    def newCharacter(self):
        if rootView.RootView.dataChanged:
            if self.doYouWantToSave():
                self.newCharacterStuff()
            else:
                pass
        else:
            self.newCharacterStuff()

    def openCharacterStuff(self):
        pass

    def openCharacter(self):
        if rootView.RootView.dataChanged:
            if self.doYouWantToSave():
                self.openCharacterStuff()
            else:
                pass
        else:
            self.openCharacterStuff()

    def updateAll(self):
        self.basicInfoFrame.updateAll()

    def doNothing(self):
        pass

    def __windowDeleteCallback(self):
        self.__root.destroy()  # if messagebox.askokcancel("Quit", "Do you really wish to quit?"):
        # self.__root.destroy()
        # Yea, we need to do more here.
        # alot more
