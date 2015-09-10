from src.constants import *
import src.globe as globe
import pygame

class Entity:
    def __init__(self):
        self.width = TILE_SIZE
        self.height = TILE_SIZE
        self.pos = pygame.Rect(0,0,self.width,self.height)
        self.data = {}
        
    def addData(self, data):
        self.data.update(data)
        
    def update(self, elapsed_time):
        pass
    
    def draw(self):
        pass
        
    def register(self):
        globe.Updater.registerUpdatee(self.update)
        globe.Updater.registerDrawee(self.draw)
        
    def unRegister(self):
        globe.Updater.removeUpdatee(self.update)
        globe.Updater.removeDrawee(self.draw)
        
    def spawn(self, location):
        self.pos = pygame.Rect(location[0], location[1], self.width, self.height)
        
    def getNextPos(self):
        return self.pos
    
    def playerCollide(self):
        pass
    
    def tileCollide(self):
        pass
        
        
class PhysicsEntity(Entity):
    def __init__(self):
        super().__init__()
        self.npos = self.pos
        self.vel = (0,0)
    
    def spawn(self, location):
        super().spawn(location)
        self.vel = (0,0)
        self.npos = self.pos
    
    def getNextPos(self):
        return self.npos
    
    def registerCollidee(self):
        globe.Updater.registerRoomCollidee(self)
    
    def registerAll(self):
        self.register()
        self.registerCollidee()
        
    def setTempPosition(self, elapsed):
        self.npos = pygame.Rect(self.pos[0] + self.vel[0]*elapsed, self.pos[1] + self.vel[1]*elapsed, self.width, self.height)
        
    def setPermanentPosition(self):
        self.pos = self.npos
        
    def update(self, elapsed):
        self.setTempPosition()
        
    def getCollidePoints(self):
        self.top = (self.npos.left + (self.width/2), self.npos.top)
        self.bottom = (self.npos.left + (self.width/2), self.npos.bottom)
        self.left = (self.npos.left, self.pos.top + (self.height/2))
        self.right = (self.npos.right, self.pos.top + (self.height/2))