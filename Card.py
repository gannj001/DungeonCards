import random

import numpy as np
from PIL import Image, ImageFont, ImageDraw


class Card(object):
    def __init__(self):

        self.WALL_COLOUR = [153, 76, 0]
        self.FLOOR_COLOUR = [255, 255, 102]
        self.name = ""
        self.room_type = "Card"

        self.north = False
        self.south = False
        self.east = False
        self.west = False
        self.exit_count = random.choice([1,2,2,2,3])
        self.HEIGHT = 3.5
        self.WIDTH = 2.5
        self.CELL_HEIGHT = 0.25
        self.CELL_WIDTH = 0.25
        self.X_COUNT = int(self.WIDTH/self.CELL_WIDTH)
        self.Y_COUNT = int(self.HEIGHT/self.CELL_HEIGHT)
        self.grid = np.empty((self.Y_COUNT, self.X_COUNT, 3), dtype=np.uint8)
        self.room_height = random.choice([4,4, 4, 5,5, 6])
        self.room_width = random.choice([3, 4,4,4, 4, 5])
        self.corridor_width = random.choice([2,2,4])
        self.pixel_factor = 12
        self.image_array = None
        self.has_room = random.choice([True, False])

        self.build_default_grid()

    def print_info(self):
        print(f"X_COUNT: {self.X_COUNT}, Y_COUNT: {self.Y_COUNT}")
        print(f"N-{self.north} S-{self.south} E-{self.east} W-{self.west}")
        print(f"Grid: {self.grid.size}, H: {self.HEIGHT}, W: {self.WIDTH}")

    def build_default_grid(self):
        for x in self.grid:
            for y in x:
                y[0]=self.WALL_COLOUR[0]
                y[1]=self.WALL_COLOUR[1]
                y[2]=self.WALL_COLOUR[2]


    def generate_exits(self):
        dir_list = ["north", "south", "east", "west"]
        while not sum([self.north, self.south, self.east, self.west]) == self.exit_count:
            exit_dir = random.choice(dir_list)
            exec(f"self.{exit_dir}=True")

    def draw_exits(self):
        if self.south:
            for y in range(int(self.Y_COUNT/2)-1, self.Y_COUNT):
                for x in range(int(self.X_COUNT / 2 - self.corridor_width / 2),
                               int(self.X_COUNT / 2 + self.corridor_width / 2)):
                    self.grid[y][x] = self.FLOOR_COLOUR
        if self.north:
            for y in range(0, int(self.Y_COUNT/2)+1):
                for x in range(int(self.X_COUNT / 2 - self.corridor_width / 2),
                               int(self.X_COUNT / 2 + self.corridor_width / 2)):
                    self.grid[y][x] = self.FLOOR_COLOUR

        if self.west:
            for y in range(int(self.Y_COUNT / 2 - self.corridor_width / 2),
                           int(self.Y_COUNT / 2 + self.corridor_width / 2)):
               for x in range(0, int(self.X_COUNT / 2)+1):
                    self.grid[y][x] = self.FLOOR_COLOUR

        if self.east:
            for y in range(int(self.Y_COUNT / 2 - self.corridor_width / 2),
                           int(self.Y_COUNT / 2 + self.corridor_width / 2)):
                for x in range(int(self.X_COUNT/2)-1, self.X_COUNT):
                    self.grid[y][x] = self.FLOOR_COLOUR

    def build_room(self):
        self.draw_exits()
        if self.has_room:
            self.draw_room()

    def draw_room(self):
        startx = int((self.X_COUNT - self.room_width)/2)
        starty = int((self.Y_COUNT - self.room_height)/2)
        for y in range(starty, starty+self.room_height):
            for x in range(startx, startx+self.room_width):
                self.grid[y][x] = self.FLOOR_COLOUR

    def add_grid_lines(self):
        for x in range(len(self.image_array)):
            for y in range(len(self.image_array[x])):
                if x % self.pixel_factor == 0:
                    self.image_array[x][y] = [0, 0, 0]
                if y % self.pixel_factor == 0:
                    self.image_array[x][y] = [0, 0, 0]

    def add_name(self, img):
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype("Courier New Bold.ttf", 16)
        draw.text((0, 0), f"{self.name}\n{self.room_type[:4]}", (255, 255, 255), font)
        return img

    def render_image(self):
        small_img = Image.fromarray(self.grid, 'RGB')
        img = small_img.resize((self.X_COUNT*self.pixel_factor, self.Y_COUNT*self.pixel_factor))
        self.image_array = np.array(img)
        self.add_grid_lines()
        small_img.save("small.png")
        big_img = Image.fromarray(self.image_array, 'RGB')
        big_img = big_img.resize((big_img.width*2, big_img.height*2))
        big_img = self.add_name(big_img)
        return big_img


class Room(Card):
    def __init__(self):
        super().__init__()
        self.room_width = random.choice([x for x in range(6, 8)])
        self.room_height = random.choice([y for y in range(8, 12)])
        self.has_room = True
        self.room_type = "room"

        
class Corridor(Card):
    def __init__(self):
        super().__init__()
        self.room_type = "corridor"

    def generate_exits(self):
        north_south = random.choice([True, False])
        if north_south:
            self.north = True
            self.south = True
        else:
            self.west = True
            self.east = True


class Junction(Card):
    def __init__(self):
        super().__init__()
        self.exit_count = 3
        self.room_type = "junction"