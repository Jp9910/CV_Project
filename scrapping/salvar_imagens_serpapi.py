import requests
from serpapi import GoogleSearch
import env
import os
from random import random
from pathlib import Path
import imghdr

# Script para salvar imagens do google usando o serpapi (https://serpapi.com/images-results)

class API:
    def __init__(self):
        self.path_artigos = "./artigos"
        self.URL = 'https://serpapi.com/search.json'

    def imageSearch(self, query):
        params = {
            "q": query,
            "engine": "google_images",
            "ijn": "0",
            "api_key": env.key
        }
        search = GoogleSearch(params)
        results = search.get_dict()
        return results

api = API()
champ = "kindred"
complemento_busca = 1
complementos_busca = ["pinterest" , "deviantart" , "drawing" , "digital drawing", "art", "fanart", "line art", "gartic"]
query = "league of legends " + champ + " " + complementos_busca[complemento_busca]
split_train_test = False

image_extensions = [".jpg", ".png"]  # add all your images file extensions
img_type_accepted_by_tf = ["bmp", "gif", "jpeg", "png"]

result = api.imageSearch(query=query)

path = os.path.dirname(__file__)
dir = f'{path}\\images\\{champ}'
if not os.path.exists(dir):
    os.makedirs(dir)
    num_img = 0
else:
    num_img = len(os.listdir(dir))
iTrain=0
iTest=0

# Iterar os resultados imagens (100 resultados)
for x in result["images_results"]:
    img_url = x["original"] # Link para a imagem

    if (split_train_test):
        if random() > 0.3: # Aproximadamente 70 e 30 para treino-validação
            iTrain+=1
            num_img = iTrain
            dir = f'{path}\\images\\train\\{champ}'
        else:
            iTest+=1
            num_img = iTest
            dir = f'{path}\\images\\test\\{champ}'
    else:
        num_img+=1

    if not os.path.exists(dir):
        os.makedirs(dir)

    # (https://stackoverflow.com/questions/30229231/python-save-image-from-url)
    try:
        img_data = requests.get(img_url).content # Pegar conteúdo da imagem
    except:
        continue

    arq = f'{dir}\\{num_img}.png'
    with open(arq, 'wb') as handler:
        handler.write(img_data) # Salvar localmente
        handler.close()

    # Check if its a valid image
    filepath = Path(arq)
    if filepath.suffix.lower() in image_extensions:
        img_type = imghdr.what(filepath)
        if img_type is None:
            print(f"{filepath} is not an image")
            os.remove(arq)
        elif img_type not in img_type_accepted_by_tf:
            print(f"{filepath} is a {img_type}, not accepted by TensorFlow")
            os.remove(arq)

# Reordenar arquivos
from renomear_arquivos import renomear
path = os.path.dirname(__file__)
dir = Path(f'{path}\\images\\{champ}')
renomear(dir)