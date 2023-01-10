# coding=UTF-8
# File: Snake.py
# SOftware: PyCharm
# time: 2021-07-21 9:22 p.m.
import random
import sys
import pygame   #(pygame)
import copy
import colorama
colorama.init(autoreset=True)
pygame.init()

f = open("settings.txt")
lines = f.read()
f.close()
dict1 = eval(lines)
print(dict1)

'''    setting argument '''
each_len = dict1['LengthOfACell']            #each units length  (Data representation - good variable names and types)
width_units = dict1['MapWidth']    #black screen width units
height_units = dict1['MapHeight']    #black screen height units
text_screen_color = "white" #text background colour
snake_x = 2  #beginning, snake head's x coordinate
snake_y = height_units//2  #beginning, snake head's y coordinate        int(((height/each_len))//2)
text_color = dict1['TextColor']    #Set text colour
text_color_random = False #random text colour
FPs = dict1['MovingSpeed']   #snake movement FPs
FPs1 = 0   #restart button movement FPs


text_screen_length = int((each_len*width_units)//2)  #text screen width is half of black screen width
width, height = width_units*each_len,height_units*each_len
size = width + text_screen_length,height
lr_interval = int(text_screen_length//10)
td_interval = int(height//5)
text_size = min(lr_interval,td_interval)
clock = pygame.time.Clock()  # FPs
snake_list = []                    # storage snake head and body location   (lists)
pretailturn = False
t = 2
# vertical snake body
snakebody_vertical = pygame.image.load("images/snakebodyHori.jpg") #add picture of vertical snake body   (picture files)
snakebody_vertical = pygame.transform.scale(snakebody_vertical, (each_len,each_len)) #size the picture
# transverse snake body
snakebody_transverse = pygame.image.load("images/snakebodyVer.png") #add picture of transverse snake body
snakebody_transverse = pygame.transform.scale(snakebody_transverse, (each_len,each_len))  #size the picture
# food
food = pygame.image.load("images/food.jpg")
food = pygame.transform.scale(food, (each_len,each_len))

#picture of snake head direction
snakehead_front = pygame.image.load("images/snakeheadUp.jpg")
snakehead_down = pygame.image.load("images/snakeheadDown.png")
snakehead_left = pygame.image.load("images/snakeheadLeft.png")
snakehead_right = pygame.image.load("images/snakeheadRight.png")
snakehead_front = pygame.transform.scale(snakehead_front, (each_len,each_len))
snakehead_down = pygame.transform.scale(snakehead_down, (each_len,each_len))
snakehead_left = pygame.transform.scale(snakehead_left, (each_len,each_len))
snakehead_right = pygame.transform.scale(snakehead_right, (each_len,each_len))

#picture of snake body while turning
snaketurn_topleft = pygame.image.load("images/snaketurnLeftUp.png")
snaketurn_topleft = pygame.transform.scale(snaketurn_topleft,(each_len,each_len))

snaketurn_topright = pygame.image.load("images/snaketurnRightUp.png")
snaketurn_topright = pygame.transform.scale(snaketurn_topright,(each_len,each_len))

snaketurn_buttomleft = pygame.image.load("images/snaketurnLeftDown.png")
snaketurn_buttomleft = pygame.transform.scale(snaketurn_buttomleft,(each_len,each_len))

snaketurn_bottomright = pygame.image.load("images/snaketurnRightDown.jpg")
snaketurn_bottomright = pygame.transform.scale(snaketurn_bottomright,(each_len,each_len))

text_screen = pygame.image.load("colors\\{}.png".format(text_screen_color))
text_screen = pygame.transform.scale(text_screen,(text_screen_length,height))

#create a 2-dimensional list as map to mark to snake and food
def create_a_map(transverse,vertical,each_size):
    map_List = []
    currect = []
    for _ in range(vertical//each_size):
        for _ in range(transverse//each_size):
            currect.append(0)
        map_List.append(currect)
        currect = []
    return map_List


def price(a,b):
    x1,y1 = a[0],a[1]                                                 #calculate my current point to destination steps
    x2,y2 = b[0],b[1]
    return abs(x1 - x2) + abs(y1 - y2)

def price2(x1,y1,x2,y2):
    return abs(x1 - x2) + abs(y1 - y2)

def price1(path):
    index = len(path) -1                                              #calculate my current point to start point steps
    priceOfNow = 1
    while path[index][2] != -1:
        priceOfNow += 1
        index = path[index][2]
    return priceOfNow

dirs = [            #direction list
    lambda x,y : (x-1,y),   #left
    lambda x,y : (x+1,y),   #right
    lambda x,y : (x,y-1),   #down
    lambda x,y : (x,y+1)    #up
]


def Draw_Food(trans,verti): #Draw food
    trans = trans*each_len
    varti = verti*each_len
    screen.blit(food,(trans,varti))

# A* search algorithm
def Astar_of_loop(x1, y1, x2, y2,mize1,windowtrans,windowverti):
    if x1 + 1 == x2 and y1 == y2 and x1 == 0 and mize1[1][y1] != 0:
        return False
    else:
        pass
    if x1 - 1 == x2 and y1 == y2 and x1 == windowverti -1 and mize1[windowverti-2][y1] != 0:
        return False
    else:
        pass
    if x1 == x2 and y1 + 1 == y2 and y1 == 0 and mize1[x1][1] != 0:
        return False
    else:
        pass
    if x1 == x2 and y1  - 1== y2 and y1 == windowtrans -1 and mize1[x1][windowtrans-2] != 0:
        return False
    else:
        pass
    mize = copy.deepcopy(mize1)
    path = []  # Store all the paths the snake has took
    current = []  # Store the current moveable location for filtering the shortest price path
    current.append((x1, y1, -1, price((x1, y1), (x2, y2))))  # List the starting point, parent index, and its price
    mize[x1][y1] = 1
    while len(current):  # When there's still room to move
        current.sort(key=lambda x: x[3], reverse=True)  # In order of price, the smallest is at the end
        nowNode = current.pop()  #NowNode is stored  the shortest price location to the destination

        path.append(nowNode)  # Store the location, parent index, and price of the current path into path list
        if nowNode[0] == x2 and nowNode[1] == y2:  # If the current node is the same as the destination
            return True #return True
        for dir in dirs:   #Try the four directions of the current position
            nextNode = dir(nowNode[0], nowNode[1])
            if nextNode[0] >=0 and nextNode[0] < windowverti and nextNode[1] >=0 and nextNode[1] < windowtrans and mize[nextNode[0]][nextNode[1]] == 0:  # 如果可以移动(0为可移动地点)
                current.append((nextNode[0], nextNode[1], len(path) - 1, price(nextNode, (x2, y2)) + price1(path)))
                mize[nextNode[0]][nextNode[1]] = t
    else:
        return False

#Snake head and snake body drawing function
"------------------------------------------------------------------------------------------------------------------------------"
"------------------------------------------------------------------------------------------------------------------------------"
"------------------------------------------------------------------------------------------------------------------------------"
"------------------------------------------------------------------------------------------------------------------------------"
"------------------------------------------------------------------------------------------------------------------------------"
def Draw_snake_head_right(trans,verti):
    screen.blit(snakehead_right,(trans*each_len,verti*each_len))

def Draw_snake_body_trans(trans,verti):
    screen.blit(snakebody_transverse,(trans*each_len,verti*each_len))

def Draw_snake_head_left(trans,verti):
    screen.blit(snakehead_left,(trans*each_len,verti*each_len))

def Draw_snake_head_up(trans,verti):
    screen.blit(snakehead_front,(trans*each_len,verti*each_len))

def Draw_snake_head_down(trans,verti):
    screen.blit(snakehead_down,(trans*each_len,verti*each_len))

def Draw_snake_body_verti(trans,verti):
    screen.blit(snakebody_vertical,(trans*each_len,verti*each_len))

def Draw_snake_turn_topleft(trans,verti):
    screen.blit(snaketurn_topleft,(trans*each_len,verti*each_len))

def Draw_snake_turn_topright(trans,verti):
    screen.blit(snaketurn_topright,(trans*each_len,verti*each_len))

def Draw_snake_turn_bottomleft(trans,verti):
    screen.blit(snaketurn_buttomleft,(trans*each_len,verti*each_len))

def Draw_snake_turn_bottomright(trans,verti):
    screen.blit(snaketurn_bottomright,(trans*each_len,verti*each_len))


#Create food in 2D list
def CreateFood(map):
    blank = []
    for i in range(len(map)):
        for j in range(len(map[i])):
            if map[i][j] == 0:
                blank.append([i,j])
    food_loca = random.choice(blank)
    food_loca_verti = food_loca[0]
    food_loca_trans = food_loca[1]
    return food_loca_trans,food_loca_verti

#Draw snakes on the screen
def control_Draw_snake(snakelist,tailturn,append,endturn, lo, prelo):
    global pretailturn
    if (prelo == lo):
        tailturn = pretailturn
    else:
        pretailturn = tailturn
    #Draw head
    if snakelist[0][0] != snakelist[1][0]:
        if snakelist[0][0] < snakelist[1][0]: #left
            Draw_snake_head_left(snakelist[0][0],snakelist[0][1])

        else:
            Draw_snake_head_right(snakelist[0][0],snakelist[0][1]) #right
    elif snakelist[0][1] != snakelist[1][1]:
        if snakelist[0][1] < snakelist[1][1]:
            Draw_snake_head_up(snakelist[0][0],snakelist[0][1]) #up

        else:
            Draw_snake_head_down(snakelist[0][0],snakelist[0][1]) #down
    #Draw Tail
    #if the last one snake body turn , and the snake length no increase(when eat the food, the length will plus 1)
    if tailturn and not append:
        if tailturn == 'topleft':
            Draw_snake_turn_topleft(snakelist[-1][0], snakelist[-1][1])
            endturn = 'topleft'
        elif tailturn == 'topright':
            Draw_snake_turn_topright(snakelist[-1][0], snakelist[-1][1])
            endturn = 'topright'
        elif tailturn == 'bottomleft':
            Draw_snake_turn_bottomleft(snakelist[-1][0], snakelist[-1][1])
            endturn = 'bottomleft'
        else:
            Draw_snake_turn_bottomright(snakelist[-1][0], snakelist[-1][1])
            endturn = 'bottomright'

    elif endturn and append:
        if endturn == 'topleft':
            Draw_snake_turn_topleft(snakelist[-1][0], snakelist[-1][1])
        elif endturn == 'topright':
            Draw_snake_turn_topright(snakelist[-1][0], snakelist[-1][1])
        elif endturn == 'bottomleft':
            Draw_snake_turn_bottomleft(snakelist[-1][0], snakelist[-1][1])
        else:
            Draw_snake_turn_bottomright(snakelist[-1][0], snakelist[-1][1])
            endturn = 'bottomright'
    else:
        if snakelist[-1][0] == snakelist[-2][0]:
            Draw_snake_body_verti(snakelist[-1][0], snakelist[-1][1])
            endturn = False
        else:
            Draw_snake_body_trans(snakelist[-1][0], snakelist[-1][1])
            endturn = False
    #Draw Snake body
    for i in range(1,len(snakelist)-1):
        #if turn
        if snakelist[i -1][0] != snakelist[i+1][0] and snakelist[i -1][1] != snakelist[i+1][1]:
            if (snakelist[i][0] > snakelist[i-1][0] and snakelist[i][1] > snakelist[i+1][1]) or (snakelist[i][0] > snakelist[i+1][0] and snakelist[i][1] > snakelist[i-1][1]):
                Draw_snake_turn_topleft(snakelist[i][0],snakelist[i][1])
                tailturn = 'topleft'
            elif (snakelist[i][0] < snakelist[i-1][0] and snakelist[i][1] < snakelist[i+1][1]) or (snakelist[i][0] < snakelist[i+1][0] and snakelist[i][1] < snakelist[i-1][1]):
                Draw_snake_turn_bottomright(snakelist[i][0],snakelist[i][1])
                tailturn = 'bottomright'
            elif (snakelist[i][0] > snakelist[i-1][0] and snakelist[i][1] < snakelist[i+1][1]) or (snakelist[i][0] > snakelist[i+1][0] and snakelist[i][1] < snakelist[i-1][1]):
                Draw_snake_turn_bottomleft(snakelist[i][0],snakelist[i][1])
                tailturn = 'bottomleft'
            else:
                Draw_snake_turn_topright(snakelist[i][0],snakelist[i][1])
                tailturn = 'topright'
        #if not turn
        elif snakelist[i][0] == snakelist[i-1][0] == snakelist[i+1][0]:
            Draw_snake_body_verti(snakelist[i][0],snakelist[i][1])
            tailturn = False
        else:
            Draw_snake_body_trans(snakelist[i][0], snakelist[i][1])
            tailturn = False
    return tailturn,endturn,snakelist[0]

# A* search algorithm, try to find the food location
def Astar_findthefood(x1, y1, x2, y2,snake_list1,map,windowtrans,windowverti,each_len):
    snake_list = copy.deepcopy(snake_list1)
    mize = copy.deepcopy(map)
    mize1 = create_a_map(width,height,each_len)
    path = []
    realpath = []

    current = []
    current.append((x1, y1, -1, price((x1, y1), (x2, y2))))
    while len(current):
        current.sort(key=lambda x: x[3], reverse=True)
        nowNode = current.pop()
        path.append(nowNode)
        if nowNode[0] == x2 and nowNode[1] == y2:
            right = nowNode
            while right[2] != -1:
                realpath.append((right[0], right[1]))
                right = path[right[2]]
            nextstep = realpath[-1]
            if right[0] > nextstep[0] and right[1] == nextstep[1]:
                direction = 'up'
            elif right[0] < nextstep[0] and right[1] == nextstep[1]:
                direction = 'down'
            elif right[0] == nextstep[0] and right[1] < nextstep[1]:
                direction = 'right'
            else:
                direction = 'left'
            for i in snake_list:
                i[0],i[1] = i[1],i[0]
            realpath += snake_list
            after_eat_location = realpath[0:len(snake_list)]
            to_reach = realpath[len(snake_list)]
            for i in after_eat_location:
                mize1[i[0]][i[1]] = 1
            aftercanfindtail = Astar_of_loop(after_eat_location[0][0],after_eat_location[0][1],to_reach[0],to_reach[1],mize1,windowtrans,windowverti)
            return True,direction,aftercanfindtail
        for dir in dirs:
            nextNode = dir(nowNode[0], nowNode[1])
            if nextNode[0] >=0 and nextNode[0] < windowverti and nextNode[1] >=0 and nextNode[1] < windowtrans and mize[nextNode[0]][nextNode[1]] == 0:  # 如果可以移动(0为可移动地点)
                current.append((nextNode[0], nextNode[1], len(path) - 1, price(nextNode, (x2, y2)) + price1(path)))
                mize[nextNode[0]][nextNode[1]] = t

    else:
        return False,None,'LEFT'

#The snake took its longest step towards its tail
def SnakeAwayFromTail(snake_list,windowtrans,windowverti,mize):
    map = copy.deepcopy(mize)
    list1 = []
    snake_list1 = copy.deepcopy(snake_list)
    x1 = snake_list1[0][1]              #8
    x2 = snake_list1[0][0]              #0
    y3 = snake_list1[-1][1]             #15
    y4 = snake_list1[-1][0]             #7
    map[x1][x2] = 1
    #map[y3][y4] = 0
    if x2 -1 >= 0 and map[x1][x2-1] == 0:
        left = price2(x1,x2-1,y3,y4)
        list1.append(('left',left))
    if x2 + 1 < windowtrans and map[x1][x2+1] == 0:
        right = price2(x1,x2+1,y3,y4)
        list1.append(('right',right))
    if x1-1 >=0 and map[x1-1][x2] == 0:
        up = price2(x1-1,x2,y3,y4)
        list1.append(('up',up))
    if x1 + 1 < windowverti and map[x1+1][x2] == 0:
        down = price2(x1+1,x2,y3,y4)
        list1.append(('down',down))
    list1.sort(key=lambda x:x[1],reverse=True)
    for i in list1:
        if i[0] == 'left':
            if Astar_of_loop(x1,x2-1,y3,y4,map,windowtrans,windowverti):
                return 'left'
            else:
                continue
        elif i[0] == 'right':

            if Astar_of_loop(x1, x2 + 1, y3, y4, map,windowtrans,windowverti):
                return 'right'
            else:
                continue
        elif i[0] == 'up':
            if Astar_of_loop(x1-1, x2, y3, y4, map,windowtrans,windowverti):
                return 'up'
            else:
                continue
        elif i[0] == 'down':
            if Astar_of_loop(x1+1, x2, y3, y4, map,windowtrans,windowverti):
                return 'down'
            else:
                continue
    return 'LEFT'
#Take a random step to a location
def TakeAStepAnywhere(snake_list,windowtran,windowver,map):
    head = snake_list[0]
    randomlist = []
    if head[0]-1 >= 0 and map[head[1]][head[0] - 1] == 0: #(if statement)
        randomlist.append('left')
    if head[0]+1 < windowtran and map[head[1]][head[0] + 1] == 0:
        randomlist.append('right')
    if head[1] - 1 >= 0 and map[head[1] - 1][head[0]] == 0:
        randomlist.append('up')
    if head[1] + 1 < windowver and map[head[1] + 1][head[0]] == 0:
        randomlist.append('down')
    return random.choice(randomlist)

#Determine if the snake can move
def SnakeCanMove(map,snake_list,windowtrans,windowverti,):
    nowhead = snake_list[0]
    if nowhead[0] - 1 >= 0 and map[nowhead[1]][nowhead[0]-1] in [0,4]:
        return True
    if nowhead[0] + 1 < windowtrans and map[nowhead[1]][nowhead[0]+1] in [0,4]:
        return True
    if nowhead[1]  -1 >= 0 and map[nowhead[1] - 1][nowhead[0]] in [0,4]:
        return True
    if nowhead[1] + 1 < windowverti and map[nowhead[1] + 1][nowhead[0]] in [0,4]:
        return True
    return 0

# Use the function above to calculate which direction the snake should go
def get_direction(map,snake_list,windowtrans,windowverti,foodtrans,foodverti,each_len):
    snake_list1 = copy.deepcopy(snake_list)
    mize = create_a_map(width,height,each_len)
    for i in range(1, len(snake_list) - 1):
        mize[snake_list[i][1]][snake_list[i][0]] = 1

    #if snake can move
    if SnakeCanMove(map,snake_list,windowtrans,windowverti):
        headpoint = snake_list[0]
        Candindthefood,direction,aftercanfindtail = Astar_findthefood(headpoint[1], headpoint[0], foodverti, foodtrans,snake_list,map,windowtrans,windowverti,each_len)
        # If snakes can find food
        if Candindthefood:
            #If can find the tail after eating the food
            if aftercanfindtail:
                #The snake took its longest step towards its tail
                return direction
            # else, The snake takes one step towards its tail on the longest path
            else:
                direction = SnakeAwayFromTail(snake_list1,windowtrans,windowverti,mize)
                return direction
        # If a snake could move and find no food, it could find its tail
        elif Astar_of_loop(headpoint[1], headpoint[0], snake_list1[-1][1],snake_list1[-1][0],mize,windowtrans,windowverti):

            #The snake takes one step towards its tail on the longest path
            direction = SnakeAwayFromTail(snake_list1,windowtrans,windowverti,mize)
            return direction

        # If can move, but food and tail are not found
        else:
            # Take a step anywhere
            direction = TakeAStepAnywhere(snake_list,windowtrans,windowverti,map)
            return direction

    #if can't move, pass
    else:
        pass

#Check to see if you have a right mouse click
def check_right_mouse(event):
    front = event.index("{")
    end = event.rindex("}")
    dict1 = eval(event[front:end + 1])
    if dict1['button'] == 3:
        if auto == False:
            print("Automatic pathfinding...")
        else:
            print("Manual mode start...")
        return True
    else:
        return False
if __name__  == '__main__':
    #Pygame initialization
    pygame.init()

    #Create window , window title by pygame
    screen = pygame.display.set_mode((size))
    pygame.display.set_caption("Snake Game")
    black = 0, 0, 0


    while True:  #(loops)
        if text_color_random:
            text_color = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)  #(random value)
        snake_list = []  # Store the coordinates of the snake's head and body
        head_loca_tran = snake_x  # The horizontal coordinate of the snake's head when start
        head_loca_vert = snake_y  # The y coordinate of the snake's head when start
        t = 2 #Mark up the two-dimensional list(the  map) of variables representing the body of the snake
        map = create_a_map(width, height, each_len) #Create a 2-d list for the map
        Draw_snake_head_right(head_loca_tran, head_loca_vert)  #draw the snake head
        Draw_snake_body_trans(head_loca_tran - 1, head_loca_vert) #draw the snake body
        Draw_snake_body_trans(head_loca_tran - 2, head_loca_vert) #draw the snake tail

        #Add the coordinates of the snake's head, body, and tail to the snake list
        snake_list.append([head_loca_tran, head_loca_vert])
        snake_list.append([head_loca_tran - 1, head_loca_vert])
        snake_list.append([head_loca_tran - 2, head_loca_vert])
        headLocation = snake_list[0]
        preheadLocation = []
        #Write the position of the snake's head, body and tail into the 2D list
        map[head_loca_vert][head_loca_tran] = 3
        map[head_loca_vert][head_loca_tran - 1] = 2
        map[head_loca_vert][head_loca_tran - 2] = 4

        #Create a food coordinates
        trans, verti = CreateFood(map)
        #Draw the food on the screen
        Draw_Food(trans, verti)

        tailturn = False #record the snake last body if it need to turn drection and the drection
        endturn = False  #record the snake tail if it need to turn drection and the drection
        eatself = False #If snake eat itself(when snake head coordinate in equal the any snake body, that meant snake eat itself)
        run = False  # the program is stop or running
        direction = 'right'  # The direction in which the snake first moved
        Food = True  # if have a food (when snake eat the food, it would turn False)
        auto = False  # if the snake is run automaticly
        append = False  # when the snake eat the food, snake length + 1, append is True, when the snake not eat the food, append is False
        win = False     #if you win the game
        restart_game = False    #if you click the restart button to restart the game
        #Draw the text screen
        screen.blit(text_screen,(width,0)) #(output)
        # Create the object of Sound (when snake eat the food, play the sound)
        eat_noise = pygame.mixer.Sound("sounds/sound.wav")
        eat_noise.set_volume(0.2)
        #Create the object of texts
        font = pygame.font.Font("font/simsun.ttc", text_size)
        text = font.render("Automatic: {}".format(str(auto)), True, (text_color))
        font1 = pygame.font.Font("font/simsun.ttc", text_size)
        text1 = font1.render("Program: {}".format("Running" if run else "Stop"), True, (text_color))
        font2 = pygame.font.Font("font/simsun.ttc", text_size)
        text2 = font2.render("SnakeLength: {}".format(len(snake_list)), True, (text_color))
        #set to location of the text on the screen
        screen.blit(text,(width + lr_interval, td_interval))
        screen.blit(text1,(width + lr_interval,td_interval * 2 + text_size))
        screen.blit(text2,(width + lr_interval,td_interval * 3 + text_size))
        #display the snake and food on the screen
        pygame.display.update()
        #display the text on the screen
        pygame.display.flip()

        #while the snake not eat itself
        while not eatself:
            #if text color random == True, take a random colour of the texts
            if text_color_random:
                text_color = random.randint(0,255),random.randint(0,255),random.randint(0,255)
            clock.tick(FPs)  #Set the FPs
            #get the event of your keyboard and mouse
            for event in pygame.event.get():  #(get user input)
                #if you click the Quit Button(the X in top right corner)
                if event.type == pygame.QUIT:
                    #exit the program
                    sys.exit()
                #1025 is you click the mouse
                elif event.type == 1025:
                    #check your check right mouse or left mouse
                    if check_right_mouse(event.__str__()):
                        #if check right mouse, open/close the automatic mode
                        auto = not auto
                    else:
                        #if check left mouse, run/stop the program
                        run = not run
                        if run:
                            print("\033[0:34mStart Running...\033[m")
                        else:
                            print("\033[0:34mPausing...\033[m")
                #if If the keyboard is pressed and running and not in automatic mode
                if event.type == pygame.KEYDOWN and run and not auto:
                    #1073741906 is W, and 119 is up arrow
                    if event.key == 1073741906 or event.key == 119:
                        #if last direction == down, it meant if snake go up it would eat itself, so we need to check it
                        if direction != 'down':
                            direction = 'up'
                    #1073741904 is Am and 97 is left arrow
                    elif event.key ==  1073741904 or event.key == 97:
                        if direction != 'right':
                            direction = 'left'
                    #same to above, down
                    elif event.key ==  1073741905 or event.key == 115:
                        if direction != 'up':
                            direction = 'down'
                    #same to above, right
                    elif event.key ==  1073741903 or event.key == 100:
                        if direction != 'left':
                            direction = 'right'

            #refresh the texts
            text = font.render("Automatic: {}".format(str(auto)), True, (text_color))
            text1 = font1.render("Program: {}".format("Running" if run else "Stop"), True, (text_color))
            text2 = font2.render("SnakeLength: {}".format(len(snake_list)), True, (text_color))
            #refresh the screen background
            screen.fill(black)
            #Update and Draw the sanke
            control_Draw_snake(snake_list, tailturn, append, endturn,headLocation, preheadLocation)
            #Draw the texts
            screen.blit(text_screen, (width, 0))
            screen.blit(text, (width + lr_interval, td_interval))
            screen.blit(text1, (width + lr_interval, td_interval * 2 + text_size))
            screen.blit(text2, (width + lr_interval, td_interval * 3 + text_size))
            #Update and Draw the dood
            Draw_Food(trans,verti)
            #display the texts, snake and food after update
            pygame.display.flip()
            pygame.display.update()
            #if program is running and have a food on the map
            if run and Food:
                #if text color random is True, rechoice the colour.
                if text_color_random:
                    text_color = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
                #copy to map
                map1 = copy.deepcopy(map)
                #if automatic now
                if auto:
                    #get the direction by calculate
                    direction = get_direction(map1,snake_list,width//each_len,height//each_len,trans,verti,each_len)
                #according to direction to update the snake head coordinate
                if direction == 'left':
                    head_loca_tran -= 1
                elif direction == 'right':
                    head_loca_tran += 1
                elif direction == 'up':
                    head_loca_vert -= 1
                elif direction == 'down':
                    head_loca_vert += 1
                #if snake head out of the screen , break the program
                if head_loca_tran < 0 or head_loca_tran >= width//each_len:
                    break
                elif head_loca_vert < 0 or head_loca_vert >= height//each_len:
                    break
                #insert the snake head coordinate to the snake list at the front
                snake_list.insert(0,[head_loca_tran, head_loca_vert])
                headLocation = snake_list[0]
                #update the map, 3 is snake head, 2 is snake body
                map[head_loca_vert][head_loca_tran] = 3
                map[snake_list[1][1]][snake_list[1][0]] = 2
                #if snake head coordinate is equal to food coordinate
                if head_loca_tran == trans and head_loca_vert == verti:
                    # Food = False, meant no food
                    Food = False
                    #play the eat sound
                    eat_noise.play()
                    #append = True, meant snake length need to plus 1
                    append = True
                #if snake not eat the food
                else:
                    #delete the last coordinate in the snake list,  The penultimate coordinate is changed to the coordinate of the snake's tail, and append = False meant the length of the snake remains the same
                    x = snake_list.pop()
                    map[x[1]][x[0]] = 0
                    map[snake_list[-1][1]][snake_list[-1][0]] = 4
                    append = False

                #update the screen and sanke
                screen.fill(black)

                screen.blit(text_screen, (width, 0))

                tailturn,endturn,preheadLocation = control_Draw_snake(snake_list,tailturn,append,endturn, headLocation,preheadLocation)

                #if not food
                if not Food:
                    #try to create a Food, if can create a food
                    try:
                        trans,verti = CreateFood(map)
                        #Add the food to the map
                        map[verti][trans] = 0
                        #Draw the food
                        Draw_Food(trans,verti)
                        #output "create food, Location: (coordinate)"
                        print(colorama.Fore.RED+"create food. location: {} {}".format(trans,verti))
                        #Food = True, meant have food now
                        Food = True
                    #if can't create a food, that meant the map was filled by snake, then you win!
                    except:
                        #win = True and break the program
                        win = True
                        break
                else:
                    #if have food, draw the food
                    Draw_Food(trans,verti)
                #update the texts, food, snake...
                text = font.render("Automatic: {}".format(str(auto)), True, (text_color))
                text1 = font1.render("Program: {}".format("Running" if run else "Stop"), True, (text_color))
                text2 = font2.render("SnakeLength: {}".format(len(snake_list)), True, (text_color))
                screen.blit(text, (width + lr_interval, td_interval))
                screen.blit(text1, (width + lr_interval, td_interval * 2 + text_size))
                screen.blit(text2, (width + lr_interval, td_interval * 3 + text_size))
                pygame.display.flip()
                pygame.display.update()
                # save snake head coordinate in the veriable - currect
                currect = [head_loca_tran, head_loca_vert]
                #if snake head coordinate in snake , meant snake eat itself
                if currect in snake_list[1::]:
                    eatself = True

        #when the game over or win
        #if text color random, rechoice the color again
        if text_color_random:
            text_color = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
        #auto and run change to False, bucause the snake game is over.
        auto = False
        run = False
        #set the restart button length
        button_length = min(width,height)//5
        #load the restart button image
        restart = pygame.image.load("images/restart3.png")
        #Set the size
        restart1 = pygame.transform.scale(restart, (button_length, button_length))

        # The top left corner coordinate of restart button
        location = restart1.get_rect()
        left = width // 2 - button_length // 2  #
        top = height // 2 - button_length // 2
        # move the restart button to the screen middle
        location = location.move(left,top)
        #if the game win
        if win:
            # the picture is "win!!"
            game_over = pygame.image.load("images/win.png")  # source : pngfree -> praying
        else:
            #if the game over, this picturn is "game over"
            game_over = pygame.image.load("images/game_over4.png")   #source : pngfree -> Khalilur Rahman
        #Set the game over/win picture size , size is the screen_length * 4/5 by screen_length * 4/5
        game_over1 = pygame.transform.scale(game_over, (button_length *  4, button_length * 4))
        #move the game over/win picture to the middle of screen
        location_game_over = game_over1.get_rect()
        location_game_over = location_game_over.move(width // 2 - (button_length *  2 // 1),height // 2 - (button_length *  2 // 1))
        #display text screen , game over/win and restart button
        screen.blit(text_screen, (width, 0))
        screen.blit(game_over1, location_game_over)
        screen.blit(restart1, (left, top))
        #refresh the content of texts
        text = font.render("Automatic: {}".format(str(auto)), True, (text_color))
        text1 = font1.render("Program: {}".format("Running" if run else "Stop"), True, (text_color))
        text2 = font2.render("SnakeLength: {}".format("--"), True, (text_color))
        screen.blit(text, (width + lr_interval, td_interval))
        screen.blit(text1, (width + lr_interval, td_interval * 2 + text_size))
        screen.blit(text2, (width + lr_interval, td_interval * 3 + text_size))
        #update screen
        pygame.display.flip()
        pygame.display.update()
        # Start the loop, when you click the restart the button or exit the program , break the loop
        while True:
            #change text color if it is randomly
            if text_color_random:
                text_color = random.randint(0,255),random.randint(0,255),random.randint(0,255)
            #update the screen
            screen.fill(black)
            clock.tick(FPs1)
            control_Draw_snake(snake_list,tailturn,append,endturn, headLocation, preheadLocation)
            screen.blit(text_screen, (width, 0))
            screen.blit(game_over1,location_game_over)
            screen.blit(restart1,(left,top))
            #get the position of your mouse
            loca_of_mouse = pygame.mouse.get_pos()
            for event in pygame.event.get():
                # same to above
                if event.type == pygame.QUIT:
                    sys.exit()
                #if clicked the mouse
                if event.type == 1025:
                    # If the click is less than 20 away from the Restart button
                    if loca_of_mouse[0] >= left - 20 and loca_of_mouse[0] - left <= button_length + 20 and loca_of_mouse[
                        1] >= top - 20 and loca_of_mouse[1] - top <= button_length + 20:
                        #restart the game
                        restart_game = True
            # If the mouse position(but not click down) is less than 20 away from the Restart button
            if FPs1 != 0 and loca_of_mouse[0] >= left - 20 and loca_of_mouse[0] - left <= button_length + 20 and loca_of_mouse[1] >= top - 20 and loca_of_mouse[1] - top <= button_length + 20:
                #reset the restart button coordinate
                left = random.randint(0,width - button_length)
                top = random.randint(0,height - button_length)

            #update the screen
            screen.blit(text_screen, (width, 0))
            text = font.render("Automatic: {}".format(str(auto)), True, (text_color))
            text1 = font1.render("Program: {}".format("Running" if run else "Stop"), True, (text_color))
            text2 = font2.render("SnakeLength: {}".format("--"), True, (text_color))
            screen.blit(text, (width + lr_interval, td_interval))
            screen.blit(text1, (width + lr_interval, td_interval * 2 + text_size))
            screen.blit(text2, (width + lr_interval, td_interval * 3 + text_size))
            pygame.display.flip()
            pygame.display.update()

            #if restart game == True, break the loop
            if restart_game == True:
                print("Restarting...")
                screen.fill(black)
                break


