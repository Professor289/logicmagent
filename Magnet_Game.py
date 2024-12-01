from collections import deque
import pygame
import sys
from elemant import MAGNET, Ball, Taraget,cellSize
from queue import PriorityQueue
width=500
height=300
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
        self.cellSize = cellSize

        
    def calculate_distance(self, x, y):
        min_dist = float('inf')
        for target in self.targets:
            target_x, target_y = target.x, target.y
            dist = abs(target_x - x) + abs(target_y - y) 
            min_dist = min(min_dist, dist)
        return min_dist


    def draw_grid(self):
        for x in range(0, self.screen.get_width(), self.cellSize):
            for y in range(0, self.screen.get_height(), self.cellSize):
                rect = pygame.Rect(x, y, self.cellSize, self.cellSize)
                color = WHITE if (x // self.cellSize < self.n and y // self.cellSize < self.n) else PURPLE
                pygame.draw.rect(self.screen, color, rect, 1)

                if x // self.cellSize < self.n and y // self.cellSize < self.n:
                    dist = self.calculate_distance(x // self.cellSize, y // self.cellSize)
                    dist_text = str(dist)
                    cost_text = self.font.render(dist_text, True, BLACK)
                    self.screen.blit(cost_text, (x + 10, y + 10))

    def drawElemant(self):
        for magnet in self.magnets:
            pygame.draw.circle(self.screen,RED if magnet.type=="+" else BLUE,magnet.position,cellSize /2)   
        
        for ball in self.balls:
            pygame.draw.circle(self.screen, BLACK,ball.position,cellSize/2)
            
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
        return (x, y) in self.blocks or any(ball.x == x and ball.y ==y for ball in self.balls) or any(magnet.x== x and magnet.y ==y for magnet in self.magnets)
       
    def move_magnet(self,magnet,x,y): 
        if 0 <=  x <self.n  and 0<= y <self.n and not self.is_block(x,y):
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
                    ball.move_towrds(magnet.x,magnet.y,self.n,self.magnets,self.balls)
                elif magnet.type == "-":
                    ball.move_away(magnet.x,magnet.y,self.n, self.magnets ,self.balls)
            ball.check_target(self.targets)
            
    def check_win(self):
        if self.is_playerMode and self.step > self.n:
            self.lost = True
            return False
        balls_on_targets = all(any((target.x, target.y) == (ball.x, ball.y) for target in self.targets) for ball in self.balls)
        magnets_on_targets = all(any((target.x, target.y) == (magnet.x, magnet.y) for target in self.targets) for magnet in self.magnets)

        if balls_on_targets and magnets_on_targets:
            self.win = True
        
        # target_positions = {(target.x, target.y) for target in self.targets}
        # magnets_on_targets = all((magnet.x, magnet.y) in target_positions for magnet in self.magnets)

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
                 
######################################################################################################################### 
    def DFS(self):  
        self.is_playerMode=False
        magnet_x1 ,magnet_y1=self.magnets[0].x, self.magnets[0].y
        Stack=[(magnet_x1,magnet_y1,  self.magnets[1].x if len(self.magnets)>1 else None,  self.magnets[1].y if len(self.magnets) > 1 else None,  [])]
        visited=set()
        
        while Stack:
            x1,y1,x2,y2 ,path = Stack.pop()
            if ((x1,y1) , (x2,y2)) in visited:
                continue
            visited.add(((x1,y1) , (x2,y2)))
             
            self.move_magnet(self.magnets[0],x1,y1)
            if x2 is not None and y2 is not None:
                self.move_magnet(self.magnets[1],x2,y2)
            path.append( ((x1,y1),(x2,y2)) if x2 is not None else None)
            
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
            # for new_x1 in range(self.n):
            #     for new_y1 in range(self.n):
            #         if 0 <= new_x1 < self.n and 0 <= new_y1 < self.n and not self.is_block(new_x1, new_y1):
            #             for dx2, dy2 in ([(0, 0)] if x2 is None else [(dx, dy) for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]]):
            #                 new_x2, new_y2 = (x2 + dx2, y2 + dy2) if x2 is not None else (None, None)
            #                 if x2 is None or (0 <= new_x2 < self.n and 0 <= new_y2 < self.n and not self.is_block(new_x2, new_y2) and (new_x1 != new_x2 or new_y1 != new_y2)):
            #                     Stack.append((new_x1, new_y1, new_x2, new_y2, new_path))
                
        print("DFS no solution")
        return False
###################################################################################################################################################################    
    def BFS(self):
        self.is_playerMode=False
        magnet_x1, magnet_y1 =self.magnets[0].x, self.magnets[0].y
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
##########################################################################    
    def cost_function(self, x1,y1,x2,y2):
        cost = self.calculate_distance(x1,y1)
        if x2 is not None and y2 is not None:
            cost += self.calculate_distance(x2,y2)
        return cost
    
    # def cost_function(self, x1, y1, new_x1, new_y1, x2, y2, new_x2, new_y2):
    #     distance_1 = abs(x1 - new_x1) + abs(y1 - new_y1)
    #     distance_2 = abs(x2 - new_x2) + abs(y2 - new_y2) if x2 is not None else 0
    #     return distance_1 + distance_2     
    
    def UCS(self):
        self.is_playerMode= False
        magnet_x1 , magnet_y1 = self.magnets[0].x, self.magnets[0].y
        state=( magnet_x1, magnet_y1 , self.magnets[1].x if len(self.magnets) > 1 else None, self.magnets[1].y if len(self.magnets) > 1 else None)
    
        P_Q = PriorityQueue()
        P_Q.put((0,state,[]))
        visited= set()
        
        while P_Q.not_empty:
            cost , (x1,y1,x2,y2), path = P_Q.get()
            if ((x1,y1), (x2,y2)) in visited:
                continue
            visited.add(((x1,y1), (x2,y2)))
            
            self.move_magnet(self.magnets[0], x1,y1)
            if x2 is not None and y2 is not None:
                self.move_magnet(self.magnets[1],x2,y2)
            # path.append(((x1,y1),(x2,y2) if x2 is not None else None))
            new_path = path + [((x1,y1),(x2,y2) if x2 is not None else None)]
            
            for new_x1 in range(self.n):
                for new_y1 in range(self.n):
                    if  0 <= new_x1 < self.n and 0 <= new_y1 < self.n and not self.is_block(new_x1, new_y1):
                        for new_x2 in range(self.n) if x2 is not None else [None]:
                            for new_y2 in range(self.n) if x2 is not None else [None]:
                                if x2 is None or (not self.is_block(new_x2, new_y2) and 
                                                (new_x1 != new_x2 or new_y1 != new_y2)):
                                    # move_cost = self.cost_function(x1, y1, new_x1, new_y1, x2, y2, new_x2, new_y2)

                                    move_cost = self.cost_function(new_x1, new_y1, new_x2, new_y2)
                                    new_cost = cost + move_cost
                                    new_state = (new_x1, new_y1, new_x2, new_y2)
                                
                                    P_Q.put((new_cost, new_state, new_path))
                                    
            if self.check_win():
                self.solution_steps=path
                print(f"UCS path solution: {self.solution_steps}")
                print(f"cost : {new_cost}")
                return True                        

        print("UCS not found solution")
        return False                     
###########################################################################################     
    # def calculate_total_cost(self, positions):
    #     total_cost = 0
    #     for i, (x, y) in enumerate(positions):
    #         for ball in self.balls:
    #             distance = abs(x - ball.x) + abs(y - ball.y)
    #             total_cost += distance  
    #         for target in self.targets:
    #             distance = abs(x - target.x) + abs(y - target.y)
    #             total_cost += distance  
    #     return total_cost
    def total_cost(self , postions):
        total_cost = 0
        for i,(x,y) in enumerate(postions):
            for target in self.targets:
                target_cost = self.calculate_distance(x,y)
                total_cost += target_cost
        return total_cost
                
     
    def is_valid_position(self, position):
        x, y = position
        return 0 <= x < self.n and 0 <= y < self.n
    
    def getAllPositions(self):
        positions = []
        for x in range(self.n):
            for y in range(self.n):
                positions.append((x,y))
        return positions
    
    def get_neighbors(self, magnet_postion):
        neighbors =[]
        all_postions= self.getAllPositions()
        
        for position in all_postions:
            x, y = position
            if position != magnet_postion:
                if self.is_valid_position(position) and not self.is_block(x, y):
                    neighbors.append(position)
        return neighbors
    
    # def get_neighbors_for_magnet(self, magnet_position):
    #     neighbors = []
    #     x, y = magnet_position
    #     for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
    #         new_position = (x + dx, y + dy)
    #         if self.is_valid_position(new_position) and not self.is_block(new_position[0], new_position[1]):
    #             neighbors.append(new_position)
    #     return neighbors
    
    def hill_climbing(self):
        self.is_playerMode = False
        if len(self.magnets) <1:
            return False
        
        current_positions = [(magnet.x, magnet.y) if magnet else None for magnet in self.magnets]

        current_cost = self.total_cost([pos for pos in current_positions if pos is not None])
        step = 0
        max_attempts = 100

        while step < max_attempts:
            moved = False
            
            for i, current_position in enumerate(current_positions):
                if current_position is None:
                    continue
                neighbors = self.get_neighbors(current_position)
                best_neighbor = None
                best_cost = current_cost
                
                for neighbor in neighbors:
                    # new_positions = current_positions[:i] + [neighbor] + current_positions[i+1:]
                    new_positions = current_positions[:]
                    new_positions[i] = neighbor
                    
                    neighbor_cost = self.total_cost(new_positions)
                    if neighbor_cost < best_cost:
                        best_cost = neighbor_cost
                        best_neighbor = neighbor
                        
                if best_neighbor:
                    current_positions[i]= best_neighbor
                    current_cost=best_cost
                    self.move_magnet(self.magnets[i], *best_neighbor)
                    print(f"Magnet {i + 1} moved to {best_neighbor}")
                    moved = True
                    if self.check_win():
                        print(f"Found solution insteps")
                        return True 
                    
            if not moved:
                print(f"No improve step {step}")
                break
            step += 1      
            
        print(f"Failed find solution after {max_attempts} steps")
        return False             
#######################################################################################################                    
    def heuristic(self,x,y,targets):
        return min (abs(x - target.x) + abs(y- target.y) for target in targets)

    def compute_move_cost(self, x1, y1, new_x1, new_y1, x2, y2, new_x2, new_y2):
        distance_1 = abs(x1 - new_x1) + abs(y1 - new_y1)
        distance_2 = abs(x2 - new_x2) + abs(y2 - new_y2) if x2 is not None else 0
        return distance_1 + distance_2  
    # def compute_move_cost(self, x1, y1, new_x1, new_y1, x2, y2, new_x2, new_y2):
    #     cost_1 = self.calculate_distance(new_x1, new_y1)
    #     cost_2 = self.calculate_distance(new_x2, new_y2) if x2 is not None else 0
    #     return cost_1 + cost_2
    
    def A_star(self):
        self.is_playerMode = False
        start_state = (self.magnets[0].x, self.magnets[0].y, 
                    self.magnets[1].x if len(self.magnets) > 1 else None,
                    self.magnets[1].y if len(self.magnets) > 1 else None)
        start_cost = 0  
        start_heuristic = self.heuristic(self.magnets[0].x, self.magnets[0].y, self.targets)

        pq = PriorityQueue()
        pq.put((start_cost + start_heuristic, start_cost, start_state, []))
        visited = set()

        while not pq.empty():
            f, g, (x1, y1, x2, y2), path = pq.get()

            if ((x1, y1), (x2, y2)) in visited:
                continue
            visited.add(((x1, y1), (x2, y2)))

            self.move_magnet(self.magnets[0], x1, y1)
            if x2 is not None and y2 is not None:
                self.move_magnet(self.magnets[1], x2, y2)
            # path.append(((x1, y1), (x2, y2) if x2 is not None else None))
            new_path = path + [((x1, y1), (x2, y2) if x2 is not None else None)]
            
            if self.check_win():
                    self.solution_steps = new_path
                    print(f"A* Solution Path: {self.solution_steps}")
                    print(f"Total cost: {g}")
                    return True        
                
            for new_x1 in range(self.n):
                for new_y1 in range(self.n):
                    if 0 <= new_x1 < self.n and 0 <= new_y1 < self.n and not self.is_block(new_x1, new_y1):
                        for new_x2 in (range(self.n) if x2 is not None else [None]):
                            for new_y2 in (range(self.n) if x2 is not None else [None]):
                                if x2 is None or (0 <= new_x2 < self.n and 0 <= new_y2 < self.n and
                                                not self.is_block(new_x2, new_y2) and
                                                (new_x1 != new_x2 or new_y1 != new_y2)):

                                    move_cost = self.compute_move_cost(x1, y1, new_x1, new_y1, x2, y2, new_x2, new_y2)
                                    new_g = g + move_cost
                                    h1 = self.heuristic(new_x1, new_y1, self.targets)
                                    h2 = self.heuristic(new_x2, new_y2, self.targets) if x2 is not None else 0
                                    new_h = h1 + h2
                                    pq.put((new_g + new_h, new_g, (new_x1, new_y1, new_x2, new_y2), new_path))
        print("A Star No solution found")
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
                
                for event in  pygame.event.get():
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
                                print("BFS found a soluntion")
                            else:
                                print("BFS not found a solution")
                        elif event.key == pygame.K_u:
                            print("UCS Staring for solution")
                            if self.UCS():
                                print("UCS found a soluntion")
                            else:
                                print("UCS not found a solution")  
                        elif event.key == pygame.K_h:  
                                    print("Starting Hill Climbing solution")
                                    if self.hill_climbing():  
                                        print("Hill Climbing found solution")
                                    else:
                                        print("Hill Climbing did not find solution")            
                        elif event.key == pygame.K_a:  
                                    print("Starting A Star solution")
                                    if self.A_star():  
                                        print("A Star found solution")
                                    else:
                                        print("A Star did not found solution")                  
            pygame.display.flip()
            self.clock.tick(60)
                            