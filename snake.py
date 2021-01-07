import pygame
import random as r

# initialize pygame
pygame.init()
pygame.mixer.init()

# colours
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
LIGHT_BLUE = (100, 149, 237)
DARK_GREY = (128, 128, 128)
LIGHT_GREY = (220, 220, 220)

# set up program
pygame.display.set_caption("Snake")
clock = pygame.time.Clock()
screen = pygame.display.set_mode([800, 800])
scoreFont = pygame.font.SysFont('Comic Sans MS', 50)
startFont = pygame.font.SysFont('Comic Sans MS', 170)
foodSound = pygame.mixer.Sound("boop.wav")
deadSound = pygame.mixer.Sound("dead.wav")

# global variables
board = {}
for i in range(0, 20):
    board["line{0}".format(i)] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
started = False
donePlaying = False
foodOnBoard = False
running = True
cont = False
posIndex = r.randint(0, 19)
posLine = r.randint(0, 19)
positions = [[posIndex, posLine]]
length = 1
direction = ""


def mouseOver(x, y, minX, maxX, minY, maxY):
    if minX < x < maxX and minY < y < maxY:
        return True
    else:
        return False


while not started:
    # mouse position
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # get user inputs
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        # exits start screen
        if event.type == pygame.MOUSEBUTTONDOWN and mouseOver(mouse_x, mouse_y, 275, 525, 550, 625):
            started = True

    # draw grid
    screen.fill(LIGHT_GREY)
    for row in range(20):
        for box in range(20):
            lineList = board["line{0}".format(row)]
            pygame.draw.rect(screen, DARK_GREY, [box * 40, row * 40, 40, 40], 1)

    # start text
    startText = startFont.render("Snake", True, BLACK, LIGHT_GREY)
    screen.blit(startText, (400 - startText.get_rect().width / 2, 250))
    names = scoreFont.render("By Jia Ming Fan and Patrick Ancheta", True, DARK_GREY, LIGHT_GREY)
    screen.blit(names, (100, 442))

    # start button, turns darker when mouse is on it
    if mouseOver(mouse_x, mouse_y, 275, 525, 550, 625):
        pygame.draw.rect(screen, BLUE, [275, 550, 250, 75])
    else:
        pygame.draw.rect(screen, LIGHT_BLUE, [275, 550, 250, 75])
    start = scoreFont.render("Start", True, BLACK)
    screen.blit(start, (360, 570))

    # update display
    pygame.display.flip()

    # fps
    clock.tick(60)

# main game loop
while running:
    while not donePlaying:

        # get user inputs
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            # changes direction
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and direction != "right":
                    direction = "left"
                if event.key == pygame.K_RIGHT and direction != "left":
                    direction = "right"
                if event.key == pygame.K_UP and direction != "down":
                    direction = "up"
                if event.key == pygame.K_DOWN and direction != "up":
                    direction = "down"

        # spawns snake food
        while not foodOnBoard:
            foodIndex = r.randint(0, 19)
            foodLine = board["line{0}".format(r.randint(0, 19))]
            # makes sure food isn't spawning on the snake
            if foodLine[foodIndex] == 0:
                foodLine[foodIndex] = 2
                foodOnBoard = True

        # increase snake size after eating
        if foodLine[foodIndex] == 1:
            foodSound.play()
            length += 1
            foodOnBoard = False

        # movement
        if direction == "left":
            posIndex -= 1
        if direction == "right":
            posIndex += 1
        if direction == "up":
            posLine -= 1
        if direction == "down":
            posLine += 1

        # hit wall
        if posIndex < 0 or posIndex > 19 or posLine < 0 or posLine > 19:
            donePlaying = True
            deadSound.play()
            break

        # hit itself
        if [posIndex, posLine] in positions and length > 1:
            deadSound.play()
            donePlaying = True
            break

        else:
            # adds head of snake
            positions.append([posIndex, posLine])

        # removes tail
        if len(positions) > length:
            removed = positions.pop(0)
            board["line{0}".format(removed[1])][removed[0]] = 0

        # make snake
        for pos in positions:
            board["line{0}".format(pos[1])][pos[0]] = 1

        # draw grid
        screen.fill(LIGHT_GREY)
        for row in range(20):
            for box in range(20):
                lineList = board["line{0}".format(row)]
                # snake
                if lineList[box] == 1:
                    pygame.draw.rect(screen, BLACK, [box * 40, row * 40, 40, 40])
                # food
                elif lineList[box] == 2:
                    pygame.draw.rect(screen, BLUE, [box * 40, row * 40, 40, 40])
                # empty box
                pygame.draw.rect(screen, DARK_GREY, [box * 40, row * 40, 40, 40], 1)

        # score
        score = scoreFont.render("Score: " + str(length - 1), False, BLACK, LIGHT_GREY)
        screen.blit(score, (30, 20))

        # update screen
        pygame.display.flip()

        # fps
        clock.tick(10)

    # game-over screen

    mouse_x, mouse_y = pygame.mouse.get_pos()

    # get user inputs
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        # quits game
        if event.type == pygame.MOUSEBUTTONDOWN and mouseOver(mouse_x, mouse_y, 150, 300, 550, 625):
            running = False
        # restarts
        if event.type == pygame.MOUSEBUTTONDOWN and mouseOver(mouse_x, mouse_y, 500, 650, 550, 625):
            cont = True

    # restarts game, resets all values
    if cont:
        donePlaying = False
        posIndex = r.randint(0, 19)
        posLine = r.randint(0, 19)
        positions = [[posIndex, posLine]]
        length = 1
        direction = ""
        foodOnBoard = False
        for i in range(0, 20):
            board["line{0}".format(i)] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        cont = False
        continue

    # draw grid
    screen.fill(LIGHT_GREY)
    for row in range(20):
        for box in range(20):
            lineList = board["line{0}".format(row)]
            pygame.draw.rect(screen, DARK_GREY, [box * 40, row * 40, 40, 40], 1)

    # end text
    playAgain = startFont.render("Play Again?", True, BLACK, LIGHT_GREY)
    screen.blit(playAgain, (400 - playAgain.get_rect().width / 2, 250))

    # score
    finalScore = scoreFont.render("Score: " + str(length - 1), True, BLACK, LIGHT_GREY)
    screen.blit(finalScore, (400 - finalScore.get_rect().width / 2, 402))

    # quit button
    if mouseOver(mouse_x, mouse_y, 150, 300, 550, 625):
        pygame.draw.rect(screen, BLUE, [150, 550, 150, 75])
    else:
        pygame.draw.rect(screen, LIGHT_BLUE, [150, 550, 150, 75])
    end = scoreFont.render("Quit", True, BLACK)
    screen.blit(end, (225 - end.get_rect().width / 2, 570))

    # restart button
    if mouseOver(mouse_x, mouse_y, 500, 650, 550, 625):
        pygame.draw.rect(screen, BLUE, [500, 550, 150, 75])
    else:
        pygame.draw.rect(screen, LIGHT_BLUE, [500, 550, 150, 75])
    restart = scoreFont.render("Restart", True, BLACK)
    screen.blit(restart, (575 - restart.get_rect().width / 2, 570))

    # update display
    pygame.display.flip()

    # fps
    clock.tick(60)

pygame.quit()
