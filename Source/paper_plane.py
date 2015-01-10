import pygame, sys
from pprint import pprint

'''
Global constants
'''

# Colors
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
BLUE     = (   0,   0, 255)
ORANGE   = ( 252, 177,  54)
BROWN    = ( 91,    0,   0)

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
        self.rect.x += self.change_x

        # Did this update cause us to hit a wall?
        block_hit_list = pygame.sprite.spritecollide(self, self.walls, False)
        for block in block_hit_list:
            # print(dir(block_hit_list))
            # If we collide on wall, check if that wall isn't on the sides
            if(block.rect.x == (SCREEN_WIDTH-10) or block.rect.x == 0):
                self.change_x = -(self.change_x)
            # if(self.rect.x )
            # Then push the airplane to the other side (We can put some fan on both sides)
            # pprint(dir(block_hit_list))
            '''
            if self.change_x > 0:
                self.rect.right = block.rect.left # Normal collision the object slides on the wall
            else:
                # Otherwise if we are moving left, do the opposite.
                self.rect.left = block.rect.right # Normal collision the object slides on the wall
            '''

        # Move up/down
        self.rect.y += self.change_y

        # Check and see if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.walls, False)
        for block in block_hit_list:
            pass
            # print "Collided"
            # self.game_over(self)

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
    def coordinates(self):
        pass


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

# Left side wall
wall = Wall(0, 0, 10, 600,BLACK)
wall_list.add(wall)
all_sprite_list.add(wall)

''' Obstacles '''
wall = Wall(10, 200, 300, 10)
wall_list.add(wall)
all_sprite_list.add(wall)

wall = Wall(700, 100, 300, 10)
wall_list.add(wall)
all_sprite_list.add(wall)


wall = Wall(500, 400, 300, 10)
wall_list.add(wall)
all_sprite_list.add(wall)

''' End of Obstacles '''

# Right side wall
wall = Wall(SCREEN_WIDTH-10, 0, 10, 600,BLACK)
wall_list.add(wall)
all_sprite_list.add(wall)


# Create the player paddle object @ the middle of the screen
player = Player(SCREEN_WIDTH/2, 0)
player.walls = wall_list

all_sprite_list.add(player)

clock = pygame.time.Clock()

done = False

speed = 1 # Speed of the airplane
tspeed = 3 # Turning speed
player.changespeed(0,speed) # Not turning at t=0
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.changespeed(-tspeed, speed)
            elif event.key == pygame.K_RIGHT:
                player.changespeed(tspeed, speed)
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                player.changespeed(-tspeed, speed)
            elif event.key == pygame.K_RIGHT:
                player.changespeed(tspeed, speed)

    # Rendering
    all_sprite_list.update()
    screen.fill(WHITE)
    all_sprite_list.draw(screen)
    pygame.display.flip()
    clock.tick(60) #Frame rate (in milliseconds)

pygame.quit()
