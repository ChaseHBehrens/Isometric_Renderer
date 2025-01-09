import pygame, sys, math, time
from pygame.locals import *
pygame.init()
pygame.mouse.set_visible(False)
mainClock = pygame.time.Clock()
screen = pygame.display.set_mode([0, 0], pygame.FULLSCREEN,32)
w, h = pygame.display.get_surface().get_size()
screen.fill([250,250,250])
camera = [0,0,0,4]
pixel_size = 4
def dispx(l):
    if camera[3] == 0:
        return (w//2)-(13*pixel_size)+(pixel_size*-12*(l[0]-camera[0]))+(pixel_size*-12*(l[1]-camera[1]))
    if camera[3] == 1:
        return (w//2)-(13*pixel_size)+(pixel_size*12*(l[0]-camera[0]))+(pixel_size*-12*(l[1]-camera[1]))
    if camera[3] == 2:
        return (w//2)-(13*pixel_size)+(pixel_size*12*(l[0]-camera[0]))+(pixel_size*12*(l[1]-camera[1]))
    if camera[3] == 3:
        return (w//2)-(13*pixel_size)+(pixel_size*-12*(l[0]-camera[0]))+(pixel_size*12*(l[1]-camera[1]))
def dispy(l):
    if camera[3] == 0:
        return (h//2)-(6*pixel_size)+(pixel_size*-6*(l[0]-camera[0]))+(pixel_size*6*(l[1]-camera[1]))+(pixel_size*-15*(l[2]-camera[2]))
    if camera[3] == 1:
        return (h//2)-(6*pixel_size)+(pixel_size*-6*(l[0]-camera[0]))+(pixel_size*-6*(l[1]-camera[1]))+(pixel_size*-15*(l[2]-camera[2]))
    if camera[3] == 2:
        return (h//2)-(6*pixel_size)+(pixel_size*6*(l[0]-camera[0]))+(pixel_size*-6*(l[1]-camera[1]))+(pixel_size*-15*(l[2]-camera[2]))
    if camera[3] == 3:
        return (h//2)-(6*pixel_size)+(pixel_size*6*(l[0]-camera[0]))+(pixel_size*6*(l[1]-camera[1]))+(pixel_size*-15*(l[2]-camera[2]))
cell_direction = {}
for k in range(4):
    camera[3] -= 1
    visited_cells = {}
    current_cell = [[[0,0,0]]]
    for i in range(50):
        current_cell.append([])
        for j in range(len(current_cell[i])):
            cell_direction[(camera[3],current_cell[i][j][0],current_cell[i][j][1],current_cell[i][j][2])] = [False,False,False,False,False,False]
            if not (current_cell[i][j][0]+1,current_cell[i][j][1],current_cell[i][j][2]) in visited_cells:
                if dispx([current_cell[i][j][0]+1,current_cell[i][j][1],current_cell[i][j][2]]) > (pixel_size*-26) and\
                   dispx([current_cell[i][j][0]+1,current_cell[i][j][1],current_cell[i][j][2]]) < w and\
                   dispy([current_cell[i][j][0]+1,current_cell[i][j][1],current_cell[i][j][2]]) > (pixel_size*-28) and\
                   dispy([current_cell[i][j][0]+1,current_cell[i][j][1],current_cell[i][j][2]]) < h:
                    current_cell[i+1].append([current_cell[i][j][0]+1,current_cell[i][j][1],current_cell[i][j][2]])
                    visited_cells[(current_cell[i][j][0]+1,current_cell[i][j][1],current_cell[i][j][2])] = True
                    cell_direction[(camera[3],current_cell[i][j][0],current_cell[i][j][1],current_cell[i][j][2])][0] = True
            if not (current_cell[i][j][0]-1,current_cell[i][j][1],current_cell[i][j][2]) in visited_cells:
                if dispx([current_cell[i][j][0]-1,current_cell[i][j][1],current_cell[i][j][2]]) > (pixel_size*-26) and\
                   dispx([current_cell[i][j][0]-1,current_cell[i][j][1],current_cell[i][j][2]]) < w and\
                   dispy([current_cell[i][j][0]-1,current_cell[i][j][1],current_cell[i][j][2]]) > (pixel_size*-28) and\
                   dispy([current_cell[i][j][0]-1,current_cell[i][j][1],current_cell[i][j][2]]) < h:
                    current_cell[i+1].append([current_cell[i][j][0]-1,current_cell[i][j][1],current_cell[i][j][2]])
                    visited_cells[(current_cell[i][j][0]-1,current_cell[i][j][1],current_cell[i][j][2])] = True
                    cell_direction[(camera[3],current_cell[i][j][0],current_cell[i][j][1],current_cell[i][j][2])][1] = True
            if not (current_cell[i][j][0],current_cell[i][j][1]+1,current_cell[i][j][2]) in visited_cells:
                if dispx([current_cell[i][j][0],current_cell[i][j][1]+1,current_cell[i][j][2]]) > (pixel_size*-26) and\
                   dispx([current_cell[i][j][0],current_cell[i][j][1]+1,current_cell[i][j][2]]) < w and\
                   dispy([current_cell[i][j][0],current_cell[i][j][1]+1,current_cell[i][j][2]]) > (pixel_size*-28) and\
                   dispy([current_cell[i][j][0],current_cell[i][j][1]+1,current_cell[i][j][2]]) < h:
                    current_cell[i+1].append([current_cell[i][j][0],current_cell[i][j][1]+1,current_cell[i][j][2]])
                    visited_cells[(current_cell[i][j][0],current_cell[i][j][1]+1,current_cell[i][j][2])] = True
                    cell_direction[(camera[3],current_cell[i][j][0],current_cell[i][j][1],current_cell[i][j][2])][2] = True
            if not (current_cell[i][j][0],current_cell[i][j][1]-1,current_cell[i][j][2]) in visited_cells:
                if dispx([current_cell[i][j][0],current_cell[i][j][1]-1,current_cell[i][j][2]]) > (pixel_size*-26) and\
                   dispx([current_cell[i][j][0],current_cell[i][j][1]-1,current_cell[i][j][2]]) < w and\
                   dispy([current_cell[i][j][0],current_cell[i][j][1]-1,current_cell[i][j][2]]) > (pixel_size*-28) and\
                   dispy([current_cell[i][j][0],current_cell[i][j][1]-1,current_cell[i][j][2]]) < h:
                    current_cell[i+1].append([current_cell[i][j][0],current_cell[i][j][1]-1,current_cell[i][j][2]])
                    visited_cells[(current_cell[i][j][0],current_cell[i][j][1]-1,current_cell[i][j][2])] = True
                    cell_direction[(camera[3],current_cell[i][j][0],current_cell[i][j][1],current_cell[i][j][2])][3] = True
            if not (current_cell[i][j][0],current_cell[i][j][1],current_cell[i][j][2]+1) in visited_cells:
                if dispy([current_cell[i][j][0],current_cell[i][j][1],current_cell[i][j][2]+1]) > (pixel_size*-28):
                    current_cell[i+1].append([current_cell[i][j][0],current_cell[i][j][1],current_cell[i][j][2]+1])
                    visited_cells[(current_cell[i][j][0],current_cell[i][j][1],current_cell[i][j][2]+1)] = True
                    cell_direction[(camera[3],current_cell[i][j][0],current_cell[i][j][1],current_cell[i][j][2])][4] = True
            if not (current_cell[i][j][0],current_cell[i][j][1],current_cell[i][j][2]-1) in visited_cells:
                if dispy([current_cell[i][j][0],current_cell[i][j][1],current_cell[i][j][2]-1]) < h:
                    current_cell[i+1].append([current_cell[i][j][0],current_cell[i][j][1],current_cell[i][j][2]-1])
                    visited_cells[(current_cell[i][j][0],current_cell[i][j][1],current_cell[i][j][2]-1)] = True
                    cell_direction[(camera[3],current_cell[i][j][0],current_cell[i][j][1],current_cell[i][j][2])][5] = True
    cell_direction[(camera[3],0,0,0)] = [True,True,True,True,True,True]
tiles = {'cube':[pygame.transform.scale(pygame.image.load(r"art\cube.xcf"),[26*pixel_size,28*pixel_size]) for i in range(4)],
         'cube2':[pygame.transform.scale(pygame.image.load(r"art\cube2.xcf"),[26*pixel_size,28*pixel_size]) for i in range(4)],
         'cube3':[pygame.transform.scale(pygame.image.load(r"art\cube3.xcf"),[26*pixel_size,28*pixel_size]) for i in range(4)],
         'cube4':[pygame.transform.scale(pygame.image.load(r"art\cube4.xcf"),[26*pixel_size,28*pixel_size]) for i in range(4)],
         'cube5':[pygame.transform.scale(pygame.image.load(r"art\cube5.xcf"),[26*pixel_size,28*pixel_size]) for i in range(4)]
        }

class tile:
    def __init__(self,index):
        self.image = tiles[index]
        self.type = 'solid'

world = {(0, 0, 0):[tile('cube')]}

def update():
    screen.fill([250,250,250])
    visible_tiles = []
    current_cell = [[camera[:3]]]
    for i in range(50):
        current_cell.append([])
        for j in range(len(current_cell[i])):
            if (tuple(current_cell[i][j]) in world) and ('solid' in [world[tuple(current_cell[i][j])][k].type for k in range(len(world[tuple(current_cell[i][j])]))]):
                visible_tiles.append(current_cell[i][j])
            else:
                if tuple(current_cell[i][j]) in world:
                    visible_tiles.append(current_cell[i][j])
                if cell_direction[(camera[3],current_cell[i][j][0]-camera[0],current_cell[i][j][1]-camera[1],current_cell[i][j][2]-camera[2])][0]:
                    current_cell[i+1].append([current_cell[i][j][0]+1,current_cell[i][j][1],current_cell[i][j][2]])
                if cell_direction[(camera[3],current_cell[i][j][0]-camera[0],current_cell[i][j][1]-camera[1],current_cell[i][j][2]-camera[2])][1]:
                    current_cell[i+1].append([current_cell[i][j][0]-1,current_cell[i][j][1],current_cell[i][j][2]])
                if cell_direction[(camera[3],current_cell[i][j][0]-camera[0],current_cell[i][j][1]-camera[1],current_cell[i][j][2]-camera[2])][2]:
                    current_cell[i+1].append([current_cell[i][j][0],current_cell[i][j][1]+1,current_cell[i][j][2]])
                if cell_direction[(camera[3],current_cell[i][j][0]-camera[0],current_cell[i][j][1]-camera[1],current_cell[i][j][2]-camera[2])][3]:
                    current_cell[i+1].append([current_cell[i][j][0],current_cell[i][j][1]-1,current_cell[i][j][2]])
                if cell_direction[(camera[3],current_cell[i][j][0]-camera[0],current_cell[i][j][1]-camera[1],current_cell[i][j][2]-camera[2])][4]:
                    current_cell[i+1].append([current_cell[i][j][0],current_cell[i][j][1],current_cell[i][j][2]+1])
                if cell_direction[(camera[3],current_cell[i][j][0]-camera[0],current_cell[i][j][1]-camera[1],current_cell[i][j][2]-camera[2])][5]:
                    current_cell[i+1].append([current_cell[i][j][0],current_cell[i][j][1],current_cell[i][j][2]-1])
    def x_sort(l):
        if camera[3] == 0:
            return -l[0]
        if camera[3] == 1:
            return -l[0]
        if camera[3] == 2:
            return l[0]
        if camera[3] == 3:
            return l[0]
    def y_sort(l):
        if camera[3] == 0:
            return l[1]
        if camera[3] == 1:
            return -l[1]
        if camera[3] == 2:
            return -l[1]
        if camera[3] == 3:
            return l[1]
    def z_sort(l):
        return l[2]
    visible_tiles.sort(key=x_sort)
    visible_tiles.sort(key=y_sort)
    visible_tiles.sort(key=z_sort)
    for i in range(len(visible_tiles)):
        for j in range(len(world[tuple(visible_tiles[i])])):
            if world[tuple(visible_tiles[i])][j].type == 'solid':
                screen.blit(world[tuple(visible_tiles[i])][j].image[camera[3]],[dispx(visible_tiles[i]),dispy(visible_tiles[i])])
           
    
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

    mainClock.tick(60)
