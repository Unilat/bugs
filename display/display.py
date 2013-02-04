'''
Created: Novemeber 5, 2001

@Author: Paul Schwendenman
'''
# * * * * * * *
# * Imported  *
# * * * * * * *
from Tkinter import *
from listcomp import change
import Sockets
from handleError import *
import time
import Grid
from Bug import Bug
from random import randint
import Debug
from Team import Team

# * * * * * * * *
# * Image Path  *
# * * * * * * * *
PATH = "images/"

MAXTEAMS = 3

# * * * * * * * *
# * Teams       *
# * * * * * * * *
teams = []
codes = []

colors =  ["#ff8000","#000cff","#1eff00"]
borders = ["#934c00","#000b75","#008209"]

# * * * * * * * *
# * Display     *
# * * * * * * * *
class Display():
    
    '''
    The GUI Display class.
    '''
    def __init__(self, root):
        
        self.root = root
        
        # List of references to bug objects
        self.buglist = []
        
        # List of references to drawn images on the canvas
        self.bugimages = []
        
        # Dictionary of Image objects to draw to the canvas
        self.bugdict = {}
        # Fill the image dictionary
        self.createImages()
        
        # Key bindings
        root.bind('<space>', self.Pass)
        root.bind('<Return>', self.Pass)
        root.bind('q', self.quitfunc)
        
        # Set up the window layout
        self.canvas = Canvas(self.root, width=600, height=408)
        self.canvas.create_rectangle(2,2,406,406,fill="white",outline="#ddd")
        self.canvas.pack(side=TOP)
        
        # Buttons
        self.buttons = []
        self.buttons.append(PhotoImage(file=PATH + "ui/startButton.gif"))
        self.buttons.append(PhotoImage(file=PATH + "ui/startButtonHover.gif"))
        self.startButton = self.canvas.create_image(412, 373, image=self.buttons[0], activeimage=self.buttons[1], anchor=NW)
        
        # Empty lists of dynamically generated widgets
        self.teamLabels = []
        self.teamGraphs = []
        self.teamMaxLabels = []
        self.teamMinLabels = []
        self.teamCurrentLabels = []
        
    def createImages(self):
        '''
        Makes a dictionary of the bugs images
        '''
        for team in range(1, MAXTEAMS+1):
            for direction in range(4):
                # directions
                self.bugdict["bug" + str(10*team + direction)] = PhotoImage(file= PATH + "bug" + str(team) + str(direction) + ".gif")
 
    def populate(self):
        '''
        Creates the bug objects and corresponding canvas graphics.
        '''
        
        for team in range(len(teams)):
            for i in range(teams[team].numBugs):
                x = randint(0,19)
                y = randint(0,19)
                while Grid.get_pos([x,y]) != Grid.states.EMPTY:
                    x = randint(0,19)
                    y = randint(0,19)
                    
                bug = Bug([x,y], randint(0,3), teams[team])
                self.buglist.append(bug)
                self.bugimages.append(self.canvas.create_image(bug._pos[0]*20+14,bug._pos[1]*20+14, \
                                                           image=self.bugdict["bug"+str(team+1)+str(bug._direction)]))
                
            # Set up graphics for bug statistics in the right panel
            self.canvas.create_rectangle(415, team * 70 + 2, 595, team * 70 + 64, \
                                         fill="#fafafa", outline="#ddd")
            self.teamLabels.append(self.canvas.create_text(420, team * 70 + 6, text="Team " + str(team+1), anchor=NW, font=("Helvetica", "13"), fill="#444"))
            self.teamCurrentLabels.append(self.canvas.create_text(420, team * 70 + 44, text="Current: " + str(teams[team].numBugs), anchor=NW, fill="#444"))
            self.teamMinLabels.append(self.canvas.create_text(495, team * 70 + 44, text="Min: " + str(teams[team].minBugs), anchor=NW, fill="#444"))
            self.teamMaxLabels.append(self.canvas.create_text(550, team * 70 + 44, text="Max: " + str(teams[team].maxBugs), anchor=NW, fill="#444"))
            self.teamGraphs.append(self.canvas.create_rectangle(415, \
                                            team * 70 + 27, 420 + 167 * teams[team].percent(), \
                                            team * 70 + 42, fill=colors[team], outline=borders[team]))
                    
    def update(self):
        '''
        Cycles through one execution of each bug, updating the image accordingly.
        '''
        for i in range(len(self.buglist)):
            self.buglist[i].execute()
            self.canvas.itemconfig(self.bugimages[i], image=self.bugdict["bug"+str(self.buglist[i].team.id+1)+str(self.buglist[i]._direction)])
            self.canvas.coords(self.bugimages[i], self.buglist[i]._pos[0]*20+14, self.buglist[i]._pos[1]*20+14)
            
        for i in range(len(teams)):
            self.canvas.coords(self.teamGraphs[i], 420, \
                                 i * 70 + 27, 420 + 167 * teams[i].percent(), \
                                 i * 70 + 42)
            self.canvas.itemconfig(self.teamCurrentLabels[i], text="Current: " + str(teams[i].numBugs), anchor=NW)
            self.canvas.itemconfig(self.teamMinLabels[i], text="Min: " + str(teams[i].minBugs), anchor=NW)
            self.canvas.itemconfig(self.teamMaxLabels[i], text="Max: " + str(teams[i].maxBugs), anchor=NW)
            
        self.root.after(100, self.update)

    def connectSocket(self):
        address = "sarcasm.ath.cx"
        port = 54363
        try:
            self.connect = Sockets.ClientConnection(address, port)
            self.connect.openSocket()
        except:
            handleError()
            self.connect.close()

    def closeSocket(self):
        self.connect.close()

    def poll(self):
        '''
        Poll is used to update the grid of bugs.        
        '''
        try:
            buglist = self.connect.recv()
            time.sleep(.5)
            self.connect.send(1)
            self.buglist = change(buglist)
            self.reload()
        except EOFError:
            self.closeSocket()
            #exit
        # This Calls the function again.        
        else:
            self.root.after(100, self.poll)

    def quitfunc(self):
        pass

    def Pass(self):
        pass

# * * * * * * * *
# * Main        *
# * * * * * * * *
def main():

    Debug.ON = False
    master = Tk()
    master.title('Bug Wars')
    master.minsize(600, 410)
    
    
    display = Display(master)
    
    codeFiles = ["../DecentBug.bo", "../DecentBug.bo", "../DecentBug.bo"]

    for i in range(len(codeFiles)):
        f = open(codeFiles[i], "rb")
        code = []
        b = f.read(1)
        while b != "":
            code.append(ord(b))
            b = f.read(1)
        teams.append(Team(i, 30, code))
    
    display.populate()
    
    #display.connectSocket()
    #display.buglist = change(list)
    #display.reload()
    #display.poll()
    
    master.after(100, display.update)
    master.mainloop()

    #display.closeSocket()

if __name__ == '__main__':
    main()
