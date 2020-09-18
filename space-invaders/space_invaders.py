import pygame,sys
import random,math
from pygame import mixer

pygame.init()  #initialize pygame

size=800,600
screen=pygame.display.set_mode(size)  #set screen for pygame

#background image
background=pygame.image.load('images/space.png')

#background sound
mixer.music.load('music/background.wav')
mixer.music.play(-1)

pygame.display.set_caption("space invaders")   #pygame title
icon=pygame.image.load('images/airplane.png')
pygame.display.set_icon(icon)                   #set icon    

playerImg=pygame.image.load('images/fighter-jet.png')  #player image
playerX=400
playerY=550
playerX_change=0     #change when we press the keys
playerY_change=0

#invaders(only one)
# invaderImg=pygame.image.load('space-invaders.png')  #invader image
# invaderX=random.randint(0,736)
# invaderY=random.randint(50,300)
# invaderX_change=0.5
# invaderY_change=40

#multiple invaders
invaderImg=[]
invaderX=[]
invaderY=[]
invaderX_change=[]
invaderY_change=[]

num_of_invaders=10

for i in range(num_of_invaders):
	invaderImg.append(pygame.image.load('images/space-invaders.png'))  #invader image
	invaderX.append(random.randint(0,736))
	invaderY.append(random.randint(50,300))
	invaderX_change.append(1)
	invaderY_change.append(50)

bulletImg=pygame.image.load('images/bullet.png')  #bullet image
bulletX=0
bulletY=550
bulletX_change=0
bulletY_change=20
bullet_state="ready"  #ready state is you can't see bullet on the screen
					  #fire state is you can see the bullet moving on the screen
#score text
score=0
font=pygame.font.Font('freesansbold.ttf',32)
textX=10
textY=10

#game over text
over_font=pygame.font.Font('freesansbold.ttf',64)

def show_score(x,y):
	show=font.render("Score: "+ str(score),True,(255,255,255))
	screen.blit(show,(x,y))

def game_over():
	over_a=over_font.render("GAME OVER",True,(255,255,255))
	screen.blit(over_a,(200,250))

def player(x,y):    #function used to blit(load) the player image on surface
	screen.blit(playerImg,(x,y))

def invader(x,y):    #function used to blit(load) the invader image on surface
	screen.blit(invaderImg[i],(x,y))

def fire_bullet(x,y):    #function used to blit(load) the bullet image on surface
	global bullet_state
	bullet_state="fire"
	screen.blit(bulletImg,(x+16,y))

def isCollision(invaderX,invaderY,bulletX,bulletY):
	distance=math.sqrt((math.pow(invaderX-bulletX,2)+(math.pow(invaderY-bulletY,2))))
	if distance<20:
		return True
	else:
		return False

while True:    #game loop
	screen.fill((0,0,0))   #RGB #all things are drawn on top of this screen
	#backgroundimage
	screen.blit(background,(0,0))

	#playerX+=0.3 increment x of the the player in the x direction continously
	for event in pygame.event.get():  #exit condition when cross is pressed
		if event.type==pygame.QUIT:
			sys.exit()

		#check if keystroke is pressed and if it is left or right
		if event.type==pygame.KEYDOWN:   #KEYDOWN when a key is pressed
			if event.key==pygame.K_LEFT:
				#print("left arrow is pressed")
				playerX_change=-3.0
			elif event.key==pygame.K_RIGHT:
				#print("right arrow is pressed")
				playerX_change=3.0
			elif event.key==pygame.K_UP:
				playerY_change=-3.0
			elif event.key==pygame.K_DOWN:
				playerY_change=3.0
			elif event.key==pygame.K_SPACE:
				if bullet_state is "ready":
					bulletSound=mixer.Sound('music/laser.wav')
					bulletSound.play()
					bulletX=playerX
					fire_bullet(bulletX,bulletY)
		elif event.type==pygame.KEYUP:
			if event.key==pygame.K_LEFT or event.key==pygame.K_RIGHT:
				#print("keystroke has been released")
				playerX_change=0
			elif event.key==pygame.K_UP or event.key==pygame.K_DOWN:
				playerY_change=0

	#check for boundaries of player or movement
	playerX+=playerX_change  # 5=5+0.1=5.1(move right) ; 5=5-0.1(move left)
	if playerX<=0:
		playerX=0
	elif playerX>=736:
		playerX=736

	playerY+=playerY_change  
	if playerY<=0:
		playerY=0
	elif playerY>=536:
		playerY=536

	#check for boundaries of invader or movement
	# invaderX+=invaderX_change           #this is inside while loop 
	# if invaderX<=0:                     #initializing invaderX_change=0 
	# 	invaderX_change=0.5             #will not change its value
	# 	invaderY+=invaderY_change
	# elif invaderX>=736:
	# 	invaderX_change=-0.5
	# 	invaderY+=invaderY_change
	for i in range(num_of_invaders):
		#game over
		if invaderY[i]>450:
			for j in range(num_of_invaders):
				invaderY[j]=2000
			game_over()
			break

		invaderX[i]+=invaderX_change[i]            
		if invaderX[i]<=0:                      
			invaderX_change[i]=0.5             
			invaderY[i]+=invaderY_change[i]
		elif invaderX[i]>=736:
			invaderX_change[i]=-0.5
			invaderY[i]+=invaderY_change[i]
		#collision of bullet and invader
		collision=isCollision(invaderX[i],invaderY[i],bulletX,bulletY)
		if collision:
			explode=mixer.Sound('music/explosion.wav')
			explode.play()
			bulletY=550
			bullet_state="ready"
			score+=1
			invaderX[i]=random.randint(0,736)
			invaderY[i]=random.randint(50,300)

		invader(invaderX[i],invaderY[i])

	#bullet movement / state
	if bulletY<=0:                #this iif condition is needed to fire    
		bulletY=550               #multiple bullets
		bullet_state="ready"

	if bullet_state is "fire":   # to make the bullet persistent(while loop)
		#bulletX=playerX
		fire_bullet(bulletX,bulletY)     #without this if condition bullet
		bulletY-=bulletY_change          #won't appear on screen

	

	player(playerX,playerY)  #function is called below fill because we want our player on top of surface not below
	show_score(textX,textY)
	
	pygame.display.update()#game screen always need to update.
							#Without it nothing will show


