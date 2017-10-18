#snake
import pygame
import sys
import random
import time

check_errors = pygame.init()

#     number of error
# (6,0)
if check_errors[1]>0:
    print("(!) Had {0} initializing errors, exiting...".format(check_errors[1]))
    sys.exit()
else:
    print("(+) PyGame sucessfully initialized ")
clock = pygame.time.Clock()
#screen
playSurface = pygame.display.set_mode((720,460))
pygame.display.set_caption(" Snake Classic ")
disp_width = 720
disp_height = 460

#colors             (r,g,b)
bright_red = pygame.Color(255, 0, 0)
bright_green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255) 
red = pygame.Color(200,0,0)
green = pygame.Color(0,200,0)
black = pygame.Color(0,0,0)
white = pygame.Color(255,255,255)
brown = pygame.Color(165,42,42)

#frame per second controller
playSurface.fill(white)
pygame.display.update()


#game over

def gameOver():
    myFont = pygame.font.SysFont('monaco' , 72)
    GOsurf= myFont.render('Game Over!' , True , red)
    GOrect = GOsurf.get_rect()
    GOrect.midtop = (360,150)
    playSurface.blit(GOsurf , GOrect)
    pygame.display.update()
    time.sleep(3)
    game_intro()


def showScore(choice = 1 ):
    sFont = pygame.font.SysFont('monaco' , 40)
    Ssurf= sFont.render('Score: '+str(score) , True , black)
    Srect = Ssurf.get_rect()
    if choice ==1:
        Srect.midtop = (80,10)
    else:
        Srect.midtop = (360,210)
    playSurface.blit(Ssurf , Srect)

def quit_game():
    pygame.quit()
    quit()    

def button(msg, x, y, w, h, ic, ac, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()


    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(playSurface, ac, (x, y, w, h))
        if action!=None  and click[0]==1:
            action()
    else:
        pygame.draw.rect(playSurface, ic, (x, y, w, h))

    smallText = pygame.font.Font("freesansbold.ttf", 15)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ((x + w / 2), (y + h / 2))
    playSurface.blit(textSurf, textRect)


def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()


def message_display(text):
    largeText = pygame.font.Font('freesansbold.ttf', 80)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((disp_width / 2), (disp_height / 2))
    playSurface.blit(TextSurf, TextRect)

    pygame.display.update()

    time.sleep(2)

    game_intro()


def game_intro():

    intro = True
    while intro:

        for events in pygame.event.get():

            if events.type == pygame.QUIT:
                quit_game()

        playSurface.fill(white)
        pygame.draw.rect(playSurface, red, [200, 600, 30, 70])
        largeText = pygame.font.Font('freesansbold.ttf', 80)
        TextSurf, TextRect = text_objects(' Snake Classic ', largeText)
        TextRect.center = ((disp_width / 2), (disp_height / 2 -50))
        playSurface.blit(TextSurf, TextRect)

        mouse = pygame.mouse.get_pos()


        button("PLAY", 110, 350, 80, 40, green, bright_green , game_loop)
        button("QUIT", 530, 350, 80, 40, red, bright_red, quit_game)

        pygame.display.update()

        clock.tick(15)

#game loop
def game_loop():
    global clock , fpsController , score
    clock = pygame.time.Clock()
    fpsController = pygame.time.Clock()
    snakePos = [100,50]
    snakeBody = [[100,50],[90,50],[80,50]]
    speed=10
    foodPos = [random.randrange(1,72)*10 , random.randrange(1,46)*10]
    foodSpawn = True
    score=0 
    direction = 'RIGHT'
    changeto = direction


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT or event.key == ord('d'):
                    changeto = 'RIGHT'
                if event.key == pygame.K_LEFT or event.key == ord('a'):
                    changeto = 'LEFT'            
                if event.key == pygame.K_UP or event.key == ord('w'):
                    changeto = 'UP'
                if event.key == pygame.K_DOWN or event.key == ord('d'):
                    changeto = 'DOWN'
                if event.key == pygame.K_ESCAPE :
                    pygame.event.post(pygame.event.Event(pygame.QUIT))
        #validate the direction
        if changeto =='RIGHT' and not direction =='LEFT':
            direction ='RIGHT'
        if changeto =='LEFT' and not direction =='RIGHT':
            direction ='LEFT'
        if changeto =='UP' and not direction =='DOWN':
            direction ='UP'
        if changeto =='DOWN' and not direction =='UP':
            direction ='DOWN'
            
        if direction =='RIGHT':
            snakePos[0]+=10
        if direction =='LEFT' :
            snakePos[0]-=10
        if direction =='DOWN':
            snakePos[1]+=10
        if direction =='UP' :
            snakePos[1]-=10

        #snake body updete
        snakeBody.insert(0 , list(snakePos))
        if snakePos[0]== foodPos[0] and snakePos[1]==foodPos[1]:
            foodSpawn = False
            score+=1            
        else:
            snakeBody.pop()
            
        if foodSpawn == False:
            foodPos = [random.randrange(1,72)*10 , random.randrange(1,46)*10]
        foodSpawn = True
        
        playSurface.fill(white)
        showScore()
        for pos in snakeBody:
            pygame.draw.rect(playSurface , blue , pygame.Rect(pos[0],pos[1],10,10))

        pygame.draw.rect(playSurface , brown , pygame.Rect(foodPos[0],foodPos[1],10,10))

        if snakePos[0] > 710 or snakePos[0] <0:
            playSurface.fill(white)
            showScore(choice=2)
            gameOver()
            
        if snakePos[1] > 450 or snakePos[1] <0:
            playSurface.fill(white)
            showScore(choice=2)
            gameOver()
            
        for block in snakeBody[1:]:
            if snakePos[0] == block[0] and snakePos[1]== block[1]:
                playSurface.fill(white)
                showScore(choice=2)
                gameOver()
                
        if score!=0 and score%10==0:
            speed+=2

        pygame.display.update()
        fpsController.tick(speed)
game_intro()   
game_loop()
    
