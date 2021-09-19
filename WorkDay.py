# This class represents a WorkDay Object.
# This will be used to store data of a complete work day
# It holds the attributes:
# - date
# - Morning, Noon and Night workers in the relevant shifts

class WorkDay:
    def __init__(self, setDate):
        self.date = setDate
        self.morningWorker = ""
        self.noonWorker = ""
        self.nightWorker = ""

    # return the object's date
    def getDate(self):
        return self.date

    # return the object's morning shift worker
    def getMorningWorker(self):
        return self.morningWorker

    # set the object's morning shift worker
    def setMorningWorker(self, name):
        if name is not None:
            self.morningWorker = name
        else:
            print("ERROR: Couldn't set Morning shift worker on date: " + self.date)

    # return the object's noon shift worker
    def getNoonWorker(self):
        return self.noonWorker

    # set the object's morning shift worker
    def setNoonWorker(self, name):
        if name is not None:
            self.noonWorker = name
        else:
            print("ERROR: Couldn't set Noon shift worker on date: " + self.date)

    # return the object's noon shift worker
    def getNightWorker(self):
        return self.nightWorker

    # set the object's morning shift worker
    def setNightWorker(self, name):
        if name is not None:
            self.nightWorker = name
        else:
            print("ERROR: Couldn't set Night shift worker on date: " + self.date)

    # Return the write data in a list of lists format for data writing
    def getWriteData(self):
        morWorker = ""
        nooWorker = ""
        nighWorker = ""
        if self.morningWorker != "":
            morWorker = self.morningWorker
        if self.noonWorker != "":
            nooWorker = self.noonWorker
        if self.nightWorker != "":
            nighWorker = self.nightWorker
        return [
            [morWorker],
            [nooWorker],
            [nighWorker]
        ]