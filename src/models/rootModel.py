class RootModel:

    def __init__(self):
        pass

    def isNumValid(self, num, min, max):
        if num < min or num > max:
            return False
        else:
            return True
