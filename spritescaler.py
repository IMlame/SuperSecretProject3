import os
import random
import sys

import arcade
from PIL import Image

import shared_vars
texture_map = {}

image_list = ["bomb.png", "broccoli.png", "catgirl1.png", "catgirl2.png", "chicken.png", "drumstick.png",
              "dumbbell.png", "facts.png", "hypothetically.png", "jordan.png", "jordanrobe.png", "jordanrobeup.png",
              "jordanup.png", "logic.png", "pea.png", "peapod.png", "robe.png", "shapiro.png", "cabbage.png"]
APPLICATION_PATH = "" if "venv/bin" in os.path.dirname(sys.executable) else os.path.dirname(sys.executable) + "/"

def scale(file: str, width: int, height: int) -> arcade.Texture:
    if shared_vars.WACKY:
        random_file = random.randint(0, len(image_list)-1)
        file = APPLICATION_PATH + "assets/images/" + image_list[random_file]
    if file + str(width) + "x" + str(height) in texture_map:
        return texture_map[file + str(width) + "x" + str(height)]
    width = int(width)
    height = int(height)
    image = Image.open(file).convert('RGBA')
    image = image.resize((width, height), resample=Image.NEAREST)
    texture = arcade.Texture(name=file + str(width) + "x" + str(height), image=image)
    texture_map[file + str(width) + "x" + str(height)] = texture
    return texture
