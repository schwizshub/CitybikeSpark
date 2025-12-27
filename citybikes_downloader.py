# -*- coding: utf-8 -*-
import requests
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

try:
    from tqdm import tqdm
    HAS_TQDM = True
except ImportError:
    HAS_TQDM = False

class CityBikesDownloader:
    def __init__(self, base_path="c:\\Data\\Citybike\\"):
        self.base_path = base_path
        self.api_url = "http://api.citybik.es/v2"
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
                print(f"[OK] Repertoire verifie/cree : {directory}")
            except Exception as e:
                print(f"[ERREUR] Creation repertoire {directory}: {e}")
                sys.exit(1)
    
    def get_all_networks(self):
        """Récupère la liste de tous les réseaux"""
        try:
            print(f"Connexion a {self.api_url}/networks...")
            response = requests.get(f"{self.api_url}/networks", timeout=30)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"[ERREUR] Recuperation des reseaux: {e}")
            raise
    
    def get_network_details(self, network_id):
        """Récupère les détails d'un réseau spécifique"""
        try:
            response = requests.get(f"{self.api_url}/networks/{network_id}", timeout=30)
            response.raise_for_status()
            return response.json()
        except Exception as e:
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
            print(f"[OK] JSON sauvegarde : {json_path}")
            
            # Sauvegarder en Parquet pour Spark
            df = pd.json_normalize(networks['networks'])
            parquet_path = os.path.join(self.base_path, "networks", f"networks_{timestamp}.parquet")
            df.to_parquet(parquet_path, index=False)
            print(f"[OK] Parquet sauvegarde : {parquet_path}")
            
            print(f"[OK] {len(networks['networks'])} reseaux sauvegardes")
            return networks
            
        except Exception as e:
            print(f"[ERREUR] Sauvegarde des reseaux: {e}")
            raise
    
    def save_all_stations(self, networks_data):
        """Sauvegarde toutes les stations de tous les réseaux"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        all_stations = []
        
        networks_list = networks_data['networks']
        
        # Utiliser tqdm si disponible
        if HAS_TQDM:
            iterator = tqdm(networks_list, desc="Telechargement des reseaux", unit="reseau")
        else:
            iterator = networks_list
            total = len(networks_list)
        
        for idx, network in enumerate(iterator, 1):
            try:
                if not HAS_TQDM:
                    print(f"[{idx}/{total}] Telechargement: {network['name']}...")
                
                details = self.get_network_details(network['id'])
                
                if details and 'network' in details and 'stations' in details['network']:
                    for station in details['network']['stations']:
                        station['network_id'] = network['id']
                        station['network_name'] = network['name']
                        station['timestamp'] = timestamp
                        all_stations.append(station)
                    
            except Exception as e:
                if not HAS_TQDM:
                    print(f"[ERREUR] Pour {network['name']}: {e}")
                continue
        
        # Sauvegarder en Parquet
        if all_stations:
            df = pd.DataFrame(all_stations)
            parquet_path = os.path.join(self.base_path, "stations", f"stations_{timestamp}.parquet")
            df.to_parquet(parquet_path, index=False)
            print(f"[OK] {len(all_stations)} stations sauvegardees dans {parquet_path}")
            return df
        else:
            print("[ATTENTION] Aucune station a sauvegarder")
            return None
    
    def download_all(self):
        """Télécharge tout"""
        print("=" * 60)
        print("   CITYBIKES DATA DOWNLOADER")
        print("=" * 60)
        print(f"Repertoire de base : {self.base_path}")
        print(f"Date/Heure : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        
        try:
            networks = self.save_networks()
            stations_df = self.save_all_stations(networks)
            
            print("=" * 60)
            print("[SUCCESS] Telechargement termine avec succes!")
            print("=" * 60)
            return stations_df
            
        except Exception as e:
            print("=" * 60)
            print(f"[ERREUR] {e}")
            print("=" * 60)
            sys.exit(1)

if __name__ == "__main__":
    try:
        downloader = CityBikesDownloader()
        downloader.download_all()
    except KeyboardInterrupt:
        print("\n[ATTENTION] Telechargement interrompu par l'utilisateur")
        sys.exit(0)
    except Exception as e:
        print(f"\n[ERREUR FATALE] {e}")
        sys.exit(1)
