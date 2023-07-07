import pygame, random, math, os, ctypes
ctypes.windll.user32.ShowWindow( ctypes.windll.kernel32.GetConsoleWindow(), 0 )
pygame.init()
font = pygame.font.Font('freesansbold.ttf', 32)
font2 = pygame.font.Font('freesansbold.ttf', 16)
BLACK = ( 0, 0, 0)
WHITE = ( 255, 255, 255)
GREEN = ( 0, 255, 0)
RED = ( 255, 0, 0)
screenwidth = 700
screenheight = 500
size = (screenwidth, screenheight)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Wierd Flappy Thing")
playerx = 25
playery = 250
playerwidth = 50
playerheight = 50
score = 0
playerspeedX = 0
playerspeedY = 0
playergravity = 0
playergravitySpeed = 0
frameno = 0
scoretext = None
scoreRect = None
obstacles = []
playery = screenheight - playerheight
gcrash = False
def newpos():
    global playergravitySpeed, playerx, playery
    playergravitySpeed += playergravity
    playerx += playerspeedX
    playery += playerspeedY + playergravitySpeed
    hitbottom()
    hittop()

def hitbottom():
    global playery, playergravitySpeed
    bottom = screenheight - playerheight
    if playery > bottom:
        playery = bottom
        playergravitySpeed = 0

def hittop():
    global playery, playergravitySpeed
    if playery < 0.001:
        playery = 0
        playergravitySpeed = 0
        
def crashwith(otherobjx, otherobjy, otherobjwidth, otherobjheight):
    myleft = playerx
    myright = playerx + playerwidth
    mytop = playery
    mybottom = playery + playerheight
    otherleft = otherobjx
    otherright = otherobjx + otherobjwidth
    othertop = otherobjy
    otherbottom = otherobjy + otherobjheight
    crash = True
    if mybottom < othertop or mytop > otherbottom or myright < otherleft or myleft > otherright:
        crash = False
    return crash

def updateGameArea():
    global frameno, score, gcrash, scoretext, scoreRect
    for i in obstacles:
        if crashwith(i[0], i[1], i[2], i[3]):
            gcrash = True
    frameno += 1
    if frameno == 1 or everyinterval(200):
        x = screenwidth
        minHeight = 10
        maxHeight = 300
        height = math.floor(random.random() * (maxHeight - minHeight + 1) + minHeight)
        minGap = 70
        maxGap = 200
        gap = math.floor(random.random() * (maxGap - minGap + 1) + minGap)
        obstacles.append([x, 0, 10, height])
        obstacles.append([x, height + gap, 10, x - height - gap])
    for i in obstacles:
        i[0] -= 1
    score = frameno
    scorestring = 'Score: ' + str(score)
    scoretext = font.render(scorestring, True, GREEN, WHITE)
    scoreRect = scoretext.get_rect()
    scoreRect.center = (100, 20)

def everyinterval(n):
    return (frameno / n) % 1 == 0

def accelerate(n):
    global playergravity
    playergravity = n


carryOn = True

clock = pygame.time.Clock()
while carryOn:
    restart = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            carryOn = False
        if gcrash:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    restart = True
                    carryOn = False
        if not gcrash:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                accelerate(-0.2)
            else:
                accelerate(0.05)

     # --- Game logic should go here
    if not gcrash:
        newpos()
        updateGameArea()
    screen.fill(WHITE)
    if gcrash:
        crashstring = 'You crashed. Score: ' + str(score) + ' Press space to try again.'
        crashtext = font2.render(crashstring, True, GREEN, BLACK)
        crashRect = crashtext.get_rect()
        crashRect.center = (screenwidth / 2, screenheight / 2)
        screen.blit(crashtext, crashRect)
    else:
        screen.blit(scoretext, scoreRect)
        pygame.draw.rect(screen, RED, [playerx, playery, playerwidth, playerheight],0)
        for i in obstacles:
            pygame.draw.rect(screen, GREEN, [i[0], i[1], i[2], i[3]],0)
    pygame.display.flip()
    clock.tick(60)
pygame.quit()
if restart:
    os.system("Echo off && python3 main.py")