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
    with open("grid.txt") as file:
        grid = file.read().split('\n')
        for i in range(0,len(grid)):
            grid[i] = grid[i].split(",")
        print(grid)

main()