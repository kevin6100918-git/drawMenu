from datetime import datetime, timezone
from os import getenv
import random

import githubImageHandler



class randomImage:
    def __init__(self, imgList: list[tuple[str, str]]):
        self.imageList = imgList
        self.randomShuffle()
    
    def randomShuffle(self):
        random.shuffle(self.imageList)

    def get(self):
        return list(self.imageList)[0]

def random_get_menu_file(category: str=""):
    # get time now
    timenow = int(datetime.now(tz=timezone.utc).hour)+8
    # select meal
    if not category:
        if timenow < 11 or timenow >= 22:
            category = "breakfast"
        else:
            category = "dinner"
    # menuRandomPool = os.listdir(os.path.join("drawMenu", "menus", category))
    menuRandomPool = githubImageHandler.get_menu_list(category)

    return randomImage(menuRandomPool).get()

def draw_menu(category: str=""):
    if category == "早":
        menuFile =  random_get_menu_file(category="breakfast")
    
    elif category == "晚":
        menuFile =  random_get_menu_file(category="dinner")
    
    else:
        menuFile =  random_get_menu_file()
    
    # restaurantName = os.path.basename(menuFile).split(".")[0]
    restaurantName = menuFile[0].split(".")[0]

    return {
        "menuFile": menuFile[1],
        "restaurantName": restaurantName
    }

