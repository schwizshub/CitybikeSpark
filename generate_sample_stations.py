# -*- coding: utf-8 -*-
import json
import os
import sys
from datetime import datetime
import pandas as pd

# Forcer l'encodage UTF-8 pour Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

def generate_sample_stations():
    """Génère 10 stations d'exemple réalistes"""
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base_path = "c:\\Data\\Citybike\\"
    
    # Données d'exemple basées sur de vrais réseaux
    sample_stations = [
        {
            "id": "velib-001",
            "name": "Gare du Nord - Paris",
            "latitude": 48.8809,
            "longitude": 2.3553,
            "free_bikes": 12,
            "empty_slots": 8,
            "timestamp": timestamp,
            "network_id": "velib-metropole",
            "network_name": "Velib' Metropole",
            "extra": json.dumps({
                "uid": "16107",
                "address": "RUE DE DUNKERQUE - 75010 PARIS",
                "banking": True,
                "bonus": False,
                "status": "OPEN"
            })
        },
        {
            "id": "velib-002",
            "name": "Tour Eiffel - Paris",
            "latitude": 48.8584,
            "longitude": 2.2945,
            "free_bikes": 5,
            "empty_slots": 15,
            "timestamp": timestamp,
            "network_id": "velib-metropole",
            "network_name": "Velib' Metropole",
            "extra": json.dumps({
                "uid": "7020",
                "address": "QUAI BRANLY - 75007 PARIS",
                "banking": True,
                "bonus": True,
                "status": "OPEN"
            })
        },
        {
            "id": "bicing-001",
            "name": "Plaça Catalunya - Barcelona",
            "latitude": 41.3851,
            "longitude": 2.1734,
            "free_bikes": 8,
            "empty_slots": 12,
            "timestamp": timestamp,
            "network_id": "bicing",
            "network_name": "Bicing",
            "extra": json.dumps({
                "uid": "1",
                "slots": 20,
                "status": "OPN",
                "online": True
            })
        },
        {
            "id": "bicing-002",
            "name": "Sagrada Familia - Barcelona",
            "latitude": 41.4036,
            "longitude": 2.1744,
            "free_bikes": 3,
            "empty_slots": 17,
            "timestamp": timestamp,
            "network_id": "bicing",
            "network_name": "Bicing",
            "extra": json.dumps({
                "uid": "405",
                "slots": 20,
                "status": "OPN",
                "online": True
            })
        },
        {
            "id": "citibike-001",
            "name": "Times Square - New York",
            "latitude": 40.7580,
            "longitude": -73.9855,
            "free_bikes": 15,
            "empty_slots": 25,
            "timestamp": timestamp,
            "network_id": "citi-bike-nyc",
            "network_name": "Citi Bike NYC",
            "extra": json.dumps({
                "uid": "3457",
                "slots": 40,
                "renting": True,
                "returning": True,
                "installed": True
            })
        },
        {
            "id": "citibike-002",
            "name": "Central Park South - New York",
            "latitude": 40.7665,
            "longitude": -73.9765,
            "free_bikes": 7,
            "empty_slots": 13,
            "timestamp": timestamp,
            "network_id": "citi-bike-nyc",
            "network_name": "Citi Bike NYC",
            "extra": json.dumps({
                "uid": "3242",
                "slots": 20,
                "renting": True,
                "returning": True,
                "installed": True
            })
        },
        {
            "id": "bixi-001",
            "name": "Place d'Armes - Montreal",
            "latitude": 45.5045,
            "longitude": -73.5546,
            "free_bikes": 10,
            "empty_slots": 15,
            "timestamp": timestamp,
            "network_id": "bixi-montreal",
            "network_name": "Bixi Montreal",
            "extra": json.dumps({
                "uid": "1",
                "slots": 25,
                "is_charging_station": False,
                "status": "IN_SERVICE"
            })
        },
        {
            "id": "dublinbikes-001",
            "name": "O'Connell Street - Dublin",
            "latitude": 53.3498,
            "longitude": -6.2603,
            "free_bikes": 6,
            "empty_slots": 14,
            "timestamp": timestamp,
            "network_id": "dublinbikes",
            "network_name": "Dublin Bikes",
            "extra": json.dumps({
                "uid": "42",
                "bike_stands": 20,
                "status": "OPEN",
                "banking": True
            })
        },
        {
            "id": "santander-001",
            "name": "Hyde Park Corner - London",
            "latitude": 51.5027,
            "longitude": -0.1527,
            "free_bikes": 9,
            "empty_slots": 11,
            "timestamp": timestamp,
            "network_id": "santander-cycles",
            "network_name": "Santander Cycles",
            "extra": json.dumps({
                "uid": "1",
                "installDate": "1278947280000",
                "installed": True,
                "locked": False,
                "terminalName": "001023"
            })
        },
        {
            "id": "ecobici-001",
            "name": "Zocalo - Mexico City",
            "latitude": 19.4326,
            "longitude": -99.1332,
            "free_bikes": 4,
            "empty_slots": 16,
            "timestamp": timestamp,
            "network_id": "ecobici",
            "network_name": "EcoBici",
            "extra": json.dumps({
                "uid": "1",
                "slots": 20,
                "status": "ACTIVE",
                "districtCode": "06"
            })
        }
    ]
    
    print("=" * 60)
    print("   GENERATEUR DE STATIONS D'EXEMPLE")
    print("=" * 60)
    print(f"Generation de {len(sample_stations)} stations...")
    
    # Créer le DataFrame
    df = pd.DataFrame(sample_stations)
    
    # Sauvegarder en Parquet
    stations_path = os.path.join(base_path, "stations")
    os.makedirs(stations_path, exist_ok=True)
    
    parquet_file = os.path.join(stations_path, f"stations_{timestamp}.parquet")
    df.to_parquet(parquet_file, index=False)
    print(f"[OK] Parquet sauvegarde : {parquet_file}")
    
    # Sauvegarder en JSON
    json_file = os.path.join(stations_path, f"stations_{timestamp}.json")
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(sample_stations, f, indent=2, ensure_ascii=False)
    print(f"[OK] JSON sauvegarde : {json_file}")
    
    # Afficher un résumé
    print("=" * 60)
    print("RESUME DES DONNEES GENEREES")
    print("=" * 60)
    print(f"Nombre total de stations : {len(sample_stations)}")
    print(f"Nombre de reseaux : {df['network_id'].nunique()}")
    print("\nReseaux inclus :")
    for network in df['network_name'].unique():
        count = len(df[df['network_name'] == network])
        print(f"  - {network} : {count} stations")
    
    print("\nVilles representees :")
    cities = ["Paris", "Barcelona", "New York", "Montreal", "Dublin", "London", "Mexico City"]
    for city in cities:
        print(f"  - {city}")
    
    print("\nStatistiques :")
    print(f"  Total velos disponibles : {df['free_bikes'].sum()}")
    print(f"  Total emplacements vides : {df['empty_slots'].sum()}")
    print(f"  Moyenne velos/station : {df['free_bikes'].mean():.1f}")
    
    print("=" * 60)
    print("[SUCCESS] Donnees d'exemple generees avec succes!")
    print("=" * 60)
    
    return df

if __name__ == "__main__":
    try:
        generate_sample_stations()
    except Exception as e:
        print(f"[ERREUR] {e}")
        sys.exit(1)
