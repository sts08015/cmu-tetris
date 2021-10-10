import math, copy, random

from cmu_112_graphics import *

#################################################
# Tetris
#################################################
def newFallingPiece(app):
    import random
    randomIndex = random.randint(0,len(app.tetrisPieces)-1)
    app.fallingPiece = app.tetrisPieces[randomIndex]
    randomIndex = random.randint(0,len(app.tetrisPieceColors)-1)
    app.fallingPieceColor = app.tetrisPieceColors[randomIndex]

    app.numFallingPieceCols = len(app.fallingPiece[0])
    app.numFallingPieceRows = len(app.fallingPiece)
    app.fallingPieceRow = 0
    app.fallingPieceCol = app.cols//2 - app.numFallingPieceCols//2

def drawCell(app,canvas,row,col,color=None):
    cen_x = app.margin + (app.cellSize/2) + app.cellSize*col
    cen_y = app.margin + (app.cellSize/2) + app.cellSize*row

    x1 = cen_x - app.cellSize/2
    y1 = cen_y - app.cellSize/2
    
    x2 = cen_x + app.cellSize/2
    y2 = cen_y + app.cellSize/2

    if color == None:
        color = app.board[row][col]
    
    canvas.create_rectangle(x1,y1,x2,y2,fill=color,outline='black',width=2.5)

def drawFallingPiece(app,canvas):
    for i in range(app.numFallingPieceRows):
        for j in range(app.numFallingPieceCols):
            if app.fallingPiece[i][j] == True:
                drawCell(app,canvas,
                         i+app.fallingPieceRow,j+app.fallingPieceCol,
                         app.fallingPieceColor)

def drawBoard(app,canvas):
    for i in range(app.rows):
        for j in range(app.cols):
            drawCell(app,canvas,i,j)

def isIn(app,x,y):
    if x<0 or x>=app.rows or y<0 or y>=app.cols:
        return False
    return True

def fallingPieceIsLegal(app):
    for i in range(app.numFallingPieceRows):
        for j in range(app.numFallingPieceCols):
            if app.fallingPiece[i][j] == True:
                x = app.fallingPieceRow + i
                y = app.fallingPieceCol + j
                if not isIn(app,x,y) or app.board[x][y] != app.emptyColor:
                    return False
    return True

def moveFallingPiece(app,drow,dcol):
    tmp_row = app.fallingPieceRow
    tmp_col = app.fallingPieceCol

    app.fallingPieceRow += drow
    app.fallingPieceCol += dcol
    
    res = fallingPieceIsLegal(app)

    if not res:
        app.fallingPieceRow = tmp_row
        app.fallingPieceCol = tmp_col

    return res

def rotateFallingPiece(app):
    #counterclockwise
    tmp_col = app.numFallingPieceCols
    tmp_row = app.numFallingPieceRows
    tmp_p = app.fallingPiece
    oldRow = app.fallingPieceRow
    oldCol = app.fallingPieceCol

    
    #swapped
    rotP = [[None]*tmp_row for i in range(tmp_col)]

    for i in range(tmp_row):
        for j in range(tmp_col):
            rotP[tmp_col-j-1][i] = tmp_p[i][j]

    app.fallingPiece = rotP
    app.numFallingPieceRows = tmp_col
    app.numFallingPieceCols = tmp_row

    offset = tmp_row//2 - app.numFallingPieceRows//2
    app.fallingPieceRow += offset

    offset = tmp_col//2 - app.numFallingPieceCols//2
    app.fallingPieceCol += offset
    
    res = fallingPieceIsLegal(app)
    
    if not res:
        app.fallingPiece = tmp_p
        app.numFallingPieceRows = tmp_row
        app.numFallingPieceCols = tmp_col
        app.fallingPieceCol = oldCol
        app.fallingPieceRow = oldRow

def hardDrop(app):
    while fallingPieceIsLegal(app):
        app.fallingPieceRow += 1
    app.fallingPieceRow -= 1

def appStarted(app):
    app.label = 'Tetris!'
    app.color = 'orange'
    app.size = 0
    app.paused = False
    app.step = False
    
    dim = gameDimensions()
    app.rows = dim[0]
    app.cols = dim[1]
    app.cellSize = dim[2]
    app.margin = dim[3]

    app.emptyColor = 'blue'
    app.board = [[app.emptyColor]*app.cols for i in range(app.rows)]
    
    # Seven "standard" pieces (tetrominoes)
    iPiece = [
        [  True,  True,  True,  True ]
    ]
    jPiece = [
        [  True, False, False ],
        [  True,  True,  True ]
    ]
    lPiece = [
        [ False, False,  True ],
        [  True,  True,  True ]
    ]
    oPiece = [
        [  True,  True ],
        [  True,  True ]
    ]
    sPiece = [
        [ False,  True,  True ],
        [  True,  True, False ]
    ]
    tPiece = [
        [ False,  True, False ],
        [  True,  True,  True ]
    ]
    zPiece = [
        [  True,  True, False ],
        [ False,  True,  True ]
    ]
    #app.timerDelay = 100
    app.tetrisPieces = [iPiece,jPiece,lPiece,
                        oPiece,sPiece,tPiece,zPiece]
    app.tetrisPieceColors = ["red","yellow","magenta",
                             "pink","cyan","green","orange"]

    app.fallingPieceColor = None
    app.fallingPiece = None
    app.numFallingPieceCols = None
    app.numFallingPieceRows = None
    app.fallingPieceRow = None
    app.fallingPieceCol = None

    app.isGameOver = False
    app.score = 0
    
    newFallingPiece(app)
    
    
def keyPressed(app, event):
    key = event.key.lower()
    if key == 's' and app.paused:
        app.step = True
    
    if (not app.paused) or app.step:
        if key == 'r':
            app.isGameOver = False
            appStarted(app)
        elif key == 'p':
            app.paused ^= True
            if app.step == True:
                app.step = False
        elif key == 'left':
            moveFallingPiece(app,0,-1)
        elif key == 'right':
            moveFallingPiece(app,0,+1)
        elif key == 'up':
            rotateFallingPiece(app)
        elif key == 'down':
            moveFallingPiece(app,+1,0)
        elif key == 'space':
            hardDrop(app)
        else:
            #newFallingPiece(app)
            #chk = fallingPieceIsLegal(app)
            #app.isGameOver = (not chk)
            pass

def removeFullRows(app):
    fullRows = 0
    r = app.rows
    c = app.cols

    tmp_board = [[None]*c for i in range(r)]

    idx = r-1
    
    for i in range(r-1,-1,-1):
        cnt = 0
        for j in range(c):
            if app.board[i][j] != app.emptyColor:
                cnt+=1
        if cnt != c:    #not full row
            tmp_board[idx] = copy.copy(app.board[i])
            idx-=1
        else:
            fullRows+=1
            app.score+=1
    
    for i in range(fullRows):
        for j in range(c):
            tmp_board[i][j] = app.emptyColor

    app.board = tmp_board
    

def placeFallingPiece(app):
    row = app.fallingPieceRow
    col = app.fallingPieceCol
    p = app.fallingPiece
    
    for i in range(app.numFallingPieceRows):
        for j in range(app.numFallingPieceCols):
            if p[i][j] == True:
                app.board[row+i][col+j] = app.fallingPieceColor

    removeFullRows(app)    

def drawScore(app,canvas):
    msg = "Score: %d" % (app.score)
    x = app.width/2
    y = app.margin/2
    canvas.create_text(x,y,text=msg,fill="blue",font=("arial bold",14))

def timerFired(app):
    if not app.paused:
        if not app.isGameOver:
            res = moveFallingPiece(app,+1,0)
            if not res:
                placeFallingPiece(app)
                newFallingPiece(app)
                chk = fallingPieceIsLegal(app)
                app.isGameOver = (not chk)
        
    
def redrawAll(app, canvas):
    canvas.create_rectangle(0,0,app.width,app.height,fill=app.color)
    drawBoard(app,canvas)
    drawScore(app,canvas)
    if not app.isGameOver:
        drawFallingPiece(app,canvas)
    if app.isGameOver:
        rs = app.margin
        cs = app.margin + app.cellSize
        re = app.width - app.margin
        ce = app.margin + app.cellSize*3
        msg = "Game Over!"
        tr = (rs+re)/2
        te = (cs+ce)/2
        canvas.create_rectangle(rs,cs,re,ce,fill='black')
        canvas.create_text(tr,te,text=msg,fill="yellow",font=("arial bold",24))
    
    
def gameDimensions():
    #default values (15,10,20,25) --> modify this values for custom
    rows = 15
    cols = 10
    cellSize = 20
    margin = 25
    return (rows,cols,cellSize,margin)
    
def playTetris():
    dim = gameDimensions()
    height = dim[0]*dim[2] + dim[3]*2
    width = dim[1]*dim[2] + dim[3]*2
    runApp(width=width, height=height)

#################################################
# main
#################################################

def main():
    playTetris()

if __name__ == '__main__':
    main()
