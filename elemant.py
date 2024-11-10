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

    def move_towrds(self, magnet_x, magnet_y, grid_size):
        if self.x == magnet_x:  
            new_y = self.y + (1 if magnet_y > self.y else -1)
            if 0 <= new_y < grid_size:
                self.y = new_y
        elif self.y == magnet_y: 
            new_x = self.x + (1 if magnet_x > self.x else -1)
            if 0 <= new_x < grid_size:
                self.x = new_x
        self.update_position()


    def move_away(self, magnet_x, magnet_y, grid_size):
        if self.x == magnet_x:  
            new_y = self.y + (1 if self.y > magnet_y else -1)
            if 0 <= new_y < grid_size:
                self.y = new_y
        elif self.y == magnet_y:  
            new_x = self.x + (1 if self.x > magnet_x else -1)
            if 0 <= new_x < grid_size:
                self.x = new_x
        self.update_position()    
                         
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
                   
                
                
                
               
