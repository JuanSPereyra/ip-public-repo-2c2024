# capa de vista/presentación

from django.shortcuts import redirect, render
from app.layers.services.services import Images, saveFavourite, getAllFavourites, deleteFavourite
from django.contrib.auth.decorators import login_required #login
from django.contrib.auth import logout #ya implementado
from django.core.paginator import Paginator #in-built paginador
#from app.layers.transport.transport import getAllImages
#from app.layers.utilities.translator import fromRequestIntoCard


def index_page(request):
    return render(request, 'index.html')

# esta función obtiene 2 listados que corresponden a las imágenes de la API y los favoritos del usuario, y los usa para dibujar el correspondiente template.
# si el opcional de favoritos no está desarrollado, devuelve un listado vacío.
def home(request, page=1):
    
    images = Images() #acá recibe imagenes de services, recibe lista

    paginator = Paginator (images, per_page=20)
    page_number = request.GET.get('page')
    page_object = paginator.get_page(page_number)
    
    favourite_list = []
    if request.user.is_authenticated:
        favourite_list = getAllFavourites(request) #devuelve objeto
    
 #   fromObjectToDicc = []
  #  for img in page_object:    
   #     fromObjectToDicc.append(fromRequestIntoCard(img)) #devuelve lista diccionario, asi se puede comparar

    # No tomaba como iguales los datos, asi que le sacamos el formato
    favourite_list_names = [fav.name.strip().lower() for fav in favourite_list]

    context = {
        'images': page_object,
        'favourite_list': favourite_list_names,  # Lista de nombres normalizados de favoritos
               }

    return render(request, 'home.html', context)

def search(request):
    search_msg = request.POST.get('query', '')
    
    #copio desde home
    favourite_list = []
  #  favourite_list = getAllFavourites(request)

   # favourite_list_names = [fav.name.strip().lower() for fav in favourite_list]
        
    if (search_msg != ''):
        images = Images(search_msg) #obtengo los jsons pasando parametro desde services.py
        return render(request, 'buscar.html', { 'images': images })
    #'favourite_list': favourite_list_names
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