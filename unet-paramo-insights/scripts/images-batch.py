
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
# Directorio donde están las imágenes
# URL de la API
URL =  const.BASE_URL + const.SPLIT_ENDPOINT

script_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(script_dir)

image_google_earth_path = get_path_module.make_path(
     parent_dir, const.DATA_DIR, const.EXTERNAL_DIR, const.GOOGLE_EARTH_DIR
)

# Lista de archivos en el directorio
files = os.listdir(image_google_earth_path)
tiff_files = [f for f in files if f.endswith(const.TIF_EXTENTION)]

for filename in tiff_files:
    # Ruta completa al archivo
    file_path = os.path.join(image_google_earth_path, filename)
    
    # Abrir el archivo en modo binario
    with open(file_path, 'rb') as f:
        # Crear el parámetro 'file'
        files = {'file': f}

        # Hacer la solicitud POST
        response = requests.post(URL, files=files, timeout=60)

        # Imprimir la respuesta
        print(response.text)
