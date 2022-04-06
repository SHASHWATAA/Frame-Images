from PIL import Image, ImageOps, ImageDraw

Image.MAX_IMAGE_PIXELS = None
import sys
import os


def resize(image, resize_only_orientation, resize_only_border):
    h = Setup.picture_in_frame_size[resize_only_orientation][resize_only_border]["height"]
    w = Setup.picture_in_frame_size[resize_only_orientation][resize_only_border]["width"]

    # print("w", w, "h", h)
    initial_image = image
    iw, ih = initial_image.size
    ratio = ih * 1.0 / iw

    if ih > iw:
        # print("h")
        resize_h = h
        resize_w = round(resize_h / ratio)
        if resize_w < w:
            resize_w = w
            resize_h = round(resize_w * ratio)
    else:
        # print("w")
        resize_w = w
        resize_h = round(resize_w * ratio)
        if resize_h < h:
            resize_h = h
            resize_w = round(resize_h / ratio)
    #
    # resize_h = h
    # resize_w = w

    resized_image = initial_image.resize((resize_w, resize_h))
    # print("rw", resize_w, "rh", resize_h)
    return resized_image


def thin_black_border(im):
    border_width = 10
    draw = ImageDraw.Draw(im)
    draw.line([(0, 0), (0, im.height)], fill=(0, 0, 0), width=border_width)
    draw.line([(0, 0), (im.width, 0)], fill=(0, 0, 0), width=round(border_width))
    draw.line([(im.width, 0), (im.width, im.height)], fill=(0, 0, 0), width=border_width+2)
    draw.line([(0, im.height), (im.width, im.height)], fill=(0, 0, 0), width=round(border_width+5))

    # im.show()
    return im


def frame_images(frame_images_file_directory, frame_images_filename, frame_images_orientation, frame_images_border):
    image_path = frame_images_file_directory + frame_images_filename
    image = Image.open(image_path)
    image = resize(image, frame_images_orientation, frame_images_border)

    frame_path = Setup.frame_folder[frame_images_orientation][frame_images_border]
    for frame in Setup.frames:
        frame_image = Image.open(frame_path + Setup.frames[frame])
        
        if frame_images_file_directory == "/Users/shashwataryal/Documents/Python/Frame Image/Images/Portrait/White Non Bordered/" and frame == "unframed":
            frame_image = Image.open("/Users/shashwataryal/Documents/Python/Frame Image/Frame Templates/Portrait/Non Bordered/White Non Bordered.png")

        if frame_images_file_directory == "/Users/shashwataryal/Documents/Python/Frame Image/Images/Landscape/White Non Bordered/" and frame == "unframed":
            frame_image = Image.open("/Users/shashwataryal/Documents/Python/Frame Image/Frame Templates/Landscape/Non Bordered/White Non Bordered.png")

        if frame_images_file_directory == "/Users/shashwataryal/Documents/Python/Frame Image/Images/Square/White Non Bordered/" and frame == "unframed":
            print('asd')
            frame_image = Image.open("/Users/shashwataryal/Documents/Python/Frame Image/Frame Templates/Square/Non Bordered/White Non Bordered.png")


        # print(frame_image.height, frame_image.width)

        position_x = Setup.position[frame_images_orientation][frame_images_border]["position_x"]
        position_y = Setup.position[frame_images_orientation][frame_images_border]["position_y"]
        dx = 0
        dy = 0

        if image.width > Setup.picture_in_frame_size[frame_images_orientation][frame_images_border]["width"]:
            dx = (image.width - Setup.picture_in_frame_size[frame_images_orientation][frame_images_border]["width"]) / 2

        if image.height > Setup.picture_in_frame_size[frame_images_orientation][frame_images_border]["height"]:
            dy = (image.height - Setup.picture_in_frame_size[frame_images_orientation][frame_images_border][
                "height"]) / 2

        # print("dy", dy, "dx", dx)

        position_x = round(position_x - dx)
        position_y = round(position_y - dy)

        ##TLC inner white frame position
        position = (position_x, position_y)

        canvas = Image.new('RGB', (frame_image.width, frame_image.height), (255, 255, 255))
        canvas.paste(image, position)

        mask = Image.open(frame_path + 'Mask.png')

        im = Image.composite(frame_image, canvas, mask)

        im.save(frame + "_" + filename  )
        # im.show()


class Setup:
    frame_folder = {
        "Landscape": {
            "Bordered": "/Users/shashwataryal/Documents/Python/Frame Image/Frame Templates/Landscape/Bordered/",
            "Non Bordered": "/Users/shashwataryal/Documents/Python/Frame Image/Frame Templates/Landscape/Non Bordered/",
            "White Non Bordered": "/Users/shashwataryal/Documents/Python/Frame Image/Frame Templates/Landscape/Non Bordered/",
        },
        "Portrait": {
            "Bordered": "/Users/shashwataryal/Documents/Python/Frame Image/Frame Templates/Portrait/Bordered/",
            "Non Bordered": "/Users/shashwataryal/Documents/Python/Frame Image/Frame Templates/Portrait/Non Bordered/",
            "White Non Bordered": "/Users/shashwataryal/Documents/Python/Frame Image/Frame Templates/Portrait/Non Bordered/",
        },
        "Square": {
            "Bordered": "/Users/shashwataryal/Documents/Python/Frame Image/Frame Templates/Square/Bordered/",
            "Non Bordered": "/Users/shashwataryal/Documents/Python/Frame Image/Frame Templates/Square/Non Bordered/",
            "White Non Bordered": "/Users/shashwataryal/Documents/Python/Frame Image/Frame Templates/Square/Non Bordered/",
        }
    }

    images_folder = {
        "Landscape": {
            "Bordered": "/Users/shashwataryal/Documents/Python/Frame Image/Images/Landscape/Bordered/",
            "Non Bordered": "/Users/shashwataryal/Documents/Python/Frame Image/Images/Landscape/Non Bordered/",
            "White Non Bordered": "/Users/shashwataryal/Documents/Python/Frame Image/Images/Landscape/White Non Bordered/",
        },
        "Portrait": {
            "Bordered": "/Users/shashwataryal/Documents/Python/Frame Image/Images/Portrait/Bordered/",
            "Non Bordered": "/Users/shashwataryal/Documents/Python/Frame Image/Images/Portrait/Non Bordered/",
            "White Non Bordered": "/Users/shashwataryal/Documents/Python/Frame Image/Images/Portrait/White Non Bordered/",
        },
        "Square": {
            "Bordered": "/Users/shashwataryal/Documents/Python/Frame Image/Images/Square/Bordered/",
            "Non Bordered": "/Users/shashwataryal/Documents/Python/Frame Image/Images/Square/Non Bordered/",
            "White Non Bordered": "/Users/shashwataryal/Documents/Python/Frame Image/Images/Square/White Non Bordered/",
        }
    }

    frames = {
        "black": "Black.png",
        "white": "White.png",
        "natural": "Oak.png",
        # "gold": "Gold.png",
        "unframed": "Unframed.png"
    }

    position = {
        "Landscape": {
            "Bordered": {"position_x": 185, "position_y": 146}, 
            "Non Bordered": {"position_x": 107, "position_y": 73},
            "White Non Bordered": {"position_x": 107, "position_y": 73},
        },
        "Portrait": {
            "Bordered": {"position_x": 160, "position_y": 190},
            "Non Bordered": {"position_x": 79, "position_y": 99},
            "White Non Bordered": {"position_x": 79, "position_y": 99},
        },
        "Square": {
            "Bordered": {"position_x": 194, "position_y": 219},
            "Non Bordered": {"position_x": 110, "position_y": 136},
            "White Non Bordered": {"position_x": 110, "position_y": 136},
        }
    }

    picture_in_frame_size = {
        "Landscape": {
            "Bordered": {"height": 996, "width": 1526},
            "Non Bordered": {"height": 1155, "width": 1689},
            "White Non Bordered": {"height": 1155, "width": 1685},
        },
        "Portrait": {
            "Bordered": {"height": 1495, "width": 966},
            "Non Bordered": {"height": 1676, "width": 1141},
            "White Non Bordered": {"height": 1676, "width": 1141},
        },
        "Square": {
            "Bordered": {"height": 930, "width": 920},
            "Non Bordered": {"height": 1093, "width": 1091},
            "White Non Bordered": {"height": 1093, "width": 1091},
        }

    }


if __name__ == '__main__':

    for orientation in Setup.images_folder:
        for border in Setup.images_folder[orientation]:
            file_directory = Setup.images_folder[orientation][border]
            for filename in os.listdir(file_directory):
                if not (filename == ".DS_Store"):
                    frame_images(file_directory, filename, orientation, border)

    #
    # if frame == "all":
    #     for frame in bordered_frame_paths:
    #         frame_images(frame)
    # else:
    #     frame_images(frame)
