
class DataHolder:

    def __init__(self, dict = None):
        self.mDataDict = {}
        if dict is not None:
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
        self.mDataConditions = {}
        if dict is not None:
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
        self.mConditionsList = []
        if conditionsList is not None:
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
            for name, value in cnd.getDataConditions().items():
                if value  != self.mDataHolder.getData(name):
                    appendNeeded = False
                    break
            if appendNeeded:
                self.mGeneratedConditionsList.append(cnd.getName())
        return self.mGeneratedConditionsList

class TransitionGenerator:

    def __init__(self, conditionGenerator = ConditionGenerator(), transitionList = None):
        self.mConditionGenerator = conditionGenerator
        self.mTransitionList = []
        if transitionList is not None:
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

    def __init__(self, initalState = 'init', transitionGenerator = TransitionGenerator()):
        self.mStates = {}
        self.mTransitionGenerator = transitionGenerator
        self.mCurrentState = initalState

    def addState(self, name, state):
        self.mStates[name] = state

    def run(self):
        #it seems that this is a weird beahaviour but this is done reasonly
        availibleTransitions = sorted(list(filter(lambda trn: trn.getStart() == self.mCurrentState, self.mTransitionGenerator.run())),
                                      key=lambda trn: len(trn.getConditions()), reverse=True)
        if len(availibleTransitions) > 0:
            self.mCurrentState = availibleTransitions[0].getFinish()

        self.mStates[self.mCurrentState].run()


#Famework ends here
###############################################################################
###############################################################################
#Testing now

import random

class WorldPerceptor(DataHolder):

    def __init__(self, dict = None):
        dict = {}
        dict['x'] = 0
        dict['y'] = 0
        dict['z'] = 0

        self.mUpdate = ['x', 'y', 'z']

        super().__init__(dict)

    def updateData(self):
        r = random.randrange(4)
        for i in range(len(self.mUpdate)):
            if i != r:
                self.mDataDict[self.mUpdate[i]] = 0
            else:
                self.mDataDict[self.mUpdate[i]] = 5
        print(self.mDataDict)

wP = WorldPerceptor()

cndList = [Condition("x_is_up", dict={"x": 5}), Condition("y_is_up", dict={"y": 5}), Condition("z_is_up", dict={"z": 5})]
trnList = [Transition("init", "xrun", conditions=["x_is_up"]), Transition("init", "yrun", conditions=["y_is_up"]), Transition("init", "zrun", conditions=["z_is_up"]),
           Transition("xrun", "zrun", conditions=["z_is_up"]), Transition("xrun", "yrun", conditions=["y_is_up"]),
           Transition("zrun", "xrun", conditions=["x_is_up"]), Transition("zrun", "yrun", conditions=["y_is_up"]),
           Transition("yrun", "zrun", conditions=["z_is_up"]), Transition("yrun", "xrun", conditions=["x_is_up"])]

class Init(State):
    def run(self):
        print('Init is active')

class YRun(State):
    def run(self):
        print('Y is active')

class XRun(State):
    def run(self):
        print('X is active')

class ZRun(State):
    def run(self):
        print('Z is active')

cG = ConditionGenerator(wP, cndList)
tG = TransitionGenerator(conditionGenerator=cG, transitionList=trnList)

sM = StateMachine(transitionGenerator=tG)
sM.addState('init', state=Init())
sM.addState('xrun', state=XRun())
sM.addState('yrun', state=YRun())
sM.addState('zrun', state=ZRun())


for i in range(10):
    sM.run()







