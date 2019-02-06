import os

from Card import *


def test():
    j = Corridor()
    j.generate_exits()
    j.name = "X#"
    j.build_room()
    j.print_info()
    img = j.render_image()

    img.save("sample.png")

def main():
    empty_folder()
    print("Old Files Deleted...")
    alpha = "abcdefghijklmnopqrstuvwxyz"
    num = "123456789"
    object_list = [Corridor(), Room(), Room(), Room(), Room(), Junction(), Junction()]
    for letter in alpha:
        for numeral in num:
            r = random.choice(object_list)
            r.name = f"{letter}{numeral}".upper()
            r.generate_exits()
            r.build_room()
            img = r.render_image()
            img.save(f"./first_deck/{r.name}_{r.room_type}.png")
    print("Done")

def empty_folder():
    for f in os.listdir("./first_deck"):
        file_path = os.path.join("./first_deck", f)
        os.unlink(file_path)


main()
