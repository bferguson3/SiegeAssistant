class RootView:

    #static variable
    dataChanged = False

    def __init__(self):
        pass

    def makeFileNameSafe(self,s):
        for c in r'[]/\;,><&*:%=+@!#^()|?^':
            s = s.replace(c, '')
        s = s.strip()
        return s
