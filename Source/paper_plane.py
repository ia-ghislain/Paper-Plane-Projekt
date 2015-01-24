import pygame, random, sys
from pygame.locals import *
from pprint import pprint
from collections import OrderedDict
from time import *
'''
Global constants
'''

# Colors
BLACK    	= (   0,   0,   0)
WHITE    	= ( 255, 255, 255)
BLUE     	= (   0,   0, 255)
ORANGE   	= ( 252, 177,  54)
BROWN    	= ( 91,    0,   0)
RED 		= (255,    0,   0)
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

def newcolour():
	# any colour but black or white 
	return (random.randint(10,250), random.randint(10,250), random.randint(10,250))

def write(msg="pygame is cool",x=0,y=0,color=ORANGE,s=False):
	myfont = pygame.font.SysFont("None", 30)
	mytext = myfont.render(msg, True, color)
	size = list(myfont.size(msg))
	if(x <= SCREEN_WIDTH/2):
		x = x+10
	else:
		x = x-10-size[0]
	mytext = mytext.convert_alpha()
	if(s == False):
		screen.blit(mytext,(x,y))
	else:
		s.blit(mytext,(x,y))
	return mytext

# This class represents the bar at the bottom that the player controls
class Player(pygame.sprite.Sprite):

	# Set speed vector
	change_x = 0
	change_y = 0
	walls = None
	frame_walls = None
	score = -2

	# Constructor function
	def __init__(self, x, y,color=ORANGE):
		# Call the parent's constructor
		super(self.__class__, self).__init__()

		# Set height, width
		self.image = pygame.Surface([15, 15])
		#Fill with ORANGE
		self.image.fill(color)

		# Make our top-left corner the passed-in location.
		self.rect = self.image.get_rect()
		self.rect.y = y
		self.rect.x = x
	def change_player_color(self,color):
		self.image.fill(color)		
	def changespeed(self, x, y):
		#Change the speed and coordinates of the player
		self.change_x = x
		self.change_y = y

	def update(self):
		if(self.score >= 0):
			write(str(self.score),SCREEN_WIDTH)
		else:
			write("0",SCREEN_WIDTH)
		# Update the player position.
		# Move left/right
		if((SCREEN_HEIGHT/5) > self.rect.y):
			# Move down, simulate grav.
			self.rect.y += self.change_y
		self.rect.x += self.change_x

		# Did this update cause us to hit a wall?
		block_hit_list = pygame.sprite.spritecollide(self, self.walls, False)
		block_hit_list_frame = pygame.sprite.spritecollide(self, self.frame_walls, False)
		
		for block in block_hit_list_frame:
			#If we hit the frame blocks then push us back in the game
			self.change_x = -(self.change_x)
		for block in block_hit_list:
				print "***Collision detected***"
				write("***Crash !***",0,0,RED)
		for block in self.walls:
			# print str(block.rect.x) + " AND => " + str(self.rect.x)
			block.rect.y = block.rect.y-(self.change_y) #Move the blocks up
			# write(str(self.rect.y),10,0)
			# write(str(block.rect.y),10,30)
			if(block.rect.y==self.rect.y): #Is the player @ the same line as block ?
				print(self.score)
				self.score +=1

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

class Menu(object):
	''' Variables definition '''
	legacy_list = []
	fields = []
	font_size = 32
	font_path = 'data/coders_crux.ttf' # Font being used
	font = pygame.font.Font # Init font
	dest_surface = pygame.Surface # Init surface
	fields_quantity = 0
	background_color = (51, 51, 51)
	text_color = (255, 255, 153)
	selection_color = (153, 102, 255)
	selection_position = 0
	paste_position = (0, 0)
	menu_width = 0
	menu_height = 0
	''' End of variables definition '''

	class Pole(object):
		text = ''
		field = pygame.Surface
		field_rect = pygame.Rect
		selection_rect = pygame.Rect

	def move_menu(self, top, left):
		self.paste_position = (top, left)
	def get_block_position(self):
		return self.paste_position
	def set_colors(self, text, selection, background):
		self.background_color = background
		self.text_color = text
		self.selection_color = selection

	def set_fontsize(self, font_size):
		self.font_size = font_size

	def set_font(self, path):
		self.font_path = path

	def get_position(self):
		return self.selection_position

	def init(self, legacy_list, dest_surface):
		self.legacy_list = legacy_list
		self.dest_surface = dest_surface
		self.fields_quantity = len(self.legacy_list)
		self.create_structure()

	def draw(self, move=0):
		if move:
			self.selection_position += move
			if self.selection_position == -1:
				self.selection_position = self.fields_quantity - 1
			self.selection_position %= self.fields_quantity
		menu = pygame.Surface((self.menu_width, self.menu_height))
		menu.fill(self.background_color)
		selection_rect = self.fields[self.selection_position].zaznaczenie_rect
		pygame.draw.rect(menu, self.selection_color, selection_rect)

		for i in xrange(self.fields_quantity):
			menu.blit(self.fields[i].pole, self.fields[i].pole_rect)
		self.dest_surface.blit(menu, self.paste_position)
		return self.selection_position

	def create_structure(self):
		self.menu_height = 0
		self.font = pygame.font.Font(self.font_path, self.font_size)
		for i in xrange(self.fields_quantity):
			self.fields.append(self.Pole())
			self.fields[i].tekst = self.legacy_list[i]
			self.fields[i].pole = self.font.render(
				self.fields[i].tekst,
				1,
				self.text_color
			)

			self.fields[i].pole_rect = self.fields[i].pole.get_rect()
			move = int(self.font_size * 0.2)

			height = self.fields[i].pole_rect.height
			self.fields[i].pole_rect.left = move
			self.fields[i].pole_rect.top = move + (move * 2 + height) * i

			width = self.fields[i].pole_rect.width + move * 2
			height = self.fields[i].pole_rect.height + move * 2
			left = self.fields[i].pole_rect.left - move
			top = self.fields[i].pole_rect.top - move

			self.fields[i].zaznaczenie_rect = (left, top, width, height)
			if width > self.menu_width:
					self.menu_width = width
			self.menu_height += height
		x = self.dest_surface.get_rect().centerx - self.menu_width / 2
		y = self.dest_surface.get_rect().centery - self.menu_height / 2
		mx, my = self.paste_position
		self.paste_position = (x+mx, y+my)

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

class Play(object):
	"""Play the game with some parameters"""
	param = {}
	def __init__(self,uparam):
		#super(self.__class__, self).__init__()
		super(Play, self).__init__()
		dparam = {	
					"pcolor":ORANGE,
					"dynamic_speed":False,
					"speed":1,
					"tspeed":3,
				}
		self.param.update(dparam) #Merge given array & default array
	def setp(self,uparam): # set parametter
		self.param.update(uparam) #Merge given array & default array

	def start(self):
		frame_wall_list = pygame.sprite.Group()
		# Left side wall
		wall = Wall(0, 0, 10, 600,BLACK)
		frame_wall_list.add(wall)
		all_sprite_list.add(wall)
		''' Obstacles samples
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
		player = Player(SCREEN_WIDTH/2, 0,self.param["pcolor"])
		player.walls = wall_list
		player.frame_walls = frame_wall_list
		
		all_sprite_list.add(player)
		
		clock = pygame.time.Clock()
		
		done = False
		
		speed = 1 # Speed of the airplane
		tspeed = 3 # Turning speed
		tesla,ttesla = 0,0 # Time elapsed since last action
		player.changespeed(0,speed) # Not turning at t=0
		dt = clock.tick(FPS) # delta of t
		pos = POS_RIGHT # Start the game @ left position
		while not done:
			screen.fill(WHITE) # Clean the screen
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
			all_sprite_list.draw(screen) # Draw everything so that text will be on top
			all_sprite_list.update()
			pygame.display.flip()
			clock.tick(FPS) #Frame rate (in milliseconds)
		pygame.quit()


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
player = Player(SCREEN_WIDTH/2, 0)
game = Play({"hey":False})
#game.setp({"pcolor":ORANGE})

def show_menu(mlst,title=""): #menu list menu is a list with (name:function)
	if not mlst: # If menu is empty
		return False
	screen.fill((51, 51, 51))
	if(menu_lst.keys() != mlst.keys()): # If not located @ the main menu
		mlst["<"] = {show_menu:(menu_lst)} #Append the go back to main menu button in options
	print game.param
	keys = mlst.keys()
	menu = Menu()
	menu.init(keys, screen)  # necessary
	menu.draw()
	mpos = menu.get_block_position()
	pygame.key.set_repeat(199, 69)  # (delay,interval)
	pygame.display.update()
	while 1:
		for event in pygame.event.get():
			if event.type == KEYDOWN:
				if event.key == K_UP:
					# here is the Menu class method
					menu.draw(-1)
				if event.key == K_DOWN:
					# here is the Menu class method
					menu.draw(1)
				if event.key == K_RETURN: # Did we press ENTER ?
					name = keys[menu.get_position()] # Get the name of the current position.
					if isinstance(mlst[name], list): # Is builtin function bunch of lists ?
						for fn in mlst[name]: # Then
							fn() # Run every function
					elif isinstance(mlst[name], dict): # Is it a standalone function
						for fn, param in mlst[name].iteritems(): # Then
							if(isinstance(param, tuple)): # Is this a tuple ?
								fn(*param) # Put tuple as fn param.
							else:
								fn(param) # Run every function
					else:
						mlst[name]() # Run it !
				if event.key == K_ESCAPE or event.key == K_LEFT: # Quit the game
					name = keys[menu.get_position()] # Get the name of the current position.
					if(name not in menu_lst.keys()):
						print title
						show_menu(menu_lst)
					else:
						pygame.display.quit()
						sys.exit()
				pygame.display.update() # Update the display so, we can animate screen
			elif event.type == QUIT:
				pygame.display.quit()
				sys.exit()
		pygame.time.wait(8)

menu_lst = OrderedDict({
			'Play !':OrderedDict({
				show_menu:OrderedDict({
					"Lvl 0":game.start
				})
			}),
			'Options':OrderedDict({
				show_menu:OrderedDict({
					"Color":OrderedDict({
						show_menu:OrderedDict({
							"Blue":OrderedDict({ game.setp:{"pcolor":BLUE},write:("Done !",0,0,BLUE) }),
							"Black":OrderedDict({ game.setp:{"pcolor":BLACK},write:("Done !",0,0,BLACK) }),
							"Brown":OrderedDict({ game.setp:{"pcolor":BROWN},write:("Done !",0,0,BROWN) }),
							"Red":OrderedDict({ game.setp:{"pcolor":RED},write:("Done !",0,0,RED) }),
							"Orange":OrderedDict({ game.setp:{"pcolor":ORANGE},write:("Done !",0,0,ORANGE) })
						})
					})
				})
			}),
			'Quit':[
				pygame.display.quit,
				sys.exit
				]
		})

def main():
	show_menu(menu_lst)
	
	#game.start()
if __name__ == '__main__': main()