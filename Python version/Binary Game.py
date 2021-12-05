from tkinter import *
from tkinter import font
from random import randint

class Row(object):
    def __init__(self):
        self.intValue = randint(1,63)
        self.binValue = bin(self.intValue)[2:]
        for b in range(7-len(self.binValue)):
            self.binValue = "0" + self.binValue
        #print(self.binValue,self.intValue)
            self.intValue, self.binValue = str(self.intValue), str(self.binValue)

    def getQuestion(self):
        if randint(0,1):
            self.answer = self.intValue
            return self.binValue, self.answer, True
        else:
            self.answer = self.binValue
            return self.intValue, self.answer, False

def MainTxt():
    print("     64 32 16  8  4  2  1 ")
    score = 0
    while True:
        row = Row()
        questionData = row.getQuestion()
        question = "    "
        if questionData[2]:
            if score != 0:
                print("     64 32 16  8  4  2  1 ")
            for i in questionData[0]:
                question += "  "+i
        else:
            question = str(questionData[0])
        ans = input(question + " = ")
        while True:
            try:
                int(ans)
                break
            except:
                ans = input(question + " = ")
                
        if ans == "":
            break
        valid = False
        if str(int(ans)) == str(int(questionData[1])):
            valid = True
        if valid:
            print("                             Correct - " + str(questionData[1]))
            score += 1
        else:
            print("                             Incorrect - " + str(questionData[1]))
    print("Vous avez eu " + str(score) + " bonnes reponses.")


class MainGUI():
    def __init__(self):
        self.fen = Tk()
        self.can = Canvas(self.fen,width=500,height=500,bg='#0C1A23')
        self.can.pack()

        self.fen.bind('<Button-1>', self.getClick)
        self.fen.bind('<Motion>', self.getMotion)
        
        self.questionGrid = []
        self.grid=[]
        self.selectedItem=[]
        self.fen.after(3000,self.add_row)
        self.drawGrid()
        
        self.fen.mainloop()

    def getClick(self,event):
        self.getMotion(event,True)
        
    def getMotion(self,event,click=False):
        obj = self.can.find_enclosed(event.x-50,event.y-70,event.x+50,event.y+70)
        for o in obj:
            if o in self.grid:
                focused=self.can.find_withtag("closest")
                for f in focused:
                    if self.can.type(f) == 'oval':
                        if f != o:
                            self.can.itemconfig(f,fill='#5A8092')
                        else:
                            self.can.itemconfig(o,fill='#708592')
                
                
                    if self.can.type(f) == 'text' and click:
                        if "0" in self.can.gettags(f):
                            state=False
                        elif "1" in self.can.gettags(f):
                            state=True
                        else:
                            print(self.can.gettags(f))
                            
                        states=["0","1"]
                        tags=list(self.can.gettags(f))
                        tags.remove(states[state])
                        tags.append(states[not state])
                        self.can.itemconfig(f,text=states[not state],tags=tags)

                print(len(focused))
                self.can.dtag(focused,"closest")
                self.can.addtag_enclosed("closest",event.x-50,event.y-70,event.x+50,event.y+70)

                
        
    def add_row(self):
        row = Row()
        questionData = row.getQuestion()
        self.questionGrid.insert(0,list(questionData))

        self.drawGrid()

        if len(self.questionGrid) == 7:
            print('Perdu!')
        else:
            self.fen.after(3000,self.add_row)

    def drawGrid(self):
        if len(self.questionGrid)==0:
            return
        cellSize=(57,74)
        customFont = font.Font(family='Source Code Pro', size=25)
        q=self.questionGrid[0]
        self.grid.append([])
        question=q[not q[2]]
        for x,v in enumerate(question):
            cellPos=(x*cellSize[0]+10,500)
            textPos=(cellPos[0]+cellSize[0]/2,cellPos[1]+cellSize[1]/2)
            tile=self.can.create_oval((cellPos),(cellSize[0]+cellPos[0]+2,cellSize[1]+cellPos[1]+2),fill="#5A8092",width=1,tags=("movable"))
            self.can.create_text(textPos,font=customFont,text=v, fill='#9AB3C1',tags=("movable",v))
            self.grid.append(tile)
    
        self.can.create_text((485,textPos[1]),anchor="e",font=customFont,text=q[q[2]], fill='#708592',tags=("movable"))
        for i in self.can.find_withtag("movable"):
            self.can.move(i,0,-cellSize[1])

MainGUI()   
#MainTxt()
