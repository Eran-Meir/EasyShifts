# This class represents a WorkDay Object.
# This will be used to store data of a complete work day
# It holds the attributes:
# - date
# - Morning, Noon and Night workers in the relevant shifts

class WorkDay:
    def __init__(self, setDate):
        self.date = setDate
        self.morningWorker = ''
        self.noonWorker = ''
        self.nightWorker = ''

# return the object's date
    def getDate(self):
        return self.date

# return the object's morning shift worker
    def getMorningWorker(self):
        return self.morningWorker

# return the object's noon shift worker
    def getNoonWorker(self):
        return self.noonWorker

# return the object's noon shift worker
    def getNightWorker(self):
        return self.nightWorker