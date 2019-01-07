from src.views import rootView
from tkinter import ttk
import tkinter as tk


class BasicInfoFrame(rootView.RootView):

    def __init__(self, frame, charData):
        self.charData = charData
        self.__frame = frame

        ttk.Label(self.__frame, text="Player Name").grid(row=0, column=0)
        self.pname = tk.StringVar()
        self.pname.trace_add("write", self.pnameChanged)
        ttk.Entry(self.__frame, width=30, textvariable=self.pname).grid(row=0, column=1)

        ttk.Label(self.__frame, text="Character Name").grid(row=1, column=0)
        self.cname = tk.StringVar()
        self.cname.trace_add("write", self.cnameChanged)
        ttk.Entry(self.__frame, width=30, textvariable=self.cname).grid(row=1, column=1)

        # game

        # experience points

        # add update values
        self.updateAll()

        # pack it in at the end
        self.__frame.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
        self.__frame.pack(fill=tk.BOTH, expand=1)

    def pnameChanged(self, *args):
        self.charData[0].basicInfo.pname = self.pname.get()
        rootView.RootView.dataChanged = True

    def cnameChanged(self, *args):
        self.charData[0].basicInfo.cname = self.cname.get()
        rootView.RootView.dataChanged = True

    def updateAll(self):
        self.pname.set(self.charData[0].basicInfo.pname)
        self.cname.set(self.charData[0].basicInfo.cname)
