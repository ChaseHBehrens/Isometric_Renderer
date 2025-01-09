import pygame, sys, math, time
from pygame.locals import *
pygame.init()
pygame.mouse.set_visible(False)
mainClock = pygame.time.Clock()
screen = pygame.display.set_mode([0, 0], pygame.FULLSCREEN,32)
w, h = pygame.display.get_surface().get_size()
screen.fill([250,250,250])
camera = [0,0,0,0]
pixel_size = 4

tiles = {'cube':['solid',0*pixel_size,[pygame.transform.scale(pygame.image.load(r"art\cube.xcf"),[26*pixel_size,28*pixel_size]) for i in range(4)]],
         'cube2':['solid',0*pixel_size,[pygame.transform.scale(pygame.image.load(r"art\cube2.xcf"),[26*pixel_size,28*pixel_size]) for i in range(4)]],
         'cube3':['solid',0*pixel_size,[pygame.transform.scale(pygame.image.load(r"art\cube3.xcf"),[26*pixel_size,28*pixel_size]) for i in range(4)]],
         'cube4':['solid',0*pixel_size,[pygame.transform.scale(pygame.image.load(r"art\cube4.xcf"),[26*pixel_size,28*pixel_size]) for i in range(4)]],
         'cube5':['solid',0*pixel_size,[pygame.transform.scale(pygame.image.load(r"art\cube5.xcf"),[26*pixel_size,28*pixel_size]) for i in range(4)]]
        }
entities = {'player' : [[7*pixel_size,0*pixel_size],[pygame.transform.scale(pygame.image.load(r"art\playerfrount.xcf"),[12*pixel_size,23*pixel_size]),\
                                                     pygame.transform.flip(pygame.transform.scale(pygame.image.load(r"art\playerfrount.xcf"),[12*pixel_size,23*pixel_size]),True,False),\
                                                     pygame.transform.scale(pygame.image.load(r"art\playerback.xcf"),[12*pixel_size,23*pixel_size]),\
                                                     pygame.transform.flip(pygame.transform.scale(pygame.image.load(r"art\playerback.xcf"),[12*pixel_size,23*pixel_size]),True,False)]]
        }
equipment = {'right_arm' : [[7*pixel_size,0*pixel_size],[pygame.transform.scale(pygame.image.load(r"art\arm1frount.xcf"),[12*pixel_size,23*pixel_size]),\
                                                         pygame.transform.flip(pygame.transform.scale(pygame.image.load(r"art\arm2frount.xcf"),[12*pixel_size,23*pixel_size]),True,False),\
                                                         pygame.transform.scale(pygame.image.load(r"art\arm1back.xcf"),[12*pixel_size,23*pixel_size]),\
                                                         pygame.transform.flip(pygame.transform.scale(pygame.image.load(r"art\arm2back.xcf"),[12*pixel_size,23*pixel_size]),True,False)]],\
             'left_arm' : [[7*pixel_size,0*pixel_size],[pygame.transform.scale(pygame.image.load(r"art\arm2frount.xcf"),[12*pixel_size,23*pixel_size]),\
                                                        pygame.transform.flip(pygame.transform.scale(pygame.image.load(r"art\arm1frount.xcf"),[12*pixel_size,23*pixel_size]),True,False),\
                                                        pygame.transform.scale(pygame.image.load(r"art\arm2back.xcf"),[12*pixel_size,23*pixel_size]),\
                                                        pygame.transform.flip(pygame.transform.scale(pygame.image.load(r"art\arm1back.xcf"),[12*pixel_size,23*pixel_size]),True,False)]]
        }
class tile:
    def __init__(self,index):
        self.image = tiles[index][2]
        self.type = tiles[index][0]
        self.offset = [0,0]
        self.offset2 = tiles[index][1]
        self.direction = 0
class entity:
    def __init__(self,index):
        self.image = entities[index][1]
        self.type = 'transparent'
        self.offset = entities[index][0]
        self.direction = 3
class player(entity):
    def __init__(self,index,position):
        super().__init__(index)
        self.position = position
        self.equiped = [equipment['right_arm'],equipment['left_arm']]
    
world = {(0,0,-1) : [tile('cube')]}
players = [player('player',(0,0,0))]
for i in range(len(players)):
    if players[i].position in world:
        world[players[i].position].append(players[0])
    else:
        world[players[i].position] = [players[0]]

def move(entity,direction):
    if len(world[entity.position]) == 1:
        del(world[entity.position])
    else:
        world[entity.position].remove(entity)
    entity.position = (entity.position[0]+direction[0],entity.position[1]+direction[1],entity.position[2]+direction[2])
    if entity.position in world:
        world[entity.position].append(entity)
    else:
        world[entity.position] = [entity]

#move(players[0],[1,0,0])


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
def update():
    screen.fill([250,250,250])
    visible_tiles = []
    visited_cells = {}
    current_cell = [[camera[:3]]]
    for i in range(50):
        current_cell.append([])
        for j in range(len(current_cell[i])):
            if (tuple(current_cell[i][j]) in world) and ('solid' in [world[tuple(current_cell[i][j])][k].type for k in range(len(world[tuple(current_cell[i][j])]))]):
                visible_tiles.append(current_cell[i][j])
            else:
                if tuple(current_cell[i][j]) in world:
                    visible_tiles.append(current_cell[i][j])
                if not (current_cell[i][j][0]+1,current_cell[i][j][1],current_cell[i][j][2]) in visited_cells:
                    if dispx([current_cell[i][j][0]+1,current_cell[i][j][1],current_cell[i][j][2]]) > (pixel_size*-26) and\
                       dispx([current_cell[i][j][0]+1,current_cell[i][j][1],current_cell[i][j][2]]) < w and\
                       dispy([current_cell[i][j][0]+1,current_cell[i][j][1],current_cell[i][j][2]]) > (pixel_size*-28) and\
                       dispy([current_cell[i][j][0]+1,current_cell[i][j][1],current_cell[i][j][2]]) < h:
                        current_cell[i+1].append([current_cell[i][j][0]+1,current_cell[i][j][1],current_cell[i][j][2]])
                        visited_cells[(current_cell[i][j][0]+1,current_cell[i][j][1],current_cell[i][j][2])] = True
                if not (current_cell[i][j][0]-1,current_cell[i][j][1],current_cell[i][j][2]) in visited_cells:
                    if dispx([current_cell[i][j][0]-1,current_cell[i][j][1],current_cell[i][j][2]]) > (pixel_size*-26) and\
                       dispx([current_cell[i][j][0]-1,current_cell[i][j][1],current_cell[i][j][2]]) < w and\
                       dispy([current_cell[i][j][0]-1,current_cell[i][j][1],current_cell[i][j][2]]) > (pixel_size*-28) and\
                       dispy([current_cell[i][j][0]-1,current_cell[i][j][1],current_cell[i][j][2]]) < h:
                        current_cell[i+1].append([current_cell[i][j][0]-1,current_cell[i][j][1],current_cell[i][j][2]])
                        visited_cells[(current_cell[i][j][0]-1,current_cell[i][j][1],current_cell[i][j][2])] = True
                if not (current_cell[i][j][0],current_cell[i][j][1]+1,current_cell[i][j][2]) in visited_cells:
                    if dispx([current_cell[i][j][0],current_cell[i][j][1]+1,current_cell[i][j][2]]) > (pixel_size*-26) and\
                       dispx([current_cell[i][j][0],current_cell[i][j][1]+1,current_cell[i][j][2]]) < w and\
                       dispy([current_cell[i][j][0],current_cell[i][j][1]+1,current_cell[i][j][2]]) > (pixel_size*-28) and\
                       dispy([current_cell[i][j][0],current_cell[i][j][1]+1,current_cell[i][j][2]]) < h:
                        current_cell[i+1].append([current_cell[i][j][0],current_cell[i][j][1]+1,current_cell[i][j][2]])
                        visited_cells[(current_cell[i][j][0],current_cell[i][j][1]+1,current_cell[i][j][2])] = True
                if not (current_cell[i][j][0],current_cell[i][j][1]-1,current_cell[i][j][2]) in visited_cells:
                    if dispx([current_cell[i][j][0],current_cell[i][j][1]-1,current_cell[i][j][2]]) > (pixel_size*-26) and\
                       dispx([current_cell[i][j][0],current_cell[i][j][1]-1,current_cell[i][j][2]]) < w and\
                       dispy([current_cell[i][j][0],current_cell[i][j][1]-1,current_cell[i][j][2]]) > (pixel_size*-28) and\
                       dispy([current_cell[i][j][0],current_cell[i][j][1]-1,current_cell[i][j][2]]) < h:
                        current_cell[i+1].append([current_cell[i][j][0],current_cell[i][j][1]-1,current_cell[i][j][2]])
                        visited_cells[(current_cell[i][j][0],current_cell[i][j][1]-1,current_cell[i][j][2])] = True
                if not (current_cell[i][j][0],current_cell[i][j][1],current_cell[i][j][2]+1) in visited_cells:
                    if dispy([current_cell[i][j][0],current_cell[i][j][1],current_cell[i][j][2]+1]) > (pixel_size*-28):
                        current_cell[i+1].append([current_cell[i][j][0],current_cell[i][j][1],current_cell[i][j][2]+1])
                        visited_cells[(current_cell[i][j][0],current_cell[i][j][1],current_cell[i][j][2]+1)] = True
                if not (current_cell[i][j][0],current_cell[i][j][1],current_cell[i][j][2]-1) in visited_cells:
                    if dispy([current_cell[i][j][0],current_cell[i][j][1],current_cell[i][j][2]-1]) < h:
                        current_cell[i+1].append([current_cell[i][j][0],current_cell[i][j][1],current_cell[i][j][2]-1])
                        visited_cells[(current_cell[i][j][0],current_cell[i][j][1],current_cell[i][j][2]-1)] = True
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
    visible_tiles.sort(key=z_sort)
    visible_tiles.sort(key=x_sort)
    visible_tiles.sort(key=y_sort)
    for i in range(len(visible_tiles)):
        for j in range(len(world[tuple(visible_tiles[i])])):
            if type(world[tuple(visible_tiles[i])][j]) != tile and ((visible_tiles[i][0],visible_tiles[i][1],visible_tiles[i][2]-1) in world):
                screen.blit(world[tuple(visible_tiles[i])][j].image[camera[3]-world[tuple(visible_tiles[i])][j].direction],[dispx(visible_tiles[i])+world[tuple(visible_tiles[i])][j].offset[0],dispy(visible_tiles[i])+world[tuple(visible_tiles[i])][j].offset[1]+world[(visible_tiles[i][0],visible_tiles[i][1],visible_tiles[i][2]-1)][0].offset2])
                if type(world[tuple(visible_tiles[i])][j]) == player:
                    for l in range(len(world[tuple(visible_tiles[i])][j].equiped)):
                        screen.blit(world[tuple(visible_tiles[i])][j].equiped[l][1][camera[3]-world[tuple(visible_tiles[i])][j].direction],[dispx(visible_tiles[i])+world[tuple(visible_tiles[i])][j].equiped[l][0][0],dispy(visible_tiles[i])+world[tuple(visible_tiles[i])][j].equiped[l][0][1]+world[(visible_tiles[i][0],visible_tiles[i][1],visible_tiles[i][2]-1)][0].offset2])
                        
            else:
                screen.blit(world[tuple(visible_tiles[i])][j].image[camera[3]-world[tuple(visible_tiles[i])][j].direction],[dispx(visible_tiles[i])+world[tuple(visible_tiles[i])][j].offset[0],dispy(visible_tiles[i])+world[tuple(visible_tiles[i])][j].offset[1]])
             
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
                    del(world[(camera[0],camera[1],camera[2]-1)])
                except:
                    world[(camera[0],camera[1],camera[2]-1)] = [tile('cube')]
                update()

    mainClock.tick(30)
