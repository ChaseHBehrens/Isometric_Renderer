import pygame, sys, math
from pygame.locals import *
pygame.init()
pygame.mouse.set_visible(False)
mainClock = pygame.time.Clock()
screen = pygame.display.set_mode([0, 0], pygame.FULLSCREEN,32)
w, h = pygame.display.get_surface().get_size()
screen.fill([250,250,250])

#screen_size = [1472,800]
camera = [0,0,0,0]
pixel_size = 4
tiles = {'cube':[pygame.transform.scale(pygame.image.load(r"art\cube.xcf"),[26*pixel_size,28*pixel_size]) for i in range(4)],
         'cube2':[pygame.transform.scale(pygame.image.load(r"art\cube2.xcf"),[26*pixel_size,28*pixel_size]) for i in range(4)],
         'cube3':[pygame.transform.scale(pygame.image.load(r"art\cube3.xcf"),[26*pixel_size,28*pixel_size]) for i in range(4)],
         'cube4':[pygame.transform.scale(pygame.image.load(r"art\cube4.xcf"),[26*pixel_size,28*pixel_size]) for i in range(4)],
         'cube5':[pygame.transform.scale(pygame.image.load(r"art\cube5.xcf"),[26*pixel_size,28*pixel_size]) for i in range(4)]
        }

class tile:
    def __init__(self,index):
        self.image = tiles[index]                                                                                                                                                             

world = {'[0, 0, 0]':tile('cube')}
for i in range(20):
    for j in range(20):
        world[str([i-10,j-10,0])] = tile('cube')


def icosphere(n):
    global raycast_angles
    raycast_angles = []
    raycast_angles.append([0,0])
    raycast_angles.append([0,180])
    for i in range(1+n):
        for j in range((i+1)*5):
            raycast_angles.append([(((360/((i+1)*5)))*j)+((180/((i+1)*5))*i),(180/(3+(3*n)))*(i+1)])
    for i in range(n):
        for j in range(5+(n*5)):
            raycast_angles.append([((360/(5+(n*5)))*j)+((180/(5+(n*5)))*i),60+((180/(3+(3*n)))*(i+1))])
    for i in range(1+n):
        for j in range((i+1)*5):
            raycast_angles.append([(((360/((i+1)*5)))*j)+((180/((i+1)*5))*i)+36,180-((180/(3+(3*n)))*(i+1))])
icosphere(10)

def sine(n):
    if n >= 0:
        return 1
    else:
        return -1
def sin(n):
    try:
        1/math.sin(math.radians(n))
        return math.sin(math.radians(n))
    except:
        return 999
def cos(n):
    try:
        1/math.cos(math.radians(n))
        return math.cos(math.radians(n))
    except:
        return 999

def x(l):
    return -l[0]
def y(l):
    return l[1]
def z(l):
    return l[2]

def update():
    screen.fill([250,250,250])
    #pygame.draw.rect(screen,[0,0,0],[0,0,screen_size[0],screen_size[1]], 1)
    visible_tiles = []
    for i in range(len(raycast_angles)):
        current_cell = camera[:3]
        no_collision = True
        x_length = abs(0.5/cos(raycast_angles[i][1]))+abs(0.5/sin(raycast_angles[i][0]))
        y_length = abs(0.5/sin(raycast_angles[i][1]))+abs(0.5/sin(raycast_angles[i][0]))
        z_length = abs(0.5/cos(raycast_angles[i][0]))
        while no_collision:
            if (x_length < y_length) and (x_length < z_length):
                x_length += abs(1/cos(raycast_angles[i][1]))+abs(1/sin(raycast_angles[i][0]))
                current_cell[0] += sine(cos(raycast_angles[i][1]))
            elif (y_length < x_length) and (y_length < z_length):
                y_length += abs(1/sin(raycast_angles[i][1]))+abs(1/sin(raycast_angles[i][0]))
                current_cell[1] += sine(sin(raycast_angles[i][0]))
            else:
                z_length += abs(1/cos(raycast_angles[i][0]))
                current_cell[2] += sine(cos(raycast_angles[i][0]))
            if (str(current_cell) in world) and (not (current_cell in visible_tiles)):
                visible_tiles.append(current_cell)
                no_collision = False
            if x_length + y_length + z_length > 20:
                no_collision = False

    visible_tiles.sort(key=x)
    visible_tiles.sort(key=y)
    visible_tiles.sort(key=z)
    for i in range(len(visible_tiles)):
        screen.blit(world[str(visible_tiles[i])].image[camera[3]],[
            (w//2)-(13*pixel_size)+(pixel_size*-12*(visible_tiles[i][0]-camera[0]))+(pixel_size*-12*(visible_tiles[i][1]-camera[1])),
            (h//2)-(6*pixel_size)+(pixel_size*-6*(visible_tiles[i][0]-camera[0]))+(pixel_size*6*(visible_tiles[i][1]-camera[1]))+(pixel_size*-15*(visible_tiles[i][2]-camera[2]))])
           
    
    #screen.blit(tiles['cube4'][0],[(w//2)-(13*pixel_size),(h//2)-(6*pixel_size)])
    pygame.display.update()
update()
while True:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == K_q:
                camera[0] += 1
                update()
            if event.key == K_s:
                camera[0] -= 1
                update()
            if event.key == K_a:
                camera[1] += 1
                update()
            if event.key == K_w:
                camera[1] -= 1
                update()
            if event.key == K_e:
                camera[2] += 1
                update()
            if event.key == K_d:
                camera[2] -= 1
                update()
            if event.key == K_r:
                camera[3] += 1
                if camera[3] > 3:
                    camera[3] = 0
                update()
            if event.key == K_f:
                camera[3] -= 1
                if camera[3] < 0:
                    camera[3] = 3
                update()
            if event.key == K_SPACE:
                try:
                    del(world[str(camera[:3])])
                except:
                    world[str(camera[:3])] = tile('cube')
                update()

    mainClock.tick(30)
