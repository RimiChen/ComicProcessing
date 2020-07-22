#### trying to build an interface for manga annotation
from os import walk
#from tkinter import *
import tkinter as tk
import math
import json
from random import randrange
from PIL import Image, ImageTk


MANGA_PATH = "YumeiroCooking/"
DEFAULT_COUNT = 0




global G_WINDOW_WIDTH
G_WINDOW_WIDTH = 1200
global G_WINDOW_HEIGHT
G_WINDOW_HEIGHT = 800
global G_MAX_LAYER
G_MAX_LAYER = 4

global window
window = tk.Tk()

global G_structure_order
G_structure_order = 10 

global book_record_json
book_record_json = {}


global page_count
page_count = DEFAULT_COUNT
global page_record
page_record = DEFAULT_COUNT
global current_image_label
current_image_label = None
global file_number
file_number = 0
global current_page_label
current_page_label = None
global image_frame_width
image_frame_width = 0
global image_frame_height
image_frame_height = 0
global current_image_w
current_image_w = 0  
global current_image_h
current_image_h = 0
global image_resize_pro
image_resize_pro = 0
global book_annotation
book_annotation = []
global frame_labels
frame_labels = []
global isFrameHide
isFrameHide = False
global reading_order_frames
reading_order_frames = []
global record_orders
record_orders = []
global current_order_count
current_order_count = 0

global reading_transition_frames
reading_transition_frames = []
global record_transitions
record_transitions = []
global current_transition_count
current_transition_count = 0

#[layer] = base frame of the layer
global layer_frames
layer_frames = []
global layer_record
#[layer][position_index][index(index of the child)] = "label"
layer_record = {}
global layer_list
#[layer] = [button_label]
layer_list = {}
global layer_position
#[layer][position_index] = frame
layer_position = {}

global layer_info
#[layer][position_index] = child#
layer_info = {}

def loadManga(bookPath):
    #### from the path, load all image file names and make the path as a list
    print("SYSTEM: load magna {"+str(bookPath)+"}")
    

    filePathList = []
    for (_, _, filenames) in walk(bookPath):
        filePathList.extend(filenames)
        break
    
    # print("\n".join(filePathList))

    return filePathList

def from_rgb(rgb):
    """translates an rgb tuple of int to a tkinter friendly color code
    """
    return "#%02x%02x%02x" % rgb 

def next_page(parent_frame, order_parent, structure_parent, menu_parent, image_label, manga_path):
    #print("next page")
    #current_image = image_label
    #current_image_label = None
    #current_image.destroy()
    global page_count
    global file_number
    global record_orders
    global current_order_count

    global record_transitions
    global current_transition_count
    
    previous_count = page_count
    page_count = (page_count + 1 )% file_number
    page_count = render_image(parent_frame, order_parent, structure_parent, menu_parent)
    record_page(previous_count)
    record_orders = []
    current_order_count = 0
    record_transitions = []
    current_transition_count = 0    
    #clean_all_structure(structure_parent)
    clean_all_in_frames(structure_parent)

    render_frame_labels(parent_frame, order_parent, structure_parent)
    #print(page_count)
    
def pre_page(parent_frame, order_parent, structure_parent, menu_parent, image_label, manga_path):
    #print("previous page")
    global page_count
    global file_number
    global record_orders
    global current_order_count

    global record_transitions
    global current_transition_count
        
    previous_count = page_count
    page_count = (page_count - 1) % file_number     
    page_count = render_image(parent_frame, order_parent, structure_parent, menu_parent)
    record_page(previous_count)
    record_orders = []
    current_order_count = 0
    record_transitions = []
    current_transition_count = 0
    #clean_all_structure(structure_parent)    
    clean_all_in_frames(structure_parent)
    
    render_frame_labels(parent_frame, order_parent, structure_parent)
    #print(page_count)


def resize_image():
    global image_frame_width
    global image_frame_height
    global current_image_w
    global current_image_h
    
    pro_w = image_frame_width/ current_image_w
    pro_h = image_frame_height/ current_image_h
    
    new_w_1 = math.floor(current_image_w * pro_w)
    new_h_1 = math.floor(current_image_h * pro_w)

    new_w_2 = math.floor(current_image_w * pro_h)
    new_h_2 = math.floor(current_image_h * pro_h)
    
    if new_w_1 > image_frame_width or new_h_1 > image_frame_height:
        return pro_h
    else:
        return pro_w

def render_image(parent_frame, order_frame, structure_parent, manga_menu_frame):
    ### load the default image
    global page_count
    load = Image.open(MANGA_PATH+manga_page_list[page_count])
    global current_image_w
    global current_image_h
    current_image_w, current_image_h = load.size
    global image_resize_pro
    image_resize_pro = resize_image()
    
    global isFrameHide
    isFrameHide = False
    
    for widget in manga_menu_frame.winfo_children():
        widget.destroy() 
    

    new_w = math.floor(current_image_w*image_resize_pro)
    new_h = math.floor(current_image_h*image_resize_pro)
    load = load.resize((new_w, new_h), Image.ANTIALIAS) 

    render = ImageTk.PhotoImage(load)
    
    global current_image_label 
    current_image_label = tk.Label(parent_frame, image=render)
    current_image_label.image = render
    current_image_label.place(x=math.floor(image_frame_width/2), y=math.floor(image_frame_height/2), anchor = tk.CENTER)
   
    hide_frame_button = tk.Button(manga_menu_frame, text="Hide/Show", bg=from_rgb((232, 255, 157)), command = lambda: hide_frame_labels(parent_frame, order_frame, structure_parent))
    hide_frame_button.place(x=50, y=0)
    
    end_frame_button = tk.Button(manga_menu_frame, text="End", bg=from_rgb((232, 255, 157)), command = lambda: finish_record())
    end_frame_button.place(x=200, y=0)    

    save_frame_button = tk.Button(manga_menu_frame, text="Save", bg=from_rgb((232, 255, 157)), command = lambda: record_page(page_count))
    save_frame_button.place(x=400, y=0)    


    global current_page_label 
    current_page_label = tk.Label(manga_menu_frame, text="Page"+str(page_count), bg=from_rgb((0, 143, 10)))
    current_page_label.place(x=0, y=0)
   





    return page_count            

def render_frame_labels(parent_frame, order_parent, structure_parent):
    print("render frame labels")
    
    global book_annotation
    global frame_labels
    global page_count
    global page_record
    global isFrameHide
    global current_order_count

    
    #page_record = page_count

    if isFrameHide == True:
      
        for frame_label in frame_labels:
            frame_label.place_forget()
        frame_labels = []
    else:
        page_number = book_annotation[page_count]["index"]
        frame_list = book_annotation[page_count]["frames"]
        destory_order_frames(order_parent)
        destory_transition_frames(order_parent)
        if len(frame_list) > 0:
            #### at least a frame in this page
            frame_labels = []
            current_order_count = 0
            clean_order()
            clean_transitions()
            for frame in frame_list:
                coord_x, coord_y = new_coord(int(frame["xmin"]), int(frame["ymin"]), int(frame["xmax"]), int(frame["ymax"]))
        # frames = 
                frame_button = tk.Button(parent_frame, text = frame["id"], bg = from_rgb((randrange(256), randrange(256), randrange(256))))
                frame_button.configure(command=lambda button=frame_button: add_order(button))
                frame_button.place(x=coord_x, y=coord_y, anchor=tk.CENTER)
                
                frame_labels.append(frame_button)
        
        
        
        load_order_frames(order_parent)
        load_transition_frames(order_parent)  


    load_structure_layers(structure_parent)


def record_page(now_page):
    global book_annotation
    global frame_labels
    global current_order_count
    global record_orders
    global record_transitions
    global layer_list
    
    
    
    
    print("============================")
    print("System: record page # "+str(now_page))
    print("Reading order:")
    print(",".join(record_orders))
    print("Transitions:")
    print(",".join(record_transitions))    
    print("Frames:")
    print(book_annotation[now_page]["frames"])
    print("Structure:")
    print(json.dumps(layer_list, indent=4))
    print("============================")
    
    page_node = {}
    page_node["page_index"] = now_page
    page_node["panel_number"] = len(frame_labels)
    page_node["reading_order"] = record_orders
    page_node["transitions"] = record_transitions
    page_node["layout"] = layer_list
    # page_node["panels"] = {}
    
    # for panel in book_annotation[page_count]["frames"]:
    #     page_node["panels"][panel["id"]] = panel
        
    if "pages" in book_record_json:
        #book_record_json["pages"].append(page_node)
        book_record_json["pages"][now_page] = page_node
    else:
        book_record_json["pages"] = {}
        #book_record_json["pages"].append(page_node)
        if page_record in book_record_json["pages"]:
            book_record_json["pages"][now_page] = page_node
        else:
            book_record_json["pages"][now_page] = page_node
            
    #page_record = page_count
    #record_orders = []
    #record_transitions = []    


    
    
def finish_record():
    global book_record_json
    global page_count
    global window
    
    #record_page(page_count)
    
    book_name = get_book_name(MANGA_PATH)
    
    book_record_json["book"] = book_name
    #book_record_json["pages"] = []
    
    json_file = open(book_name+"_"+str(randrange(65536))+".json", "w")
    # magic happens here to make it pretty-printed
    json_file.write(json.dumps(book_record_json, indent=4))
    json_file.close()     
    
    window.quit() 
    
    
    
    
      
    
    
def hide_frame_labels(parent_frame, order_parent, structure_parent):
    global isFrameHide
    
    if isFrameHide == True:
        
        isFrameHide = False
    else:
        isFrameHide = True
        
    render_frame_labels(parent_frame, order_parent, structure_parent)
    
def add_order(self_button):
    global reading_order_frames
    global record_orders
    global current_order_count
    global frame_labels


    current_len = len(record_orders)
    current_id = self_button["text"]


    
    # print("=================================")
    # print("\n".join(record_orders))
    # print("=================================")

    frame_count = len(frame_labels)
    #print(frame_count)

    if frame_count == 0 :
        print("SYSTEM:　no frame in this page")
    else:
        total_width = math.floor(G_WINDOW_WIDTH/2)
        toatl_needed_blocks = frame_count * 2
        
        each_width = math.floor(total_width / toatl_needed_blocks)
        pair_width = math.floor(2 * total_width / toatl_needed_blocks)

        if current_len > 0:
            final_name = record_orders[current_len -1]
            if final_name == current_id:
                ## do nothing 
                print("SYSTEM: already added "+ str(current_id))
            else:
                record_orders.append(current_id)        
                
                ### generate button
                new_order_id = tk.Button(reading_order_frames[current_order_count], text = current_id, bg = from_rgb((randrange(256), randrange(256), randrange(256))))
                new_order_id.configure(command=lambda button=new_order_id: remove_order(button))
                new_order_id.place(x=0, y=0, anchor=tk.CENTER)
                # print("Add to reading order "+ str(current_order_count))    

                current_order_count = current_order_count + 1

        else:
            record_orders.append(current_id)
            ### generate button
            new_order_id = tk.Button(reading_order_frames[current_order_count], text = current_id, bg = from_rgb((randrange(256), randrange(256), randrange(256))))
            new_order_id.configure(command=lambda button=new_order_id: remove_order(button))
            new_order_id.place(x=0, y=0, anchor=tk.CENTER)
            # print("Add to reading order "+ str(current_order_count))    
            
            current_order_count = current_order_count + 1               
    
    
def add_transition(self_button):
    global reading_transition_frames
    global record_transitions
    global current_transition_count
    global frame_labels


    current_len = len(record_transitions)
    current_id = self_button["text"]


    
    # print("=================================")
    # print("\n".join(record_orders))
    # print("=================================")

    frame_count = len(frame_labels)
    #print(frame_count)

    if frame_count == 0 :
        print("SYSTEM:　no frame in this page")
    else:
        if current_transition_count < frame_count - 1:
            
            total_width = math.floor(G_WINDOW_WIDTH/2)
            toatl_needed_blocks = frame_count * 2
            
            each_width = math.floor(total_width / toatl_needed_blocks)
            pair_width = math.floor(2 * total_width / toatl_needed_blocks)

            record_transitions.append(current_id)
            ### generate button
            new_transition_id = tk.Button(reading_transition_frames[current_transition_count], text = current_id, bg = from_rgb((randrange(256), randrange(256), randrange(256))))
            new_transition_id.configure(command=lambda button=new_transition_id: remove_transition(button))
            new_transition_id.place(x=0, y=0, anchor=tk.CENTER)
            # print("Add to reading transition "+ str(current_transition_count))    
            
            current_transition_count = current_transition_count + 1 
        else:
            print("SYSTEM: should not have more transition than #panels -1")
        
            
    
def remove_order(now_button):
    #print(now_button["text"])
    
    global record_orders
    global current_order_count
    global reading_order_frames

    current_len = len(record_orders)    
    current_id = now_button["text"]
    
    final_id = record_orders[current_len -1]
    #print("##"+str(final_id))
    #print("??"+str(current_id))
    
    if current_id == final_id:
        ## can be delete
        record_orders.pop()
        
        for widget in reading_order_frames[current_order_count-1].winfo_children():
            widget.destroy()  
        
        current_order_count = current_order_count -1
                    
    else:
        print("SYSTEM: delete by orders")

def remove_transition(now_button):
    #print(now_button["text"])
    
    global record_transitions
    global current_transition_count
    global reading_transition_frames

    current_len = len(record_transitions)    
    current_id = now_button["text"]
    
    final_id = record_transitions[current_len -1]
    #print("##"+str(final_id))
    #print("??"+str(current_id))
    
    ### only remove the last one
    
    if current_transition_count >= 0:
        record_transitions.pop()
            
        for widget in reading_transition_frames[current_transition_count-1].winfo_children():
            widget.destroy()  
            
        current_transition_count = current_transition_count -1
                    


def clean_order():
    global record_orders
    global current_order_count
    global reading_order_frames
    
    for frame in reading_order_frames:
        for widget in reading_order_frames[frame].winfo_children():
            widget.destroy()      

    reocrd_orders = []
    current_order_count = 0              


def clean_transitions():
    global record_transitions
    global current_transition_count
    global reading_transition_frames
    
    for frame in reading_transition_frames:
        for widget in reading_transition_frames[frame].winfo_children():
            widget.destroy()      

    reocrd_transitions = []
    current_transition_count = 0    
    
def load_manga_109_annotations(json_path):
    print("load_manga_109_annotations")
    annotations = []
    book_dictionary = {}
    
    
    #json_file = open(json_path, "r")
    with open(json_path) as json_file:
    
        annotations = json.load(json_file)
        
    count = 0
    for annotation in annotations:
        
        book_dictionary[count] = annotation
        # print(annotation)
        count = count + 1
        
    return book_dictionary
    
def get_book_name(path_string):
    name_string_array = path_string.split("/")
    string_lenth = len(name_string_array)
    
    book_name_index = (string_lenth -1)-1
    
    book_name = name_string_array[book_name_index]
    return book_name

def get_image_shift():
    global current_image_w
    global current_image_h
    
    global image_frame_width
    global image_frame_height
    
    global image_resize_pro
    
    new_w = math.floor(current_image_w*image_resize_pro)
    new_h = math.floor(current_image_h*image_resize_pro)
    
    left_top_x = math.floor(image_frame_width/2 - new_w/2)
    left_top_y = math.floor(image_frame_height/2 - new_h/2)
    
    return left_top_x, left_top_y

def new_coord(x_min, y_min, x_max, y_max):
    center_point_x = math.floor((x_min+x_max)/2)
    center_point_y = math.floor((y_min+y_max)/2)
    
    
    center_point_x = math.floor(center_point_x*image_resize_pro)
    center_point_y = math.floor(center_point_y*image_resize_pro)
    
    shift_x, shift_y = get_image_shift()
    
    center_point_x = center_point_x +shift_x
    center_point_y = center_point_y +shift_y
    
    return center_point_x, center_point_y
    
def load_order_frames(parent_frame):
    # frame_labels: current frame buttons
    global G_WINDOW_WIDTH
    global G_WINDOW_HEIGHT
    
    global frame_labels
    global reading_order_frames
    global G_structure_order
    
    frame_count = len(frame_labels)
    #print(frame_count)
    
    
    if frame_count == 0 :
        print("SYSTEM:　no frame in this page")
    else:
        total_width = math.floor(G_WINDOW_WIDTH/2)
        toatl_needed_blocks = frame_count * 2
        
        each_width = math.floor(total_width / toatl_needed_blocks)
        pair_width = math.floor(2 * total_width / toatl_needed_blocks)
        
        for count in range(frame_count):
            #### panel --> transistion --> panel .....
            new_panel_frame = tk.Frame(parent_frame, width=each_width, height=parent_frame.winfo_height(), bg=from_rgb((255, 255, 0)))
            new_panel_frame.place(x=pair_width * count, y=0)
            reading_order_frames.append(new_panel_frame)        
        
def destory_order_frames(parent_frame):
    global reading_order_frames
    #print(reading_order_frames)
    
    # for in_frame in reading_order_frames:
    # #     print(in_frame)
    # #     #in_frame.place_forget()
    #     in_frame.destory()
    # # parent_frame.destory()  
    for widget in parent_frame.winfo_children():
       widget.destroy()  
         
    reading_order_frames = []
        
def load_transition_frames(parent_frame):
    # frame_labels: current frame buttons
    global G_WINDOW_WIDTH
    global G_WINDOW_HEIGHT
    
    global frame_labels
    global reading_transition_frames
    global G_structure_order
    
    frame_count = len(frame_labels)
    #print(frame_count)
    
    
    if frame_count == 0 :
        print("SYSTEM:　no frame in this page")
    else:
        total_width = math.floor(G_WINDOW_WIDTH/2)
        toatl_needed_blocks = frame_count * 2
        
        each_width = math.floor(total_width / toatl_needed_blocks)
        pair_width = math.floor(2 * total_width / toatl_needed_blocks)
        
        for count in range(frame_count):
            #### panel --> transistion --> panel .....
            new_panel_frame = tk.Frame(parent_frame, width=each_width, height=parent_frame.winfo_height(), bg=from_rgb((255, 0, 255)))
            new_panel_frame.place(x=pair_width * count+each_width, y=0)
            reading_transition_frames.append(new_panel_frame)        
        
def destory_transition_frames(parent_frame):
    global reading_transition_frames
    #print(reading_order_frames)
    
    # for in_frame in reading_order_frames:
    # #     print(in_frame)
    # #     #in_frame.place_forget()
    #     in_frame.destory()
    # # parent_frame.destory()  
    for widget in parent_frame.winfo_children():
       widget.destroy()  
         
    reading_transition_frames = []
        
def clean_all_in_frames(parent_frame):
    for widget in parent_frame.winfo_children():
           widget.destroy()      


def load_structure_layers(structure_parent):
    global G_MAX_LAYER
    global layer_frames
    global layer_record
    global layer_list
    global layer_position
    global layer_info

    max_layer = G_MAX_LAYER
    button_width = 50
    total_structure_height = structure_parent.winfo_height()
    total_structure_width = structure_parent.winfo_width()

    
    print(total_structure_height)
    print(total_structure_width)

    layer_frames = []
    for layer in range(max_layer):
        #print(layer)
        layer_record[layer] = {}
        layer_list[layer] = []
        layer_position[layer] = {}
        layer_info[layer] = {}
        new_layer = tk.Frame(master= structure_parent, width=total_structure_width, height=math.floor(total_structure_height/max_layer), bg=from_rgb((232, randrange(256), randrange(256))))
        new_layer.place(x=0, y=math.floor(total_structure_height/max_layer * layer))
        
        # layer_add = tk.Button(new_layer, text="Layer"+str(layer)+"+", bg=from_rgb((232, 255, 157)))
        # layer_add.configure(command=lambda button=layer_add: add_node(button, total_structure_width, total_structure_height))
        # layer_add.place(x = total_structure_width, y = math.floor(total_structure_height/max_layer * layer))        
        
        layer_frames.append(new_layer) 
        
    # layer_record[0] = {}
    # layer_record[0][0] = 1
    # structure_base(layer_frames[0], math.floor(total_structure_width*0.8),  math.floor(total_structure_height*0.8), 20, math.floor(total_structure_width*0.1), 1, 0)
    up_width = math.floor(total_structure_width)
    width = math.floor(total_structure_width)
    height = math.floor(total_structure_height/max_layer)
    layer = 0

    #structure_base(layer_frames[0], up_width, width,  height, 20, 0, "0_0_0")
    drawLabelset(layer_frames[0], width, height, 0, 0, button_function, "0_0_0", "Root")
   
    # global layer_record
    # #[layer][position_index][index(index of the child)] = "label"
    # global layer_list
    # #[layer] = [button_label]
    # global layer_position
    # #[layer][position_index] = frame
    # global layer_info
    # #[layer][position_index] = child#  

    pos_key = "0_0_0"
    layer_list[0].append(pos_key)
    
    layer_record[0] = {}
    layer_record[0][0] = {}
    layer_record[0][0][0] = pos_key
     
    # record root
    layer_info[-1]= {}
    layer_info[-1][0]= 1
    
    color = from_rgb((232, randrange(256), randrange(256)))
    new_layer = tk.Frame(master= layer_frames[1], width=width, height=height, bg=color)
    new_layer.place(x=0, y=0)
    layer_position[1][0] = new_layer  

   

    

      
 
def clean_all_structure(structure_parent):
    print("SYSTEM: clean the structures")
    global layer_frames
    
    for layer in layer_frames:
        clean_all_in_frames(layer_frames[layer])
    load_structure_layers(structure_parent)
    
    
# def structure_base(button, parent_frame, up_width, height, button_width, layer):
    global G_MAX_LAYER
    global layer_frames
    global layer_record 
    global layer_list
    global layer_position   
    
    #print("layer: "+str(layer)+", index: "+str(index)+", pos_count: "+str(pos_count))

    pos_label = button["text"]
    position_string = pos_label.split("_")

    print("$$"+pos_label)
    
    clean_all_in_frames(parent_frame)
    print(json.dumps(layer_list, indent=4))    
    
    #### search layer_list  
    count = 0
    pos_count = 0
    for label in layer_list[layer -1]:
        if label == pos_label:
            pos_count = count
        count = count + 1
        
    if pos_count in layer_record[layer]:
        index = len(layer_record[layer][pos_count])
        layer_record[layer][pos_count][index] = 1 
    else:
        layer_record[layer][pos_count] = {}
        index = 0
        layer_record[layer][pos_count][index] = 1
    
    label_this = str(layer)+"_"+str(pos_count)+"_"+str(index)
    layer_list[layer].append(label_this)
    
    if layer +1 < G_MAX_LAYER:
        #layer_position[layer +1] = {}
        for item in range(len(layer_list[layer])):
            temp_width = math.floor(layer_frames[layer+1].winfo_width()/len(layer_list[layer]))
            new_color = from_rgb((232, randrange(256), randrange(256)))
            
            next_layer = tk.Frame(master= layer_frames[layer+1], width=temp_width, height=height, bg=new_color)
            next_layer.place(x=0+item*temp_width, y=0)
            
            if item in layer_position[layer +1]:
                ### frame exist
                layer_position[layer +1][item].place(width = temp_width, height= height, x=0+item*temp_width, y=0)
            else:
                layer_position[layer +1][item] = next_layer               

    
    #print(layer_position[layer +1])
    ## recover all frames

    for current in layer_list[layer]:
        current_string = current.split("_")
        now_layer = int(current_string[0])
        now_pos = int(current_string[1])
        now_index = int(current_string[2])
        
        color = from_rgb((232, randrange(256), randrange(256)))
        new_width = math.floor(layer_position[now_layer][now_pos].winfo_width()/len(layer_record[now_layer][now_pos]))
        new_layer = tk.Frame(master= parent_frame, width=new_width, height=height, bg=color)
        parent_width = parent_frame.winfo_width()
        #need_width = parent_width/len(layer_list[layer-1]) 
        new_layer.place(x=0+now_index*new_width, y=0) 

        label_for_this = str(now_layer)+"_"+str(now_pos)+"_"+str(now_index)
        print(label_for_this)
    
        if layer +1 < G_MAX_LAYER:
            # next_layer = tk.Frame(master= layer_frames[layer+1], width=new_width, height=height, bg=color)
            # next_layer.place(x=0+pos_count*up_width+need*new_width, y=0) 

            layer_add = tk.Button(new_layer, text=label_for_this, bg=from_rgb((232, 255, 157)))
            layer_add.configure(command=lambda button=layer_add: structure_base(button, layer_position[layer+1][pos_count], new_width, height, button_width, layer+1))
            layer_add.place(x = 0, y = 0)          
def button_function(current_button):
    global G_MAX_LAYER
    global layer_frames
    #[layer] = base frame of the layer
    global layer_frames
    global layer_record
    #[layer][position_index][index(index of the child)] = "label"
    global layer_list
    #[layer] = [button_label]
    global layer_position
    #[layer][position_index] = frame
    global layer_info
    #[layer][position_index] = child#
    
    button_label = current_button["text"]
    button_label_string = button_label.split("_")
    ### get layer
    layer = int(button_label_string[0])+1
    ### get parent index
    if layer > 0:
        # list
        parent_layer_list = layer_list[layer -1]
        parent_index = parent_layer_list.index(button_label)
        parent_layer = layer - 1
    else:
        # root
        parent_layer = -1
        parent_index = 0
    
    #print("layer = "+str(layer)+", parent_layer = "+str(parent_layer))
    #print("layer = "+str(layer)+", parent_index = "+str(parent_index))
    
    
    # record this node
    if parent_index in layer_info[parent_layer]:
        # exist other child
        this_index = layer_info[parent_layer][parent_index]
        ## also add this
        layer_info[parent_layer][parent_index] = layer_info[parent_layer][parent_index] +1
    else:
        this_index = 0
        layer_info[parent_layer][parent_index] = 1

    # update layer_list and  layer_record
    new_label = str(layer)+"_"+str(parent_index)+"_"+str(this_index)
    layer_list[layer].append(new_label)
    
    if parent_index in layer_record[layer]:
        #layer_record[layer][parent_index] exist
        layer_record[layer][parent_index][this_index] = new_label
    else:
        layer_record[layer][parent_index] = {}
        layer_record[layer][parent_index][this_index] = new_label
        
    # add this label to this layer
    if parent_index < 0:
        #print("this is the first layer")
        target_frame = layer_position[layer][parent_index]
        clean_all_in_frames(target_frame)
    else:
        target_frame = layer_position[layer][parent_index]
        clean_all_in_frames(target_frame)
    
    this_width = target_frame.winfo_width()/(this_index+1)
    this_height = target_frame.winfo_height()
    
    ## redraw previous and this
    for previous in range(this_index+1):
        recorded_label = layer_record[layer][parent_index][previous]
        index_label = get_label_text(recorded_label)
        drawLabelset(target_frame, this_width, this_height, previous*this_width, 0, button_function, recorded_label, index_label)
        
    # this
    recorded_label = layer_record[layer][parent_index][this_index]
    index_label = get_label_text(recorded_label)
    drawLabelset(target_frame, this_width, this_height, this_index*this_width, 0, button_function, recorded_label, index_label)    
    
    ## update the layer_position for next layer
    next_layer = layer+1
    #print("next layer = "+str(next_layer))
        
    if next_layer < G_MAX_LAYER:
        next_layer_number = len(layer_list[layer])
        #root_frame = layer_position[0][0]
        root_frame = layer_frames[0]
        new_next_width = math.floor(root_frame.winfo_width()/next_layer_number)
        new_next_height = root_frame.winfo_height()

        # update existing frames
        for sub_frame in layer_position[next_layer]:
            layer_position[next_layer][sub_frame].place(width = new_next_width, height= new_next_height, x=sub_frame*new_next_width, y=0)
        
        color = from_rgb((232, randrange(256), randrange(256)))
        new_layer = tk.Frame(master= layer_frames[next_layer], width=new_next_width, height=new_next_height, bg=color)
        new_layer.place(x=(next_layer_number-1)*new_next_width, y=0)
        layer_position[next_layer][next_layer_number-1] = new_layer               
        
        
    
def get_label_text(index_label):
    return index_label    
def drawLabelset(parent_frame, width, height, x, y, button_fun, button_label, label_text):

        color = from_rgb((232, randrange(256), randrange(256)))
        new_layer = tk.Frame(master= parent_frame, width=width, height=height, bg=color, bd = 2)
        new_layer.place(x=x, y=y) 
   
        tag_label = tk.Label(new_layer, text=label_text, bd=1, font="Times 14", anchor=tk.N, bg=from_rgb((255, 255, 255)))
        tag_label.place(relx=0.05, rely=0.25, relwidth = 0.9, relheight = 0.5)        

        layer_add = tk.Button(new_layer, text=button_label, bg=from_rgb((232, 255, 157)))
        layer_add.configure(command=lambda button=layer_add:  button_fun(button))
        layer_add.place(x = 0, y = 0)          

    
    
               
def GUIterface(window_w, window_h, manga_path, manga_page_list):
    print("SYSTEM: Lauch the interface")
    global book_annotation

    global window
    #window = tk.Tk()
    window.title("Annotation interface")
    global G_structure_order


    main_frame = tk.Frame(master=window, width=window_w, height=window_h)
    main_frame.pack()
    
    manga_frame = tk.Frame(main_frame, width=math.floor(window_w/2), height=window_h, bg=from_rgb((0, 143, 10)))
    manga_frame.place(x=0, y=0) 
    
    manga_image_frame = tk.Frame(manga_frame, bg=from_rgb((232, 255, 157)))
    manga_image_frame.place(relx=0.05, rely=0.05, relwidth = 0.9, relheight = 0.9) 
    manga_image_frame.update()
    
    manga_menu_frame = tk.Frame(manga_frame, bg=from_rgb((0, 255, 157)))
    manga_menu_frame.place(relx=0.05, y=0, relwidth = 0.9, relheight = 0.05) 
    manga_menu_frame.update()    
    
    

    #print(manga_image_frame.winfo_width())
    global image_frame_width
    image_frame_width = manga_image_frame.winfo_width()
    global image_frame_height
    image_frame_height = manga_image_frame.winfo_height()
    
   
  
    structure_frame = tk.Frame(master=main_frame, width=math.floor(window_w/2), height=math.floor(window_h*(1-2/G_structure_order)), bg=from_rgb((232, 255, 157)))
    structure_frame.place(x=math.floor(window_w/2), y=0)
    structure_label = tk.Label(structure_frame, text="Page Structure", bg=from_rgb((232, 255, 157)))
    structure_label.place(x=0, y=0)
    

    
    transition_frame = tk.Frame(master=main_frame, width=math.floor(window_w/2), height=math.floor(window_h/G_structure_order), bg=from_rgb((0, 143, 10)))
    transition_frame.place(x=math.floor(window_w/2), y=math.floor(window_h*(1-2/G_structure_order)))
    transition_label = tk.Label(transition_frame, text="Transitions", bg=from_rgb((0, 143, 10)))
    transition_label.place(x=0, y=0)  
    

    transition_frame_width = math.floor(window_w/2 /7)
    transition_button_y = 30
    
    transition_moment_button = tk.Button(transition_frame, text="Moment", bg=from_rgb((232, 255, 157)))
    transition_moment_button.configure(command=lambda button=transition_moment_button: add_transition(button))
    transition_moment_button.place(x = transition_frame_width * 0, y = transition_button_y)
    
    transition_action_button = tk.Button(transition_frame, text="Action", bg=from_rgb((232, 255, 157)))
    transition_action_button.configure(command=lambda button=transition_action_button: add_transition(button))
    transition_action_button.place(x = transition_frame_width * 1, y = transition_button_y)
    
    transition_subject_button = tk.Button(transition_frame, text="Subject", bg=from_rgb((232, 255, 157)))
    transition_subject_button.configure(command=lambda button=transition_subject_button: add_transition(button))
    transition_subject_button.place(x = transition_frame_width * 2, y = transition_button_y)
    
    transition_scene_button = tk.Button(transition_frame, text="Scene", bg=from_rgb((232, 255, 157)))
    transition_scene_button.configure(command=lambda button=transition_scene_button: add_transition(button))
    transition_scene_button.place(x = transition_frame_width * 3, y = transition_button_y)
    
    transition_aspect_button = tk.Button(transition_frame, text="Aspect", bg=from_rgb((232, 255, 157)))
    transition_aspect_button.configure(command=lambda button=transition_aspect_button: add_transition(button))
    transition_aspect_button.place(x = transition_frame_width * 4, y = transition_button_y)
    
    transition_non_button = tk.Button(transition_frame, text="Non_sequitur", bg=from_rgb((232, 255, 157)))
    transition_non_button.configure(command=lambda button=transition_non_button: add_transition(button))
    transition_non_button.place(x = transition_frame_width * 5, y = transition_button_y)
    
    transition_other_button = tk.Button(transition_frame, text="Other", bg=from_rgb((232, 255, 157)))
    transition_other_button.configure(command=lambda button=transition_other_button: add_transition(button))
    transition_other_button.place(x = transition_frame_width * 6, y = transition_button_y)
    
      
    
    order_frame = tk.Frame(master=main_frame, width=math.floor(window_w/2), height=math.floor(window_h/G_structure_order), bg=from_rgb((255, 255, 255)))
    order_frame.place(x=math.floor(window_w/2), y=math.floor(window_h*(1-1/G_structure_order)))
    order_label = tk.Label(transition_frame, text="Reading Order", bg=from_rgb((255, 255, 255)))
    order_label.place(x=0, y=window_h/G_structure_order -20)    
    
    # frame_labels: current frame buttons
    #order_frames(order_frame) 

    next_button = tk.Button(manga_frame, text = ">>", command = lambda: next_page(manga_image_frame, order_frame, structure_frame, manga_menu_frame, current_image_label, MANGA_PATH))
    next_button.place(x=math.floor(window_w/2 - window_w/2*0.05), y=math.floor(window_h/2))
     
    pre_button = tk.Button(manga_frame, text = "<<", command = lambda: pre_page(manga_image_frame, order_frame, structure_frame, manga_menu_frame, current_image_label, MANGA_PATH)) 
    pre_button.place(x=0, y=math.floor(window_h/2))


    # hide_frame_button = tk.Button(manga_menu_frame, text="Hide/Show", bg=from_rgb((232, 255, 157)), command = lambda: hide_frame_labels(manga_image_frame, order_frame, structure_frame))
    # hide_frame_button.place(x=50, y=0)
    
    # end_frame_button = tk.Button(manga_menu_frame, text="End", bg=from_rgb((232, 255, 157)), command = lambda: hide_frame_labels(manga_image_frame, order_frame, structure_frame))
    # end_frame_button.place(x=200, y=0)    

    # global current_page_label 
    # current_page_label = tk.Label(manga_menu_frame, text="Page"+str(page_count), bg=from_rgb((0, 143, 10)))
    # current_page_label.place(x=0, y=0)


    #clean_all_structure(structure_frame)
    render_image(manga_image_frame, order_frame, structure_frame, manga_menu_frame)
    render_frame_labels(manga_image_frame, order_frame, structure_frame) 


    window.mainloop()
  

    
#### Launch the GUI
if __name__ == "__main__":
    
    
    # global G_WINDOW_WIDTH
    # global G_WINDOW_HEIGHT
    # G_WINDOW_WIDTH = 1200
    # G_WINDOW_HEIGHT = 800
    
    print(G_WINDOW_WIDTH)
    print(G_WINDOW_HEIGHT)
    manga_page_list = loadManga(MANGA_PATH)
    file_number = len(manga_page_list)
    book_name = get_book_name(MANGA_PATH)
    json_path = book_name+"_pages.json"
    ## Lauch the interface
    book_annotation = load_manga_109_annotations(json_path)
    GUIterface(G_WINDOW_WIDTH, G_WINDOW_HEIGHT, MANGA_PATH, manga_page_list)