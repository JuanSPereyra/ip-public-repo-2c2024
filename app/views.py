# capa de vista/presentación

from django.shortcuts import redirect, render
from app.layers.services.services import getAllImages
from django.contrib.auth.decorators import login_required #login
from django.contrib.auth import logout

def index_page(request):
    return render(request, 'index.html')

# los favoritos del usuario, y los usa para dibujar el correspondiente template.
# si el opcional de favoritos no está desarrollado, devuelve un listado vacío.
def home(request):
    images = getAllImages() #acá recibe imagenes API

    favourite_list = []

    return render(request, 'home.html', { 'images': images, 'favourite_list': favourite_list }) 

def search(request):
    search_msg = request.POST.get('query', '')

    # si el texto ingresado no es vacío, trae las imágenes y favoritos desde services.py,
    # y luego renderiza el template (similar a home).
    if (search_msg != ''):

        return redirect('buscar')
    else:
        return redirect('home')


# Estas funciones se usan cuando el usuario está logueado en la aplicación.
@login_required
def getAllFavouritesByUser(request):
    favourite_list = []
    return render(request, 'favourites.html', { 'favourite_list': favourite_list })

@login_required
def saveFavourite(request):
    pass

@login_required
def deleteFavourite(request):
    pass

@login_required
def exit(request):
    pass