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

    def getTextFromChildNodes(self, list):
        t = ''
        for nd in list:
            if nd.nodeType == nd.TEXT_Node:
                t = t + nd.data
        return t

