# capa de servicio/lógica de negocio

from ..persistence import repositories
from ..utilities.translator import fromRepositoryIntoCard, fromRequestIntoCard, fromTemplateIntoCard
from django.contrib.auth import get_user
from app.layers.transport.transport import getAllImages
from app.layers.utilities.card import Card

from django.http import HttpRequest
def get_user(request: HttpRequest):
    return request.user

def searchImages(input=None):
    # obtiene un listado de datos "crudos" desde la API, usando a transport.py.
    json_collection = getAllImages() #datos crudos usando transport.py
    # recorre cada dato crudo de la colección anterior, lo convierte en una Card y lo agrega a images.
    images = []
    for item in json_collection:
        if input.lower()==json_collection['name'].lower():
            images.append(item)    

    return images

# añadir favoritos (usado desde el template 'home.html')
def saveFavourite(request):
    fav = fromTemplateIntoCard(request) # transformamos un request del template en una Card.
    fav.user = get_user(request) # le asignamos el usuario correspondiente.

    return repositories.saveFavourite(fav) # lo guardamos en la base.

# usados desde el template 'favourites.html'
def getAllFavourites(request):
    if not request.user.is_authenticated:
        return []
    else:
        user = get_user(request)

        favourite_list = repositories.getAllFavourites(user) # buscamos desde el repositories.py TODOS los favoritos del usuario (variable 'user').
        mapped_favourites = []

        for favourite in favourite_list:
            card = '' # transformamos cada favorito en una Card, y lo almacenamos en card.
            mapped_favourites.append(card)

        return mapped_favourites

def deleteFavourite(request):
    favId = request.POST.get('id')
    return repositories.deleteFavourite(favId) # borramos un favorito por su ID.