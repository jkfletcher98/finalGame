"""Sock Goblins!
    Player tries to collect as many socks as possible in 30 seconds
    Goblins are also trying to pick up socks
    Player earns extra points for making pairs"""

import random, pygame, simpleGE

class Instructions(simpleGE.Scene):
    def __init__(self, score):
        super().__init__()
        self.background.fill(pygame.Color("light blue"))
        
        self.response = "Play"
        
        self.title = simpleGE.Label()
        self.title.text = "SOCK GOBLINS!!!"
        self.title.center = (320, 60)
        self.title.size = (250, 30)
        
        self.lblInstructions = simpleGE.MultiLabel()
        self.lblInstructions.textLines = [
            "The Sock Goblins are at it again!",
            "Collect your socks before you lose them!",
            "Use WASD to move."
            ]
                                        
        self.lblInstructions.center = (320, 240)
        self.lblInstructions.size = (500, 250)
        
        self.btnPlay = simpleGE.Button()
        self.btnPlay.text = "Play"
        self.btnPlay.center = (100, 400)
        
        self.btnQuit = simpleGE.Button()
        self.btnQuit.text = "Quit"
        self.btnQuit.center = (550, 400)
        
        self.prevScore = score
        self.prevScore = simpleGE.Label()
        self.prevScore.text = f"Previous Score: {score}"
        self.prevScore.center = (320, 400)
        self.prevScore.size = (250, 30)
        
        self.sprites = [self.title, self.lblInstructions, self.btnPlay, self.btnQuit, self.prevScore]
        
    def process(self):
        if self.btnQuit.clicked:
            self.response = "Quit"
            self.stop()
        if self.btnPlay.clicked:
            self.reponse = "Play"
            self.stop()

class Game(simpleGE.Scene):
    def __init__(self):
        super().__init__()
        #temporary until i figure out the map
        #self.background.fill(pygame.Color("light blue"))
        
        self.character = Character(self)
        
        #self.lblOutput = LblOutput()
        
        self.numSocks = 4
        self.socks = []
        for i in range(self.numSocks):
            self.socks.append(Sock(self))
        
        self.tileset = []
        
        self.ROWS = 15
        self.COLS = 20
        
        self.loadMap()
        
        self.lblScore = LblScore()
        self.score = 0
        
        self.timer = simpleGE.Timer()
        self.timer.totalTime = 30
        self.lblTime = LblTime()
        
        self.sprites = [self.tileset, self.socks, self.character, self.lblScore, self.lblTime]
        
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
                
                
                
    def process(self):
        for sock in self.socks:
            if self.character.collidesWith(sock):
                sock.reset()
                self.score += 10
                self.lblScore.text = f"Score: {self.score}"
                
        self.lblTime.text = f"Time: {self.timer.getTimeLeft():.0f}"
        
        if self.timer.getTimeLeft() <= 0:
            print(f"Score: {self.score}")
            self.stop()
        
class Character(simpleGE.Sprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.walkAnim = simpleGE.SpriteSheet("character-spreadsheet.png", (64, 64), 4, 9, 0.1)
        
        self.walkAnim.startCol = 1
        self.animRow = 2
        self.moveSpeed = 3
        
        self.tileOver = (0, 0)
        self.tileState = 0
        
    def process(self):
        
        #walls = [x for x in self.scene.tileset if x.state == 1]
        
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
         
        #for wall in self.scene.walls:
            #if self.collidesWith(wall):
                #self.x += self.correction[0]
                #self.y += self.correction[1]
                
        if walking:
            self.copyImage(self.walkAnim.getNext(self.animRow))
        else:
            self.copyImage(self.walkAnim.getCellImage(0, self.animRow))
            
#I couldn't get this to work quite right
#so I decided to just focus on cleaning up the visuals
class Tile(simpleGE.Sprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.images = [
            pygame.image.load("floor_tiles.png"),
            pygame.image.load("default_tiles.png")]
        
        self.stateName = ["floor", "wall"]
      
        for i in range(0, 2):
           self.images[i] = pygame.transform.scale(self.images[i], (32, 32))
      
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
            self.scene.character.tileState = self.state
        
            rowCol = f"{self.tilePos[0]}, {self.tilePos[1]}"
            
            
            
            #self.scene.lblOutput.text = f"{stateInfo} {rowCol}"
        
#FOR TESTING
#class LblOutput(simpleGE.Label):
    #def __init__(self):
        #super().__init__()
        #self.center = (320, 25)
        #self.text = "current tile: "
        #self.fgColor = "white"
        #self.bgColor = "black"
        #self.clearBlack = True
            
class Sock(simpleGE.Sprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.setSize(48, 48)
        self.sockImages = [pygame.image.load("sock-0.png"),
                           pygame.image.load("sock-1.png"),
                           pygame.image.load("sock-2.png"),
                           pygame.image.load("sock-3.png")]
        
        for i in range(0, 4):
            self.sockImages[i] = pygame.transform.scale(self.sockImages[i], (48, 48))
            
        self.reset()
        
    def reset(self):
        self.getImage = random.randrange(4)
        self.copyImage(self.sockImages[self.getImage])
        self.y = random.randint(48, 432)
        self.x = random.randint(48, 592)
        
class LblScore(simpleGE.Label):
    def __init__(self):
        super().__init__()
        self.text = "Score: 0"
        self.center = (560, 15)
        
class LblTime(simpleGE.Label):
    def __init__(self):
        super().__init__()
        self.text = "Time: 30"
        self.center = (80, 15)
        
def main():
    keepGoing = True
    score = 0
    while keepGoing:
        instructions = Instructions(score)
        instructions.start()
        if instructions.response == "Play":
            game = Game()
            game.start()
            score = game.score
        else:
            keepGoing = False
            exit()
    
if __name__ == "__main__":
    main()