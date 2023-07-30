from model import *

class Scene:
    def __init__(self, app):
        self.app = app
        self.objects = []
        self.load()

    def add_object(self, obj):
        self.objects.append(obj)

    def load(self):
        app = self.app
        add = self.add_object

        coord = [0,2,-2]
        for i in coord:
            for j in coord:
                for k in coord:
                    add(Cube(app, x=k, y=j ,z=i))
        
    def render(self):
        for obj in self.objects:
            obj.render()
