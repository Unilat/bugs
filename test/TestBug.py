'''
Created on Dec 15, 2011

@author: Calvin
'''

if __name__ == '__main__':
    
    from Bug import Bug
    import Grid
    import Debug
    import time
    import random
    
    Debug.ON = False
    
    codeFiles = ["../MoveForward.bo", "../BackAndForth.bo", "../TurnRightFriend.bo", "../Infect.bo", "../DecentBug.bo"]
    codes = []

    for i in range(len(codeFiles)):
        f = open(codeFiles[i], "rb")
        codes.append([])
        b = f.read(1)
        while b != "":
            codes[i].append(ord(b))
            b = f.read(1)

    bug = []
    taken = []
    
    def populate(codeNum, teams):
        for j in range(1, teams + 1):
            for i in range(10):
                x = random.randint(0,19)
                y = random.randint(0,19)
                while [x,y] in taken:
                    x = random.randint(0,19)
                    y = random.randint(0,19)
                    
                bug.append(Bug(codes[codeNum], [x,y], random.randint(0,3), j))
    
    populate(4, 3)
    Grid.display()
    while 1:
        for b in bug:
            b.execute()
        print "\n" * 25
        Grid.display()
        time.sleep(.1)
