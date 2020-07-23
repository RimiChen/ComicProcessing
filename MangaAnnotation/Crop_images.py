# Improting Image class from PIL module 
from os import walk
import os
import math
import json
from random import randrange
from PIL import Image, ImageTk


MANGA_IMAGE_PATH = "manga_images/Saisoku/"
MANGA_ANNOTATION_PATH = "annotation_data/Saisoku/"
SPLIT_FOLDER = "split_pages"
#MANGA_IMAGE_PATH = "manga_images/AisazuNihaIrarenai/"
#MANGA_IMAGE_PATH = "manga_images/Saisoku/"
#MANGA_ANNOTATION_PATH = "annotation_data/Saisoku/"

def crop_image(image_obj, min_x, min_y, max_x, max_y):
    
    # Opens a image in RGB mode 
    #im = Image.open(r"C:\Users\Admin\Pictures\geeks.png") 
    im = image_obj
    
    # Size of the image in pixels (size of orginal image) 
    # (This is not mandatory) 
    width, height = im.size 
    
    # Setting the points for cropped image 
    left = min_x
    top = min_y
    right = max_x
    bottom = max_y
    
    # Cropped image of above dimension 
    # (It will not change orginal image) 
    im_crop = im.crop((left, top, right, bottom)) 
    
    # Shows the image in image viewer 
    #im_crop.show()
    
    return im_crop
 
def loadManga(bookPath):
    #### from the path, load all image file names and make the path as a list
    print("SYSTEM: load magna {"+str(bookPath)+"}")
    

    filePathList = []
    for (_, _, filenames) in walk(bookPath):
        filePathList.extend(filenames)
        break
    
    # print("\n".join(filePathList))

    return filePathList

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


# def get_OCR_file(book_annotation):
def get_page_name(page_number):
    page_name = str(page_number)
    if page_number < 100:
        if page_number <10:
            page_name = "00"+str(page_number)
        else:
            page_name = "0"+str(page_number)
    
    return page_name

if __name__ == "__main__":
    book_path_list = [
        "manga_images/YumeiroCooking/",
        "manga_images/Saisoku/",
        "manga_images/AisazuNihaIrarenai/"
    ]
    
    book_index = {}
    book_count = 0
    for book in book_path_list:
        book_name = get_book_name(book)
        book_index[book_name] = book_count
        book_count = book_count +1
    
    
    
    manga_page_list = loadManga(MANGA_IMAGE_PATH )
    file_number = len(manga_page_list)
    book_name = get_book_name(MANGA_ANNOTATION_PATH)
    json_path = book_name+"_pages.json"
    book_annotation = load_manga_109_annotations(MANGA_ANNOTATION_PATH+json_path)
    #print("\n".join(manga_page_list))        
    
    folder_path = MANGA_IMAGE_PATH+SPLIT_FOLDER
    try:
        os.mkdir(folder_path)
    except OSError:
        print ("Creation of the directory %s failed" % folder_path)
    else:
        print ("Successfully created the directory %s " % folder_path)
    
    
    #get_OCR_file(book_annotation)
    
    
    
    #page = 2
    manga_page_number = len(manga_page_list)
    
    new_pages = {}
    
    new_page_count = 0
    for page in range(manga_page_number):
        image_obj = Image.open(MANGA_IMAGE_PATH+manga_page_list[page])
        image_id_record = {}
        new_image_list = {}
        new_image_list[page] = {}
        count = 0
        image_width, image_height = image_obj.size
        # print("w = "+str(image_width)+", h = "+str(image_height))
        min_x = {}
        min_y = {} 
        max_x = {}
        max_y = {}
        
        
        middle_x = math.floor(image_width/2)
        
        min_x[0] = middle_x
        min_x[1] = 0
        
        min_y[0] = 0
        min_y[1] = 0
         

        max_x[0] = image_width
        max_x[1] = middle_x
        
        max_y[0] = image_height
        max_y[1] = image_height
        

        
        new_image_1 = crop_image(image_obj, min_x[0], min_y[0], max_x[0], max_y[0])
        new_pages[new_page_count] = new_image_1       
        new_page_count = new_page_count +1

        new_image_2 = crop_image(image_obj, min_x[1], min_y[1], max_x[1], max_y[1])
        new_pages[new_page_count] = new_image_2       
        new_page_count = new_page_count +1        
        # for frame in book_annotation[page]["frames"]:
        #     image_id_record[count] = frame["id"]
        #     min_x = int(frame["xmin"])
        #     min_y = int(frame["ymin"])
        #     max_x = int(frame["xmax"])
        #     max_y = int(frame["ymax"])
        #     new_image = crop_image(image_obj, min_x, min_y, max_x, max_y)
        #     new_image_list[page][count] = new_image
        #     count = count + 1
        
        
    #new_image.show()
    for result_page in new_pages:
        need_image = new_pages[result_page]
        page_name = get_page_name(result_page)
        #print(page_name)
        need_image.save(MANGA_IMAGE_PATH+SPLIT_FOLDER+"/"+page_name+".jpg") 
    #print(book_annotation[2]) 