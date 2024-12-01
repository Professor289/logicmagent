cellSize=60
class MAGNET:
    def __init__ (self, x, y , type):
        self.x= x
        self.y= y
        self.type= type
        self.position=(x * cellSize +  cellSize / 2 , y * cellSize + cellSize / 2)
        
    def move(self,x,y):
        self.x=x
        self.y=y        
        self.position=(x * cellSize +  cellSize / 2 , y * cellSize + cellSize / 2)   
         
class Ball:
    def __init__(self,x,y):
        self.x=x
        self.y=y        
        self.position=(x * cellSize +  cellSize // 2 , y * cellSize + cellSize // 2)
        self.is_target = False

    def move_towrds(self, magnet_x, magnet_y, grid_size, magnets, balls):
        if self.x == magnet_x:  
            new_y = self.y + (1 if magnet_y > self.y else -1)
            if self.if_can_move(new_x= self.x , new_y= new_y ,n=grid_size ,magnets=magnets, balls= balls):
                self.y = new_y
        elif self.y == magnet_y: 
            new_x = self.x + (1 if magnet_x > self.x else -1)
            if self.if_can_move(new_x= new_x , new_y= self.y ,n=grid_size ,magnets=magnets, balls= balls):
                self.x = new_x
        self.update_position()


    def move_away(self, magnet_x, magnet_y, grid_size, magnets, balls):
        if self.x == magnet_x:  
            new_y = self.y + (1 if self.y > magnet_y else -1)
            if self.if_can_move(new_x= self.x , new_y= new_y ,n=grid_size ,magnets=magnets, balls= balls):
                self.y = new_y
        elif self.y == magnet_y:  
            new_x = self.x + (1 if self.x > magnet_x else -1)
            if self.if_can_move(new_x= new_x , new_y= self.y ,n=grid_size ,magnets=magnets, balls= balls):
                self.x = new_x
        self.update_position() 
        
    def if_can_move(self, new_x, new_y, n, magnets , balls ):
        if not (0 <= new_x < n and 0<=new_y < n  ):
            return False
        for ball in balls:
            if ball.x == new_x and ball.y == new_y:
                return False
        for magnet in magnets:
            if magnet.x == new_x and magnet.y == new_y:
                return False
        return True    
                
               
                         
    def update_position(self):
        self.position =(self.x * cellSize + cellSize //2 ,self.y * cellSize + cellSize // 2 )    
        
    def check_target(self, targets):
        for target in targets :
            if self.position == target.position:
                self.is_target = True
                break
            
class Taraget :
        def __init__(self,x,y):
            self.x=x
            self.y=y
            self.position =(x * cellSize + cellSize /2 , y * cellSize + cellSize /2 )    
                   
                
                
                
               
