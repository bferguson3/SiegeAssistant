from src.models import rootModel, basicInfo


class CharData(rootModel.RootModel):

    def __init__(self):
        self.basicInfo = basicInfo.BasicInfo("Unknown Player","Unknown Character", 0)
