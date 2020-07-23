# Improting Image class from PIL module 
from os import walk
import os
import math
import json
from random import randrange
from PIL import Image, ImageTk


#MANGA_IMAGE_PATH = "manga_images/YumeiroCooking/"
#MANGA_ANNOTATION_PATH = "annotation_data/YumeiroCooking/"
MANGA_IMAGE_PATH = "manga_images/AisazuNihaIrarenai/"
MANGA_ANNOTATION_PATH = "annotation_data/AisazuNihaIrarenai/"
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


def get_OCR_file(book_annotation):
        
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
    
    folder_path = MANGA_IMAGE_PATH+"crop_result"
    try:
        os.mkdir(folder_path)
    except OSError:
        print ("Creation of the directory %s failed" % folder_path)
    else:
        print ("Successfully created the directory %s " % folder_path)
    
    
    get_OCR_file(book_annotation)
    
    
    
    #page = 2
    manga_page_number = len(manga_page_list)
    for page in range(manga_page_number):
        image_obj = Image.open(MANGA_IMAGE_PATH+manga_page_list[page])
        image_id_record = {}
        new_image_list = {}
        new_image_list[page] = {}
        count = 0
        for frame in book_annotation[page]["frames"]:
            image_id_record[count] = frame["id"]
            min_x = int(frame["xmin"])
            min_y = int(frame["ymin"])
            max_x = int(frame["xmax"])
            max_y = int(frame["ymax"])
            new_image = crop_image(image_obj, min_x, min_y, max_x, max_y)
            new_image_list[page][count] = new_image
            count = count + 1
        
        
        #new_image.show()
        for result_panel in new_image_list[page]:
            need_image = new_image_list[page][result_panel]
            need_image.save(MANGA_IMAGE_PATH+"crop_result/"+str(page)+"_"+str(result_panel)+".jpg") 
        #print(book_annotation[2]) 