#global variables
#2d array
grid = ""
#dictionary to prevent going to previous squares
locations = {}

def main():
    #an edit mode should be made in order to edit the grid, with various tools especially for bigger grids
    print("Would you like to pathfind, replace grid, or close program? (p:pathfind, r:replace grid, d:display grid, c:close program)")
    running = True
    answer = input()
    while(running):
        if(answer=="p" or answer=="P"):
            print("Entering pathfinding mode.")
            running = False
            pathFind()
        elif(answer=="r" or answer=="R"):
            print("Entering editing mode.")
            running = False
            replaceGrid()
        elif(answer=="d" or answer=="D"):
            running = False
            readGrid()
            for row in grid:
                print(row)
        elif(answer=="c" or answer=="C"):
            running = False
            print("Program closed.")
        else:
            print("Invalid answer. Would you like to pathfind, edit grid, or close program? (p:pathfind, r:replace grid, d:display grid, c:close program)")
            answer = input()

def replaceGrid():
    #erase file
    with open("grid.txt","w") as file:
        file.write("")
    with open("grid.txt","a") as file:
        stream = True
        #To make sure that there is no blank line at the beginning of the file
        written = False
        #take in input until the input is invalid
        while(stream):
            print("Enter row of 0's and nonnegative numbers, separated by commas, where any nonzero nonnegative number is a wall and 0 is nothing")
            userInput = input()
            #break row into elements to check validity
            temp = userInput.split(",")
            #check if row is invalid
            for element in temp:
                number = False
                for i in range(0,10):
                    if(element==str(i)):
                        number = True
                    stream = number
            #if row is valid, add it to the grid
            if stream:
                #this appends because the file is opened in append mode
                if(written):
                    file.write("\n" + userInput)
                else:
                    file.write(userInput)
                    written = True
    #alert the user that edit mode is being exited
    print("Invalid row, exiting edit mode")

def readGrid():
    with open("grid.txt") as file:
        #to make sure that the changes are saved
        global grid
        grid = file.read().split('\n')
        for i in range(0,len(grid)):
            grid[i] = grid[i].split(",")
            for j in range(0,len(grid[i])):
                grid[i][j] = int(grid[i][j])

def pathFind():
    readGrid()
    print("Enter starting position as two numbers separated with a comma: ")
    start = getCoord()
    print("Enter ending position as two numbers separated with a comma: ")
    end = getCoord()
    #to make sure that the user sees the changes made
    print("All invalid values have been replaced with 0. The start is:",start,"The end is:",end)
    #to make sure that pathfinding is even possible before trying
    #cases in which index is out of bounds
    if(start[1] > len(grid) or end[1] >= len(grid)):
        print("Invalid starting or ending point, y position is out of bounds.")
        exit()
    if(start[0] > len(grid[start[1]]) or end[0] >= len(grid[end[1]])):
        print("Invalid starting or ending point, x position is out of bounds.")
        exit()
    #case in which ending point is inside a wall
    if(grid[end[1]][end[0]]!=0):
        print("Invalid ending point, it must not be inside a wall.")
        exit()
    #use a tree to find path
    result = checkPath(start[0],start[1],"right",[],end) or checkPath(start[0],start[1],"left",[],end) or checkPath(start[0],start[1],"up",[],end) or checkPath(start[0],start[1],"down",[],end)
    if(result):
        #pathfinding success
        print("The steps taken from",start,"to",end,"are",result)
    else:
        #pathfinding fail
        print("There is no way to get from",start,"to",end)

def getCoord():
    pos = tuple(input().split(","))
    #input validation
    while(not isinstance(pos,tuple)):
        print("Invalid position. Re-enter position: ")
        pos = tuple(input().split(","))
    #replace empty and non-number values with 0
    temp = []
    for x in pos:
        try:
            x = int(x)
        except:
            x = 0
        temp.append(x)
    pos = tuple(temp)
    #make sure that the length of the tuple is at least 2, it doesn't matter if it is more because in the end this takes place in a 2d space
    if(len(pos) < 2):
        pos = (pos[0],0)
    elif(not isinstance(pos[1],int)):
        pos = (pos[0],0)
    elif(pos[1] < 0):
        pos = (pos[0],0)
    if(not isinstance(pos[0],int)):
        pos = (0,pos[1])
    elif(pos[0] < 0):
        pos = (0,pos[1])
    return pos
        

#return value is a boolean or tuple, the final return should be a False or a tuple. A tuple signifies success and a False signifies failure.
#this isn't the most efficient path yet
def checkPath(x,y,direction,directions,target):
    #if the start is equal to the end, nothing needs to be done.
    if(x==target[0] and y==target[1]):
        print("The starting point is equal to the ending point. No pathfinding required.")
        exit()
    #check
    print(x,y,grid[y],direction, directions)
    #used to compare original position and new position to see if a change is made
    newX = x
    newY = y
    if(direction=="left"):
        if(x > 0):
            if(grid[y][x-1]==0):
                newX-=1
        else:
            return False
    elif(direction=="right"):
        if(x+1 < len(grid[y])):
            if(grid[y][x+1]==0):
                newX+=1
        else:
            return False
    elif(direction=="up"):
        #len(grid[y-1]) > x is required to check right bound in case of a 2D array not being rectangular
        #No need to check left bound as x is always greater than -1
        if(y > 0 and len(grid[y-1]) > x):
            if(grid[y-1][x]==0):
                newY-=1
        else:
            return False
    elif(direction=="down"):
        if(y+1 < len(grid) and len(grid[y+1]) > x):
            if(grid[y+1][x]==0):
                newY+=1
        else:
            return False
    #return false if a wall is encountered
    if(x==newX and y==newY):
        return False
    if(grid[newY][newX]==0):
        x = newX
        y = newY
        global locations
        #prevent returning previous points to speed up performance and prevent infinite loops
        if(x,y) in locations:
            return False
        locations[(x,y)] = 1
        directions.append(direction)
        if(x==target[0] and y==target[1]):
            #once the spot is found return the required information
            return (directions)
        #use slicing (:) in order to create copies of the arrays to prevent recursive calls changing current call's array
        #use extra condition to make sure that no resources are wasted backtracking and to prevent infinite recursing
        left = direction!="right" and checkPath(x,y,"left",directions[:],target)
        #this works because as long as the value is not false or 0, the value is evaluated as true
        #this way the array of directions can be passed up to the first function call
        if(left):
            return left
        right = direction!="left" and checkPath(x,y,"right",directions[:],target)
        #these conditionals are placed right after the variable is assigned because if the correct path is found there isn't any more reason to check a different path, at least for simple pathfinding
        if(right):
            return right
        up = direction!="down" and checkPath(x,y,"up",directions[:],target)
        if(up):
            return up
        down = direction!="up" and checkPath(x,y,"down",directions[:],target)
        if(down):
            return down
        #if all directions fail, pathfinding fails
        return False
    else:
        #wall is in the way, return false
        return False

#The idea is:
#check all four directions
#if any direction is movable, move in that direction, else return false
#when receiving the value false, try moving in another direction
#when no direction can be moved in, the pathfinding is halted

main()