import pygame
import sys
from elemant import backgroundcolor, size_cell, HEIGHT, WIDTH, Ball, Magnet, Target

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
purple = (130, 0, 138)

class LogicMagnet:
    def __init__(self, n, full_steps):
        pygame.init()
        self.n = n
        self.full_steps = full_steps
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("لعبة المغناطيس")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 40)
        self.grid = [[None for _ in range(n)] for _ in range(n)]
        self.magnets = []
        self.balls = []
        self.targets = []
        self.blocks = [] 
        self.steps = 0
        self.win = False
        self.lost = False
        self.selecte_magnrt = None
        self.isplayer = True 
        
    def add_target(self,x, y):
            self.targets.append(Target(x, y))
        
    def add_ball(self,x, y):
            self.balls.append(Ball(x, y))
    
    def add_magnet(self, x,y, type):
            self.magnets.append(Magnet(x, y, type))    

    def add_block(self, x,  y):  
            self.blocks.append((x, y))

    def is_block(self ,x, y): 
        return (x, y) in self.blocks
    def draw_grid(self):
        for x in range(0, WIDTH, size_cell):
            for y in range(0, HEIGHT, size_cell):
                rect = pygame.Rect(x, y, size_cell, size_cell)
                color = WHITE if (y // size_cell < self.n and x // size_cell < self.n) else purple
                pygame.draw.rect(self.screen, color, rect, 1)


    def draw_elemant(self):
        for block in self.blocks:  
            block_rect = pygame.Rect(block[0] * size_cell, block[1] * size_cell, size_cell, size_cell)
            pygame.draw.rect(self.screen, purple, block_rect)

        for magnet in self.magnets:
            pygame.draw.circle(self.screen, RED if magnet.type == "+" else BLUE, magnet.position, size_cell // 2)
        
        for ball in self.balls:
            pygame.draw.circle(self.screen, BLACK, ball.position, size_cell // 4)
        
        for target in self.targets:
            pygame.draw.circle(self.screen, GREEN, target.position, size_cell // 4)
 
 
    def apply_magnet_impact(self, magnet):
        for ball in self.balls:
            if not ball.is_on_target:
                if magnet.type == "-":
                     ball.move_away_from(magnet.x, magnet.y, self.magnets, self.n)
                     
                elif magnet.type == "+":
                     ball.move_towards(magnet.x, magnet.y, self.magnets, self.n)
        for ball in self.balls:
            ball.check_target(self.targets)
            
    def move_magnet(self, magnet, x, y):
        if 0 <= x < self.n and 0 <= y < self.n and not self.is_block(x, y):  
            magnet.move(x, y)
            if self.isplayer:  
                self.steps += 1
            self.apply_magnet_impact(magnet)           
            

    def check_win(self):
        if self.isplayer and self.full_steps < self.steps:
            self.lost = True
            return False

        balls_on_target = all(ball.is_on_target for ball in self.balls)#هنا تحقق جميع الكرات الحديدية في الاهداف
        #هنا تحقق من ان المغانط  في الاهداف
        magnets_on_target = all(
            any(
            (target.x, target.y) == (magnet.x, magnet.y) for target in self.targets
            )
            for magnet in self.magnets)
        
        if balls_on_target and magnets_on_target:
            self.win = True
        return self.win

    def message_win(self):
        win_text = self.font.render(f"you win game bro in {self.steps}steps!", True, BLACK)
        self.screen.blit(win_text, (WIDTH // 6, HEIGHT // 2))

    def message_lost(self):
        loss_text = self.font.render("you lost good luck bro", True, RED)
        self.screen.blit(loss_text, (WIDTH // 6,HEIGHT // 2))

    def handle_mouse_click(self, pos):
        x , y = pos[0] // size_cell, pos[1] // size_cell
        if self.selecte_magnrt:
            self.move_magnet(self.selecte_magnrt, x, y)
            self.selecte_magnrt = None
        else:
            for magnet in self.magnets:
                if (magnet.x, magnet.y) == (x, y):
                    self.selecte_magnrt = magnet
                    break

    def game_loop(self):
        while True:
            self.screen.fill(backgroundcolor)
            self.draw_grid()
            self.draw_elemant()

            if self.win:
                self.message_win()
            elif self.lost:
                self.message_lost()
            else:
                if self.check_win():
                    self.win = True
                elif self.lost:
                    self.message_lost()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        self.isplayer = True  
                        self.handle_mouse_click(pygame.mouse.get_pos())
            
            pygame.display.flip()
            self.clock.tick(60)
