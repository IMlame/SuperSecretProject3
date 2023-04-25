import arcade
from PIL import Image

texture_map = {}


def scale(file: str, width: int, height: int) -> arcade.Texture:
    if file + str(width) + "x" + str(height) in texture_map:
        return texture_map[file + str(width) + "x" + str(height)]

    image = Image.open(file).convert('RGBA')
    image = image.resize((width, height), resample=Image.NEAREST)
    texture = arcade.Texture(name=file + str(width) + "x" + str(height), image=image)
    texture_map[file + str(width) + "x" + str(height)] = texture
    return texture
