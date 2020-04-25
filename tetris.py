import pygame, sys, random, math
import numpy as np



###GAME CONSTANTS###
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1200
BLOCK_SIZE = 50
BLACK = (0,0,0)
WHITE = (255,255,255)
GRID_LOCATION = (200,80)
GRID_LOCATION_X = 200
GRID_LOCATION_Y = 80
GRID_WIDTH = 10
GRID_HEIGHT = 21
NUMBER_OF_SHAPES = 6
NUMBER_OF_ROTATIONS = 4
NUMBER_OF_SHAPEBLOCKS = 4
LEVEL1_DELAY = 900
LEVEL2_DELAY = 800
LEVEL3_DELAY = 700
LEVEL4_DELAY = 600
LEVEL5_DELAY = 500
LEVEL6_DELAY = 400
LEVEL7_DELAY = 300
LEVEL8_DELAY = 200
SCOREBOX_LOCATION_X = 1000
SCOREBOX_LOCATION_Y = 300
LEVELBOX_LOCATION_X = 1000
LEVELBOX_LOCATION_Y = 600



###CLASSES###
class Gridpoint: pass



###METHODS###
#Read the next byte from an opened file and return the corresponding integer:
def rb(file):
	return int.from_bytes(file.read(1), byteorder='little')

#Randomly decide what the next shape is going to be and select an associated coloured block image:
def randomisenewshape():
	global currentshape, currentblock
	currentshape = random.randint(0,NUMBER_OF_SHAPES-1)
	if currentshape == 0: currentblock = blueblock
	elif currentshape == 1: currentblock = redblock
	elif currentshape == 2: currentblock = greenblock
	elif currentshape == 3: currentblock = purpleblock
	elif currentshape == 4: currentblock = grayblock
	elif currentshape == 5: currentblock = pinkblock

#Move grid content one step down when a line is detected to be filled:
def movegridcontentdown(f):
	#Copy grid content from and including line 0 up to and including the line above f one step down:
	tetragrid[1:f+1][:] = tetragrid[0:f][:]
	tetragrid[0][:] = np.zeros((1,10), dtype=np.uint8)

#Clear grid:
def cleargrid():
	pygame.draw.rect(screen, BLACK, ((GRID_LOCATION_X,GRID_LOCATION_Y),(GRID_WIDTH*BLOCK_SIZE,GRID_HEIGHT*BLOCK_SIZE)))

#Draw grid contents:
def drawgrid():
	for i in range(GRID_WIDTH):
		for j in range(GRID_HEIGHT):
			#if position (i,j) in grid is non-zero, plot the block corresponding to the number there:
			if tetragrid[j][i]!=0:
				if tetragrid[j][i]==1: drawblock(blueblock,i,j)
				elif tetragrid[j][i]==2: drawblock(redblock,i,j)
				elif tetragrid[j][i]==3: drawblock(greenblock,i,j)
				elif tetragrid[j][i]==4: drawblock(purpleblock,i,j)
				elif tetragrid[j][i]==5: drawblock(grayblock,i,j)
				elif tetragrid[j][i]==6: drawblock(pinkblock,i,j)

#Draw single block at position i,j in the grid:
def drawblock(block,i,j):
	screen.blit(block, (GRID_LOCATION_X+BLOCK_SIZE*i, GRID_LOCATION_Y+BLOCK_SIZE*j))
	return None

#Draw filled gray box at position i,j in the grid:
def drawgraybox(i,j,intensity):
	pygame.draw.rect(screen, (intensity,intensity,intensity), ((GRID_LOCATION_X+BLOCK_SIZE*i,GRID_LOCATION_Y+BLOCK_SIZE*j),(BLOCK_SIZE,BLOCK_SIZE)))

#Draw filled black box at position i,j in the grid:
def drawblackbox(i,j):
	pygame.draw.rect(screen, BLACK, ((GRID_LOCATION_X+BLOCK_SIZE*i,GRID_LOCATION_Y+BLOCK_SIZE*j),(BLOCK_SIZE,BLOCK_SIZE)))

#Draw black box border at position i,j in the grid:
def drawblackboxborder(i,j):
	pygame.draw.rect(screen, BLACK, ((GRID_LOCATION_X+BLOCK_SIZE*i,GRID_LOCATION_Y+BLOCK_SIZE*j),(BLOCK_SIZE,BLOCK_SIZE)),1)
	
#Draw white box border at position i,j in the grid:
def drawwhiteboxborder(i,j):
	pygame.draw.rect(screen, WHITE, ((GRID_LOCATION_X+BLOCK_SIZE*i,GRID_LOCATION_Y+BLOCK_SIZE*j),(BLOCK_SIZE,BLOCK_SIZE)),1)
	
#Update falling block positions according to current shape, rotation and frame position:
def updateblockpositions():
	global block
	for i in range(4):
		block[i].x = tetraframe.x + tetrarotation[currentshape][currentrotation][i][0]
		block[i].y = tetraframe.y + tetrarotation[currentshape][currentrotation][i][1]

def updatetestblockpositions():
	global testblock
	for i in range(4):
		testblock[i].x = tetraframe.x + tetrarotation[currentshape][testrotation][i][0]
		testblock[i].y = tetraframe.y + tetrarotation[currentshape][testrotation][i][1]
	
#Draw current block type at falling block positions:
def drawcurrentshape():
	global currentblock
	for i in range(4): drawblock(currentblock,block[i].x,block[i].y)

#Draw black boxes at current falling block positions:
def erasecurrentshape():
	for i in range(4): drawblackbox(block[i].x, block[i].y)

def rotationworks():
	if testblock[0].x<0 or testblock[1].x<0 or testblock[2].x<0 or testblock[3].x<0: return False
	elif testblock[0].x>=GRID_WIDTH or testblock[1].x>=GRID_WIDTH or testblock[2].x>=GRID_WIDTH or testblock[3].x>=GRID_WIDTH: return False
	elif tetragrid[testblock[0].y][testblock[0].x]!=0 or tetragrid[testblock[1].y][testblock[1].x]!=0 or tetragrid[testblock[2].y][testblock[2].x]!=0 or tetragrid[testblock[3].y][testblock[3].x]!=0: return False
	else: return True

def fallingworks():
	if block[0].y==GRID_HEIGHT-1 or block[1].y==GRID_HEIGHT-1 or block[2].y==GRID_HEIGHT-1 or block[3].y==GRID_HEIGHT-1: return False
	elif tetragrid[block[0].y+1][block[0].x]!=0 or tetragrid[block[1].y+1][block[1].x]!=0 or tetragrid[block[2].y+1][block[2].x]!=0 or tetragrid[block[3].y+1][block[3].x]!=0: return False
	else: return True

def movingleftworks():
	if block[0].x==0 or block[1].x==0 or block[2].x==0 or block[3].x==0: return False
	elif tetragrid[block[0].y][block[0].x-1]!=0 or tetragrid[block[1].y][block[1].x-1]!=0 or tetragrid[block[2].y][block[2].x-1]!=0 or tetragrid[block[3].y][block[3].x-1]!=0: return False
	else: return True
	
def movingrightworks():
	if block[0].x==GRID_WIDTH-1 or block[1].x==GRID_WIDTH-1 or block[2].x==GRID_WIDTH-1 or block[3].x==GRID_WIDTH-1: return False
	elif tetragrid[block[0].y][block[0].x+1]!=0 or tetragrid[block[1].y][block[1].x+1]!=0 or tetragrid[block[2].y][block[2].x+1]!=0 or tetragrid[block[3].y][block[3].x+1]!=0: return False
	else: return True

def recordblocks():
	for i in range(4): tetragrid[block[i].y][block[i].x] = currentshape+1

def gameover():
	global font
	gameoverfont = pygame.font.Font(None, 75)
	screen.fill(BLACK)
	gameovertext = gameoverfont.render("GAME OVER",1,WHITE)
	textpos = gameovertext.get_rect(centerx=SCREEN_WIDTH/2,centery=SCREEN_HEIGHT/2)
	screen.blit(gameovertext, textpos)

	scoretextpos = scoretext.get_rect(centerx=SCREEN_WIDTH/2-25, centery=SCREEN_HEIGHT/2+125)
	screen.blit(scoretext, scoretextpos)
	scorenumtext = font.render(str(score),1,WHITE)
	scorenumtextpos = scorenumtext.get_rect(left=SCREEN_WIDTH/2+55, centery=SCREEN_HEIGHT/2+125)
	screen.blit(scorenumtext, scorenumtextpos)
	
	pygame.display.update()
	
	while 1:
		pygame.event.get()
		keystates = pygame.key.get_pressed()
		if keystates[pygame.K_RETURN] or keystates[pygame.K_ESCAPE]: break
	sys.exit()

def lineisfilled(y):
	for x in range(GRID_WIDTH):
		if tetragrid[y][x]==0: return False
	return True


def playlineeliminationanimation(linelist):
	for a in range(40):
		for i in linelist:
			for x in range(GRID_WIDTH):
				drawgraybox(x,i,200/2*(1+math.sin(a/30*5*math.pi)))
		pygame.display.update()
		pygame.time.delay(20)		

		

###GAME START###	
#Initialise game:
tetragrid = np.zeros((21,10), dtype=np.uint8)
tetrarotation = np.zeros((NUMBER_OF_SHAPES,NUMBER_OF_ROTATIONS,NUMBER_OF_SHAPEBLOCKS,2), dtype=np.uint8)

#Load the shape definitions from file:
f = open('shapedata.dat', 'rb')
for j in range(6):
	for i in range(4):
		tetrarotation[j][i] = ((rb(f),rb(f)),(rb(f),rb(f)),(rb(f),rb(f)),(rb(f),rb(f)))
f.close()

pygame.init()
pygame.mouse.set_visible(False)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)

blueblock = pygame.image.load("blueblock.bmp").convert()
redblock = pygame.image.load("redblock.bmp").convert()
greenblock = pygame.image.load("greenblock.bmp").convert()
purpleblock = pygame.image.load("purpleblock.bmp").convert()
grayblock = pygame.image.load("grayblock.bmp").convert()
pinkblock = pygame.image.load("pinkblock.bmp").convert()
gamefield_border = pygame.Rect((GRID_LOCATION_X-5,GRID_LOCATION_Y-5),(BLOCK_SIZE*GRID_WIDTH+10,BLOCK_SIZE*GRID_HEIGHT+10))
	
screen.fill((0,0,0))
pygame.draw.rect(screen, WHITE, gamefield_border, 1)
pygame.display.update()

currentshape = 3
currentrotation = 0
testrotation = 0
oldrotation = 0
tetraframe = Gridpoint()
tetraframe.x = 4
tetraframe.y = 0
block = [Gridpoint(),Gridpoint(),Gridpoint(),Gridpoint()]
testblock = [Gridpoint(),Gridpoint(),Gridpoint(),Gridpoint()]
score = 0
level = 1
delay = LEVEL1_DELAY
linestoeliminate = []

#Choose a random initial shape and select block image accordingly:
randomisenewshape()

#Update block positions according to this selected shape:
updateblockpositions()

#Draw initial shape:
drawcurrentshape()
pygame.display.update()

lasttime = pygame.time.get_ticks()

#Draw score info:
font = pygame.font.Font(None, 50)
scoretext = font.render("SCORE: ",1,WHITE)
scoretextpos = scoretext.get_rect(centerx=SCOREBOX_LOCATION_X, centery=SCOREBOX_LOCATION_Y)
screen.blit(scoretext, scoretextpos)
scorenumtext = font.render(str(score),1,WHITE)
scorenumtextpos = scorenumtext.get_rect(centerx=SCOREBOX_LOCATION_X, centery=SCOREBOX_LOCATION_Y+70)
screen.blit(scorenumtext, scorenumtextpos)

#Draw level info:
leveltext = font.render("LEVEL: ",1,WHITE)
leveltextpos = leveltext.get_rect(centerx=LEVELBOX_LOCATION_X, centery=LEVELBOX_LOCATION_Y)
screen.blit(leveltext, leveltextpos)
levelnumtext = font.render(str(level),1,WHITE)
levelnumtextpos = levelnumtext.get_rect(centerx=LEVELBOX_LOCATION_X, centery=LEVELBOX_LOCATION_Y+70)
screen.blit(levelnumtext, levelnumtextpos)

pygame.display.update()


#Main loop:
while 1:
	for event in pygame.event.get():
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_RIGHT and movingrightworks():
				erasecurrentshape()
				tetraframe.x = tetraframe.x + 1
				updateblockpositions()
				drawcurrentshape()
			if event.key == pygame.K_LEFT and movingleftworks():
				erasecurrentshape()
				tetraframe.x = tetraframe.x - 1
				updateblockpositions()
				drawcurrentshape()
			if event.key == pygame.K_DOWN and fallingworks():
				erasecurrentshape()
				tetraframe.y = tetraframe.y + 1
				updateblockpositions()
				drawcurrentshape()
				
			if event.key == pygame.K_LALT:
				testrotation = currentrotation + 1
				if testrotation == NUMBER_OF_ROTATIONS: testrotation = 0
				updatetestblockpositions()
				if rotationworks():
					erasecurrentshape()
					currentrotation = testrotation
					updateblockpositions()
					drawcurrentshape()
			if event.key == pygame.K_LCTRL:
				testrotation = currentrotation - 1
				if testrotation<0: testrotation = NUMBER_OF_ROTATIONS-1
				updatetestblockpositions()
				if rotationworks():
					erasecurrentshape()
					currentrotation = testrotation
					updateblockpositions()
					drawcurrentshape()
			if event.key == pygame.K_SPACE:
				erasecurrentshape()
				while fallingworks():
					tetraframe.y = tetraframe.y + 1
					updateblockpositions()
				drawcurrentshape()
				lasttime = 0
			if event.key == pygame.K_ESCAPE:
				print(tetragrid)
				sys.exit()
	
	currenttime = pygame.time.get_ticks()
	if currenttime - lasttime > delay:
		lasttime = currenttime
		if fallingworks():
			erasecurrentshape()
			tetraframe.y = tetraframe.y + 1
			updateblockpositions()
			drawcurrentshape()
		else:
			recordblocks()
			
			#Check for filled lines and eliminate any:
			linestoeliminate = []
			if lineisfilled(block[0].y): linestoeliminate.append(block[0].y)			
			if lineisfilled(block[1].y) and block[1].y!=block[0].y: linestoeliminate.append(block[1].y)
			if lineisfilled(block[2].y) and block[2].y!=block[1].y: linestoeliminate.append(block[2].y)
			if lineisfilled(block[3].y) and block[3].y!=block[2].y: linestoeliminate.append(block[3].y)
			if len(linestoeliminate)>0:
				playlineeliminationanimation(linestoeliminate)
				for k in linestoeliminate: movegridcontentdown(k)
			
			if len(linestoeliminate)==1: score = score+1
			elif len(linestoeliminate)==2: score = score+5
			elif len(linestoeliminate)==3: score = score+25
			elif len(linestoeliminate)==4: score = score+125
			
			scorenumtext = font.render(str(score),1,WHITE)
			scorenumtextpos = scorenumtext.get_rect(centerx=SCOREBOX_LOCATION_X, centery=SCOREBOX_LOCATION_Y+70)
			pygame.draw.rect(screen, BLACK, scorenumtextpos)
			screen.blit(scorenumtext, scorenumtextpos)
			
			if level==1 and score>100:
				level=2
				delay=LEVEL2_DELAY
			if level==2 and score>200:
				level=3
				delay=LEVEL3_DELAY
			if level==3 and score>300:
				level=4
				delay=LEVEL4_DELAY
			if level==4 and score>400:
				level=5
				delay=LEVEL5_DELAY
			if level==5 and score>500:
				level=6
				delay=LEVEL6_DELAY
			if level==6 and score>600:
				level=7
				delay=LEVEL7_DELAY
			if level==7 and score>700:
				level=8
				delay=LEVEL8_DELAY
			
			levelnumtext = font.render(str(level),1,WHITE)
			levelnumtextpos = levelnumtext.get_rect(centerx=LEVELBOX_LOCATION_X, centery=LEVELBOX_LOCATION_Y+70)
			pygame.draw.rect(screen, BLACK, levelnumtextpos)
			screen.blit(levelnumtext, levelnumtextpos)
			
			cleargrid()
			drawgrid()
			
			randomisenewshape()
			currentrotation = 0
			tetraframe.x = 4
			tetraframe.y = 0
			testrotation = 0
			updatetestblockpositions()
			if not rotationworks(): gameover()
			updateblockpositions()
			drawcurrentshape()
	drawgrid()		
	pygame.display.update()