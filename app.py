import random
import requests
import sys
from datetime import datetime
import holidays

API_KEY = 'kluczapi'
GEOCODE_URL = "https://api.openrouteservice.org/geocode/search"
ROUTE_URL = "https://api.openrouteservice.org/v2/directions/driving-car"

def get_random_city():
    with open('miasta.txt', 'r', encoding='utf-8') as file:
        cities = [line.strip() for line in file.readlines() if line.strip()]
    return random.choice(cities)

def get_coordinates(city):
    headers = {'Authorization': API_KEY}
    params = {'text': city, 'boundary.country': 'PL'}
    
    response = requests.get(GEOCODE_URL, headers=headers, params=params)
    
    if response.status_code == 200:
        data = response.json()
        if data['features']:
            lon, lat = data['features'][0]['geometry']['coordinates']
            return lon, lat
    print(f"Nie znaleziono współrzędnych dla miasta: {city}")
    return None

def dzienwolny(date):
    pl_holidays = holidays.Poland()
    return date.weekday() >= 5 or date in pl_holidays

def droga():
    random_city = get_random_city()
    start_coords = get_coordinates(random_city)
    end_coords = get_coordinates("Poznań")

    if not start_coords or not end_coords:
        print("Nie można pobrać współrzędnych miast.")
        return

    headers = {
        'Authorization': API_KEY,
        'Content-Type': 'application/json'
    }
    json_data = {
        'coordinates': [list(start_coords), list(end_coords)]
    }

    response = requests.post(ROUTE_URL, headers=headers, json=json_data)
    
    if response.status_code == 200:
        route_data = response.json()
        distance = (route_data['routes'][0]['summary']['distance'] / 1000) * 2  # w km, tam i z powrotem
        duration = (route_data['routes'][0]['summary']['duration'] / 60) * 2  # w minutach, tam i z powrotem
        print(f"Droga z {random_city} do Poznania i z powrotem:")
        print(f"Dystans: {distance:.2f} km")
        print(f"Czas przejazdu: {duration:.2f} minut, albo {duration / 60:.2f} godzin")
    else:
        print(f"Błąd API: {response.status_code} - {response.text}")

def main():
    if len(sys.argv) != 2:
        print("Użycie: python app.py <droga/data>")
        print("Dostępne funkcje: droga, data")
        return

    function = sys.argv[1]
    if function == 'droga':
        droga()
    elif function == 'data':
        date_str = input("Wpisz datę (YYYY-MM-DD): ")
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
        if dzienwolny(date):
            print(f"{date} to weekend lub święto.")
        else:
            print(f"{date} to dzień roboczy.")
    else:
        print("Nieznana funkcja. Użyj 'droga' lub 'data'.")

if __name__ == "__main__":
    main()