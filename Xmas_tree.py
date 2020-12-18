import board
import neopixel
import random
import time
import cv2

num_pixels = 150
limit=3

ORDER = neopixel.RGB
pixels = neopixel.NeoPixel(board.D18,num_pixels,brightness = .50, auto_write=False, pixel_order=ORDER)

def random_color():
    return (random.randint(0,255),random.randint(0,255),random.randint(0,255))

def color_list(pixels,colors=[]):
    colors_len = len(colors)
    pixels_len = len(pixels)
    colors_loops = (pixels_len // colors_len) +1
    color_list = (colors * colors_loops)[0:pixels_len]
    return color_list

# create color lists
RGRG = color_list(pixels,[(255,0,0),(0,255,0)])
RWRW = color_list(pixels,[(255,0,0),(255,255,255)])
WWWW = color_list(pixels,[(255,255,255)])
RAND = color_list(pixels,[random_color() for pixel in pixels])
BWBW = color_list(pixels,[(0,0,255),(255,255,255)])  
RGWRGW = color_list(pixels,[(255,0,0),(0,255,0),(255,255,255)])
ROWS = [[0,7],[8,47],[48,78],[79,101],[102,127],[128,140],[141,146],[147,149]]
LONGEST_ROW_LEN = (47-8+1)

column_matrix = []
for i in range(LONGEST_ROW_LEN):
    column_list = []
    for j, row in enumerate(ROWS):
        if j == 0: continue
        row_list = list(range(row[0],row[1]+1) )
        relative_index = int(i/LONGEST_ROW_LEN*len(row_list))
        column_list.append(row_list[relative_index])
    column_matrix.append(column_list)
print(column_matrix)

def columns_rotate(pixels,color_list,delay,n_times=1,clear=True):
    n=0
    while n<n_times:
        for i, col in enumerate(column_matrix):
            for row_col in col:
                pixels[row_col] = color_list[i]
            pixels.show()
            time.sleep(delay)
        if clear==True:
            pixels.fill((0,0,0))
            pixels.show()
        n+=1

    
def row_up(pixels,color_list,row_delay,n_times=1,reverse_run = False,clear=True):
    n=0
    while n<n_times:
        print("n: ",n)
        for i, row in enumerate(ROWS):
            pixels_to_update = range(row[0],row[1]+1,1)
            for j, pix_id in enumerate(pixels_to_update):
                pixels[pix_id] = color_list[i]
            pixels.show()
            time.sleep(row_delay)
        if clear==True:
            pixels.fill((0,0,0))
            pixels.show()
        n+=1

def run_up(pixels_list,color_list,run_delay,n_times=1,reverse_run=False,clear=True):
    n=0
    while n<n_times:    
        for i in range(len(pixels_list)):
            if reverse_run==True:
                pixels_list[len(pixels_list)-i-1] = color_list[i]
            else:
                pixels_list[i] = color_list[i]
            pixels_list.show()
            time.sleep(run_delay)
        if clear==True:
            pixels.fill((0,0,0))
            pixels.show()
        n+=1
        
def fill_and_change(pixels,fill_color,change_color,delay,n_times=1,use_xmas_colors=False):
    xmas_colors = [(255,0,0),(0,255,0),(255,255,255)]
    n=0
    while n<n_times:
        if use_xmas_colors==True:
            random.shuffle(xmas_colors)
            fill_color = xmas_colors[0]
            change_color = xmas_colors[1]
        pixels.fill(fill_color)
        pixels.show()
        pixels_index = [i for i, pixel in enumerate(pixels)]
        random.shuffle(pixels_index)
        for i in pixels_index:
            pixels[i] = change_color
            time.sleep(delay)
            pixels.show()
        n+=1
        
    pixels.fill((0,0,0))
    pixels.show()

delay = .1
n_times = 1

try:
    while True:
        hour = time.localtime().tm_hour
        if  (hour>=11 and hour <22) or (hour>5 and hour <8):
            pass
        else:
            time.sleep(60)
            continue
        columns_rotate(pixels,WWWW,delay,n_times=3)
        columns_rotate(pixels,RGRG,delay,n_times=3)
        columns_rotate(pixels,RWRW,delay,n_times=3)
        columns_rotate(pixels,BWBW,delay,n_times=3)
        columns_rotate(pixels,RAND,delay,n_times=3)
        columns_rotate(pixels,RGWRGW,delay,n_times=3)
        row_up(pixels,RGRG,delay*5,n_times=3)
        row_up(pixels,RWRW,delay*5,n_times=3)
        row_up(pixels,BWBW,delay*5,n_times=3)
        row_up(pixels,RAND,delay*5,n_times=3)
        row_up(pixels,RGWRGW,delay*5,n_times=3)
        fill_and_change(pixels,(0,0,0),(255,255,255),delay,5,use_xmas_colors=True)
        run_up(pixels,WWWW,delay,n_times)
        run_up(pixels,WWWW,delay,n_times,reverse_run=True)
        run_up(pixels,RWRW,delay,n_times)
        run_up(pixels,RWRW,delay,n_times,reverse_run=True)
        run_up(pixels,BWBW,delay,n_times)
        run_up(pixels,BWBW,delay,n_times,reverse_run=True)
        run_up(pixels,RGRG,delay,n_times)
        run_up(pixels,RGRG,delay,n_times,reverse_run=True)
        run_up(pixels,RAND,delay,n_times)
        run_up(pixels,RAND,delay,n_times,reverse_run=True)
        run_up(pixels,RGWRGW,delay,n_times)
        run_up(pixels,RGWRGW,delay,n_times,reverse_run=True)
        
except KeyboardInterrupt:
    pass
    
pixels.deinit()
        


