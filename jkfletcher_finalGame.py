"""Sock Goblins!
    Player tries to collect as many socks as possible in 30 seconds
    Goblins are also trying to pick up socks
    Player earns extra points for making pairs"""

import random, pygame, simpleGE

class Game(simpleGE.Scene):
    def __init__(self):
        super().__init__()
        
        self.character = Character(self)
        
        self.numSocks = 4
        self.socks = []
        for i in range(self.numSocks):
            self.socks.append(Sock(self))
        
        self.tileset = []
        
        self.ROWS = 15
        self.COLS = 20
        
        self.loadMap()
        
        self.sprites = [self.character, self.tileset, self.socks]
        
    def loadMap(self):
        map = [
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,1],
            [1,0,0,0,0,1,1,1,1,1,0,0,1,1,1,0,0,0,0,1],
            [1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,1,1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1],
            [1,0,0,1,1,1,1,1,0,0,1,0,0,0,0,0,0,0,0,1],
            [1,0,0,1,0,0,0,0,0,0,1,0,0,1,1,1,1,0,0,1],
            [1,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,1],
            [1,0,0,1,1,1,1,1,0,0,1,0,0,0,0,0,1,0,0,1],
            [1,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
            ]
        
        for row in range(self.ROWS):
            self.tileset.append([])
            for col in range(self.COLS):
                currentVal = map[row][col]
                newTile = Tile(self)
                newTile.setState(currentVal)
                newTile.tilePos = (row, col)
                xPos = 16 + (32 * col)
                yPos = 16 + (32 * row)
                newTile.x = xPos
                newTile.y = yPos
                self.tileset[row].append(newTile)
        
class Character(simpleGE.Sprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.walkAnim =  simpleGE.SpriteSheet("character-spreadsheet.png", (64, 64), 4, 9, 0.1)
        
        self.walkAnim.startCol = 1
        self.animRow = 2
        self.moveSpeed = 3
        
        self.tileOver = (0, 0)
        self.tileState = 0
        
    def process(self):
        self.correction = (0, 0)
        self.dx = 0
        self.dy = 0
        walking = False
        if self.isKeyPressed(pygame.K_w):
            self.animRow = 0
            self.dy = -self.moveSpeed
            self.correction = (0, -self.moveSpeed)
            walking = True
        if self.isKeyPressed(pygame.K_a):
            self.animRow = 1
            self.dx = -self.moveSpeed
            self.correction = (self.moveSpeed, 0)
            walking = True
        if self.isKeyPressed(pygame.K_s):
            self.animRow = 2
            self.dy = self.moveSpeed
            self.correction = (0, self.moveSpeed)
            walking = True
        if self.isKeyPressed(pygame.K_d):
            self.animRow = 3
            self.dx = self.moveSpeed
            self.correction = (-self.moveSpeed, 0)
            walking = True
            
        if walking:
            self.copyImage(self.walkAnim.getNext(self.animRow))
        else:
            self.copyImage(self.walkAnim.getCellImage(0, self.animRow))
            
        if self.tileState == 1:
            self.x = self.correction[0]
            self.y = self.correction[1]
            walking = False
            
            
class Tile(simpleGE.Sprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.images = [
            pygame.image.load("woodenfloor.png"),
            pygame.image.load("default_tiles.png")]
        
        self.stateName = ["floor", "wall"]
        
        self.setSize(16, 16)
        self.FLOOR = 0
        self.WALL = 1
        self.state = self.FLOOR
        
    def setState(self, state):
        self.state = state
        self.copyImage(self.images[state])
        
    def process(self):
        if self.collidesWith(self.scene.character):
            stateInfo = self.stateName[self.state]
            self.scene.character.tileOver = self.tilePos
            self.scene.character.tilestate = self.state
            rowCol = f"{self.tilePos[0]}, {self.tilePos[1]}"
            
class Sock(simpleGE.Sprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.sockImages = ["sock-0.png", "sock-1.png", "sock-2.png", "sock-3.png"]
        self.setSize = (8, 8)
        self.getImage = random.randrange(3)
        self.setImage(self.sockImages[self.getImage])
        self.y = random.randint(0, self.screenHeight)
        self.x = random.randint(0, self.screenWidth)
        
def main():
    game = Game()
    game.start()
    
if __name__ == "__main__":
    main()