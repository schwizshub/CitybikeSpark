import requests
import json
import os
from datetime import datetime
import pandas as pd

class CityBikesDownloader:
    def __init__(self, base_path="c:\\Data\\Citybike\\"):
        self.base_path = base_path
        self.api_url = "http://api.citybik.es/v2"
        
        # Créer les répertoires si nécessaire
        os.makedirs(base_path, exist_ok=True)
        os.makedirs(os.path.join(base_path, "networks"), exist_ok=True)
        os.makedirs(os.path.join(base_path, "stations"), exist_ok=True)
        
    def get_all_networks(self):
        """Récupère la liste de tous les réseaux"""
        response = requests.get(f"{self.api_url}/networks")
        return response.json()
    
    def get_network_details(self, network_id):
        """Récupère les détails d'un réseau spécifique"""
        response = requests.get(f"{self.api_url}/networks/{network_id}")
        return response.json()
    
    def save_networks(self):
        """Sauvegarde tous les réseaux"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        networks = self.get_all_networks()
        
        # Sauvegarder en JSON
        json_path = os.path.join(self.base_path, "networks", f"networks_{timestamp}.json")
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(networks, f, indent=2)
        
        # Sauvegarder en Parquet pour Spark
        df = pd.json_normalize(networks['networks'])
        parquet_path = os.path.join(self.base_path, "networks", f"networks_{timestamp}.parquet")
        df.to_parquet(parquet_path, index=False)
        
        print(f"✓ {len(networks['networks'])} réseaux sauvegardés")
        return networks
    
    def save_all_stations(self, networks_data):
        """Sauvegarde toutes les stations de tous les réseaux"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        all_stations = []
        
        for network in networks_data['networks']:
            try:
                print(f"Téléchargement: {network['name']}...")
                details = self.get_network_details(network['id'])
                
                for station in details['network']['stations']:
                    station['network_id'] = network['id']
                    station['network_name'] = network['name']
                    station['timestamp'] = timestamp
                    all_stations.append(station)
                    
            except Exception as e:
                print(f"✗ Erreur pour {network['name']}: {e}")
        
        # Sauvegarder en Parquet
        df = pd.DataFrame(all_stations)
        parquet_path = os.path.join(self.base_path, "stations", f"stations_{timestamp}.parquet")
        df.to_parquet(parquet_path, index=False)
        
        print(f"✓ {len(all_stations)} stations sauvegardées")
        return df
    
    def download_all(self):
        """Télécharge tout"""
        print("=== Début du téléchargement CityBikes ===")
        networks = self.save_networks()
        stations_df = self.save_all_stations(networks)
        print("=== Téléchargement terminé ===")
        return stations_df

# Utilisation
if __name__ == "__main__":
    downloader = CityBikesDownloader()
    downloader.download_all()
``_
