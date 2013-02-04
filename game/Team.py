'''
Created on Dec 18, 2011

@author: Calvin
'''

class Team(object):
    '''
    Represents one team of bugs
    '''

    totalBugs = 0

    def __init__(self, teamId, numBugs, bugCode):
        '''
        Constructor
        '''
        self.numBugs = numBugs
        self.maxBugs = numBugs
        self.minBugs = numBugs
        self.bugCode = bugCode
        self.id = teamId
        Team.totalBugs += numBugs
        
    def percent(self):
        return float(self.numBugs) / float(Team.totalBugs)
    
    def inc(self):
        self.numBugs += 1
        if self.numBugs > self.maxBugs:
            self.maxBugs = self.numBugs
        
    def dec(self):
        self.numBugs -= 1
        if self.numBugs < self.minBugs:
            self.minBugs = self.numBugs