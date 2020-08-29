from PIL import Image
from os import listdir
import time
from os.path import isfile, join
import os

source_directory = "/Tools"
onlyfiles = [f for f in listdir(source_directory) if isfile(join(source_directory, f))]

def crop_photo(photo):
    file = photo.split("/")[2]
    if ".png" not in photo:
        print(f"Skipping {photo}")
    else:  
        destination_directory = "/croppedphotos"
        destination_file_name = f"{destination_directory}/{file}"
        if os.path.isfile(destination_file_name):
            print(f"{photo} image already cropped...Moving on")
        else:
            print(f"Cropping {photo} to {destination_file_name}")
            im = Image.open(photo)
            box = (349, 2, 1017, 670 )
            cropped = im.crop(box)
            cropped.save(destination_file_name)

print(f"Getting ready to crop {len(onlyfiles)} files")
time.sleep(5)
for file in onlyfiles:
    crop_photo(F"{source_directory}/{file}")



