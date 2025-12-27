import requests
import json
import os
import sys
from datetime import datetime
import pandas as pd

class CityBikesDownloader:
    def __init__(self, base_path="c:\\Data\\Citybike\\"):
        self.base_path = base_path
        self.api_url = "http://api.citybik.es/v2"
        
        # Vérifier et créer les répertoires
        self._setup_directories()
        
    def _setup_directories(self):
        """Crée tous les répertoires nécessaires"""
        dirs = [
            self.base_path,
            os.path.join(self.base_path, "networks"),
            os.path.join(self.base_path, "stations"),
            os.path.join(self.base_path, "analysis"),
            os.path.join(self.base_path, "logs")
        ]
        
        for directory in dirs:
            try:
                os.makedirs(directory, exist_ok=True)
                print(f"✓ Répertoire vérifié/créé : {directory}")
            except Exception as e:
                print(f"✗ Erreur création répertoire {directory}: {e}")
                sys.exit(1)
    
    def get_all_networks(self):
        """Récupère la liste de tous les réseaux"""
        try:
            print(f"Connexion à {self.api_url}/networks...")
            response = requests.get(f"{self.api_url}/networks", timeout=30)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"✗ Erreur lors de la récupération des réseaux: {e}")
            raise
    
    def get_network_details(self, network_id):
        """Récupère les détails d'un réseau spécifique"""
        try:
            response = requests.get(f"{self.api_url}/networks/{network_id}", timeout=30)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"✗ Erreur pour le réseau {network_id}: {e}")
            return None
    
    def save_networks(self):
        """Sauvegarde tous les réseaux"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        try:
            networks = self.get_all_networks()
            
            # Sauvegarder en JSON
            json_path = os.path.join(self.base_path, "networks", f"networks_{timestamp}.json")
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(networks, f, indent=2, ensure_ascii=False)
            print(f"✓ JSON sauvegardé : {json_path}")
            
            # Sauvegarder en Parquet pour Spark
            df = pd.json_normalize(networks['networks'])
            parquet_path = os.path.join(self.base_path, "networks", f"networks_{timestamp}.parquet")
            df.to_parquet(parquet_path, index=False)
            print(f"✓ Parquet sauvegardé : {parquet_path}")
            
            print(f"✓ {len(networks['networks'])} réseaux sauvegardés")
            return networks
            
        except Exception as e:
            print(f"✗ Erreur lors de la sauvegarde des réseaux: {e}")
            raise
    
    def save_all_stations(self, networks_data):
        """Sauvegarde toutes les stations de tous les réseaux"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        all_stations = []
        
        total_networks = len(networks_data['networks'])
        
        for idx, network in enumerate(networks_data['networks'], 1):
            try:
                print(f"[{idx}/{total_networks}] Téléchargement: {network['name']}...")
                details = self.get_network_details(network['id'])
                
                if details and 'network' in details and 'stations' in details['network']:
                    for station in details['network']['stations']:
                        station['network_id'] = network['id']
                        station['network_name'] = network['name']
                        station['timestamp'] = timestamp
                        all_stations.append(station)
                    
            except Exception as e:
                print(f"✗ Erreur pour {network['name']}: {e}")
                continue
        
        # Sauvegarder en Parquet
        if all_stations:
            df = pd.DataFrame(all_stations)
            parquet_path = os.path.join(self.base_path, "stations", f"stations_{timestamp}.parquet")
            df.to_parquet(parquet_path, index=False)
            print(f"✓ {len(all_stations)} stations sauvegardées dans {parquet_path}")
            return df
        else:
            print("⚠ Aucune station à sauvegarder")
            return None
    
    def download_all(self):
        """Télécharge tout"""
        print("=" * 60)
        print("   CITYBIKES DATA DOWNLOADER")
        print("=" * 60)
        print(f"Répertoire de base : {self.base_path}")
        print(f"Date/Heure : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        
        try:
            networks = self.save_networks()
            stations_df = self.save_all_stations(networks)
            
            print("=" * 60)
            print("✓ Téléchargement terminé avec succès!")
            print("=" * 60)
            return stations_df
            
        except Exception as e:
            print("=" * 60)
            print(f"✗ ERREUR : {e}")
            print("=" * 60)
            sys.exit(1)

# Point d'entrée principal
if __name__ == "__main__":
    try:
        downloader = CityBikesDownloader()
        downloader.download_all()
    except KeyboardInterrupt:
        print("\n⚠ Téléchargement interrompu par l'utilisateur")
        sys.exit(0)
    except Exception as e:
        print(f"\n✗ ERREUR FATALE : {e}")
        sys.exit(1)
