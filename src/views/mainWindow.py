from src.views import rootView, basicInfoFrame
from src.models import charData
import tkinter as tk
import tkinter.ttk as ttk
# import urllib.parse
import os
from tkinter import messagebox, filedialog
import xml.dom.minidom as md
import datetime
import pkgutil
import res


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

        # import the language
        try:
            langbin = pkgutil.get_data('res', 'language.xml')
            lang_xml = langbin.decode('UTF-8', 'ignore')

            currentlanguage = "english"  # we'll eventually read this from an options file

            dom = md.parseString(lang_xml)
            root = dom.getElementsByTagName('language')

            language_failure = True
            count = 0
            for element in root:
                if element.hasAttribute('name'):
                    if element.getAttribute('name') == currentlanguage and count < 1:
                        language_failure = False
                        self.readLangFromXML(element)

            if language_failure:
                messagebox.showerror("Oops",
                                     "Unable to parse language file." + os.linesep + "Program may not work correctly.")
                self.langBackupPlan()

        except Exception as e:
            messagebox.showerror("Oops",
                                 "Unable to load language file." + os.linesep + "Program may not work correctly.")
            print(e)
            self.langBackupPlan()

        # setup the menu bar
        __menubar = tk.Menu(self.__root)
        __filemenu = tk.Menu(__menubar, tearoff=0)

        # start the file cascade
        menubar_dict = self.language_dict['mainwindow']['menubar']
        __filemenu.add_command(label=menubar_dict['new'], command=self.newCharacter)
        __filemenu.add_command(label=menubar_dict['open'], command=self.openCharacter)
        __filemenu.add_command(label=menubar_dict['save'], command=self.saveCharacter)
        __filemenu.add_command(label=menubar_dict['saveas'], command=self.saveAsCharacter)
        __filemenu.add_separator()
        __filemenu.add_command(label=menubar_dict['vpdf'], command=self.doNothing, state='disabled')
        __filemenu.add_command(label=menubar_dict['epdf'], command=self.doNothing, state='disabled')
        __filemenu.add_command(label=menubar_dict['etxt'], command=self.exportAsTXT)
        __filemenu.add_separator()
        __filemenu.add_command(label=menubar_dict['exit'], command=self.__windowDeleteCallback)

        __menubar.add_cascade(label=menubar_dict['file'], menu=__filemenu)

        self.__root.config(menu=__menubar)

        # make the base frame
        __frame = ttk.Frame(self.__root)
        __frame.master.title(self.language_dict['mainwindow']['mainwindow_phrases']['windowtitle'])

        # start the tabs
        __nb = ttk.Notebook(__frame)

        __fBasic = ttk.Frame(__nb)

        self.basicInfoFrame = basicInfoFrame.BasicInfoFrame(__fBasic, self.charData, self.language_dict)

        __nb.add(__fBasic, text=self.language_dict['mainwindow']['mainwindow_phrases']['basicinfotitle'])

        __fAttrib = ttk.Frame(__nb)
        # stuff here
        __nb.add(__fAttrib, text=self.language_dict['mainwindow']['mainwindow_phrases']['attributestitle'])

        # pack that stuff or it won't appear.
        __nb.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
        __nb.pack(fill=tk.BOTH, expand=1)
        __frame.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
        __frame.pack(fill=tk.BOTH, expand=1)

        # final stuff
        rootView.RootView.dataChanged = False

    def doYouWantToSave(self):
        response = messagebox.askyesnocancel(title=self.language_dict['mainwindow']['messageboxes']['doyouwanttosave_title'],
                                             message=self.language_dict['mainwindow']['messageboxes']['doyouwanttosave_message'])
        if response:
            if self.saveCharacter():
                return True  # save worked, move on.
            else:
                return False  # save failed, don't delete the data
        elif response is None:
            return False  # calcel the operation
        else:
            return True  # they don't want to save, but go ahead and do whatever

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
                                                title=self.language_dict['mainwindow']['messageboxes']['saveas_title'],
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
        if filePath is not None:
            try:
                imp = md.getDOMImplementation()
                doc = imp.createDocument(None, "Siege_Character", None)
                root = doc.documentElement
                ele = doc.createElement('Basic_Info')
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
        response = filedialog.askopenfilename(parent=self.__root,
                                              initialdir=self.useThisSaveDirectory,
                                              title="Open...",
                                              defaultextension='sec',
                                              filetypes=(("Siege Engine Characters", "*.sec"), ("all files", "*.*")))
        if response:
            try:
                self.newCharacterStuff()  # just to clear everything out
                f = open(response, 'rb')
                dom = md.parse(f)
                bi = dom.getElementsByTagName('Basic_Info')[0]
                self.basicInfoFrame.loadFromXML(bi)
                f.close()

                # end with
                self.hasCharFileName = True
                self.useThisSaveDirectory, self.charFileName = os.path.split(response)
                self.updateAll()
                rootView.RootView.dataChanged = False

            except Exception as e:
                messagebox.showerror("Oops", "Unable to open file at: " + response)
                print(e)

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

    def exportAsTXT(self):
        useThisName = ''
        if self.hasCharFileName:
            useThisName = self.charFileName
        else:
            useThisName = self.makeFileNameSafe(self.charData[0].basicInfo.cname)
        response = filedialog.asksaveasfilename(parent=self.__root, initialfile=useThisName,
                                                initialdir=self.useThisSaveDirectory,
                                                title="Export As...",
                                                defaultextension='txt',
                                                filetypes=(("Text File", "*.txt"), ("all files", "*.*")))
        try:
            if response is not None:
                endl = os.linesep
                f = open(response, 'wt')
                f.write("Temporary Siege Engine Character sheet" + endl)
                f.write(endl)
                f.write(
                    "Because the program is still under development, this admittedly ugly text-only sheet will have to do for now." + endl)
                f.write(endl)
                self.basicInfoFrame.exportToTxt(f, endl)
                f.write(endl)
                # print("This report was generated on "+ datetime.date.strftime('%A %b, %m')+" at "+datetime.time.strftime()+endl)
                t = datetime.datetime.now()
                print("This report was generated on " + t.strftime('%A, %d %m at %I:%M %p') + endl)

                f.close()
        except Exception as e:
            messagebox.showerror("Oops", "Unable to export txt file at: " + response)
            print(e)

    def __windowDeleteCallback(self):
        if rootView.RootView.dataChanged:
            response = self.doYouWantToSave()
            if response:  # remember, true means either the save worked, or they didn't want to save
                self.__root.destroy()
        else:
            self.__root.destroy()

    def readLangFromXML(self, root):
        masterlist = ('mainwindow','basic_info')
        headlist = ('menubar','mainwindow_phrases', 'error_phrases','messageboxes')
        self.language_dict = {}
        for my_window_list in masterlist:
            w_list = {}
            for header in headlist:
                elelist = root.getElementsByTagName(header)[0]
                q_list = elelist.getElementsByTagName('phrase')
                q_dict = {}
                for phrase in q_list:
                    t1 = phrase.getAttribute('item')
                    t2 = phrase.childNodes[0].data
                    q_dict.update({t1: t2})

                w_list.update({header:q_dict})
            self.language_dict.update({my_window_list:w_list})

    def langBackupPlan(self):
        menubar_dict = {'file':'File','new': 'New Character', 'open': 'Open...', 'save': 'Save', 'saveas': 'Save As...',
                        'vpdf': 'View as PDF', 'epdf': 'Export as PDF', 'etxt': 'Export as TXT', 'exit': 'Exit'}
        mainwindow_dict = {'windowtitle':'Siege Assistant'}
        error_dict = {'error_title':"Oops...",'save_file_error':'Unable to save file at: '}
        window_dict = {'menubar': menubar_dict,'mainwindow_phrases':mainwindow_dict, 'error_phrases':error_dict}
        self.language_dict = {'mainwindow':window_dict}
