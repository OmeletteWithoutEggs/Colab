import pyray as raylib
from pyray import Color
from source.vectors import Vector2

class Renderer:
    def __init__(self,width,height,title,SSAA_SCALE = 2):
        self.SSAA_SCALE = SSAA_SCALE
        self.width = width
        self.height = height
        self.title = title

        raylib.set_config_flags(raylib.FLAG_WINDOW_RESIZABLE|raylib.FLAG_WINDOW_HIGHDPI|raylib.FLAG_MSAA_4X_HINT)
        raylib.init_window(self.width,self.height,b"Program")
        raylib.set_target_fps(200)

        self.camera = raylib.Camera2D((self.width/2,self.height/2),raylib.Vector2(0,0),0,1)

        #self._loadTargetWindow()

    def getCamera(self):
        return self.camera

    def _loadTargetWindow(self):
        self.targetWindow = raylib.load_render_texture(self.width*self.SSAA_SCALE,self.height*self.SSAA_SCALE)
        raylib.set_texture_filter(self.targetWindow.texture, raylib.TEXTURE_FILTER_BILINEAR)

        self.sourceRect = raylib.Rectangle(0,0,self.targetWindow.texture.width,-self.targetWindow.texture.height)
        self.destRect = raylib.Rectangle(0,0,self.width,self.height)

    def _handleResize(self):
        if raylib.is_window_resized():
            self.width = raylib.get_screen_width()
            self.height = raylib.get_screen_height()

            self.camera.offset = raylib.Vector2(self.width/2,self.height/2)

            #raylib.unload_render_texture(self.targetWindow)
            self._loadTargetWindow()

    def beginDrawing(self):
        self._handleResize()
        raylib.begin_drawing()
        #raylib.begin_texture_mode(self.targetWindow)
        raylib.clear_background(Color(32, 32, 32, 255))
        raylib.begin_mode_2d(self.camera)

    def endDrawing(self):
        raylib.end_mode_2d()
        #raylib.end_texture_mode()

        #raylib.begin_drawing()
        #raylib.clear_background(Color(0,0,0,255))
        #raylib.draw_texture_pro(self.targetWindow.texture, self.sourceRect, self.destRect, raylib.Vector2(0,0), 0, Color(255,255,255,255))
        raylib.end_drawing()

    def __enter__(self):
        self.beginDrawing()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.endDrawing()
        return False 

    def __del__(self):
        print("closing window")
        #raylib.unload_render_texture(self.targetWindow)
        raylib.close_window()

    def drawRectanglePro(self,position,size,origin,rotation,colour):
        if not isinstance(colour,Color):
            colour = Color(*colour)
        rectangle = raylib.Rectangle(position[0],position[1],size[0],size[1])
        origin = raylib.Vector2(origin[0],origin[1])
        raylib.draw_rectangle_pro(rectangle,origin,rotation,colour)

    def drawRectangle(self,position,size,colour):
        if not isinstance(colour,Color):
            colour = Color(*colour)
        raylib.draw_rectangle(position[0],position[1],size[0],size[1],colour)

    def drawLineDashed(self,startPos,endPos,dashLength, dashSpacing,colour):
        if not isinstance(colour,Color):
            colour = Color(*colour)
        p1 = raylib.Vector2(startPos[0],startPos[1])
        p2 = raylib.Vector2(endPos[0],endPos[1])
        raylib.draw_line_dashed(p1,p2,dashLength,dashSpacing,colour)

    def drawLineStrip(self,points,thickness,colour,position = Vector2(0,0)):
        if not isinstance(colour,Color):
            colour = Color(*colour)
        for i in range(1,len(points)):
            p1 = raylib.Vector2(points[i-1][0]+position.x,points[i-1][1]+position.y)
            p2 = raylib.Vector2(points[i][0]+position.x,points[i][1]+position.y)
            raylib.draw_line_ex(p1,p2,thickness,colour)


    def drawCircle(self,position,radius,colour):
        if not isinstance(colour,Color):
            colour = Color(*colour)
        position = raylib.Vector2(position[0],position[1])
        raylib.draw_circle_v(position,radius,colour)

    def drawRectangleLines(self,position,size,thickness,colour):
        if not isinstance(colour,Color):
            colour = Color(*colour)
        rect = raylib.Rectangle(position[0],position[1],size[0],size[1])
        raylib.draw_rectangle_lines_ex(rect,thickness,colour)


    def drawText(self,text,position,size,colour,alignement = "center",spacing = 2):
        """alignement : 'left' | 'center' | 'right' """

        text = str(text)

        if not self.font:
            raise Exception("font not loaded")
        if not isinstance(colour,Color):
            colour = Color(*colour)

        textWidth = raylib.measure_text_ex(self.font,text,size,spacing)[0]

        match alignement:
            case "center":
                origin = raylib.Vector2(textWidth/2,0)
            case "left":
                origin = raylib.Vector2(0,0)
            case "left":
                origin = raylib.Vector2(textWidth,0)
            case _:
                origin = raylib.Vector2(0,0)

            
        position = raylib.Vector2(position[0],position[1])

        raylib.draw_text_pro(self.font,text,position,origin,0,size,spacing,colour)

    def loadFont(self,file):
        self.font = raylib.load_font(file)
    