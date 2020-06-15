### read and process xml data
import sys
import xml.etree.ElementTree as ET
from googletrans import Translator
import json


class ComicBook:
    def __init__(self):
        self.bookName = ""
        self.characters = []
        self.pageList = []
        # if needed, turn the translater on
        self.translateFlag = False

        # page {}:
        # frame [], text [], body [], face []
       
### script start from here
if __name__ == "__main__":
    # read target script  (read xml and get running object)
    
    ## assigned xml file path
    fileName = "./annotation_data/AisazuNihaIrarenai.xml"
    print("SYSTEM: load the script "+fileName)
    
    ## initialize the translater (googleTrans)
    translator = Translator()
        
    ## parse xml as a tree structure
    tree = ET.parse(fileName)
    comicBook = tree.getroot()
    
    ## new a comic book object
    newComicBook = ComicBook()
    
    #<book title="AisazuNihaIrarenai">
    #   <character>
    #   <pages>
    #       <face>
    #       <frame>
    #       <text>
    #       <body>
    
    ## book tag
    #print(comicBook.tag)
    print("=====SYSTEM: get book title.=====")
    # book title
    newComicBook.bookName = comicBook.attrib["title"]
    print(newComicBook. bookName)
    
    print("=====SYSTEM: parse and translate character.=====")
    
    for characters in comicBook.iter('character'):
        newCaracterObj = {}
        newCaracterObj["id"] = characters.attrib["id"]
        ## translated name
        # need to translate to English
        translatedString = translator.translate(characters.attrib["name"])
        #print(translatedString.text)
        newCaracterObj["charaName"] = translatedString.text
        newComicBook.characters.append(newCaracterObj)
    print(json.dumps(newComicBook.characters, indent=4))
    print("===============================================")
    
    for pages in comicBook.iter('page'):
        
        ## see the content of one page
        # page = {}
        # index
        # overallWidth, overallHeight
        newPageObj = {}
        newPageObj["index"] = pages.attrib["index"]
        newPageObj["overallW"] = pages.attrib["width"]
        newPageObj["overallH"] = pages.attrib["height"]
        newPageObj["frames"] = []
        newPageObj["faces"] = []
        newPageObj["texts"] = []
        newPageObj["bodys"] = []
        
        for child in pages:
            
            ### here we can get text, face, body, frame
            #print(child.tag)
            #print("=====================")
            if child.tag == "frame":
                # <frame id="0000097c" xmin="480" ymin="700" xmax="746" ymax="1111"/>
                newFrameObj = {}
                newFrameObj["id"] = child.attrib["id"]
                newFrameObj["xmin"] = child.attrib["xmin"]
                newFrameObj["ymin"] = child.attrib["ymin"]
                newFrameObj["xmax"] = child.attrib["xmax"]
                newFrameObj["ymax"] = child.attrib["ymax"]
                
                newPageObj["frames"].append(newFrameObj)
                
            elif child.tag == "text":
                # <text id="0000097d" xmin="664" ymin="458" xmax="722" ymax="676">準備OK‼</text>
                
                #print(translatedString.text)
                newTextObj = {}
                
                translatedString = translator.translate(child.text)
                
                newTextObj["id"] = child.attrib["id"]
                newTextObj["xmin"] = child.attrib["xmin"]
                newTextObj["ymin"] = child.attrib["ymin"]
                newTextObj["xmax"] = child.attrib["xmax"]
                newTextObj["ymax"] = child.attrib["ymax"]
                newTextObj["text"] = translatedString.text
                
                newPageObj["texts"].append(newTextObj)
                
            elif child.tag == "face":
                # <face id="0000097a" xmin="1071" ymin="687" xmax="1112" ymax="719" character="0000097b"/>
                newFaceObj = {}
                newFaceObj["id"] = child.attrib["id"]
                newFaceObj["xmin"] = child.attrib["xmin"]
                newFaceObj["ymin"] = child.attrib["ymin"]
                newFaceObj["xmax"] = child.attrib["xmax"]
                newFaceObj["ymax"] = child.attrib["ymax"]
                newFaceObj["character"] = child.attrib["character"]   
                
                newPageObj["faces"].append(newFaceObj)
                          
            elif child.tag == "body":
                # <body id="0000097e" xmin="978" ymin="167" xmax="1198" ymax="496" character="0000097b"/>
                newBodyObj = {}
                newBodyObj["id"] = child.attrib["id"]
                newBodyObj["xmin"] = child.attrib["xmin"]
                newBodyObj["ymin"] = child.attrib["ymin"]
                newBodyObj["xmax"] = child.attrib["xmax"]
                newBodyObj["ymax"] = child.attrib["ymax"]
                newBodyObj["character"] = child.attrib["character"]   
                
                newPageObj["bodys"].append(newBodyObj)
                
            else:
                print("SYSTEM: new tag! "+str(child))
        
        #print(pages.attrib)

        newComicBook.pageList.append(newPageObj)
     
     
    #print(json.dumps(newComicBook.pageList, indent=4))
    
    json_file = open(str(newComicBook.bookName)+"_characters.json", "w")
    # magic happens here to make it pretty-printed
    json_file.write(json.dumps(newComicBook.characters, indent=4))
    json_file.close()   
    
    json_file = open(str(newComicBook.bookName)+"_pages.json", "w")
    # magic happens here to make it pretty-printed
    json_file.write(json.dumps(newComicBook.pageList, indent=4))
    json_file.close()   
        
    
        
        