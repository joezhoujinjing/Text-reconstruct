import shell
import util
import wordsegUtil

############################################################
# The segmentation problem under a unigram model

class SegmentationProblem(util.SearchProblem):
    def __init__(self, query, unigramCost):
        self.query = query
        self.unigramCost = unigramCost

    def startState(self):
        # -------------------------------------------------------------------------
        return 0
        # -------------------------------------------------------------------------

    def isGoal(self, state):
        # -------------------------------------------------------------------------
        return state==len(self.query)
        # -------------------------------------------------------------------------

    def succAndCost(self, state):
        # -------------------------------------------------------------------------
        result =[]
        for index in range(state+1,len(self.query)+1):
            cost=self.unigramCost(self.query[state:index])
            succ=index
            action=self.query[state:index]
            result.append((action,succ,cost))
        return result
        # -------------------------------------------------------------------------

def segmentWords(query, unigramCost):
    if len(query) == 0:
        return ''
    ucs = util.UniformCostSearch(verbose=0)
    ucs.solve(SegmentationProblem(query, unigramCost))

    # -------------------------------------------------------------------------
    result=" ".join(ucs.actions)
    return result
    # -------------------------------------------------------------------------

############################################################
# The vowel insertion problem under a bigram cost

class VowelInsertionProblem(util.SearchProblem):
    def __init__(self, queryWords, bigramCost, possibleFills):
        self.queryWords = queryWords
        self.bigramCost = bigramCost
        self.possibleFills = possibleFills

    def startState(self):
        # -------------------------------------------------------------------------
        return ("-BEGIN-",0)
        # -------------------------------------------------------------------------

    def isGoal(self, state):
        # -------------------------------------------------------------------------
        return state[1]==len(self.queryWords)
        # -------------------------------------------------------------------------

    def succAndCost(self, state):
        # -------------------------------------------------------------------------
        result=[]
        rear=self.possibleFills(self.queryWords[state[1]])
        if len(rear)==0:
            rear=set([self.queryWords[state[1]]])
        for w2 in rear:
            cost=self.bigramCost(state[0],w2)
            result.append((w2,(w2,state[1]+1),cost))
        return result
        # -------------------------------------------------------------------------

def insertVowels(queryWords, bigramCost, possibleFills):
    # -------------------------------------------------------------------------
    ucs = util.UniformCostSearch(verbose=0)
    ucs.solve(VowelInsertionProblem(queryWords, bigramCost,possibleFills))
    result=" ".join(ucs.actions)
    return result
    # -------------------------------------------------------------------------

############################################################
# Problem 3b: Solve the joint segmentation-and-insertion problem

class JointSegmentationInsertionProblem(util.SearchProblem):
    def __init__(self, query, bigramCost, possibleFills):
        self.query = query
        self.bigramCost = bigramCost
        self.possibleFills = possibleFills

    def startState(self):
        # -------------------------------------------------------------------------
        return ("-BEGIN-",0)
        # -------------------------------------------------------------------------

    def isGoal(self, state):
        # -------------------------------------------------------------------------
        return state[1]==len(self.query)
        # -------------------------------------------------------------------------

    def succAndCost(self, state):
        # -------------------------------------------------------------------------
        result =[]
        N=len(self.query)
        for index in range(state[1]+1,len(self.query)+1):
            rear=self.possibleFills(self.query[state[1]:index])
            for w2 in rear:
                cost=self.bigramCost(state[0],w2)
                result.append((w2,(w2,index),cost))
        return result
        # -------------------------------------------------------------------------

def segmentAndInsert(query, bigramCost, possibleFills):
    if len(query) == 0:
        return ''
    # -------------------------------------------------------------------------
    ucs = util.UniformCostSearch(verbose=0)
    ucs.solve(JointSegmentationInsertionProblem(query, bigramCost,possibleFills))
    result=" ".join(ucs.actions)
    return result
    # -------------------------------------------------------------------------

############################################################
if __name__ == '__main__':
    shell.main()