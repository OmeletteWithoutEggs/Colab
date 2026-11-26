import sys

#https://www.geeksforgeeks.org/python/python-import-from-parent-directory/
sys.path.append("./")



lazy import raylibpy as raylib
from raylibpy import Color
from source.vectors import Vector2
from source.player import Player
from source.rendering import Renderer
from source.recording import Recorder
from source.world import Scene,StaticPlatform
from source.collisions import AxisAlignedCollider
import json

class Program:

    def __init__(self):
        self.position = Vector2(0,0)
        self.scene = Scene()
        self.player = Player(Vector2(0,0),(30,50),Color(250, 189, 47,255))
        self.moveSpeed = 500
        self.snapDistance = 10

        self.renderer = Renderer(700,800,"Program")
        self.renderer.loadFont("assets\\fonts\\firjar\\Firjar-Bold.ttf")
        self.camera:raylib.Camera2D = self.renderer.getCamera()
        self.camera.target = self.position.xy
        self.camera.offset = (self.renderer.width/2,self.renderer.height/2)

    def handleInput(self):
        if raylib.is_key_down(raylib.KEY_UP):
            self.position.y -= self.deltaTime * self.moveSpeed
        
        if raylib.is_key_down(raylib.KEY_DOWN):
            self.position.y += self.deltaTime * self.moveSpeed

        if raylib.is_key_down(raylib.KEY_LEFT):
            self.position.x -= self.deltaTime * self.moveSpeed

        if raylib.is_key_down(raylib.KEY_RIGHT):
            self.position.x += self.deltaTime * self.moveSpeed

        if raylib.is_key_down(raylib.KEY_EQUAL):
            self.camera.zoom += self.deltaTime * self.camera.zoom

        if raylib.is_key_down(raylib.KEY_MINUS):
            self.camera.zoom -= self.deltaTime * self.camera.zoom

        if raylib.is_mouse_button_pressed(raylib.MouseButton.MOUSE_BUTTON_LEFT):
            self.startPos = Vector2(self.mouseX,self.mouseY)

        if raylib.is_mouse_button_released(raylib.MouseButton.MOUSE_BUTTON_LEFT):
            self.endPos = Vector2(self.mouseX,self.mouseY)
            if self.endPos.x != self.startPos.x and self.endPos.y != self.startPos.y:
                
                x = min(self.startPos.x,self.endPos.x)
                y = min(self.startPos.y,self.endPos.y)

                width = abs(self.endPos.x - self.startPos.x)
                height = abs(self.endPos.y - self.startPos.y)

                self.scene.addPlatform(StaticPlatform((x,y),(width,height)))

        if raylib.is_key_down(raylib.KEY_BACKSPACE):
            realMousePos = raylib.get_screen_to_world_2d(raylib.get_mouse_position(),self.camera)
            for platform in self.scene.platforms.copy():
                platformCollider :AxisAlignedCollider = platform.collider
                if realMousePos.x > platformCollider.left and realMousePos.y > platformCollider.top:
                    if realMousePos.x < platformCollider.right and realMousePos.y < platformCollider.bottom:
                        self.scene.platforms.remove(platform)
            
    def updatePlayer(self):
        self.player.processInput()
        self.player.updatePhysics(self.deltaTime)
        self.player.collide(self.scene.getColliders(),self.scene.bounds)

    def run(self):
        while not raylib.window_should_close():

            self.mouseX, self.mouseY = raylib.get_screen_to_world_2d(raylib.get_mouse_position(),self.camera)[0:2]
            self.mouseX = ((self.mouseX+(self.snapDistance/2)) // self.snapDistance) * self.snapDistance
            self.mouseY = ((self.mouseY+(self.snapDistance/2)) // self.snapDistance) * self.snapDistance
            self.camera.offset = (self.renderer.width/2,self.renderer.height/2)
            self.camera.target = self.position.xy
            self.handleInput()
            self.deltaTime = raylib.get_frame_time()
            self.updatePlayer()
            self.render()
        del self.renderer

        name = input("Enter file name to save:")
        if not name == "":
            with open("saves/"+name+".json","x") as file:
                json.dump(self.scene.serialise(),file,indent=4)


    def renderDebug(self):
        self.scene.drawDebug(self.renderer)
        

    def render(self):
        with self.renderer:
            self.scene.draw(self.renderer)
            self.player.draw(self.renderer)
            self.player.drawDebug(self.renderer)
            self.renderDebug()
            self.renderer.drawCircle((self.mouseX,self.mouseY),3,Color(249, 188, 47, 255))
            self.renderer.drawCircle((0,0),6,(85, 145, 152, 255))

            gridSize = 40
            topX,topY = raylib.get_screen_to_world_2d(raylib.Vector2(0,0),self.camera)
            bottomX, bottomY = raylib.get_screen_to_world_2d(raylib.Vector2(self.renderer.width,self.renderer.height),self.camera)

            startX = int(topX//gridSize) * gridSize
            startY = int(topY//gridSize) * gridSize

            x = startX
            while x <= bottomX:
                self.renderer.drawLineDashed((x,topY),(x,bottomY),5,5,(240, 128, 28, 255))
                x += gridSize
            y = startY
            while y <= bottomY:
                self.renderer.drawLineDashed((topX,y),(bottomX,y),5,5,(240, 128, 28, 255))
                y += gridSize

        raylib.draw_fps(10,10)

if __name__ == "__main__":
    program = Program()
    program.run()



