
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

class State:

    def run(self):
        raise NotImplementedError

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

class TransitionGenerator:

    def __init__(self, conditionGenerator = ConditionGenerator(), transitionList = None):
        self.mConditionGenerator = conditionGenerator
        if transitionList is None:
            self.mTransitionList = []
        else:
            self.mTransitionList = transitionList
        self.mGeneratedTransitions = []

    def addTransition(self, transition):
        self.mTransitionList.append(transition)

    def run(self):
        self.mGeneratedTransitions.clear()
        currentConditions = self.mConditionGenerator.run()
        for trn in self.mTransitionList:
            appendNeeded = True
            for name in trn.getConditions():
                if not name in currentConditions:
                    appendNeeded = False
                    break
            if appendNeeded:
                self.mGeneratedTransitions.append(trn)
        return self.mGeneratedTransitions


class StateMachine:

    def __init__(self, initalState = 'initial', transitionGenerator = TransitionGenerator()):
        self.mStates = {}
        self.mTransitionGenerator = transitionGenerator
        self.mCurrentState = initalState

    def addState(self, name, state):
        self.mStates[name] = state

    def run(self):
        #it seems that this is a weird beahaviour but this is done reasonly
        availibleTransitions = sorted(list(filter(lambda trn: trn.getStart() == self.mCurrentState, self.mTransitionGenerator.run())),
                                      key=lambda trn: len(trn.getConditions()), reversed=True)
        if len(availibleTransitions) > 0:
            self.mCurrentState = availibleTransitions[0].getFinish()

        self.mStates[self.mCurrentState].run()

