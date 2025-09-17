#global variables
#2d array
grid = ""
introPrompt = "Would you like to pathfind, edit grid, display grid, or close program? (p:pathfind, e:edit grid, d:display grid, c:close program)"
rowPrompt = "Enter a row of 0's and nonnegative numbers, separated by commas, where any nonzero nonnegative number is a wall and 0 is nothing."


def main():
    #create file if it doesn't exist
    try:
        with open("grid.txt","x") as file:
            pass
    except:
        pass
    print(introPrompt)
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
        elif(answer=="d" or answer=="D"):
            displayGrid()
            print("The grid is displayed above.",introPrompt)
            answer = input()
        elif(answer=="c" or answer=="C"):
            running = False
            print("Program closed.")
        else:
            print("Invalid answer.",introPrompt)
            answer = input()

def editGrid():
    displayGrid()
    print("The current grid is shown above. What changes would you like to make? (a:append row, e:edit row, d:delete grid, c:close editing mode)")
    answer = input()
    while(True):
        if(answer=="a" or answer=="A"):
            with open("grid.txt","a") as file:
                print("Entering appending mode.")
                stream = True
                #take in input until the input is invalid
                while(stream):
                    print("Enter row of 0's and nonnegative numbers, separated by commas, where any nonzero nonnegative number is a wall and 0 is nothing. Enter an invalid row to exit appending mode.")
                    userInput = input()
                    #break row into elements to check validity
                    temp = userInput.split(",")
                    #check if row is invalid
                    for element in temp:
                        number = False
                        for i in range(0,10):
                            if(element.strip()==str(i)):
                                number = True
                            stream = number
                    #if row is valid, add it to the grid
                    if stream:
                        #this appends because the file is opened in append mode
                        file.write("\n" + userInput)
            print("Invalid row, exiting appending mode.")
        elif(answer=="e" or answer=="E"):
            print("Enter row number:")
            num = input()
            try:
                row = grid[int(num)]
                num = int(num)
                print("Would you like to delete, replace, add, or insert into this row? (d:delete, r:replace, a:add, i:insert)")
                action = input()
                if(action=="d" or action=="D"):
                    deleteRow(num)
                    displayGrid()
                    print("Row deleted. The new grid is shown above.")
                elif(action=="r" or action=="R"):
                    print(rowPrompt)
                    newRow = input()
                    temp = newRow.split(",")
                    valid = True
                    #check if row is invalid
                    for element in temp:
                        number = False
                        for i in range(0,10):
                            if(element.strip()==str(i)):
                                number = True
                        if(not number):
                            valid = False
                    if(valid):
                        changeRow(num,newRow)
                        displayGrid()
                        print("Row replaced. The new grid is shown above.")
                    else:
                        print("Invalid row.")
                elif(action=="a" or action=="A"):
                    print(rowPrompt)
                    addOn = input()
                    newRow = str(row)[1:len(str(row))-1] + "," + addOn
                    print(newRow)
                    temp = newRow.split(",")
                    valid = True
                    #check if row is invalid
                    for element in temp:
                        number = False
                        for i in range(0,10):
                            if(element.strip()==str(i)):
                                number = True
                        if(not number):
                            valid = False
                    if(valid):
                        changeRow(num,newRow)
                        displayGrid()
                        print("Row has been appended to. The new grid is shown above.")
                    else:
                        print("Invalid row.")
                elif(action=="i" or action=="I"):
                    print(rowPrompt)
                    newRow = input()
                    temp = newRow.split(",")
                    valid = True
                    #check if row is invalid
                    for element in temp:
                        number = False
                        for i in range(0,10):
                            if(element.strip()==str(i)):
                                number = True
                        if(not number):
                            valid = False
                    if(valid):
                        insertRow(num,newRow,False)
                        displayGrid()
                        print("Row has been inserted. The new grid is shown above.")
                    else:
                        print("Invalid row.")
                else:
                    print("Invalid option.")
            except Exception as e:
                print("Invalid row number.")
        elif(answer=="d" or answer=="D"):
            #erase file
            with open("grid.txt","w") as file:
                file.write("")
            print("Grid deleted.")
        elif(answer=="c" or answer=="C"):
            print("Exiting editing mode.")
            main()
            #exit loop
            return 0
        print("What would you like to do? (a:append row, e:edit row, d:delete grid, c:close editing mode)")
        answer = input()

def changeRow(num,newRow):
    deleteRow(num)
    insertRow(num,newRow,False)

#if row is blank no row is inserted
#if exclude is true the row at num is deleted
def insertRow(num,row,exclude):
    temp = []
    index = 0
    while(index < len(grid)):
        if(index!=num or not exclude):
            temp.append(grid[index])
        index+=1
    with open("grid.txt","w") as file:
        file.write("")
    with open("grid.txt","a") as file:
        written = False
        index = 0
        print(temp)
        for r in temp:
            text = str(r)[1:len(str(r))-1]
            #row!="" is here so that the delete row function can work
            if(index==num and row!=""):
                if(written):
                    file.write("\n" + row)
                else:
                    file.write(row)
            if(written):
                file.write("\n" + text)
            else:
                file.write(text)
            written = True
            index+=1
        if(index==num and row!=""):
            if(written):
                file.write("\n" + row)
            else:
                file.write(row)
    #update grid
    readGrid()
            

def deleteRow(num):
    insertRow(num,"",True)

def readGrid():
    with open("grid.txt") as file:
        #to make sure that the changes are saved
        global grid
        grid = file.read().split('\n')
        for i in range(0,len(grid)):
            grid[i] = grid[i].split(",")
            for j in range(0,len(grid[i])):
                if(grid[i][j]!=""):
                    grid[i][j] = int(grid[i][j])

def displayGrid():
    readGrid()
    for row in grid:
        print(row)

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
    if(start[1] >= len(grid) or end[1] >= len(grid)):
        print("Invalid starting or ending point, y position is out of bounds.")
        exit()
    if(start[0] >= len(grid[start[1]]) or end[0] >= len(grid[end[1]])):
        print("Invalid starting or ending point, x position is out of bounds.")
        exit()
    #case in which ending point is inside a wall
    if(grid[end[1]][end[0]]!=0):
        print("Invalid ending point, it must not be inside a wall.")
        exit()
    #dictionary to prevent going to previous squares
    locations = {}
    #use a tree to find path
    result = checkPath(start[0],start[1],"right",[],end,locations) or checkPath(start[0],start[1],"left",[],end,locations) or checkPath(start[0],start[1],"up",[],end,locations) or checkPath(start[0],start[1],"down",[],end,locations)
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
def checkPath(x,y,direction,directions,target,locations):
    #if the start is equal to the end, nothing needs to be done.
    if(x==target[0] and y==target[1]):
        print("The starting point is equal to the ending point. No pathfinding required.")
        exit()

    # # debugging check
    # print(x,y,grid[y],direction, directions)

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
        directions.append(direction)
        # # debugging check
        # print(x,y,grid[y],direction, directions)
        if(x==target[0] and y==target[1]):
            #once the spot is found return the required information
            return (directions)
        #prevent returning previous points to speed up performance and prevent infinite loops
        if(x,y) in locations:
            return False
        locations[(x,y)] = 1
        #use slicing (:) in order to create copies of the arrays to prevent recursive calls changing current call's array
        #use copy of the dictionary to make sure that changes made in the later calls won't affect previous calls
        #use extra condition to make sure that no resources are wasted backtracking and to prevent infinite recursing
        left = direction!="right" and checkPath(x,y,"left",directions[:],target,locations.copy())
        right = direction!="left" and checkPath(x,y,"right",directions[:],target,locations.copy())
        up = direction!="down" and checkPath(x,y,"up",directions[:],target,locations.copy())
        down = direction!="up" and checkPath(x,y,"down",directions[:],target,locations.copy())
        #the value of the function call can be assigned into a variable and used in a if statement despite the fact that it might not return a boolean because as long as the value is not false or 0, the value is evaluated as true
        #this way the array of directions can be passed up to the first function call
        #these statements below serve to check for shortest path from start to end by comparing the amount of directions followed
        shortest = left
        if(right):
            if(not shortest or len(right) < len(shortest)):
                shortest = right
        elif(up):
            if(not shortest or len(up) < len(shortest)):
                shortest = up 
        elif(down):
            if(not shortest or len(down) < len(shortest)):
                shortest = down
        #if all of the directions return false, then the value is shortest will be false
        return shortest
    else:
        #wall is in the way, return false
        return False

#The idea is:
#check all four directions
#if any direction is movable, move in that direction, else return false
#when receiving the value false, try moving in another direction
#when no direction can be moved in, the pathfinding is halted

main()