from src.constants import *
import src.globe as globe

class Animation:
    def __init__(self, frames, duration, startingLocation, scrollObj=False):
        self.frames = frames
        self.frameDuration = duration
        self.timeCounter = 0
        self.curSpriteIndex = 0
        self.loc = startingLocation
        self.scrollObj = scrollObj
        
    def getCurSprite(self):
        return self.frames[self.curSpriteIndex]
        
    def update(self, elapsed_time, loc=False):
        self.timeCounter += elapsed_time
        if(loc):
            self.loc = loc
        
        if(self.timeCounter > self.frameDuration and len(self.frames) > 0):
            self.curSpriteIndex += 1
            self.timeCounter = 0
            if(self.curSpriteIndex == len(self.frames)):
                self.curSpriteIndex = 0
        
    def getDrawPos(self):
        if(self.scrollObj):
            pos = globe.Camera.getDrawPos(self.loc)
        else:
            pos = self.loc
        return pos
        
    def draw(self, pos = False):
        if(not(pos)):
            pos = self.getDrawPos()
        if(globe.Camera.amOnScreen(pos)):
            DISPLAYSURF.blit(self.getCurSprite(), pos);
            
    def getWidth(self):
        return self.getCurSprite().get_width()
    
    def getHeight(self):
        return self.getCurSprite().get_height()
        
       
class DebugAnimation(Animation):
    def __init__(self, location, size, color, scrollObj=False):
        super().__init__([],5,location,scrollObj)
        self.size = size
        self.color = color
        
    def update(self, elapsed_time, loc=False):
        if(loc):
            self.loc = loc
            
    def draw(self):
        pos = self.getDrawPos()
        pygame.draw.rect(DISPLAYSURF, self.color, pygame.Rect(pos[0],pos[1],self.size[0], self.size[1]))
        
        
class Camera:
    def __init__(self):
        self.offsetX = 0
        self.offsetY = 0
        self.idealPlayerPos = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
        self.realPlayerPos = self.idealPlayerPos
        self.scollingX = False
        self.scrollingY = False
        
    def start(self, player):
        self.player = player
        self.oldPos = player.pos
        globe.Updater.registerUpdatee(self.update)
        
    def update(self, elapsed_time):
        #Handling x scroll
        if(globe.Room.getWidth() <= WINDOWWIDTH):
            self.realPlayerPos = (self.player.pos[0], self.realPlayerPos[1])
        elif(self.player.pos[0] > WINDOWWIDTH/2 and self.player.pos[0] <= globe.Room.getWidth() - (WINDOWWIDTH /2)):
            self.offsetX = self.player.pos[0] - self.idealPlayerPos[0]
            self.realPlayerPos = (self.idealPlayerPos[0], self.realPlayerPos[1])
        else:
            self.realPlayerPos = (self.player.pos[0], self.realPlayerPos[1])
            if(self.player.pos[0] > globe.Room.getWidth() - (WINDOWWIDTH /2)):
                self.realPlayerPos = (WINDOWWIDTH - (globe.Room.getWidth() - self.player.pos[0]),self.realPlayerPos[1])
                self.offsetX = globe.Room.getWidth() - (WINDOWWIDTH)
            else:
                self.offsetX = 0
            
        #Handling Y scroll    
        if(globe.Room.getHeight() <= WINDOWHEIGHT):
            self.realPlayerPos = (self.realPlayerPos[0], self.player.pos[1])
        elif(self.player.pos[1] > WINDOWHEIGHT/2 and self.player.pos[1] <= globe.Room.getHeight() - (WINDOWHEIGHT /2)):    
            self.offsetY = self.player.pos[1] - self.idealPlayerPos[1]
            self.realPlayerPos = (self.realPlayerPos[0], self.idealPlayerPos[1])
        else:
            self.realPlayerPos = (self.realPlayerPos[0], self.player.pos[1])
            if(self.player.pos[1] > globe.Room.getHeight() - (WINDOWHEIGHT /2)):
                self.realPlayerPos = (self.realPlayerPos[0], (WINDOWHEIGHT - (globe.Room.getHeight() - self.player.pos[1])))
                self.offsetY = globe.Room.getHeight() - (WINDOWHEIGHT)
            else:
                self.offsetY = 0
        
    def getDrawPos(self, pos):
        return (pos[0] - self.offsetX, pos[1] - self.offsetY)
    
    def getPlayerDrawPos(self):
        return (self.realPlayerPos[0], self.realPlayerPos[1])
    
    def getBackgroundDrawPos(self, pos):
        scrollFactorX = globe.Room.getPref('bgScollFactorX')
        scrollFactorY = globe.Room.getPref('brScrollFactorY')
        if(not(globe.Room.getPref('bgConstantScroll'))):
            if(scrollFactorX == 0):
                newX = self.getDrawPos(pos)[0]
            else:
                newX = pos[0]-(self.offsetX/scrollFactorX)
            if(scrollFactorY == 0):
                newY = self.getDrawPos(pos)[1]
            else:
                newY = pos[1] - (self.offsetY/scrollFactorY)
            return (newX, newY)
        else: 
            ofX = self.player.pos[0]/scrollFactorX
            ofY = self.player.pos[1]/scrollFactorY
            return (pos[0]-ofX, pos[1]-ofY)
    
    def fillScreen(self):
        DISPLAYSURF.fill(BLACK)
        
    def amOnScreen(self, position, tolerance = TILE_SIZE):
        if(position[0] > WINDOWWIDTH + tolerance):
            return False
        if(position[1] > WINDOWHEIGHT + tolerance):
            return False
        return True
    
    def newRoom(self):
        self.realPlayerPos = self.player.pos
        self.offsetX = 0
        self.offsetY = 0