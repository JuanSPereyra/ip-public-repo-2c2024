# capa de vista/presentación

from django.shortcuts import redirect, render
from app.layers.services.services import personaje_azar, Images, saveFavourite, getAllFavourites, deleteFavourite, obtener_info
from django.contrib.auth.decorators import login_required #login
from django.contrib.auth import logout #ya implementado

from .config import config

def index_page(request):
    return surprise_character(request)

# esta función obtiene 2 listados que corresponden a las imágenes de la API y los favoritos del usuario, y los usa para dibujar el correspondiente template.
# si el opcional de favoritos no está desarrollado, devuelve un listado vacío.
def home(request):

    url = config.DEFAULT_REST_API_URL

    page_number = int(request.GET.get('page', 1))
    url += str(page_number)

    pages, next_url, prev_url = obtener_info(url) #llamo a funcion de services
    
    paginas = list(range(1, pages+1))
    
    images = Images(url) #acá recibe imagenes de services, recibe lista
    
    favourite_list = []
    if request.user.is_authenticated:
        favourite_list = getAllFavourites(request) #devuelve objeto
    
    favourite_list_names = [fav.name.strip().lower() for fav in favourite_list]

    context = {
        'images': images,
        'favourite_list': favourite_list_names,  # Lista de nombres normalizados de favoritos
        'next_url': next_url,
        'prev_url': prev_url,
        'page_number': page_number,
        'pages': pages,
        'paginas': paginas
    }

    return render(request, 'home.html', context)

def search(request):
    search_msg = request.GET.get('name', '')

    if not search_msg:
        search_msg = request.POST.get('query', '')

    #copio desde home
    favourite_list = []
    if request.user.is_authenticated:
        favourite_list = getAllFavourites(request) #devuelve objeto
    
    favourite_list_names = [fav.name.strip().lower() for fav in favourite_list]

    if (search_msg != ''):

        page_number = int(request.GET.get('page', 1))

        url = config.DEFAULT_REST_API_URL + str(page_number) + "&name=" + str(search_msg)

        images = Images(url, search_msg) #obtengo los jsons pasando parametro desde services.py


        pages, next_url, prev_url = obtener_info(url) #llamo a funcion de services

        if pages != None:
            paginas = list(range(1, pages+1))
        else:
            paginas = 0

        context = {
            'images': images,
            'favourite_list': favourite_list_names,  # Lista de nombres normalizados de favoritos
            'next_url': next_url,
            'prev_url': prev_url,
            'page_number': page_number,
            'pages': pages,
            'paginas': paginas,
            'search_msg': search_msg
        }
        
        return render(request, 'buscar.html', context)

    else:
        return redirect('home')

def surprise_character(request):
    winner = personaje_azar()
    favourite_list = []
    if request.user.is_authenticated:
        favourite_list = getAllFavourites(request) #devuelve objeto
    
    favourite_list_names = [fav.name.strip().lower() for fav in favourite_list]

    context = {
        'winner': winner,
        'favourite_list': favourite_list_names,  # Lista de nombres normalizados de favoritos
        }   

    return render(request, 'index.html', context)

# Estas funciones se usan cuando el usuario está logueado en la aplicación.

@login_required
def getAllFavouritesByUser(request):
    favourite_list = getAllFavourites(request) #trae lista de services
    
    return render(request, 'favourites.html', { 'favourite_list': favourite_list })

@login_required
def saveFavouriteView(request):
    saveFavourite(request) #services
    return render(request, 'favourites-add.html')


@login_required
def deleteFavouriteView(request):
    deleteFavourite(request)
    return render(request, 'favourites-delete.html')

@login_required
def exit(request):
    logout(request)
    return render(request, 'exit.html')