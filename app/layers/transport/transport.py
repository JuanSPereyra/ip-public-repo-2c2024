# capa de transporte/comunicación con otras interfaces o sistemas externos.
#COMPLETO COMPLETO COMPLETO
import requests
from ...config import config

def getCountInfo(url):
    response = requests.get(url)
    datos = response.json()
    id_max = datos['info']['count']

    return id_max

def winner_information(url):
    response = requests.get(url)
    info = response.json() 

    return info

def getAllInfo(url , input=None):
    if input is None:
        json_info = requests.get(url).json()
    else:
        json_info = requests.get(config.DEFAULT_REST_API_SEARCH + str(input)).json()

    if 'error' in json_info:
        print("[transport.py]: la búsqueda no arrojó resultados.")
        return None
    
    return json_info['info']

# comunicación con la REST API.
# este método se encarga de "pegarle" a la API y traer una lista de objetos JSON crudos (raw).
def getAllImages(url, input=None):
    if input is None:
        json_response = requests.get(url).json()
    else:
        json_response = requests.get(url).json()

    json_collection = []

    # si la búsqueda no arroja resultados, entonces retornamos una lista vacía de elementos.
    if 'error' in json_response:
        print("[transport.py]: la búsqueda no arrojó resultados.")
        return json_collection

    for object in json_response['results']:
        try:
            if 'image' in object:  # verificar si la clave 'image' está presente en el objeto (sin 'image' NO nos sirve, ya que no mostrará las imágenes).
                json_collection.append(object)
            else:
                print("[transport.py]: se encontró un objeto sin clave 'image', omitiendo...")

        except KeyError: 
            # puede ocurrir que no todos los objetos tenga la info. completa, en ese caso descartamos dicho objeto y seguimos con el siguiente en la próxima iteración.
            pass

    return json_collection