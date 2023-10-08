from asyncio import Condition
import tkinter as tk
import time
import os
import math
from tkinter.font import BOLD
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
        self.layer_entry.insert(0, "0")
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
        self.canvas.bind("<ButtonRelease-1>", self.click_up)
        self.canvas.bind("<ButtonRelease-3>", self.click_up)
        self.canvas.bind("<Motion>", self.mouse_motion)
        
        self.xpos = -100
        self.ypos = -100
        self.camera_speed = 3
        
        self.mouse_x = 0
        self.mouse_y = 0
        
        self.items_not_to_remove = []
        
        self.current_keys = []
        
        self._map = []
        with open(PATH+"map.txt", "r") as file:
            for line in file:
                args = line.split()
                self._map.append(MapObject(*args))
                
    def key_down(self, event):
        if event.char not in self.current_keys:
            self.current_keys.append(event.char)
        if event.keycode == 16 and 'L-Shift' not in self.current_keys: #l-shift
            self.current_keys.append('L-Shift')
        if event.char in ["1", "2", "3"]:
            mapmodes = ["standard", "layer", "solid"]
            settings.mapmode_var.set(mapmodes[int(event.char)-1])
            
        print(self.current_keys)
    
    def key_up(self, event):
        if event.keysym in self.current_keys:
            self.current_keys.remove(event.char)
        if event.keycode == 16 and 'L-Shift' in self.current_keys:
            self.current_keys.remove('L-Shift')
            
    def click(self, event):
        if event.num == 1 and 'LMB' not in self.current_keys:
            self.current_keys.append('LMB')
        elif event.num == 3 and 'RMB' not in self.current_keys:
            self.current_keys.append('RMB')
            
    def click_up(self, event):
        if event.num == 1 and 'LMB' in self.current_keys:
            self.current_keys.remove('LMB')
        elif event.num == 3 and 'RMB' in self.current_keys:
            self.current_keys.remove('RMB')
        self.items_not_to_remove.clear()
        
    def mouse_motion(self, event):
        self.mouse_x = event.x
        self.mouse_y = event.y
        
    def get_item_id_by_pos(self, x, y):
        output = []
        for i, item in enumerate(self._map):
            if item.xpos == x and item.ypos == y:
                output.append(i)
        return output
        
    def update(self):
        if "w" in self.current_keys and "s" not in self.current_keys:
            self.ypos -= self.camera_speed
        elif "s" in self.current_keys and "w" not in self.current_keys:
            self.ypos += self.camera_speed
        if "a" in self.current_keys and "d" not in self.current_keys:
            self.xpos -= self.camera_speed
        elif "d" in self.current_keys and "a" not in self.current_keys:
            self.xpos += self.camera_speed
            

        x, y = self.mouse_x + self.xpos, self.mouse_y + self.ypos
        if settings.snap_to_grid_var.get():
            x -= x % 32
            y -= y % 32
    
        items = self.get_item_id_by_pos(x, y)
        if 'LMB' in self.current_keys:
            if settings.mapmode_var.get() == "standard" and len(items) < 2 and not any([self._map[item].sprite == tile_selection.selected_sprite for item in items]):
                if len(items) == 0:
                    self._map.append(MapObject("VisualObject", tile_selection.selected_sprite, x, y, 32, 32, settings.layer_entry.get(), settings.is_solid_var.get()))
                elif 'L-Shift' in self.current_keys:
                    self._map.append(MapObject("VisualObject", tile_selection.selected_sprite, x, y, 32, 32, self._map[items[0]].layer-1, settings.is_solid_var.get()))
                else:
                    self._map.append(MapObject("VisualObject", tile_selection.selected_sprite, x, y, 32, 32, self._map[items[0]].layer+1, settings.is_solid_var.get()))
            
            elif settings.mapmode_var.get() == "layer" and any([item.xpos == x and item.ypos == y for item in self._map]):
                items = self.get_item_id_by_pos(x, y)
                self._map[items[len(items)-1]].layer = settings.layer_entry.get()
            
            elif settings.mapmode_var.get() == "solid" and any([item.xpos == x and item.ypos == y for item in self._map]) and (x, y) not in self.items_not_to_remove:
                items = self.get_item_id_by_pos(x, y)
                self._map[items[len(items)-1]].is_solid = not self._map[items[len(items)-1]].is_solid
                self.items_not_to_remove.append((x, y))

        elif 'RMB' in self.current_keys and any([item.xpos == x and item.ypos == y for item in self._map]) and (x, y) not in self.items_not_to_remove and settings.mapmode_var.get() == 'standard':
            if len(items) == 2:
                sum_of_conditions = int(self._map[items[0]].layer < self._map[items[1]].layer) + int('L-Shift' in self.current_keys)
                self._map.pop(items[sum_of_conditions % 2])
            else:
                self._map.pop(items[0])
            if len(self.get_item_id_by_pos(x, y)) > 0:
                self.items_not_to_remove.append((x, y))

            
    def render(self):
        self.canvas.delete("all")
       
        sorted_map = []
        for item in self._map:
            added = False
            for i in range(len(sorted_map)-1):
                if (item.layer <= sorted_map[i].layer):
                    sorted_map.insert(i, item)
                    added = True
                    break
            if not added:
                sorted_map.insert(0, item)

        for item in sorted_map:
            print(item.layer)
            self.canvas.create_image(item.xpos-self.xpos, item.ypos-self.ypos, anchor=tk.NW, image=tile_selection.sprites[item.sprite])
            if settings.mapmode_var.get() == "layer":
                self.canvas.create_text(item.xpos-self.xpos+item.width/2, item.ypos-self.ypos+item.height/2, text=item.layer, font=('arial', 15, 'bold'))
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
        self.canvas = tk.Canvas(root, width=1400, height=300)
        self.canvas.grid(row=0, column=0, columnspan=3)
        self.canvas.bind("<Button-1>", self.click)
        
        self.sprites = {}
        os.chdir(PATH+"graphics\\tiles\\")
        items = os.listdir()
        for item in items:
            self.sprites["tiles/"+item[:-4]] = tk.PhotoImage(file=PATH+"graphics\\tiles\\"+item)
            
        self.selection_images = []
        for i, sprite in enumerate(self.sprites.values()):
            x = 40*i - 35 * 40 * math.floor(i/35)+5
            y = 40*math.floor(i/35)+5
            self.selection_images.append(self.canvas.create_image(x, y, anchor=tk.NW, image=self.sprites[list(self.sprites.keys())[i]]))
            
        self.selected_sprite = list(self.sprites.keys())[0]    
        self.selection_rect = self.canvas.create_rectangle(3, 3, 39, 39, width=2)
        
    def click(self, event):
        item = math.floor(event.x / 40) + 35 * math.floor(event.y / 40)
        if item < len(self.selection_images):
            self.selected_sprite = list(self.sprites.keys())[item]
            x = 40*item - 35 * 40 * math.floor(item/35)+3
            y = 40*math.floor(item/35)+3
            self.canvas.coords(self.selection_rect, x, y, x+36, y+36)
        

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