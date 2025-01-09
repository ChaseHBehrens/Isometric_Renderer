import pygame
from sys import exit
pygame.init()

pixel_size = 4
width = pygame.display.Info().current_w 
height = pygame.display.Info().current_h - 50
width = (width//pixel_size)*pixel_size
height = (height//pixel_size)*pixel_size
tilex = (width//(24*pixel_size))+2
tiley = (height//(6*pixel_size))+2
if tilex%2 != 0: tilex += 1 
if tiley%2 != 0: tiley += 1 


screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)

pygame.display.set_caption('RPG')
clock = pygame.time.Clock()
animation_index = 0



class player:
    def __init__(self):
        self.direction = 0
        self.image = pygame.image.load(r"art\playerfrount.xcf")
        

players = []
players.append(player())





def generate_world():
    global world
    global world_obgects
    global world_size
    world_size = 100
    world = [[[None for i in range(world_size)] for j in range(world_size)] for l in range(100)]
    world_obgects = [[[None for i in range(world_size)] for j in range(world_size)] for l in range(100)]
    
    for i in range(world_size):
        for j in range(world_size):
            if (j+i)%2 == 0:
                world[0][i][j] = 'cube4'
            else:
                world[0][i][j] = 'cube5'
    '''
    world[1][8][1] = 'cube4'
    world[1][8][2] = 'cube5'
    world[2][8][2] = 'cube4'
    world[2][8][1] = 'cube5'
    world[0][5][1] = 'cube2'
    '''
    world[0][0][0] = 'cube3'
    '''
    world[0][1][0] = 'cube'
    '''
    world_obgects[1][0][0] = players[0]
    
    
    
    
generate_world()

def set_art():
    global blocks
    blocks = {'cube':[pygame.transform.scale(pygame.image.load(r"art\cube.xcf"),[26*pixel_size,28*pixel_size])],
              'cube2':[pygame.transform.scale(pygame.image.load(r"art\cube2.xcf"),[26*pixel_size,28*pixel_size])],
              'cube3':[pygame.transform.scale(pygame.image.load(r"art\cube3.xcf"),[26*pixel_size,28*pixel_size])],
              'cube4':[pygame.transform.scale(pygame.image.load(r"art\cube4.xcf"),[26*pixel_size,28*pixel_size])],
              'cube5':[pygame.transform.scale(pygame.image.load(r"art\cube5.xcf"),[26*pixel_size,28*pixel_size])]
             }
set_art()

def render(x,y,z,d):
    # generates camera veiw
    def over_size(n):
        if n >= world_size:
            return world_size-n
        else:
            return n
    
    screen.fill([0,0,0])

    if d == 0:
        camera_veiw = [[[world[z+l][over_size(x+(i+(j+1)//2)-5)][over_size(y-(i-(j//2)))] for i in range(tilex)] for j in range(tiley)] for l in range(10)]
        obgect_camera_veiw = [[[world_obgects[z+l][over_size(x+(i+(j+1)//2)-5)][over_size(y-(i-(j//2)))] for i in range(tilex)] for j in range(tiley)] for l in range(10)]
    if d == 1:
        camera_veiw = [[[world[z+l][over_size(x+(((tilex-1)-i)+(j+1)//2)-4)][over_size(y+(((tilex-1)-i)-(j//2)))] for i in range(tilex)] for j in range(tiley)] for l in range(10)]
        obgect_camera_veiw = [[[world_obgects[z+l][over_size(x+(((tilex-1)-i)+(j+1)//2)-4)][over_size(y+(((tilex-1)-i)-(j//2)))] for i in range(tilex)] for j in range(tiley)] for l in range(10)]
    if d == 2:
        camera_veiw = [[[world[z+l][over_size(x+(((tilex-1)-i)+(((tiley-1)-j)+1)//2)-4)][over_size(y-(((tilex-1)-i)-(((tiley-1)-j)//2)))] for i in range(tilex)] for j in range(tiley)] for l in range(10)]
        obgect_camera_veiw = [[[world_obgects[z+l][over_size(x+(((tilex-1)-i)+(((tiley-1)-j)+1)//2)-4)][over_size(y-(((tilex-1)-i)-(((tiley-1)-j)//2)))] for i in range(tilex)] for j in range(tiley)] for l in range(10)]
    if d == 3:
        camera_veiw = [[[world[z+l][over_size(x+(i+(((tiley-1)-j)+1)//2)-4)][over_size(y+(i-(((tiley-1)-j)//2)))] for i in range(tilex)] for j in range(tiley)] for l in range(10)]
        obgect_camera_veiw = [[[world_obgects[z+l][over_size(x+(i+(((tiley-1)-j)+1)//2)-4)][over_size(y+(i-(((tiley-1)-j)//2)))] for i in range(tilex)] for j in range(tiley)] for l in range(10)]

    
    for i in range(len(camera_veiw)):
        for j in range(len(camera_veiw[i])):
            for l in range(len(camera_veiw[i][j])):
                if camera_veiw[i][j][l]:
                    if d==0 or d ==2:
                        screen.blit(blocks[camera_veiw[i][j][l]][animation_index%len(blocks['cube'])],[(l*pixel_size*24)+(12*(j%2)*pixel_size)-(12*pixel_size),(j*pixel_size*6)+(i*pixel_size*-15)-(6*pixel_size)])                            
                    else:
                        screen.blit(blocks[camera_veiw[i][j][l]][animation_index%len(blocks['cube'])],[(l*pixel_size*24)+(-12*(j%2)*pixel_size),(j*pixel_size*6)+(i*pixel_size*-15)-(6*pixel_size)])
                        
                if obgect_camera_veiw[i][j][l]:
                    if d==0 or d==2:
                        screen.blit(pygame.transform.scale((obgect_camera_veiw[i][j][l]).image,[11*pixel_size,23*pixel_size]),[(l*pixel_size*24)+(12*(j%2)*pixel_size)-(12*pixel_size),(j*pixel_size*6)+(i*pixel_size*-15)-(6*pixel_size)])
                    else:
                        screen.blit(pygame.transform.scale((obgect_camera_veiw[i][j][l]).image,[11*pixel_size,23*pixel_size]),[(l*pixel_size*24)+(-12*(j%2)*pixel_size),(j*pixel_size*6)+(i*pixel_size*-15)-(6*pixel_size)])
                        
    
    pygame.display.update()

a = 0
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode(((event.w//pixel_size)*pixel_size,(event.h//pixel_size)*pixel_size),pygame.RESIZABLE)
            if event.w//384 != 0:
                pixel_size = event.w//384
            screen = pygame.display.set_mode(((event.w//pixel_size)*pixel_size,(event.h//pixel_size)*pixel_size),pygame.RESIZABLE)
            width = (event.w//pixel_size)*pixel_size
            height = (event.h//pixel_size)*pixel_size
            tilex = (width//(24*pixel_size))+2
            tiley = (height//(6*pixel_size))+2
            if tilex%2 != 0: tilex += 1 
            if tiley%2 != 0: tiley += 1 
            set_art()
    keys = pygame.key.get_pressed()

    
    if a != 3:
        a += 1
    else:
        a = 0
    
    render(0,0,0,0)
    
    
    if animation_index == 99:
        animation_index = 0
    else:
        animation_index += 1
    clock.tick(1)









