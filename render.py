import pygame as pg
import moderngl as mgl
import sys
from model import *
from camera import Camera
import scene

class GraphicsEngine:
    def __init__(self, win_size=(1600,900)):
        #init pygame modules
        pg.init()
        #window size
        self.WIN_SIZE = win_size
        #set opengl attr
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE)
        #create opengle context 
        pg.display.set_mode(self.WIN_SIZE, flags=pg.OPENGL | pg.DOUBLEBUF)
        #mouse settings
        pg.event.set_grab(True)
        pg.mouse.set_visible(False)
        #detect and use existing opengl context
        self.ctx = mgl.create_context()
        self.ctx.enable(flags=mgl.DEPTH_TEST | mgl.CULL_FACE)
        #create an object to help track time 
        self.clock = pg.time.Clock()
        self.delta_time = 0
        #camera
        self.camera = Camera(self)
        #scene
        self.scene = scene.Scene(self)
        self.prime = 1
    
    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                self.scene.destory()
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN and event.key == pg.K_p:
                self.prime = -1 
            if event.type == pg.KEYDOWN and event.key == pg.K_2: #DOWN
                self.move("D")
            if event.type == pg.KEYDOWN and event.key == pg.K_8: #UP
                self.move("U")
            if event.type == pg.KEYDOWN and event.key == pg.K_6: #RIGHT
                self.move("R")
            if event.type == pg.KEYDOWN and event.key == pg.K_4: #LEFT
                self.move("L")
            if event.type == pg.KEYDOWN and event.key == pg.K_7: #FRONT
                self.move("F")
            if event.type == pg.KEYDOWN and event.key == pg.K_9: #BACK
                self.move("B")
    
    def move(self,move): 
        if len(move) == 2:
            self.prime = -1
            move = move[0]
        move_dict = {"D":((0,1,0), [17,15,26,8,25,24,16,7,6]), "U":((0,-1,0), [4,13,21,22,5,23,12,14,3]), "R": ((0,0,-1), [17,12,16,11,13,15,14,10,9]),
                      "L":((0,0,1), [19,23,24,22,20,25,21,26,18]), "F":((1,0,0), [8,17,11,14,5,23,20,26,2]) , "B":((-1,0,0), [25,19,22,4,13,10,16,7,1]) }
        get_move = move_dict[move]
        axis = get_move[0]
        axis = tuple([self.prime * i for i in axis])
        self.rotate(axis, get_move[1])


    def render(self):
        #clear framebuffer
        self.ctx.clear(color=(0.08, 0.16, 0.18))
        #render scene
        self.scene.render()
        #swap buffers
        pg.display.flip()

    def rotate(self, axis, rotation_list):
        not_currently_rotating = True
        for i in rotation_list:
                obj = self.scene.objects[i]
                if obj.rotate:
                    not_currently_rotating = False
                    break

        if not_currently_rotating:
            temp = rotation_list[:-1]
            rotation_list = temp[::self.prime] + [rotation_list[-1]]
            for i in rotation_list:
                obj = self.scene.objects[i]
                obj.rotate = True
                obj.initial_rotate_time = 0
                obj.rotate_axis = axis
                 
            temp_corner = self.scene.objects[rotation_list[0]]
            temp_edge = self.scene.objects[rotation_list[1]]

            for i in range(3):
                self.scene.objects[rotation_list[i*2]] = self.scene.objects[rotation_list[i*2 + 2]]
                self.scene.objects[rotation_list[i*2 + 1]] = self.scene.objects[rotation_list[i*2 + 3]]
                
            self.scene.objects[rotation_list[-3]] = temp_corner
            self.scene.objects[rotation_list[-2]] = temp_edge 
            self.prime = 1       

    def run(self):
        # self.move("U'")
        while True:
            self.check_events()
            self.camera.update()
            self.render()
            self.delta_time = self.clock.tick(60)
            


if __name__ == '__main__':
    app = GraphicsEngine()
    app.run()
