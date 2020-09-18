import pygame,sys,random

pygame.init()

size=width,height=600,400
screen=pygame.display.set_mode(size)

pygame.display.set_caption("snake")
icon=pygame.image.load('images/snake.png')
pygame.display.set_icon(icon)

#initaial position of snake
snake_x=100
snake_y=100
snake_size=10

#snake movement
move_x=0
move_y=0
velocity=0.1

#food for snake
food_x=random.randint(0,width)
food_y=random.randint(0,height)
food_size=10

#extras
score=0
snake_list=[]
snake_length=1
game_over=False

font=pygame.font.Font('freesansbold.ttf',32)

def text_screen(text,color,x,y):
	a=font.render(text,True,color)
	screen.blit(a,(x,y))

def plot_snake(screen,color,snake_list,snake_size):
	for x,y in snake_list:
		pygame.draw.rect(screen,color,[x,y,snake_size,snake_size])

if __name__ == '__main__':
	
	while True:
		screen.fill((255,255,255))

		if game_over:
			screen.fill((255,255,255))
			text_screen("GAME OVER",(0,0,0),200,100)

			for event in pygame.event.get():
				if event.type==pygame.QUIT:
					sys.exit()

		else:
			for event in pygame.event.get():
				if event.type==pygame.QUIT:
					sys.exit()

				if event.type==pygame.KEYDOWN:
					if event.key==pygame.K_LEFT:
						move_x=-velocity
						move_y=0           #to stop snake from moving diagonally(resultant)
					elif event.key==pygame.K_RIGHT:
						move_x=velocity
						move_y=0
					elif event.key==pygame.K_UP:
						move_y=-velocity
						move_x=0
					elif event.key==pygame.K_DOWN:
						move_y=velocity
						move_x=0

			snake_x+=move_x
			snake_y+=move_y

			if abs(snake_x-food_x)<6 and abs(snake_y-food_y)<6:
				score+=1
				food_x=random.randint(0,width)
				food_y=random.randint(0,height)
				snake_length+=50

			head = []     #increasing  lenght of snake
			head.append(snake_x)
			head.append(snake_y)
			snake_list.append(head)

			if len(snake_list)>snake_length:  #control length of snake
				del snake_list[0]

			if head in snake_list[:-1]:
				game_over = True

			if snake_x<0 or snake_x>width or snake_y<0 or snake_y>height:
				game_over = True

			plot_snake(screen,(255,0,0),snake_list,snake_size)
			text_screen("Score: " + str(score),(0,0,0), 0, 0)
			
			pygame.draw.rect(screen,(0,0,0),[food_x,food_y,food_size,food_size])
		
		pygame.display.update()

