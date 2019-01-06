from src.models import rootModel


class BasicInfo(rootModel.RootModel):

    def __init__(self, pname, cname, xp):
        self.pname = pname
        self.cname = cname
        self.setXP(xp)

    def setXP(self, xp):
        if self.isNumValid(xp, 0, 999999999):
            self.__xp = xp
        else:
            self.__xp = 0

    def getXP(self):
        return self.__xp
