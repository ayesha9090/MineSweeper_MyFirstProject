import random,os,threading,time
from tkinter import messagebox
from tkinter import *
from PIL import ImageTk, Image
import configparser
import time

 #class having all the attributes common in every class
class gameattr:
    def __init__(self,rows,cols,mines):
        self.rows=rows
        self.cols=cols
        self.mines=mines
        self.board=[]
        self.buttons=[]
    @property
    def rows(self):
        return self._rows
   
    @rows.setter
    def rows(self,r):
        self._rows=r
    
    @property
    def cols(self):
        return self._cols
    @cols.setter
    def cols(self,c):
        self._cols=c
    
    @property
    def mines(self):
        return self._mines
    @mines.setter
    def mines(self,m):
        self._mines=m
#Main game window 
class GUI(gameattr):
    def __init__(self,rows,cols,mines):
        super().__init__(rows,cols,mines)
    def window(self):
        self.root=Tk()
        self.root.title('Minesweeper')
        self.root.iconphoto(True, PhotoImage(file='D:\mc\minesweeper.png'))
        my_img= ImageTk.PhotoImage(Image.open('D:\mc\mini.png'))
        myLabel=Label(image=my_img)
        myLabel.pack()
        Start=Button(self.root,text='Start',fg='black',bg='grey',command= lambda : start(self.rows,self.cols,self.mines).created())
        Start.pack(fill=X)
        Exit=Button(self.root,text='Quit',fg='black',bg='grey',command=self.root.quit)
        Exit.pack(fill=X)
        self.root.mainloop()
    def setter(self,r,c,m):
        self.rows=r
        self.cols=c
        self.mines=m

#class which return the list of solution grid   
class Grid(gameattr):
    def __init__(self,rows,cols,mines):
        super().__init__(rows,cols,mines)
        self.create()
    
    def create(self):
        self.board=[]
        for i in range(0,(self.rows)):
            self.board.append([])
            for _ in range (0,(self.cols)):
                self.board[i].append(0)
        for i in range(0,self.mines):
            self.placebomb()
        
        for x in range(0,self.rows):
            for y in range(0,self.cols):
                if self.board[x][y]=='*':
                    self.nearbomb(x,y)
    
        
    def placebomb(self):
        x=random.randint(0,((self.rows)-1))
        y=random.randint(0,((self.cols)-1))
        while self.board[x][y] =='*':
            x = random.randint(0, ((self.rows)-1))
            y = random.randint(0, ((self.cols)-1))

        self.board[x][y] ='*'
    def nearbomb(self,x,y):
        s=self.board
        if x==0:
            if s[x+1][y]!='*':
                s[x+1][y]+=1
            if y>=0 and y<((self.cols)-1):
                if s[x][y+1]!='*':
                    s[x][y+1]+=1
            if y>0 and y<=self.cols:
                if s[x][y-1]!='*':
                    s[x][y-1]+=1
        if x==((self.rows)-1):
            if s[x-1][y]!='*':
                s[x-1][y]+=1
            if y>=0 and y<((self.cols)-1):
                if s[x][y+1]!='*':
                    s[x][y+1]+=1
            if y>0 and y<=self.cols:
                if s[x][y-1]!='*':
                    s[x][y-1]+=1
        if x>0 and x<((self.rows)-1):
            if s[x+1][y]!='*':
                s[x+1][y]+=1
            if s[x-1][y]!='*':
                s[x-1][y]+=1
            if y>=0 and y<((self.cols)-1):
                if s[x][y+1]!='*':
                    s[x][y+1]+=1
            if y>0 and y<=((self.cols)-1):
                if s[x][y-1]!='*':
                    s[x][y-1]+=1
#class which creates the whole game  
class start(gameattr):
    def __init__(self,rows,cols,mines):
        super().__init__(rows,cols,mines)
    def created(self):
        global top,timer,check,i,gameover,Winner
        top=Toplevel()
        self.saveattr()
        self.createMenu()
        self.createWindow()
        
        timer=True
        check=False
        time.sleep(1.1)
        Time.counter()
        
    def saveattr(self):
        if os.path.exists("config.ini"):
            self.loadConfig()
        else:
            self.saveConfig()
    def saveConfig(self):
        
    #configuration
        config = configparser.ConfigParser()
        config.add_section("game")
        config.set("game", "rows", str(self.rows))
        config.set("game", "cols", str(self.cols))
        config.set('game','mines',str(self.mines))
        
        with open("config.ini", "w") as file:
            config.write(file)
    def loadConfig(self):
        
        config = configparser.ConfigParser()
        config.read("config.ini")
        self.rows = config.getint("game", "rows")
        self.cols = config.getint("game", "cols")
        self.mines = config.getint("game", "mines")  
        
    def createMenu(self):
        global top
        menubar=Menu(top)
        menusize=Menu(top,tearoff=0)
        menusize.add_command(label='Easy',command=lambda rows=10,cols=10,mines=15:self.setsize(10,10,10))
        menusize.add_command(label='Medium',command=lambda rows=15,cols=15,mines=20:self.setsize(15,15,20))
        menusize.add_command(label='Difficult',command=lambda rows=20,cols=20,mine=20:self.setsize(20,20,40))
        menusize.add_separator()
        menubar.add_cascade(label='Level',menu=menusize)
        menubar.add_cascade(label='exit',command=lambda:top.destroy())
        menubar.add_cascade(label='Restart',command=lambda :(self.gamepre()))
        top.config(menu=menubar)
    
    
    def createWindow(self):
        global top,grid,buttons,v,count,i,gameover
        gameover=False
        rows=self.rows
        cols=self.cols
        mines=self.mines
        buttons=self.buttons
        buttons=[]
        g=Grid(self.rows,self.cols,self.mines)
        grid=g.board
    
    
        count=(mines)
        v=StringVar()
        v.set(str(mines))
        i=StringVar()
        label=Label(top,text='Flags:',fg='white',bg='green')
        label1=Label(top,textvariable=v, relief=GROOVE)
        label.grid(row=0,column=0)
        label1.grid(row=0,column=1) 
        timelbl=Label(top,bg='black',fg='white' , textvariable=i) 
        timelbl.grid(row=0,column=5)
        for x in range(0, rows):
            buttons.append([])
            for y in range(0, cols):
                b = Button(top, text=" ", width=2, command=lambda x=x,y=y: self.display(x,y))
                b.bind("<Button-3>", lambda e, x=x, y=y:self.Flag(x, y))
                b.grid(row=x+1, column=y, sticky=N+W+S+E)
                buttons[x].append(b)

    
    def display(self,x,y):
        global grid,buttons,Winner,times,gameover
        disabledbuttons=self.disabledbuttons
        rows=self.rows
        cols=self.cols
        mines=self.mines
        if grid[x][y]=='*':
            buttons[x][y].config(text=str(grid[x][y]),bg='red',fg='white',state=DISABLED)
            gameover=True
            messagebox.showinfo('Game Over','You lose!!')
            for i in range(rows):
                for j in range(cols):
                    buttons[i][j].config(relief=GROOVE,state=DISABLED)
                    if grid[i][j]=='*':
                        buttons[i][j].config(text='*',fg='black')
                
        else:
            if grid[x][y]>0:
                buttons[x][y].config(text=str(grid[x][y]),bg='black',fg='white',relief=GROOVE, state=DISABLED)
            if grid[x][y]==0:
                buttons[x][y].config(text=' ',bg='grey',fg='black',state=DISABLED)
                disabledbuttons(x,y)
        buttons[x][y].config(state=DISABLED)
        self.Winner()
        if (Winner==True or gameover==True):
            file1=open('time.txt','a')
            file1.write('Time\n')
            file1.writelines(str(times)+'s')
            file1.close
    def disabledbuttons(self,x,y):
        global grid, buttons
        if x==0:
            for i in range(0,int(self.cols/2)):
                if grid[x][i]!='*' and buttons[x][i]['state']=='normal':
                    if grid[x][i]==0:
                        buttons[x][i].config(text=' ',bg='grey',fg='black',state=DISABLED)
                    else:
                        buttons[x][i].config(text=str(grid[x][i]),bg='black',fg='white',state=DISABLED)
   
   
        for i in range(int(x/2),x):
            for j in range(int(y/2),y):
                if grid[i][j]!='*' and buttons[i][j]['state']=='normal':
                    if grid[i][j]==0:
                        buttons[i][j].config(text=' ',bg='grey',fg='black',state=DISABLED)
                    else:
                       buttons[i][j].config(text=str(grid[i][j]),bg='black',fg='white',state=DISABLED)
    def Winner(self):
        global buttons,grid,Winner
        rows=self.rows
        cols=self.cols
        Winner=False
        if all(grid[x][y]!='*' for x in range(rows) for y in range(cols) ):
            Winner=True
            messagebox.showinfo('Congratulations','You Won!!')  
            

    def gamepre(self):
        global top,times,gameover,timer,check
        times=0
        gameover = False
        #destroy all - prevent memory leak
        for x in top.winfo_children():
            if type(x) != Menu:
                x.destroy()
        self.createWindow()
        timer=True
        check=False
        time.sleep(1.1)
        Time.counter()
        
    def setsize(self,r,c,m):
        global gameover
        GUI(self.rows,self.cols,self.mines).setter(r,c,m)
        gameover=False
        self.rows=r
        self.cols=c
        self.mines=m
        self.saveConfig()
        self.gamepre()
    
    def Flag(self,x,y):
        global grid,count,buttons
        global v
    

        count-=1
        v.set(str(count))

        if grid[x][y]=='*':
            grid[x][y]='F'
        buttons[x][y].config(text='F',fg='white',bg='green',state=DISABLED)
class Time:
    @staticmethod
    def counter():
        global timer,top,i,gameover,Winner
        if timer:
            timer=False
            t=threading.Thread(target=Time.whileloop)
            t.setDaemon(True)
            t.start()
        top.after(1,Time.counter)
    @staticmethod
    def whileloop():
        global check,i,times,gameover
        times=0
        check=True
        while check:
            times+=1
            i.set(str(times))
            if (gameover==True):
                break
                
            time.sleep(1)


#Main Program starts from here.       
g=GUI(10,10,10)
g.window()


  
    

