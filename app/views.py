# capa de vista/presentación

from django.shortcuts import redirect, render
from app.layers.services.services import getAllImages, saveFavourite, getAllFavourites
from django.contrib.auth.decorators import login_required #login
from django.contrib.auth import logout #ya implementado
from django.core.paginator import Paginator #in-built paginador


def index_page(request):
    return render(request, 'index.html')

# esta función obtiene 2 listados que corresponden a las imágenes de la API y los favoritos del usuario, y los usa para dibujar el correspondiente template.
# si el opcional de favoritos no está desarrollado, devuelve un listado vacío.
def home(request, page=1):
    images = getAllImages() #acá recibe imagenes de services
    paginator = Paginator (images, per_page=20)
    page_number = request.GET.get('page')
    page_object = paginator.get_page(page_number)
    context = { 'images': page_object}

    favourite_list = []

    return render(request, 'home.html', context) 
# { 'favourite_list': favourite_list }

def search(request):
    search_msg = request.POST.get('query', '')
    favourite_list = [] #esto NO va acá

    if (search_msg != ''):
        images = getAllImages(search_msg) #obtengo los jsons pasando parametro desde services.py
        return render(request, 'buscar.html', { 'images': images, 'favourite_list': favourite_list })
    
    else:
        return redirect('home')


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
def deleteFavourite(request):
    pass

@login_required
def exit(request):
    logout(request)
    return redirect('login')