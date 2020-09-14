import random
import numpy as np
from timeit import default_timer as timer

#the lines below defines the text print color - nothing to do with gameplay. labels might be wrong.
magenta = '\u001b[35m'
cyan = '\u001b[36m'
red = '\u001b[31m'
green = '\u001b[33m'
white= '\u001b[37m'

colors = random.randint(3,4) #number of colors - 2, 3, or 4
width=random.randint(4,8)#set board size
height=width#board is square

if colors<2:
  colors=2
if colors>4:
  colors=4
if width<2:
  width=2

#create the game board array
gameboard = np.zeros((width,height,3))#3rd dimension is color, uncovered or not, surrounding number

#set colors into the board
#then count totals - make sure no color total is zero
def set_colors_into_board():
  xpos,ypos=0,0
  while ypos<height:
    while xpos<width:
      gameboard[xpos][ypos][0] = random.randint(1,colors)
      xpos+=1
    xpos=0
    ypos+=1
    count_totals()
  
#calculate adjacent number of same tiles
def calculate_adjacents():
  calcx,calcy=0,0
  while calcy<height:
    while calcx<width:
      if calcx+1<width:
        if gameboard[calcx][calcy][0]==gameboard[calcx+1][calcy][0] and (calcx+1<width):
          gameboard[calcx][calcy][2]+=1
      if calcy+1<height:
        if gameboard[calcx][calcy][0]==gameboard[calcx][calcy+1][0] and (calcy+1<height):
          gameboard[calcx][calcy][2]+=1
      if gameboard[calcx][calcy][0]==gameboard[calcx-1][calcy][0] and (calcx-1>=0):
        gameboard[calcx][calcy][2]+=1
      if gameboard[calcx][calcy][0]==gameboard[calcx][calcy-1][0] and (calcy-1>=0):
        gameboard[calcx][calcy][2]+=1
      calcx+=1
    calcx=0
    calcy+=1

#convert the color number into a letter - easier to comprehend
def numtochar(num):
  if num==1:
    return "magenta"
  elif num==2:
    return "blue"
  elif num==3:
    return "red"
  elif num==4:
    return "yellow"

tota,totb,totc,totd=0,0,0,0
curtota,curtotb,curtotc,curtotd=0,0,0,0
def count_totals():
  #calculate the per-total totals - needs to be done at the start
  countx,county=0,0
  global tota,totb,totc,totd,curtota,curtotb,curtotc,curtotd
  tota,totb,totc,totd=0,0,0,0
  while county<height:
    while countx<width:
      if gameboard[countx][county][0]==1:
        tota+=1
      if gameboard[countx][county][0]==2:
        totb+=1
      if gameboard[countx][county][0]==3:
        totc+=1
      if gameboard[countx][county][0]==4:
        totd+=1
      countx+=1
    countx=0
    county+=1
  curtota,curtotb,curtotc,curtotd=tota,totb,totc,totd
  #calculate the totals=======
    
def check_zero_totals():
  if colors>1 and tota==0:
    set_colors_into_board()
  if colors>1 and totb==0:
    set_colors_into_board()
  if colors>2 and totc==0:
    set_colors_into_board()
  if colors>3 and totd==0:
    set_colors_into_board
    
#calculate the current totals, done each time a correct guess is done
def printcurrenttotals():
  global curtota,curtotb,curtotc,curtotd
  if colors==4:
    print(white+"remaining:",magenta+numtochar(1),curtota,"|",cyan+numtochar(2),curtotb,"|",red+numtochar(3),curtotc,"|",green+numtochar(4),curtotd)
  elif colors==3:
    print(white+"remaining:",magenta+numtochar(1),curtota,"|",cyan+numtochar(2),curtotb,"|",red+numtochar(3),curtotc)
  elif colors==2:
    print(white+"remaining:",magenta+numtochar(1),curtota,"|",cyan+numtochar(2),curtotb)

def return_color_total(color):
  if color==1:
    #print("curtota is",curtota)
    return curtota
  elif color==2:
    #print("curtotb is",curtotb)
    return curtotb
  elif color==3:
    #print("curtotc is",curtotc)
    return curtotc
  elif color==4:
    #print("curtotd is",curtotd)
    return curtotd

#print the in-progress board
def printcurrentboard ():
  #print("key: color , number surrounding")
  printx,printy=0,0
  while printy<width:
    while printx <height:
      if(gameboard[printx][printy][1]==1):
        print(str(currentprintcolor(printx,printy))+"[",int(gameboard[printx][printy][2]),"]",end="")
      else:
        print(white+"[ ? ]",end="")
      printx+=1
    print()
    printx=0
    printy+=1
  print(white,end="")#reset color back to white

def currentprintcolor(x,y):
  if gameboard[x][y][0]==1:
    return magenta
  elif gameboard[x][y][0]==2:
    return cyan
  elif gameboard[x][y][0]==3:
    return red
  elif gameboard[x][y][0]==4:
    return green

def efficiency():
  percentcomplete = (((width*height)-remaining)/(width*height))*100
  if guesses!=0:
    print (white+"uncovered",width*height-remaining,"tiles (",str(percentcomplete)[:4],"%) in",guesses,"guesses: efficiency: (",str(((width*height-remaining)/guesses)*100)[:2],"%), time:",str((timer()-starttime)*100)[:4])

#guess function
remaining=width*height
guesses=0
def guess(x,y,color):
  global curtota,curtotb,curtotc,curtotd,guesses,remaining
  guesses+=1
  if(gameboard[x][y][0]==color) and (gameboard[x][y][1]==0):
    #print(str(currentprintcolor(x,y))+"guess #",guesses,"x: ",x,",y: ",y,", color: ",numtochar(color)," - correct guess")
    gameboard[x][y][1]=1
    remaining-=1
    if gameboard[x][y][0]==1:
      curtota-=1
    if gameboard[x][y][0]==2:
      curtotb-=1
    if gameboard[x][y][0]==3:
      curtotc-=1
    if gameboard[x][y][0]==4:
      curtotd-=1
    return 1
  elif (gameboard[x][y][1] != 0):
    print(str(currentprintcolor(x,y))+"guessing:",guesses,",x: ",x,",y: ",y,", color: ",numtochar(color)," - tile already uncovered")
    return 2
  elif (gameboard[x][y][0] != color):
    #print(white+"guess #",guesses,"x: ",x,",y: ",y,", color: ",numtochar(color)," - WRONG guess")
    return 0

def resetguesses():
  #we need to set gameboard[x][y][1]=0 for each tile, in order to solve the same board a second time
  xpos,ypos=0,0
  while ypos<height:
    while xpos<width:
      gameboard[xpos][ypos][1] = 0
      xpos+=1
    xpos=0
    ypos+=1

  #reset totals
  count_totals()
  global guesses,remaining,starttime
  guesses=0
  remaining=width*height
  starttime=timer()
  print(white+"==guesses have been reset==")

def give_color_order(whichpos):
  mylist=[curtota,curtotb,curtotc,curtotd]  
  newlist=sorted(range(len(mylist)), key=lambda k: mylist[k], reverse=True)
  #print(newlist)
  return newlist[whichpos]
    
#modified brute 2: also start out with color that has greatest count
def modified_brute_2():
  print(white+"++solving board with brute 2 (select highest count first)++")
  solvingx,solvingy=0,0
  while(solvingy<height):
    while(solvingx<width):
      if gameboard[solvingx][solvingy][1]==0:
        guess(solvingx,solvingy,give_color_order(0)+1)
      if gameboard[solvingx][solvingy][1]==0:
        guess(solvingx,solvingy,give_color_order(1)+1)
      if gameboard[solvingx][solvingy][1]==0:
        if colors > 2:
          guess(solvingx,solvingy,give_color_order(2)+1)
      if gameboard[solvingx][solvingy][1]==0:
        if colors == 4:
          guess(solvingx,solvingy,give_color_order(3)+1)
      solvingx+=1
    solvingx=0
    solvingy+=1

def init():
  print("INITIALIZING")
  global starttime
  set_colors_into_board()#must do this at beginning of the game
  calculate_adjacents()#must do this at beginning of the game
  starttime=timer()

def userplay():
  while(remaining>0):
    print(white,remaining,"spaces remaining to be found")
    print("enter X from 1 to",width,end="")
    xguess=int(input(":"))
    print("enter Y from 1 to",height,end="")
    yguess=int(input(":"))
    print("enter color from 1 to",colors,end="")
    colguess=int(input(":"))
    guess(xguess-1,yguess-1,int(colguess))
    printcurrentboard()
    printcurrenttotals()
  efficiency()


#application begins below
init()
printcurrentboard()
printcurrenttotals()

userplay()

resetguesses()
modified_brute_2()
efficiency()
