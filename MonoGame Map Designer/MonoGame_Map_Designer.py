from re import S
import tkinter as tk
import time

root = tk.Tk()
root.title("Map Designer")

def save_file(event):
    print("bung")


menubar = tk.Menu(root)

filemenu = tk.Menu(menubar, tearoff=0)
filemenu.add_command(label="Save", command=lambda:save_file(0))
menubar.add_cascade(label="File", menu=filemenu)
root.config(menu=menubar)

class Map:
    def __init__(self, root):
        self.canvas = tk.Canvas(root, width=1400, height=800)
        self.canvas.pack()
        
        self.xpos = 0
        self.ypos = 0
        self.camera_speed = 5
        
        self.current_keys = []
        
        self._map = []
        
        with open("C:\\users\\04alsa25\\source\\repos\\MonoGameTest\\MonoGameTest\\Content\\map.txt", "r") as file:
            for line in file:
                args = line.split()
                self._map.append(MapObject(*args))
                
        for x in self._map:
            print(x)
        
    def key_down(self, event):
        self.current_keys.append(event.button)
    
    def key_up(self, event):
        self.current_keys.remove(event.button)
        
    def update(self):
        if "w" in self.current_keys and "s" not in self.current_keys:
            self.ypos -= self.camera_speed
        elif "s" in self.current_keys and "w" not in self.current_keys:
            self.ypos += self.camera_speed
        if "a" in self.current_keys and "d" not in self.current_keys:
            self.xpos -= self.camera_speed
        elif "d" in self.current_keys and "a" not in self.current_keys:
            self.xpos += self.camera_speed
            
class MapObject:
    def __init__(self, _type, sprite, xpos, ypos, width, height, layer, is_solid):
        self._type = _type
        self.sprite = sprite
        self.xpos = xpos
        self.ypos = ypos
        self.width = width
        self.height = height
        self.layer = layer
        self.is_solid = is_solid
        
    def get_output_string(self):
        return f"{self._type} {self.sprite} {self.xpos} {self.ypos} {self.width} {self.height} {self.layer} {self.is_solid}"
        

class TileSelection:
    def __init__(self, root):
        self.canvas = tk.Canvas(root, width=1400, height=100)
        self.canvas.pack()
        

tile_selection = TileSelection(root)
_map = Map(root)
root.bind("<KeyPress>", _map.key_down)
root.bind("<KeyRelease>", _map.key_up)

root.bind("<Control-s>", save_file)


root.mainloop()