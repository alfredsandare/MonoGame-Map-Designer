from PIL import Image, ImageTk
import math

PATH = "C:\\Users\\alfre\\Source\\repos\\alfredsandare\\MonoGameTest\\MonoGameTest\\Content\\"

def get_part_of_image(img, x1, y1, x2, y2):
    output = []
    img_data = list(img.getdata())
    for y in range(img.height):
        for x in range(img.width):
            if x1 <= x < x2 and y1 <= y < y2:
                output.append(img_data[y*img.width+x])
                
    output_img = Image.new("RGBA", (x2-x1, y2-y1))
    output_img.putdata(output)
    return output_img

def divide_image(img, x_size, y_size):
    output_imgs = []
    amount_of_tiles_horizontally = int(img.width / x_size)
    amount_of_tiles_vertically = int(img.height / y_size)
    
    for y in range(amount_of_tiles_vertically):
        for x in range(amount_of_tiles_horizontally):
            output_imgs.append(get_part_of_image(img, x * x_size, y * y_size, (x+1) * x_size, (y+1) * y_size))
        print(str(100*y/amount_of_tiles_vertically)+"%")
            
    return output_imgs
            

tiles_img = Image.open(PATH+"working\\tiles.png")

sub_img = get_part_of_image(tiles_img, 640, 0, 896, 960) #all the grass, ground, water, trees
tiles = divide_image(sub_img, 32, 32)

for i, tile in enumerate(tiles):
    tile.save(PATH+"test\\"+str(i)+".png")

#sub_img.save(PATH+"temp.png")