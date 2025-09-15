def main():
    print("Would you like to pathfind, edit grid, or close program? (p:pathfind, e:edit grid, c:close program)")
    running = True
    answer = input()
    while(running):
        if(answer=="p" or answer=="P"):
            print("Entering pathfinding mode.")
            running = False
            pathFind()
        elif(answer=="e" or answer=="E"):
            print("Entering editing mode.")
            running = False
            editGrid()
        elif(answer=="c" or answer=="C"):
            running = False
            print("Program closed.")
        else:
            print("Invalid answer")
            answer = input()

def editGrid():
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

def pathFind():
    #2d array
    grid = ""
    with open("grid.txt") as file:
        grid = file.read().split('\n')
        for i in range(0,len(grid)):
            grid[i] = grid[i].split(",")
    print("Enter starting position as two numbers separated with a comma: ")
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

        #use a tree to find path

#return value is a boolean or tuple, the final return should be a False or a tuple. A tuple signifies success and a False signifies failure.
def checkPath(x,y,direction,directions,target):
    newX = x
    newY = y
    if(direction=="left"):
        if(x > 0):
            if(grid[y][x-1]==0):
                newX-=1
        else:
            return False
    elif(direction=="right"):
        if(x < len(grid[y])):
            if(grid[y][x+1]==0):
                newX+=1
        else:
            return False
    elif(direction=="up"):
        if(y > 0):
            if(grid[y-1][x]==0):
                newY-=1
        else:
            return False
    elif(direction=="down"):
        if(y < len(grid)):
            if(grid[y+1][x]==0):
                newY+=1
        else:
            return False
    if(grid[newY][newX]==0):
        directions.append(direction)
        x = newX
        y = newY
        if(x==target[0] and y==target[1]):
            #once the spot is found return the required information
            return (directions,x,y)
        if(checkPath(x,y,"left",directions,target)):
            return True
        elif(checkPath(x,y,"right",directions,target)):
            return True
        elif(checkPath(x,y,"up",directions,target)):
            return True
        elif(checkPath(x,y,"down",directions,target)):
            return True
        else:
            return False
    else:
        return False

#The idea is:
#check all for directions
#if any direction is movable, move in that direction, else return false
#when receiving the value false, try moving in another direction
#when no direction can be moved in, the pathfinding is halted



main()