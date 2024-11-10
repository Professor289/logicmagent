from collections import deque
import pygame
import sys
from elemant import MAGNET, Ball, Taraget,cellSize

width=700
height=500
backgroundcolor = (210, 210, 210)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
PURPLE = (128, 0, 128)

class MagnetBRo:
    def __init__(self, n , allStep):
        pygame.init()
        self.n=n
        self.allStep=allStep
        self.screen = pygame.display.set_mode((width,height))
        self.clock= pygame.time.Clock()
        pygame.display.set_caption("magnetBro")
        self.font=pygame.font.SysFont(None,40)
        self.gred= [[None for _ in range(n)]for _ in range(n)]
        self.magnets=[]
        self.balls=[]
        self.targets=[]
        self.blocks = [] 
        self.step=0
        self.win=False
        self.lost=False
        self.is_playerMode=True
        self.solution_steps = []
        self.selected_magnet=None
        
        
    def draw_grid(self):
        for x in range(0,width,cellSize):
            for y in range(0,height,cellSize):
                rect=pygame.Rect(x,y,cellSize,cellSize)
                color= WHITE if(x / cellSize <self.n and y / cellSize <self.n)else PURPLE
                pygame.draw.rect(self.screen,color,rect,1)  
                
    def drawElemant(self):
        for magnet in self.magnets:
            pygame.draw.circle(self.screen,RED if magnet.type=="+" else BLUE,magnet.position,cellSize /2)   
        
        for ball in self.balls:
            pygame.draw.circle(self.screen, BLACK,ball.position,cellSize/4)
            
        for target in self.targets:
            pygame.draw.circle(self.screen,GREEN,target.position, cellSize /4) 
            
        for block in self.blocks:  
            block_rect = pygame.Rect(block[0] * cellSize, block[1] * cellSize, cellSize, cellSize)
            pygame.draw.rect(self.screen, PURPLE, block_rect)
            
    def add_magnet(self,x,y,type):
        self.magnets.append(MAGNET(x,y,type))
        
        
    def add_Ball(self,x,y):
        self.balls.append(Ball(x,y))               
        
    def add_target(self,x,y):
        self.targets.append(Taraget(x,y))

    def add_block(self, x, y):  
       self.blocks.append((x, y))

    def is_block(self, x, y): 
        return (x, y) in self.blocks 
       
    def move_magnet(self,magnet,x,y): 
        if 0<=  x <self.n  and 0<= y <self.n and not self.is_block(x,y):
            magnet.move(x,y)
            if self.is_playerMode:
                self.step += 1
            self.apply_impact_magnet(magnet)
            return True
        return False
                
                
    def apply_impact_magnet(self,magnet):
        for ball in self.balls:
            if  not ball.is_target:
                if magnet.type =="+":
                    ball.move_towrds(magnet.x,magnet.y,self.n)
                elif magnet.type == "-":
                    ball.move_away(magnet.x,magnet.y,self.n)
        for ball in self.balls:
            ball.check_target(self.targets)
            
    def check_win(self):
        if self.is_playerMode and self.step >self.n:
            self.lost =True
            return False
        
        balls_isOn_Target= all(ball.is_target for ball in self.balls)
        magnets_IsOn_Target=all(any((target.x,target.y)==(magnet.x,magnet.y) for target in self.targets) 
                                for magnet in self.magnets)
        
        if balls_isOn_Target and magnets_IsOn_Target :
            self.win=True
        return self.win        
            
                
    def win_massege(self):
        win_text= self.font.render(f"You won the game in {self.step} steps!",True,BLACK)
        self.screen.blit(win_text,(width/6,height/2))
        
    def lost_massege(self):
        win_text= self.font.render(f"You lost ",True,RED)
        self.screen.blit(win_text,(width/6,height/2)) 
        
    def mouse_click(self,pos):
        x,y =pos[0] / cellSize ,pos [1] /cellSize
        if self.selected_magnet:
            self.move_magnet(self.selected_magnet,x,y)
            self.selected_magnet = None
        else :
            for magnet in self.magnets:
                 if (magnet.x,magnet.y) == (x,y): 
                     self.selected_magnet=magnet
                     break
                 
 
    def DFS(self):  
        self.is_playerMode=False
        magnet_x1 ,magnet_y1=self.magnets[0].x, self.magnets[0].y
        magnet_x2 ,magnet_y2=self.magnets[1].x, self.magnets[1].y
        Stack=[(magnet_x1,magnet_y1,  magnet_x2 if len(self.magnets)>1 else None,  magnet_y2 if len(self.magnets) > 1 else None,  [])]
        visited=set()
        
        while Stack:
            x1,y1,x2,y2 ,path = Stack.pop()
            if ((x1,y1) , (x2,y2)) in visited:
                continue
            visited.add(((x1,y1) , (x2,y2)))
             
            self.move_magnet(self.magnets[0],x1,y1)
            if x2 is not None and y2 is not None:
                self.move_magnet(self.magnets[1],x2,y2)
            path.append( ((x1,y1),(x2,y2)) )
            
            if self.check_win():
                self.solution_steps=path
                print(f"DFS solution path: {self.solution_steps}")
                return True
            
            diraction=[(-1,0),(1,0),(0,-1),(0,1)]
            for dx1 , dy1 in diraction:
                new_x,new_y= x1+dx1 ,y1+dy1
                if 0 <= new_x < self.n and 0 <= new_y <self.n and not self.is_block(new_x, new_y):
                    for dx2, dy2 in (diraction if x2 is not None else [(0, 0)] ):
                        new_x2, new_y2 = (x2+dx2 , y2 + dy2) if x2 is not None else (None,None)
                        if x2 is None or (0 <= new_x2 < self.n and 0 <= new_y2 < self.n  and not self.is_block(new_x2, new_y2) and (new_x != new_x2 or new_y != new_y2)) :
                            Stack.append((new_x,new_y,new_x2,new_y2,path))
        print("DFS no solution")
        return False
    
    def BFS(self):
        self.is_playerMode=False
        magnet_x1, magnet_y1 =self.magnets[0].x, self.magnets[0].y
        magnet_x2 , magnet_y2 =self.magnets[1].x, self.magnets[1].y
        queue = deque([(magnet_x1,magnet_y1,self.magnets[1].x if len(self.magnets) > 1 else None,self.magnets[1].y if len(self.magnets) > 1 else None , [])])
        visited =set()
        
        while queue:
            x1,y1, x2, y2 ,path = queue.popleft()
            if ((x1,y1) , (x2,y2)) in visited:
                continue
            visited.add(((x1,y1),(x2,y2)))
            
            self.move_magnet(self.magnets[0],x1,y1)
            if x2 is not None and y2 is not None:
                self.move_magnet(self.magnets[1],x2,y2)
            path.append(((x1,y1),(x2,y2) if x2 is not None else None))
            
            if self.check_win():
                self.solution_steps =path
                print(f"DFS solution path: {self.solution_steps}")
                return True
            
            diraction = [(1,0),(-1,0),(0 , 1),(0,-1)]
            for dx , dy in diraction:
                new_x1 ,new_y1 = x1+ dx , dy + y1
                if 0 <= new_x1 < self.n and 0 <= new_y1 < self.n:
                    for dx2 , dy2 in diraction:
                        new_x2, new_y2= (x2 +dx2 , y2 +dy2) if x2 is not None else (None, None) 
                        if x2 is None or (0 <= new_x2 < self.n and 0 <= new_y2 < self.n and not self.is_block(new_x2, new_y2) and (new_x1 != new_x2 or new_y1 != new_y2)):
                            queue.append((new_x1,new_y1,new_x2,new_y2,path))
                            
        print("BFS no solution ")
        return False 
    
                       
    def game_loop(self):
        while True:
            self.screen.fill(backgroundcolor)
            self.draw_grid()
            self.drawElemant()
            
            if self.win:
                self.win_massege()
            elif self.lost:
                self.lost_massege() 
            else:
                if self.check_win():
                    self.win = True
                elif  self.lost:
                    self.lost_massege() 
                
                for event in   pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        self.is_playerMode= True
                        self.mouse_click(pygame.mouse.get_pos())
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_d:
                           print("Starting DFS to solution ")
                           if self.DFS():
                               print("DFS found solution")
                           else:
                               print("DFS not found solution")
                        elif event.key == pygame.K_b:
                            print("BFS Staring solution")
                            if self.BFS():
                                print("BFS found soluntion")
                            else:
                                print("BFS not found solution") 
            pygame.display.flip()
            self.clock.tick(60)
                            