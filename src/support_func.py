from geopy.geocoders import Nominatim
import time 
import dotenv
from tqdm import tqdm
import requests
import os
import pandas as pd
import seaborn as sns
import os
from geopy.geocoders import OpenCage



def get_coords(location_list, token):
    """
    Obtiene las coordenadas geográficas (latitud y longitud) de una lista de ubicaciones.

    Parámetros:
    ----------
    location_list : list
        Lista de ubicaciones en formato de texto (por ejemplo, nombres de ciudades o direcciones).

    Retorno:
    -------
    pandas.DataFrame
        Un DataFrame con las columnas "Nombre", "Latitud" y "Longitud", donde "Nombre" es el nombre normalizado
        de la ubicación, y "Latitud" y "Longitud" corresponden a las coordenadas geográficas de cada ubicación.
    """
    loc_dict = dict()
    names = []
    lat = []
    long = []

    geolocator = OpenCage(api_key=token)
    
    for loc in tqdm(location_list):
        loc_get = geolocator.geocode(loc)
        names.append(loc_get.raw["components"]["_normalized_city"])
        lat.append(loc_get.latitude)
        long.append(loc_get.longitude)
    loc_dict["Nombre"] = names
    loc_dict["Latitud"] = lat
    loc_dict["Longitud"] = long
    return pd.DataFrame(loc_dict)

def look_for(latlong, category, radius, nres, sort):
    """
    Realiza una búsqueda de lugares usando la API de Foursquare.

    Parámetros:
    ----------
    latlong : str
        Coordenadas geográficas en formato "latitud,longitud" (por ejemplo, "40.730610,-73.935242").
    category : str
        Categoría del lugar que se desea buscar (por ejemplo, "restaurant", "park", etc.).
    radius : int
        Radio de búsqueda en metros a partir de las coordenadas proporcionadas.
    nres : int
        Número máximo de resultados a devolver.
    sort : str
        Método de ordenamiento de los resultados (por ejemplo, "distance", "relevance").

    Retorno:
    -------
    dict
        Un diccionario con los resultados de la búsqueda en formato JSON.
    """
    url = f"https://api.foursquare.com/v3/places/search?ll={latlong}&radius={radius}&categories={category}&sort={sort.upper()}&limit={nres}"
    headers = {
    "Accept": "application/json",
    "Authorization": os.getenv("token2")
    }
    response = requests.request("GET", url, headers=headers)
    return response.json()