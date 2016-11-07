
class DataHolder:

    def __init__(self, dict = None):
        if dict is None:
            self.mDataDict = {}
        else:
            self.mDataDict.update(dict)

    def setData(self, key, value):
        self.mDataDict[key] = value

    def getData(self, key):
        return self.mDataDict.get(key, None)

    def updateData(self):
        raise NotImplementedError

class Condition:

    def __init__(self, name, dict = None):
        self.mName = name
        if dict is None:
            self.mDataConditions = {}
        else:
            self.mDataConditions.update(dict)

    def setName(self, name):
        self.mName = name

    def getName(self):
        return self.mName

    def getDataConditions(self):
        return self.mDataConditions

    def setDataConditions(self, dict):
        self.mDataConditions.update(dict)

class Transition:

    def __init__(self, start, finish, conditions = None):
        self.mStart = start
        self.mFinish = finish
        if conditions is None:
            self.mConditions = []
        else:
            self.mConditions = conditions

    def getStart(self):
        return self.mStart

    def getFinish(self):
        return self.mFinish

    def getConditions(self):
        return self.mConditions

class ConditionGenerator:

    def __init__(self, dataHolder = DataHolder(), conditionsList = None):
        self.mDataHolder = dataHolder
        if conditionsList is None:
            self.mConditionsList = []
        else:
            self.mConditionsList = conditionsList
        self.mGeneratedConditionsList = []

    def setDataHolder(self, dataHolder):
        self.mDataHolder = dataHolder

    def setComditionsList(self, conditionsList):
        self.mConditionsList = conditionsList

    def addCondition(self, condition):
        self.mConditionsList.append(condition)

    def run(self):
        self.mDataHolder.updateData()
        self.mGeneratedConditionsList.clear()
        for cnd in self.mConditionsList:
            appendNeeded = True
            for name, value in cnd.getDataConditions():
                if value  != self.mDataHolder.getData(name):
                    appendNeeded = False
                    break
            if appendNeeded:
                self.mGeneratedConditionsList.append(cnd.getName())
        return self.mGeneratedConditionsList

