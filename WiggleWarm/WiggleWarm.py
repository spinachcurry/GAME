import pygame
import os
import sys
import random
import time

# 게입창 초기 위치 
win_posx = 700
win_posy = 300
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (win_posx, win_posy)


# 윈도우창 설정 
WINDOW_WIDTH = 540
WINDOW_HEIGHT = 600
GRID = 30
GRID_WIDTH = int(WINDOW_WIDTH/GRID)
GRID_HEIGHT = int(WINDOW_HEIGHT/GRID)


# 색상 설정
BLACK = 0,0,0
WHITE = 255,255,255
RED = 255,0,0
GREEN1 = 25,102,25
GREEN2 = 51,204,51
GREEN3 = 233,249,185
BLUE = 17,17,212
LIGHT_BLUE1 = 153,204,255
LIGHT_BLUE2 = 204,229,255

NORTH = ( 0, -1)
SOUTH = ( 0,  1)
WEST  = (-1,  0)
EAST  = ( 1,  0)


# 지렁이 클래스
class Warm: 
    def __init__(self):
        self.length = 1
        self.create_warm()
        self.color1 = GREEN2
        self.color2 = GREEN3
        self.head_color = GREEN1
        
    def create_warm(self):
        self.length = 3
        self.positions = [(int(WINDOW_WIDTH/2), int(WINDOW_HEIGHT/2))]
        self.direction = random.choice([NORTH, SOUTH, WEST, EAST])
        global game_score
        game_score = 0
        
    def move_warm(self, surface):
        
        #print(len(self.positions))
        head = self.get_haed_position()
        x,y = self.direction
        next = ((head[0] + (x*GRID)) % WINDOW_WIDTH, (head[1] + (y*GRID)) % WINDOW_HEIGHT)
        if next in self.positions[2:]:
            self.create_warm()
            gameover(surface)
        else:
            self.positions.insert(0, next)
            if len(self.positions) > self.length:
                del self.positions[-1]
                
    def draw_warm(self, surface):
        for index, pos in enumerate(self.positions):
            if index == 0:
                draw_object(surface, self.head_color, pos)
            elif index % 2 == 0:
                draw_object(surface, self.color1, pos)
            else:
                draw_object(surface, self.color2, pos)
            
    def game_control(self, arrowkey):
        if(arrowkey[0]*-1, arrowkey[1]*-1) == self.direction:
            return
        else:
            self.direction = arrowkey
            
    def get_haed_position(self):
        return self.positions[0]
    
# 먹이 클래스
class Feed:
    def __init__(self):
        self.position = (0, 0)
        self.color = RED
        self.randomize_feed()
        
    def randomize_feed(self):
        self.position = (random.randint(0, GRID_WIDTH-1) * GRID,
                         random.randint(0, GRID_HEIGHT-1) * GRID)
    
    def draw_feed(self, surface):
        draw_object(surface, self.color, self.position)
        

# 전역
def draw_background(surface):
    background = pygame.Rect((0,0),(WINDOW_WIDTH, WINDOW_WIDTH))
    pygame.draw.rect(surface, WHITE, background)
    draw_grid(surface)
    
def draw_grid(surface):
    for row in range(0,int(GRID_HEIGHT)):
        for col in range(0, int(GRID_WIDTH)):
            if (row+col) % 2 == 0:
                rect = pygame.Rect((col*GRID, row*GRID),(GRID, GRID))
                pygame.draw.rect(surface, LIGHT_BLUE1, rect)
            else:
                rect = pygame.Rect((col*GRID, row*GRID), (GRID, GRID))
                pygame.draw.rect(surface, LIGHT_BLUE2, rect)

def draw_object(surface, color, pos):
    rect = pygame.Rect((pos[0], pos[1]),(GRID, GRID))
    pygame.draw.rect(surface, color, rect)
    pygame.draw.rect(surface, WHITE, rect, 1)

def position_confirm(warm, feed_group):
    for feed in feed_group:
        if warm.get_haed_position() == feed.position:
            global game_score
            game_score += 1
            warm.length += 1
            feed.randomize_feed()

def show_info(surface, warm, spped):
    font = pygame.font.SysFont('serif', 30)
    image = font.render(f'score : {game_score}  BodyLength:{warm.length}  LV:{int(speed//2)}', True, BLUE)
    pos = image.get_rect()
    pos.move_ip(20,20)
    pygame.draw.rect(image, BLACK, (pos.x-20, pos.y-20, pos.width, pos.height), 2)
    surface.blit(image, pos)
    
def gameover(surface):
    font = pygame.font.SysFont('serif', 50)
    image = font.render('GAME OVER', True, BLACK)
    pos = image.get_rect()
    pos.move_ip(120,220)
    surface.blit(image,pos)
    pygame.display.update()
    time.sleep(3)
    
player = Warm()
run = True
game_score = 0


# 먹이 그룹
def draw_feed_group(feed_group, surface):
    for feed in feed_group:
        feed.draw_feed(surface)
        
feed = Feed()
feed_group = []

for i in range(3):
    feed = Feed()
    feed_group.append(feed)
    
for feed in feed_group:
    print(feed.position)
    

# 게임 루프
pygame.init()
pygame.display.set_caption('WIGGLE WARM')
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()

while run:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                run = False
            if event.key == pygame.K_UP:
                player.game_control(NORTH)
            if event.key == pygame.K_DOWN:
                player.game_control(SOUTH)
            if event.key == pygame.K_RIGHT:
                player.game_control(EAST)
            if event.key == pygame.K_LEFT:
                player.game_control(WEST)
    
    draw_background(screen)
    player.move_warm(screen)
    position_confirm(player, feed_group)
    player.draw_warm(screen)
    draw_feed_group(feed_group, screen)
    #feed.draw_feed(screen)
    speed = player.length/2
    show_info(screen, player, speed)
    pygame.display.flip()
    pygame.display.update()
    clock.tick(5+speed)
    

#파이게임 일시정지
def pause():
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pause = False
    
# 파이게임 종료
print('pygame closed')
pygame.quit()
sys.exit()