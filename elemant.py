WIDTH = 700
HEIGHT = 300
size_cell = 60
backgroundcolor = (201, 200, 201)
class Magnet:
    def __init__(self, x, y, type):
        self.x = x
        self.y = y
        self.type = type
        self.position = (x * size_cell + size_cell // 2, y * size_cell + size_cell // 2)

    def move(self, x, y):
        self.x = x
        self.y = y
        self.position = (x * size_cell + size_cell // 2, y * size_cell + size_cell // 2)

class Ball:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.position = (x * size_cell + size_cell // 2, y * size_cell + size_cell // 2)
        self.is_on_target = False

    def move_towards(self, magnet_x, magnet_y, magnets, grid_size):
        if self.x == magnet_x and abs(self.y - magnet_y) > 1:
            new_y = self.y + 1 if self.y < magnet_y else self.y - 1
            if 0 <= new_y < grid_size: 
                self.y = new_y
        elif self.y == magnet_y and abs(self.x - magnet_x) > 1:
            new_x = self.x + 1 if self.x < magnet_x else self.x - 1
            if 0 <= new_x < grid_size: 
                self.x = new_x
        self.update_position()

    def move_away_from(self, magnet_x, magnet_y, magnets, grid_size):
        if self.x == magnet_x and abs(self.y - magnet_y) > 0:
            new_y = self.y - 1 if self.y < magnet_y else self.y + 1
            if 0 <= new_y < grid_size:  
                self.y = new_y
        elif self.y == magnet_y and abs(self.x - magnet_x) > 0:
            new_x = self.x - 1 if self.x < magnet_x else self.x + 1
            if 0 <= new_x < grid_size: 
                self.x = new_x
        self.update_position()


    def update_position(self):
        self.position = (self.x * size_cell + size_cell // 2, self.y * size_cell + size_cell // 2)

    def check_target(self, targets):
        for target in targets:
            if self.position == target.position:
                self.is_on_target = True
                break

class Target:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.position = (x * size_cell + size_cell // 2, y * size_cell + size_cell // 2)
