
"""
This module contains a script that reads all .tif files in the current directory,
makes a POST request to an API for each file, and then prints the response.
"""
import os
import requests
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
# pylint: disable=wrong-import-position
import config.constants as const
import packages.utils.get_path as get_path_module


# URL de la API
URL =  const.BASE_URL + const.PREDICT_ENDPOINT

script_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(script_dir)

all_images_path = get_path_module.make_path(
    parent_dir, const.DATA_DIR, const.OUTPUT_DIR, const.IMAGES_DIR
)


tif_files = []
for dirpath, dirnames, filenames in os.walk(all_images_path):
    for filename in filenames:
        if filename.endswith(const.TIF_EXTENTION):
            tif_files.append(os.path.join(dirpath, filename))

for filename in tif_files:
    # Ruta completa al archivo
    file_path = os.path.join(filename)

    # Abrir el archivo en modo binario
    with open(file_path, 'rb') as f:
        # Crear el parámetro 'file'
        files = {'file': f}

        # Hacer la solicitud POST
        response = requests.post(URL, files=files, timeout=60)

        # Imprimir la respuesta
        print(response.text)
