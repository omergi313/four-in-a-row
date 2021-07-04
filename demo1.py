from time import sleep
from datetime import datetime

import tkinter as tk
import pandas as pd
import json
import os,sys, itertools
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg



def initialize():
    return Game(tk.Toplevel())

def timestamp():
    return datetime.now().strftime("%M%D%Y_%H:%M:%S:%f")

def checkrow(b,r,c,color): # self explainatory
    yes1 = b[r][c] == color and b[r][c+1] == color and b[r][c+2] == color and b[r][c+3] == color
    yes2 = b[r][c] == color and b[r][c-1] == color and b[r][c-2] == color and b[r][c-3] == color
    return yes1 or yes2

def checkcol(b,r,c,color): # self explainatory
    return b[r][c] == color and b[r+1][c] == color and b[r+2][c] == color and b[r+3][c] == color

def checkdoubletriple(b,r,c,color): # self explainatory
    yes1 = b[r][c] ==  color and b[r+1][c+1] == color and b[r+2][c+2] == color and b[r+3][c+3] == color
    yes3 = b[r][c] ==  color and b[r+1][c-1] == color and b[r+2][c-2] == color and b[r+3][c-3] == color
    return yes1 or yes3

def checkwin(b): 
    for r in range(len(b)): # all rows again..........
        row = b[r]
        for c in range(len(row)): # itterate each column
            try: # try checking if red or yellow players answer the winner conditions
                if checkrow(b,r,c,'red') or checkcol(b,r,c,'red') or checkdoubletriple(b,r,c,'red'):
                    return 'red wins'
                if checkrow(b,r,c,'yellow') or checkcol(b,r,c,'yellow') or checkdoubletriple(b,r,c,'yellow'):
                    return 'yellow wins'
            except: # they didnt? boo hoooo
                return None





'''
This is a real, original, tkinter native classic "four in a row" game !
The Game class comprises of two main parts: 
'''
class Game:
    def __init__(self,root):
        self.root = root
        # initiate click counter with 0 clicks per column
        self.clicks = {k:0 for k in range(7)}
        # initiate a printable board representation in list of lists
        self.board = [['X' for i in range(7)] for j in range(6)]
        
        # create the frame to put the game board and anchor it to the top
        self.frameup = tk.Frame(self.root,bg='blue')
        self.frameup.pack(anchor=tk.N,expand=True,fill='both')
        
        # create the frame to put the stuff that are not the game board (you'll see LOL)
        self.framedown = tk.Frame(self.root,bg='pink')
         # also ancor down to the south
        self.framedown.pack(anchor=tk.S,expand=True,fill='both')
        
        # create a label to announce the winner
        self.winnerlabel = tk.Label(self.framedown,text='no winner yet')
        self.winnerlabel.pack()

        
        # make an empty list of buttons
        self.buttns = []
        # create a counter to keep track of who's turn it is
        self.count = 0
        
        # we're not sure if thats the best way to bind all the buttons with the
        # place in the list so it would fit the game board but it worked for us
        for i in range(6): 
            row = []
            for j in range(7):
                # create seven buttons for every row and put it in a list
                row.append(tk.Button(self.frameup,text=f'row{i}col{j}',bg='blue'))
                '''
                bind it to the function that colors the lowest button that is not colored!
                meaning: when left-mouse-button is pushed, the color_change method
                will receive the position of the button pressed according to the grid
                '''
                row[j].bind('<Button-1>',lambda event, self=self, r=i, c=j: self.color_change(event, r,c))
                
                row[j].grid(row=i,column=j)
            
            self.buttns.append(row) # keep up with the list of buttons
                            
            
    '''
    when a button in the board in pressed, this function will activate
    red always begins. 
    
    '''
    def color_change(self,event,r,c):
        if self.count % 2 == 0: # if red pushed the button
            self.board[5-self.clicks[c]][c] = 'red' # update the board game
            self.buttns[5-self.clicks[c]][c].configure(bg='red') # paint it red
        else: # if yellow clicked do the same just for yellow
            self.board[5-self.clicks[c]][c] = 'yellow'
            self.buttns[5-self.clicks[c]][c].configure(bg='yellow')
        
        
        self.clicks[c]+=1 # update column clicks 
        temp = [str(i) for i in self.board]
        #print('\n'.join(temp))
        self.count += 1 # update click counts
        
        sleep(0.5) # so fun we had to inforce patience
        
        # make sure you don't need to check yourself if you won
        self.winnerlabel.configure(text=checkwin(self.board)) 
        
        # always good to keep track of whats going on
        # JK, we save the board so you can enjoy our analytics app
        self.saveboard()
        
                 
    def restart(self):
        self.root.destroy()
        self.root = initialize()
        
    
    def winnermode(self):
        # first we need to remove the pink frame
        self.framedown.destroy()
        # make a new one especially for the winner
        self.frame4 = tk.Frame(self.root,bg=self.currwinner)
        self.frame4.pack(anchor=tk.S,expand=True,fill='both')
        
        # new-game button that links to a function that destroys the current game and returns a new Game instance
        self.newgame = tk.Button(self.frame4,text='new game',command=self.restart)
        # or exit, what ever you want
        self.backhome = tk.Button(self.frame4,text='go back',command=self.root.destroy)
        
        # LOL tkinter
        self.newgame.grid(row=0,column=0,padx=20,pady=20,sticky=tk.SE)
        self.backhome.grid(row=0,column=3,padx=123,pady=12,sticky=tk.NE)


    def saveboard(self):
        # take the first word in that winner label
        t = self.winnerlabel['text'].split(' ')[0]
        colors = ['red','yellow']
        
        # if its red or yellow than put it in the current winner attribute 
        # else put there an empty string just to double check
        self.currwinner = ['',t][t in colors]
        
        '''
        we request 10 extra points just for the next dict comprehension that organizez all the list to dicts
        because we wanted to save results in json (cough, cough) but it was really
        unnecessary so we just saved it as text
        '''
        currboarddict = {j:{i:self.board[j][i] for i in range(len(self.board[j]))} for j in range(len(self.board))}
        
        
        
        # announce the winner and prove it with the board
        toappend = {'winner':self.currwinner,'board':currboarddict}
        toappend = json.dumps(toappend)
        
    
        # only save games that are finished
        if self.currwinner != '':
            # and write it to a file
            with open('log.txt','a+') as f:
                f.write(str(toappend))
                f.write('\n\n')
            # also make sure to get you hooked up by introducing a revolutionary UX
            # as soon as someone wins you can start a new game or go back to analyze some data
            self.winnermode()
        else:
            pass




class Analytics:
    def __init__(self,root):
        # root the analytics stuff
        self.root = root
        self.root.geometry('800x800')

        # a more simple layout only with pack (so much faster)
        self.frame = tk.Frame(self.root,bg='blue')
        self.frame.pack(anchor=tk.N,expand=True,fill='both')
        
        # add some instruction in a label
        self.instructions = tk.Label(self.frame,text='first choose the games you want to view\nand then choose the function!\nHAVE FUN!')
        self.instructions.pack()        
        
        # a tkinter listbox obj to see all the games tracked in the log file
        self.listbox = tk.Listbox(self.frame,selectmode=tk.MULTIPLE)
        # read the file and split it to lines only if they are not empty
        self.lines = [l for l in open('log.txt','r').read().split('\n\n') if l !='']
        
        i=0 # insert all the lines to the listbox
        for line in self.lines:
            self.listbox.insert(i,'game number'+str(i)) 
            i+=1
        self.listbox.pack()
        
        # button to select how many games to analyze as you could ever dream
        self.selectbutton = tk.Button(self.frame,text='select game number\numbers',command=self.hello)
        self.selectbutton.pack()

        # for the lazy folks, select all buttton
        self.selectallbutton = tk.Button(self.frame,text='select all',command=self.selectall)
        self.selectallbutton.pack()
    
        # insert options to analyze (pandas describe dunction)
        self.graphslist = tk.Listbox(self.frame)
        self.graphslist.insert(0,'count')
        self.graphslist.insert(1,'mean')
        self.graphslist.insert(2,'std.')
        self.graphslist.insert(3,'min')
        self.graphslist.insert(4,'25')
        self.graphslist.insert(5,'50')
        self.graphslist.insert(6,'75')
        self.graphslist.insert(7,'max')
        self.graphslist.pack()
        
        # button so when pushed the program knows to show the data
        self.databutton = tk.Button(self.frame,text='select',command=self.makedata)
        self.databutton.pack()

        self.graphbutton = tk.Button(self.frame,text='try graph',command=self.graphy)
        self.graphbutton.pack(anchor=tk.S)

        # frame to put the data in
        self.frame4 = tk.Frame(self.root,bg='blue')
        self.frame4.pack(anchor=tk.S,expand=True,fill='both')
        
        # labels to put the data in
        self.boardlabel = tk.Label(self.frame4)
        self.boardlabel.pack(expand=True,fill='both')
        self.rowslabel = tk.Label(self.frame4)
        self.rowslabel.pack(expand=True,fill='both')
        self.colslabel = tk.Label(self.frame4)
        self.colslabel.pack(expand=True,fill='both')
        
    
    
    def selectall(self): # selects all the games for you
        self.listbox.select_set(0,len(self.lines))
        self.hello() # and after selcted, we then updates the selection for the function
        
        
    def hello(self): # just add all the games from the log file to a list
        self.lst = []
        for selection in self.listbox.curselection():
            self.lst.append(self.lines[selection])
        
        
    def makedata(self): # deeply regret the json formating desicion here
        self.df = pd.DataFrame()
        # unpack all the data from string visualization of dict to reald dict
        self.df['winner'] = [json.loads(line)["winner"] for line in self.lines ]
        # make a new colum to put 1 if red won and 0 if he lost
        self.df['red'] = [1 if json.loads(line)["winner"]=='red' else 0 for line in self.lines ]
        # make a new colum to put 1 if yellow won and 0 if he lost
        self.df['yellow'] = [1 if json.loads(line)["winner"]=='yellow' else 0 for line in self.lines ]
        # also the board is important to unpack jesus
        self.df['board'] = [json.loads(line)["board"] for line in self.lines ]
        
        # make a new column in the data base for every row won
        for r in range(len(self.df['board'][0])):
            
            self.df[f'row{r}'] = [j[str(r)] for j in self.df['board']]
        
        
        # add all the games selected by the user to plot to a list because tkinter is very confusing
        self.plots = []
        for a in self.lst:
            self.plots.append(json.loads(a))
        
        # and according to his selection we put the selected in a list of dataframes
        boardstoplot = [pd.DataFrame(plot['board']) for plot in self.plots]
        
        
        # menual encoding 
        encoder = {'X':0,'red':1,'yellow':2}
        self.rows = []
        self.cols = []
        for b in boardstoplot:
            b.replace(encoder,inplace=True)
            for row in b:
                #print(self.graphslist.curselection())
                self.rows.append(b[row].describe()[self.graphslist.curselection()[0]])
            for col in b.T:
                self.cols.append(b.T[col].describe()[self.graphslist.curselection()[0]])
                
            print(b[row].describe())

            
            # put all the finally ready data in the label
            self.boardlabel.config(text='board:\n'+str(b))
            self.rowslabel.config(text='rows result:\n'+', '.join(map(str,self.rows)))
            self.colslabel.config(text='cols result:\n'+', '.join(map(str,self.cols)))


    def graphy(self):
        #ax = self.df[['red','yellow']].plot.hist()
        self.figure = plt.Figure(figsize=(6,5), dpi=100)
        self.ax = self.figure.add_subplot(1)
        self.chart_type = FigureCanvasTkAgg(self.figure, self.root)
        self.chart_type.get_tk_widget().pack(anchor=tk.S)

        self.ppp = [self.rows,self.cols]
        self.pltt = plt.plot(self.ppp[0],self.ppp[1][1:],kind='bar',legend=True, ax=self.ax)
        self.ax = self.pltt
        self.ax.set_title('rows')




'''

This is the father root application. 
It functions as a placeholder for tkinter Toplevel objects that contaiins the main 
functions in the program.

'''
class Fourinarow: #father window
    def __init__(self,master):
        self.frame = tk.Frame(master,bg='blue', width=450, height=50) # make a frame 
        self.frame.pack(anchor=tk.N,expand=True,fill='both') # put the frame in up north in root window
        
        # create all the beautiful buttons that call our amazing application when pressed!
        self.startB = tk.Button(self.frame, text="START", command=self.callgame)
        self.analB = tk.Button(self.frame, text="ANALYTICS", command=self.callanalytics)
        self.quitB = tk.Button(self.frame, text="QUIT", command=master.destroy)
        
        # place them in a grid....
        self.startB.grid(row=0,column=0)
        self.analB.grid(row=1,column=0)
        self.quitB.grid(row=2,column=0)

        
    # this function instances the Game class as a child window (AKA Toplevel)
    def callgame(self): 
        self.root2 = tk.Toplevel()
        self.app2 = Game(self.root2)
        
    
    # do the same for Analytics class 
    def callanalytics(self): 
        self.root3 = tk.Toplevel()
        self.app3 = Analytics(self.root3)
        
        
        

if __name__=='__main__':
    root = tk.Tk() 
    root.geometry('500x500')

    app = Fourinarow(root) #instance father window
    root.mainloop() #run program

