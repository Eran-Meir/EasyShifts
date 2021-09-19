# This class represents a DayOptions Object.
# This will be used to store data and easily assemble the work arrangement
# It holds the attributes:
# - date
# - Morning, Noon and Night Sets which contain available workers for that same date and shifts

class DayOptions:
    def __init__(self, setDate):
        self.date = setDate
        self.morningOptionsSet = set()
        self.noonOptionsSet = set()
        self.nightOptionsSet = set()

    # return the object's date
    def getDate(self):
        return self.date

    # return the object's morning options set
    def getMorningOptionsSet(self):
        return self.morningOptionsSet

    # return the object's noon options set
    def getNoonOptionsSet(self):
        return self.noonOptionsSet

    # return the object's night options set
    def getNightOptionsSet(self):
        return self.nightOptionsSet

    # updates the morning options list with param 'name'
    def addToMorningOptionsSet(self, name):
        self.morningOptionsSet.update(name)

    # updates the noon options list with param 'name'
    def addToNoonOptionsSet(self, name):
        self.noonOptionsSet.update(name)

    # updates the night options list with param 'name'
    def addToNightOptionsSet(self, name):
        self.nightOptionsSet.update(name)

    # clears empty string '' from our sets
    def clearNullStringFromSets(self):
        emptyString = ''
        self.morningOptionsSet.discard(emptyString)
        self.noonOptionsSet.discard(emptyString)
        self.nightOptionsSet.discard(emptyString)

    # If the worker was assigned to one shift then remove him from the other options
    def removeWorkerFromDayIfAssigned(self, name):
        self.morningOptionsSet.discard(name)
        self.noonOptionsSet.discard(name)
        self.nightOptionsSet.discard(name)