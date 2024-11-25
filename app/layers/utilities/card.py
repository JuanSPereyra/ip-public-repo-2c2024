class Card:
    #Representa una tarjeta con información de un personaje.
    def __init__(self, url, name, status, last_location, first_seen, species, user=None, id=None):
        self.url = url
        self.name = name
        self.status = status
        self.last_location = last_location
        self.first_seen = first_seen
        self.species = species
  

        self.user = user
        self.id = id

    def __str__(self):
        #Devuelve una representación en cadena de la tarjeta.
        return f'IMG URL: {self.url}, name: {self.name}, status: {self.status}, última ubicación: {self.last_location}, primera vez visto: {self.first_seen}, estatus: {self.species}, Usuario: {self.user}, Id: {self.id}'
    
    # método equals.
    #Compara si dos tarjetas son iguales.
    def __eq__(self, other):
        if not isinstance(other, Card):
            return False
        return (self.url, self.name, self.status) == \
               (other.url, other.name, other.status)

    # método hashCode.
    #Devuelve el hash de la tarjeta.
    def __hash__(self):
        return hash((self.url, self.name, self.status))