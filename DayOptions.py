class DayOptions:
    def __init__(self, setDate):
        self.date = setDate
        self.morningOptionsSet = set()
        self.noonOptionsSet = set()
        self.nightOptionsSet = set()

    @property
    def getDate(self):
        return self.date

    @property
    def getMorningOptionsList(self):
        return self.morningOptionsSet

    @property
    def getNoonOptionsList(self):
        return self.noonOptionsSet

    @property
    def getNightOptionsList(self):
        return self.nightOptionsSet

    def addToMorningOptionsList(self, name):
        self.morningOptionsSet.update(name)

    def addToNoonOptionsList(self, name):
        self.noonOptionsSet.update(name)

    def addToNightOptionsList(self, name):
        self.nightOptionsSet.update(name)

    def clearNullStringFromSets(self):
        emptyString = ''
        self.morningOptionsSet.discard(emptyString)
        self.noonOptionsSet.discard(emptyString)
        self.nightOptionsSet.discard(emptyString)