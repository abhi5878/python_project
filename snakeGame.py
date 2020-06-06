import pygame
import random
import time

pygame.init()
display_width=600
display_height=500
disp=pygame.display.set_mode((display_width,display_height))
pygame.display.update()
pygame.display.set_caption('Snake Game')

white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

snake_block=10
snake_speed=20

clock=pygame.time.Clock()
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

def our_snake(snake_block,snake_list):
    for x in snake_list:
        pygame.draw.rect(disp, black, [x[0], x[1], snake_block, snake_block])

def message(msg,color):
    messg = font_style.render(msg, True, color)
    disp.blit(messg, [display_width/6, display_height/3])

def yout_score(score,color):
    messg=score_font.render("Your Score: "+str(score), True, color)
    disp.blit(messg, [0,0])

def active_operation(event,snake_block):
    x1_change,y1_change=0,0
    if event.key==pygame.K_UP:
        y1_change=-snake_block
        x1_change=0
    elif event.key==pygame.K_DOWN:
        y1_change=snake_block
        x1_change=0
    elif event.key==pygame.K_LEFT:
        x1_change=-snake_block
        y1_change=0
    elif event.key==pygame.K_RIGHT:
        x1_change=snake_block
        y1_change=0
    elif event.key==pygame.K_SPACE:
        x1_change=0
        y1_change=0
    
    return x1_change, y1_change

def gameLoop():
    game_finish=False
    game_close=False

    key_list=[pygame.K_UP, pygame.K_DOWN,  pygame.K_LEFT, pygame.K_RIGHT, pygame.K_SPACE]

    snake_list=[]
    snake_length=1

    x1=display_width/2
    y1=display_height/2

    x1_change=0
    y1_change=0

    event_list=[]

    foodx = round(random.randrange(0, display_width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, display_height - snake_block) / 10.0) * 10.0

    while not game_finish:

        while game_close is True:
            disp.fill(white)
            message("You Lost! Press Q-Quit or C-Play Again", red)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_q:
                        game_finish=True
                        game_close=False
                    elif event.key==pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                game_finish=True
            elif event.type==pygame.KEYDOWN and event.key in key_list:
                x1_change,y1_change=active_operation(event, snake_block)
                event_list.append(event)

                if len(event_list)>2:
                    element=event_list[0]
                    event_list.pop(0)
                    event_list.append(element)
                    event_list.pop(2)

                if event.key!=pygame.K_SPACE and len(snake_list)>2 and len(event_list)==2 and [x1+x1_change, y1+y1_change]==snake_list[len(snake_list)-2]:
                    x1_change,y1_change=active_operation(event_list[0],snake_block)
                    del event_list[1]

        if x1>display_width or x1<0 or y1<0 or y1>display_height:
            game_close=True


        x1+=x1_change
        y1+=y1_change
        disp.fill(blue)
        pygame.draw.rect(disp, red, [foodx, foody, snake_block, snake_block])
        snake_head=[x1,y1]


        snake_list.append(snake_head)
        if len(snake_list)>=2 and snake_list[-1]==snake_list[-2]:
            snake_list.pop(-1)
        #For maintainig the constant length of snake
        #We need to delete tail block
        if len(snake_list)>snake_length:
            del snake_list[0]

        for parts in snake_list[:-1]:
            if parts==snake_head:
                game_close=True

        
        our_snake(snake_block, snake_list)
        yout_score(snake_length-1, black)

        pygame.display.update()

        if x1==foodx and y1==foody:
            foodx = round(random.randrange(0, display_width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, display_height - snake_block) / 10.0) * 10.0
            snake_length+=1

        clock.tick(snake_speed)

    pygame.quit()
    quit()

gameLoop()