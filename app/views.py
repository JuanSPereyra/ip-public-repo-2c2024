# capa de vista/presentación

from django.shortcuts import redirect, render
from app.layers.services.services import Images, saveFavourite, getAllFavourites, deleteFavourite, obtener_info
from django.contrib.auth.decorators import login_required #login
from django.contrib.auth import logout #ya implementado
from django.core.paginator import Paginator #in-built paginador


def index_page(request):
    return render(request, 'index.html')

# esta función obtiene 2 listados que corresponden a las imágenes de la API y los favoritos del usuario, y los usa para dibujar el correspondiente template.
# si el opcional de favoritos no está desarrollado, devuelve un listado vacío.
def home(request):

    url = "https://rickandmortyapi.com/api/character"
    page_number = int(request.GET.get('page', 1))
    print(page_number)
    url += "?page=" + str(page_number)

    pages, next_url, prev_url = obtener_info(url)
    print(pages)
    print(next_url)
    print(prev_url)
    
    paginas = list(range(1, pages+1))
    
    images = Images(url) #acá recibe imagenes de services, recibe lista

#esto funciona dentro del paginador 3/7
#    paginator = Paginator (images, per_page=7)
#    page_number = request.GET.get('page')
#    print(page_number)
#    page_object = paginator.get_page(page_number)
#    print(page_object)
    
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
    search_msg = request.POST.get('query', '')
    
    #copio desde home
    favourite_list = []
    if request.user.is_authenticated:
        favourite_list = getAllFavourites(request) #devuelve objeto
    
    favourite_list_names = [fav.name.strip().lower() for fav in favourite_list]
        
    if (search_msg != ''):
        images = Images(search_msg) #obtengo los jsons pasando parametro desde services.py

        context = {
        'images': images,
        'favourite_list': favourite_list_names,  # Lista de nombres normalizados de favoritos
    }
        
        return render(request, 'buscar.html', context)

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
def deleteFavouriteView(request):
    deleteFavourite(request)
    return render(request, 'favourites-delete.html')

@login_required
def exit(request):
    logout(request)
    return render(request, 'exit.html')