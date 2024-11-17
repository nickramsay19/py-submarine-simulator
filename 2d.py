import itertools
import operator
import pygame

# constants
WIDTH, HEIGHT = 800, 600
SKY_HEIGHT = 100  # Height of the sky portion
WATER_COLOR = (0, 0, 255)  # Blue water color
SKY_COLOR = (135, 206, 235)  # Sky blue color

RECT_COLOR = (255, 0, 0)  # Color of the rectangle
RECT_SIZE = 50  # Size of the rectangle
RECT_SPEED = 5  # Speed of the rectangle movement

'''class Body:
    xs: float 
    zs: float

class Space:
    singleton coordinate system information
    
    x0: float
    z0: float
    x1: float
    z1: float

    bodies: list[Body]

    def __init__(self, x0: float, z0: float, x1: float, z1: float, bodies: list[Body] = []):
        self.x0 = x0
        self.z0 = z0
        self.x1 = x1
        self.x1 = x1
        self.bodies = bodies

class Camera:
    singleton view of a Space
    screen: pygame.Surface
    space: Space
    x0: float
    z0: float
    x1: float
    z1: float

    def __init__(self, screen: pygame.Surface, space: Space, x0: float = None, z0: float = None, x1: float = None, z1: float = None):
        self.screen = screen
        self.space = space
        self.x0 = x0 or space.x0
        self.z0 = z0 or space.z0
        self.x1 = x1 or space.x1
        self.z1 = z1 or space.z1'''

class Body:
    xs: float
    zs: float

    xv: float
    zv: float

    ya: float # angle of rotation around the y axis
    yav: float # angular velocity around the y axis

    def __init__(self, xs: float, zs: float, xv: float = .0, zv: float = .0, ya: float = .0, yav: float = .0):
        self.xs = xs
        self.zs = zs
        self.xv = xv
        self.zv = zv
        self.ya = ya
        self.yav = yav

    def apply_force(self, f: Vec):
        pass
        

class BallastTank(Body):


def main():

    pygame.init()
    pygame.display.set_caption('submarine simulator')

    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    x0, z0, x1, z1 = -500, -500, 500, 500

    

    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            rect_x -= RECT_SPEED
        if keys[pygame.K_RIGHT]:
            rect_x += RECT_SPEED
        if keys[pygame.K_UP]:
            rect_y -= RECT_SPEED
        if keys[pygame.K_DOWN]:
            rect_y += RECT_SPEED

        screen.fill(SKY_COLOR)  # Fill the background with sky color
        pygame.draw.rect(screen, WATER_COLOR, (0, SKY_HEIGHT, WIDTH, HEIGHT - SKY_HEIGHT))

        pygame.draw.rect(screen, 

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == '__main__':
    main()


