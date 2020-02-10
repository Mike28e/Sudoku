
import pygame
import time
import random
pygame.font.init()

class Box:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.val = None
        self.highlighted = False
        self.permanent = False
        self.good = None


def draw_board(window, Boxes):
    window.fill((255,255,255))
    pygame.draw.line(window, (0,0,0), (0, 50), (450, 50), 1)
    pygame.draw.line(window, (0,0,0), (50, 0), (50, 450), 1)

    pygame.draw.line(window, (0,0,0), (0, 100), (450, 100), 1)
    pygame.draw.line(window, (0,0,0), (100, 0), (100, 450), 1)

    pygame.draw.line(window, (0,0,0), (0, 150), (450, 150), 4)
    pygame.draw.line(window, (0,0,0), (150, 0), (150, 450), 4)

    pygame.draw.line(window, (0,0,0), (0, 200), (450, 200), 1)
    pygame.draw.line(window, (0,0,0), (200, 0), (200, 450), 1)

    pygame.draw.line(window, (0,0,0), (0, 250), (450, 250), 1)
    pygame.draw.line(window, (0,0,0), (250, 0), (250, 450), 1)

    pygame.draw.line(window, (0,0,0), (0, 300), (450, 300), 4)
    pygame.draw.line(window, (0,0,0), (300, 0), (300, 450), 4)

    pygame.draw.line(window, (0,0,0), (0, 350), (450, 350), 1)
    pygame.draw.line(window, (0,0,0), (350, 0), (350, 450), 1)

    pygame.draw.line(window, (0,0,0), (0, 400), (450, 400), 1)
    pygame.draw.line(window, (0,0,0), (400, 0), (400, 450), 1)

    pygame.draw.line(window, (0,0,0), (0, 450), (450, 450), 4)

    for i in range(9):
        for j in range(9):
            if Boxes[i][j].val != None:
                if Boxes[i][j].permanent == True:
                    cellVal = pygame.font.SysFont("comicsans", 40).render(str(Boxes[i][j].val), 1, (0,0,0))
                else:
                    cellVal = pygame.font.SysFont("comicsans", 40).render(str(Boxes[i][j].val), 1, (128,128,128))
                window.blit(cellVal, ((50 * i)+17,(50 * j)+15))
            if Boxes[i][j].highlighted == True:
                pygame.draw.rect(window, (255,128,0), ((i * 50), (j * 50), 50, 50), 2)
            elif Boxes[i][j].good == True:
                pygame.draw.rect(window, (0,255,0), ((i * 50), (j * 50), 50, 50), 2)
            elif Boxes[i][j].good == False:
                pygame.draw.rect(window, (255,0,0), ((i * 50), (j * 50), 50, 50), 2)

    

    

def draw_time(window, startTime):
    play_time = round(time.time() - startTime)
    window.blit(pygame.font.SysFont("comicsans", 30).render("Time: " + str(play_time), 1, (0,0,0)), (10,470))
    pygame.display.update()


def reset_selected(Boxes):
    for i in range(9):
        for j in range(9):
            Boxes[i][j].highlighted = False

def set_game_values(Boxes):

    filled = True
    
    for x in range(9):
        for y in range(9):
            if Boxes[x][y].val == None:
                filled = False
                numList = [1,2,3,4,5,6,7,8,9]

                for i in range(9):
                    num = random.choice(numList)
                    if verify(Boxes, num, x, y):
                        Boxes[x][y].val = num
                        Boxes[x][y].permanent = True
                        if set_game_values(Boxes):
                            return True
                        Boxes[x][y].val = None
                        Boxes[x][y].permanent = False
                        numList.remove(num)
                    else:
                        numList.remove(num)
                if len(numList) == 0 or Boxes[x][y].val == None:
                    return False
    if filled == True:
        return True
    return False

def clear_playable_values(Boxes):
    for i in range(3):
        for j in range(3):
            posList = [(x,y) for x in range((i*3),(i*3)+3) for y in range((j*3),(j*3)+3)]
            for _ in range(4):
                pos = random.choice(posList)
                Boxes[pos[0]][pos[1]].val = None
                Boxes[pos[0]][pos[1]].permanent = False
                posList.remove(pos)

    
def check_status(Boxes):
    for x in range(9):
        for y in range(9):
            if Boxes[x][y].permanent == False and Boxes[x][y].val != None:
                if verify(Boxes, Boxes[x][y].val, x, y):
                    Boxes[x][y].good = True
                else:
                    Boxes[x][y].good = False
    

def verify(Boxes, num, x, y):
    
    for i in range(9):
        if i != y and Boxes[x][i].val == num and Boxes[x][i].good != False:
            return False
    
    for j in range(9):
        if j != x and Boxes[j][y].val == num and Boxes[j][y].good != False:
            return False

    x_box = ((x//3) * 3)
    y_box = ((y//3) * 3)

    for boxPos_x in range(x_box, x_box + 3):
        for boxPos_y in range(y_box, y_box + 3):
            if boxPos_x != x and boxPos_y != y and Boxes[boxPos_x][boxPos_y].val == num and Boxes[boxPos_x][boxPos_y].good != False:
                return False

    return True
    
def main():
    window = pygame.display.set_mode((450,500))
    pygame.display.set_caption("Test App")
    window.fill((255,255,255))
    key = None
    x = -1
    y = -1

    Boxes = [[Box(i,j) for i in range(9)] for j in range(9)]
    set_game_values(Boxes)
    clear_playable_values(Boxes)
    
    startTime = time.time()
    running = True

    while running:
        draw_board(window, Boxes)
        draw_time(window, startTime)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    key = 1
                if event.key == pygame.K_2:
                    key = 2
                if event.key == pygame.K_3:
                    key = 3
                if event.key == pygame.K_4:
                    key = 4
                if event.key == pygame.K_5:
                    key = 5
                if event.key == pygame.K_6:
                    key = 6
                if event.key == pygame.K_7:
                    key = 7
                if event.key == pygame.K_8:
                    key = 8
                if event.key == pygame.K_9:
                    key = 9
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                x = pos[0] // (450 // 9)
                y = pos[1] // (450 // 9)
                key = None

            if x in range(9) and y in range(9):
                reset_selected(Boxes)
                Boxes[x][y].highlighted = True
                if key != None and Boxes[x][y].permanent == False:
                    Boxes[x][y].val = key

            check_status(Boxes)

main()
pygame.quit()

