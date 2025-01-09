import pygame, sys, math
from pygame.locals import *
pygame.init()
pygame.mouse.set_visible(False)
mainClock = pygame.time.Clock()
screen = pygame.display.set_mode([0, 0], pygame.FULLSCREEN,32)
w, h = pygame.display.get_surface().get_size()
screen.fill([250,250,250])

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

def update():
    screen.fill([250,250,250])
    #render
    for z in range(round((h/pixel_size)/7)):
        for y in range(round((h/pixel_size)/4)+1):
            for x in range(round((w/pixel_size)/24)+1):
                try:
                    if camera[3] == 0:
                        screen.blit(world[str([camera[0]+(round(round((w/pixel_size)/24)/2)-x)+math.floor((round(round((h/pixel_size)/2)/3)-y)/2),camera[1]+(round(round((w/pixel_size)/24)/2)-x)-math.ceil((round(round((h/pixel_size)/2)/3)-y)/2),camera[2]+z-(round((h/pixel_size)/13)//2)])].image[camera[3]],(((w//2)-(13*pixel_size))+(24*pixel_size*x)+((y%2)*pixel_size*12)-(24*pixel_size*((w/pixel_size)//48)),((h//2)-(6*pixel_size))+(6*pixel_size*y)-(6*pixel_size*((h/pixel_size)//12))-(18*pixel_size*6)-(15*pixel_size*z)+((round((h/pixel_size)/7)//2)*8*pixel_size)))
                    if camera[3] == 1:
                        screen.blit(world[str([camera[0]-(round(round((w/pixel_size)/24)/2)-x)+math.ceil((round(round((h/pixel_size)/2)/3)-y)/2),camera[1]-(round(round((w/pixel_size)/24)/2)-x)-math.floor((round(round((h/pixel_size)/2)/3)-y)/2),camera[2]+z-(round((h/pixel_size)/13)//2)])].image[camera[3]],(((w//2)-(13*pixel_size))+(24*pixel_size*x)+((y%2)*pixel_size*12)-(24*pixel_size*((w/pixel_size)//48)),((h//2)-(6*pixel_size))+(6*pixel_size*y)-(6*pixel_size*((h/pixel_size)//12))-(18*pixel_size*6)-(15*pixel_size*z)+((round((h/pixel_size)/7)//2)*8*pixel_size)))
                    
                        
                        
                except:
                    pass
    screen.blit(tiles['cube4'][0],[(w//2)-(13*pixel_size),(h//2)-(6*pixel_size)])
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
