import tkinter as tk
import time
import os
import math
from unittest.mock import seal

root = tk.Tk()
root.title("Map Designer")

def save_file(event):
    with open(PATH+"map.txt", "w") as file:
        file.writelines([item.get_output_string() for item in _map._map])


#PATH = "C:\\Users\\alfre\\Source\\repos\\alfredsandare\\MonoGameTest\\MonoGameTest\\Content\\"
PATH = "C:\\users\\04alsa25\\source\\repos\\MonoGameTest\\MonoGameTest\\Content\\"

menubar = tk.Menu(root)

filemenu = tk.Menu(menubar, tearoff=0)
filemenu.add_command(label="Save", command=lambda:save_file(0))
menubar.add_cascade(label="File", menu=filemenu)
root.config(menu=menubar)

class Settings:
    def __init__(self, root):
        self.snap_to_grid_var = tk.BooleanVar(value=True)
        self.snap_to_grid_checkbutton = tk.Checkbutton(root, var=self.snap_to_grid_var, text="Snap to grid")
        self.snap_to_grid_checkbutton.grid(row=1, column=0, columnspan=2, sticky=tk.NW)
        
        self.layer_label = tk.Label(root, text="Layer:")
        self.layer_label.grid(row=2, column=0)
        self.layer_entry = tk.Entry(root)
        self.layer_entry.insert(0, "1")
        self.layer_entry.grid(row=2, column=1)
        
        self.is_solid_var = tk.BooleanVar(value=True)
        self.is_solid_checkbutton = tk.Checkbutton(root, var=self.is_solid_var, text="Solid")
        self.is_solid_checkbutton.grid(row=3, column=0)
        
        self.mapmode_var = tk.StringVar(value="standard")
        self.mapmode_label = tk.Label(text="Mapmode:")
        self.mapmode_label.grid(row=4, column=0, sticky=tk.W, columnspan=2)
        
        self.mapmode_standard_radiobutton = tk.Radiobutton(root, var=self.mapmode_var, text="Standard", value="standard")
        self.mapmode_standard_radiobutton.grid(row=5, column=0, sticky=tk.W, columnspan=2)
        
        self.mapmode_layer_radiobutton = tk.Radiobutton(root, var=self.mapmode_var, text="Layer", value="layer")
        self.mapmode_layer_radiobutton.grid(row=6, column=0, sticky=tk.W, columnspan=2)
        
        self.mapmode_layer_radiobutton = tk.Radiobutton(root, var=self.mapmode_var, text="Solid", value="solid")
        self.mapmode_layer_radiobutton.grid(row=7, column=0, sticky=tk.W, columnspan=2)
        
        self.empty = tk.Label(text="")
        self.empty.grid(row=8, column=0, pady=260)
        

class Map:
    def __init__(self, root):
        self.canvas = tk.Canvas(root, width=1400, height=800)
        self.canvas.grid(row=1, column=2, padx=4, rowspan=10)
        self.canvas.bind("<Button-1>", self.click)
        self.canvas.bind("<Button-3>", self.click)
        
        #self.canvas.bind("<Key>", self.change_mapmode)
        
        self.xpos = -100
        self.ypos = -100
        self.camera_speed = 3
        
        self.current_keys = []
        
        self._map = []
        
        with open(PATH+"map.txt", "r") as file:
            for line in file:
                args = line.split()
                self._map.append(MapObject(*args))
                
    def key_down(self, event):
        if event.char not in self.current_keys:
            self.current_keys.append(event.char)
        if event.char in ["1", "2", "3"]:
            mapmodes = ["standard", "layer", "solid"]
            settings.mapmode_var.set(mapmodes[int(event.char)-1])
    
    def key_up(self, event):
        if event.char in self.current_keys:
            self.current_keys.remove(event.char)
            
    def click(self, event):
        x, y = event.x + self.xpos, event.y + self.ypos
        if settings.snap_to_grid_var.get():
            x -= x % 32
            y -= y % 32
        
        if event.num == 1:
            if settings.mapmode_var.get() == "standard" and not any([item.xpos == x and item.ypos == y for item in self._map]):
                self._map.append(MapObject("VisualObject", tile_selection.selected_sprite, x, y, 32, 32, settings.layer_entry.get(), settings.is_solid_var.get()))
            elif settings.mapmode_var.get() == "layer" and any([item.xpos == x and item.ypos == y for item in self._map]):
                self._map[self.get_item_id_by_pos(x, y)].layer = settings.layer_entry.get()
            elif settings.mapmode_var.get() == "solid" and any([item.xpos == x and item.ypos == y for item in self._map]):
                self._map[self.get_item_id_by_pos(x, y)].is_solid = not self._map[self.get_item_id_by_pos(x, y)].is_solid
                
        elif event.num == 3 and any([item.xpos == x and item.ypos == y for item in self._map]):
            self._map.pop(self.get_item_id_by_pos(x, y))
            
    def get_item_id_by_pos(self, x, y):
        for i, item in enumerate(self._map):
            if item.xpos == x and item.ypos == y:
                break
        return i
        
    def update(self):
        if "w" in self.current_keys and "s" not in self.current_keys:
            self.ypos -= self.camera_speed
        elif "s" in self.current_keys and "w" not in self.current_keys:
            self.ypos += self.camera_speed
        if "a" in self.current_keys and "d" not in self.current_keys:
            self.xpos -= self.camera_speed
        elif "d" in self.current_keys and "a" not in self.current_keys:
            self.xpos += self.camera_speed
            
    def render(self):
        self.canvas.delete("all")
        for item in self._map:
            self.canvas.create_image(item.xpos-self.xpos, item.ypos-self.ypos, anchor=tk.NW, image=tile_selection.sprites[item.sprite])
            if settings.mapmode_var.get() == "layer":
                self.canvas.create_text(item.xpos-self.xpos+item.width/2, item.ypos-self.ypos+item.height/2, text=item.layer)
            elif settings.mapmode_var.get() == "solid" and item.is_solid:
                self.canvas.create_rectangle(item.xpos-self.xpos+4, item.ypos-self.ypos+4, item.xpos-self.xpos+24, item.ypos-self.ypos+24, fill="black")
               
       
                
class MapObject:
    def __init__(self, _type, sprite, xpos, ypos, width, height, layer, is_solid):
        self._type = _type
        self.sprite = sprite
        self.xpos = int(xpos)
        self.ypos = int(ypos)
        self.width = int(width)
        self.height = int(height)
        self.layer = int(layer)
        self.is_solid = bool(int(is_solid))
        
    def get_output_string(self):
        return f"{self._type} {self.sprite} {self.xpos} {self.ypos} {self.width} {self.height} {self.layer} {int(self.is_solid)}\n"
        

class TileSelection:
    def __init__(self, root):
        self.canvas = tk.Canvas(root, width=1400, height=100)
        self.canvas.grid(row=0, column=0, columnspan=3)
        self.canvas.bind("<Button-1>", self.click)
        
        self.sprites = {}
        os.chdir(PATH+"tiles\\")
        items = os.listdir()
        for item in items:
            self.sprites["tiles/"+item[:-4]] = tk.PhotoImage(file=PATH+"tiles\\"+item)
            
        self.selection_images = []
        for i, sprite in enumerate(self.sprites.values()):
            self.selection_images.append(self.canvas.create_image(40*i+5, 5, anchor=tk.NW, image=self.sprites[list(self.sprites.keys())[i]]))
            
        self.selected_sprite = list(self.sprites.keys())[0]    
        self.selection_rect = self.canvas.create_rectangle(3, 3, 39, 39, width=2)
        
    def click(self, event):
        item = math.floor(event.x / 40)
        if item < len(self.selection_images):
            self.selected_sprite = list(self.sprites.keys())[item]
            self.canvas.coords(self.selection_rect, 40*item+3, 3, 40*item+39, 39)
        
        

tile_selection = TileSelection(root)
_map = Map(root)
settings = Settings(root)
root.bind_all("<KeyPress>", _map.key_down)
root.bind_all("<KeyRelease>", _map.key_up)

root.bind("<Control-s>", save_file)


while 1:
    _map.update()
    _map.render()
    root.update()
    time.sleep(0.0166667)