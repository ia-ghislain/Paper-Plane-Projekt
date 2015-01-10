import pygame, random
'''
Global constants
'''

# Colors
BLACK    	= (   0,   0,   0)
WHITE    	= ( 255, 255, 255)
BLUE     	= (   0,   0, 255)
ORANGE   	= ( 252, 177,  54)
BROWN    	= ( 91,    0,   0)
POS_LEFT 	= 0
POS_RIGHT	= 1
FPS			= 60
EVENT_TL = pygame.USEREVENT + 1 # Event turn left
EVENT_TR = pygame.USEREVENT + 2 # Event turn right
# Screen dimensions
SCREEN_WIDTH  = 800
SCREEN_HEIGHT = 600

'''
End of GC
'''

def texts(score):
   font=pygame.font.Font(None,30)
   scoretext=font.render("Score:"+str(score), 1,(255,255,255))
   screen.blit(scoretext, (500, 457))

# This class represents the bar at the bottom that the player controls
class Player(pygame.sprite.Sprite):

	# Set speed vector
	change_x = 0
	change_y = 0
	walls = None
	frame_walls = None
	score = 0

	# Constructor function
	def __init__(self, x, y):
		# Call the parent's constructor
		super(self.__class__, self).__init__()

		# Set height, width
		self.image = pygame.Surface([15, 15])
		#Fill with ORANGE
		self.image.fill(ORANGE)

		# Make our top-left corner the passed-in location.
		self.rect = self.image.get_rect()
		self.rect.y = y
		self.rect.x = x

	def changespeed(self, x, y):
		#Change the speed and coordinates of the player
		self.change_x = x
		self.change_y = y

	def update(self):
		# Update the player position.
		# Move left/right
		if((SCREEN_HEIGHT/5) > self.rect.y):
			# Move down, simulate grav.
			self.rect.y += self.change_y
		else:
			pass
		self.rect.x += self.change_x

		# Did this update cause us to hit a wall?
		block_hit_list = pygame.sprite.spritecollide(self, self.walls, False)
		block_hit_list_frame = pygame.sprite.spritecollide(self, self.frame_walls, False)
		
		for block in block_hit_list_frame:
			self.change_x = -(self.change_x)

		for block in block_hit_list:
			# print(dir(block_hit_list))
			# If we collide on wall, check if that wall isn't on the sides
			# if(block.rect.x == (SCREEN_WIDTH-10) or block.rect.x == 0):
				# Then we push the airplane to the other side (We can put some fan on both sides)
				# self.change_x = -(self.change_x)
			# else: #Collided with an obstacle
				print "***Collision detected***"
		for block in self.walls:
			# print str(block.rect.x) + " AND => " + str(self.rect.x)
			block.rect.y = block.rect.y-(self.change_y)
			if(block.rect.x==self.rect.x):
				self.score +=1
				print self.score

class Wall(pygame.sprite.Sprite):
	# Wall the player can run into.
	def __init__(self, x, y, width, height,color=BROWN):
		# Constructor for the wall that the player can run into.
		# Call the parent's constructor
		super(self.__class__, self).__init__()

		# Make a blue wall, of the size specified in the parameters
		self.image = pygame.Surface([width, height])
		self.image.fill(color)

		# Make our top-left corner the passed-in location.
		self.rect = self.image.get_rect()
		self.rect.y = y
		self.rect.x = x
	
def gen_wall(pos,slimit=500,color=BROWN):
	size = random.randint(100,slimit)
	# pos = random.randint(0,1)
	if(pos == POS_LEFT):
		x = 10
	else:
		x = SCREEN_WIDTH-size-10
	wall = Wall(x, SCREEN_HEIGHT+10, size, 30,color)
	wall_list.add(wall)
	all_sprite_list.add(wall)
	# 
	# wall = Wall(10, SCREEN_HEIGHT+10, 400, 10)
	# wall_list.add(wall)
	# all_sprite_list.add(wall)


# Call this function so the Pygame library can initialize itself
pygame.init()

# Create an 800x600 sized screen
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

# Set the title of the window
pygame.display.set_caption('SUUUUPPPEEERRR Paper Plane v0.1')

# List to hold all the sprites
all_sprite_list = pygame.sprite.Group()

# Make the walls. (x_pos, y_pos, width, height)
wall_list = pygame.sprite.Group()
frame_wall_list = pygame.sprite.Group()

# Left side wall
wall = Wall(0, 0, 10, 600,BLACK)
frame_wall_list.add(wall)
all_sprite_list.add(wall)

''' Obstacles 
self, x, y, width, height,color=BROWN
'''
wall = Wall(10, SCREEN_HEIGHT/5, 300, 500,BLUE)
wall_list.add(wall)
all_sprite_list.add(wall)

wall = Wall(SCREEN_WIDTH-310, SCREEN_HEIGHT/5, 300, 500,BLUE)
wall_list.add(wall)
all_sprite_list.add(wall)

''' End of Obstacles '''

# Right side wall
wall = Wall(SCREEN_WIDTH-10, 0, 10, 600,BLACK)
frame_wall_list.add(wall)
all_sprite_list.add(wall)


# Create the player paddle object @ the middle of the screen
player = Player(SCREEN_WIDTH/2, 0)
player.walls = wall_list
player.frame_walls = frame_wall_list

all_sprite_list.add(player)

clock = pygame.time.Clock()

done = False

speed = 1 # Speed of the airplane
tspeed = 3 # Turning speed
tesla = ttesla = 0 # Time elapsed since last action
player.changespeed(0,speed) # Not turning at t=0
dt = clock.tick(FPS) # delta of t
pos = POS_RIGHT # Start the game @ left position
while not done:
	tesla += dt
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			done = True
		elif event.type == EVENT_TL:
			player.changespeed(-tspeed, speed)
			pygame.time.set_timer(EVENT_TL, 0) # Stop the event to be repeated
		elif event.type == EVENT_TR:
			player.changespeed(tspeed, speed)
			pygame.time.set_timer(EVENT_TR, 0) # Stop the event to be repeated
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT:
				pygame.time.set_timer(EVENT_TL,250) #25 ms before the action is realised
			elif event.key == pygame.K_RIGHT:
				pygame.time.set_timer(EVENT_TR,250) #25 ms before the action is realised
	if (tesla > 2000):
		pos = 1-pos #Turn in the opposite dir.
		tesla = 0 # Reset timer
		gen_wall(pos) #Generate a wall
		print "Time to generate wall"
	# Rendering
	all_sprite_list.update()
	screen.fill(WHITE)
	all_sprite_list.draw(screen)
	pygame.display.flip()
	clock.tick(FPS) #Frame rate (in milliseconds)

pygame.quit()
