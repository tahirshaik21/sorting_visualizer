
import pygame
import random
import math
pygame.init()
#class that describes measurements and colors to draw  bar graph dynamically
class draw:

    # describing colours
    black=0,0,0
    green=0,255,0
    red=255,0,0
    blue=0,0,255
    white=255,255,255
    orange=255, 165, 0
    back_ground=orange
    grad=[(118,118,118),(130,130,130),(255,255,255)]

    #padding for top and sides
    side_pad=100
    top_pad=100

    #font type and size for headings
    small_font=pygame.font.SysFont('ariel',25)
    Large_font=pygame.font.SysFont('ariel',50)

    #stores and dispalys window (width,height)
    def __init__(self,width,height,lst):
        self.width=width
        self.height=height
        self.window=pygame.display.set_mode((self.width,self.height))#two braces are used here
        pygame.display.set_caption("Sorting")
        self.set_list(lst)

    # defines the dynamic block width and height  
    def set_list(self,lst):
        self.lst=lst
        self.min_val=min(lst)
        self.max_val=max(lst)
        self.block_width=round((self.width-self.side_pad)/(len(lst)))
        self.block_height=math.floor((self.height-self.top_pad)/(self.max_val-self.min_val))
        self.start_=self.side_pad//2

#method to  represent or draw bars
#color position represents for moving colors
#clear_bg to static display of headings
def draw_list(draw_info,color_position={},clear_bg=False):
    lst=draw_info.lst

    if clear_bg:
        clear_rect= (draw_info.side_pad//2,draw_info.top_pad,draw_info.width-draw_info.side_pad,draw_info.height-draw_info.side_pad)
        pygame.draw.rect(draw_info.window,draw_info.back_ground,clear_rect)
    for i,val in enumerate(lst):
        x=draw_info.start_ + i*draw_info.block_width
        y=draw_info.height -(val - draw_info.min_val)*draw_info.block_height
        color=draw_info.grad[i%3]
        if i in color_position:
            color=color_position[i]
        pygame.draw.rect(draw_info.window,color,(x,y,draw_info.block_width,draw_info.height))

    if clear_bg:
        pygame.display.update()
        
# renders algorithm name and specific order
def draw_ac(draw_info,algo_name,ascending=True):
    draw_info.window.fill(draw_info.back_ground)

    #blit is used to add or place a window over another
    title=draw_info.small_font.render(f"{algo_name} - {'Ascending' if ascending else 'Descending'}",1,draw_info.black)
    draw_info.window.blit(title,(draw_info.width/2 - title.get_width()/2 ,5))

    heading=draw_info.small_font.render(" B - Bubble sort | Insertion Sort | S -Selection Sort |R - Randomize ",1,draw_info.black)
    draw_info.window.blit(heading,(draw_info.width/2 - heading.get_width()/2 ,25))

    sorting =draw_info.small_font.render(" A - Ascending | D - Descending ",1,draw_info.black)
    draw_info.window.blit(sorting,(draw_info.width/2 - sorting.get_width()/2 ,45))
    
    #calls draw_list method to draw bar graphs
    draw_list(draw_info)
    pygame.display.update()

#bubble sort
def bubble_sort(draw_info,ascending=True):
    lst=draw_info.lst
    for i in range(len(lst)-1):
        for j in range(len(lst)-1-i):
            if (lst[j]>lst[j+1] and ascending ) or (lst[j]<lst[j+1] and not ascending):
                lst[j],lst[j+1]=lst[j+1],lst[j]
                draw_list(draw_info,{j:draw_info.red,j+1:draw_info.blue},True)
                yield True
    return lst

#insertion sort
def insertion_sort(draw_info,ascending=True):
    lst=draw_info.lst
    for i in range(1,len(lst)):
        key=lst[i]
        while True:
            sort_a= i>0 and lst[i-1]> key and ascending
            sort_d= i>0 and lst[i-1] < key and not ascending

            if not sort_a and not sort_d:
                break
            lst[i]=lst[i-1]
            i-=1
            lst[i]=key
            draw_list(draw_info,{i:draw_info.red,i-1:draw_info.blue},True)
            yield True   
    return lst

#selection sort
def selection_sort(draw_info, ascending=True):
    lst=draw_info.lst
    for i in range(len(lst)):
        min_idx = i
        for j in range(i+1, len(lst)):
            #draw_list(draw_info,{i:draw_info.black,min_idx:draw_info.red,j:draw_info.blue})
            if (lst[j] < lst[min_idx] and ascending) or (lst[j] > lst[min_idx] and not ascending):
                #min_idx=j
                for a in range(min_idx,j+1):
                    draw_list(draw_info, {min_idx:draw_info.red, a: draw_info.blue}, True)
                    yield True
                min_idx = j
                draw_list(draw_info, {j:draw_info.red, min_idx: draw_info.blue}, True)
                yield True
        lst[i], lst[min_idx] = lst[min_idx], lst[i]
        draw_list(draw_info, {i:draw_info.blue, min_idx: draw_info.red}, True)
        
    return lst


#method to generate random number list
def generate_list(n,min_val,max_val):
    lst=[]
    for _ in range(n):
        lst.append(random.randint(min_val,max_val))
    return lst

#main method
def main():
    #var to keep the game running till a halt key is pressed
    run=True
    #to borrow clock
    clock=pygame.time.Clock()
    #values to generate list
    n=50
    min_val=10
    max_val=500
    #list generation
    lst=generate_list(n,min_val,max_val)
    #draw class is called with window sizes
    draw_info=draw(800,600,lst)
    #variables to store the sorting and ascending or descending
    sorting=False
    ascending=True

    #default display of sort i.e. bubble
    sorting_algorithm=bubble_sort
    algo_name="Bubble Sort"
    #generator that corresponds to yield 
    sorting_algo_generator=None

    while run:
        clock.tick(60)
        if sorting:

            #required as yield is used
            try:
                next(sorting_algo_generator)
            except StopIteration:
                sorting=False
        else:
            draw_ac(draw_info,algo_name,ascending)
        pygame.display.update()

        #storing event such that we don't need to pygame.event simply event variable

        for event in pygame.event.get():

            #quit button press
            if event.type ==pygame.QUIT:
                run=False
            if event.type!=pygame.KEYDOWN:
                continue

            # R key pressed to randomize 
            if event.key==pygame.K_r:
                lst=generate_list(n,min_val,max_val)
                draw_info.set_list(lst)
                pygame.display.update()
                sorting=False

            # B key to call bubble sort
            elif event.key==pygame.K_b and not sorting:
                sorting=True
                
                sorting_algo_generator=sorting_algorithm(draw_info,ascending)

            # D key to change to Descending
            elif event.key==pygame.K_d and not sorting:
                ascending=False

            # A key to change to Ascending
            elif event.key==pygame.K_a and not sorting:
                ascending=True

            # I key to implement Insertion Sort
            elif event.key==pygame.K_i and not sorting:
                sorting=True
                sorting_algorithm=insertion_sort
                algo_name="Insertion Sort"
                sorting_algo_generator=sorting_algorithm(draw_info,ascending)

            # S key to implement Selection Sort
            elif event.key==pygame.K_s and not sorting:
                sorting=True
                sorting_algorithm=selection_sort
                algo_name="Selection Sort"
                sorting_algo_generator=sorting_algorithm(draw_info,ascending)              
            
    # Actual exit of pygame      
    pygame.quit()
if __name__=='__main__':
    main()
