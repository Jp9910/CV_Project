#https://stackoverflow.com/questions/68191448/unknown-image-file-format-one-of-jpeg-png-gif-bmp-required
from pathlib import Path
import imghdr

champ = "lux"
data_dir = "C:\\Users\\JPC\\Documents\\ufs\\aprendizagem-de-maquina-profundo\\projeto\\scrapping\\images\\" + champ
image_extensions = [".jpg"]  # add all your images file extensions

img_type_accepted_by_tf = ["bmp", "gif", "jpeg", "png"]
for filepath in Path(data_dir).rglob("*"):
    if filepath.suffix.lower() in image_extensions:
        img_type = imghdr.what(filepath)
        if img_type is None:
            print(f"{filepath} is not an image")
        elif img_type not in img_type_accepted_by_tf:
            print(f"{filepath} is a {img_type}, not accepted by TensorFlow")