class DayOptions:
    def __init__(self, setDate):
        self.date = setDate
        self.morningOptionsList = []
        self.noonOptionsList = []
        self.nightOptionsList = []

    @property
    def getDate(self):
        return self.date

    @property
    def getMorningOptionsList(self):
        return self.morningOptionsList

    @property
    def getNoonOptionsList(self):
        return self.noonOptionsList

    @property
    def getNightOptionsList(self):
        return self.nightOptionsList

    def addToMorningOptionsList(self, name):
        self.morningOptionsList.append(name)

    def addToNoonOptionsList(self, name):
        self.noonOptionsList.append(name)

    def addToNightOptionsList(self, name):
        self.nightOptionsList.append(name)
