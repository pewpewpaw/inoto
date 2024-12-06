import requests
import os
import pathlib
import json
from bs4 import BeautifulSoup
import time
from tqdm import *
import json
import requests
from rich.table import Table
from rich.console import Console
from datetime import *
from colorama import *

init(autoreset=True)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
    }

def get_latest_cves():
    response = requests.get("https://cve.circl.lu/api/last/10")
    
    if response.status_code == 200:
        cves = response.json()
        console = Console()
        table = Table(show_lines=True)
        
        table.add_column("CVE ID", justify="left", width=20)
        table.add_column("Description", justify="center", width=50)
        table.add_column("Publié", justify="left", width=15)
        
        for cve in cves:
            cve_id = cve.get("id", "Aucun ID trouvé")
            aliases = cve.get("aliases", [])
            cve_alias = aliases[0] if aliases else "Aucun alias trouvé"
            description = cve.get("summary", "Aucune description disponible.")
            published_date = cve.get("published", "N/A")

            if published_date != "N/A":
                try:
                    published_date = datetime.strptime(published_date, "%Y-%m-%dT%H:%M:%SZ").strftime("%d-%m-%Y %H:%M:%S")
                except ValueError:
                    published_date = "Date invalide"
            
            table.add_row(cve_alias, description, published_date)
        
        console.print(table)
    else:
        print("Erreur lors de la récupération des CVEs.")


def news_single():
    print("system de scraping a faire")


#### recupere les 10 derniere articles site hacker news

def top_article():
    liste = []
    response = requests.get("https://hacker-news.firebaseio.com/v0/topstories.json")
    top = response.json()
    for tops in top[0:10]:
        liste.append(tops)
    print(liste)
    for id in liste[0:10]:
        article = requests.get(f"https://hacker-news.firebaseio.com/v0/item/{id}.json")
        details = article.json()
        details_type = json.dumps(details["type"], indent=6)
        details_url = json.dumps(details["url"], indent=6)
        details_title = json.dumps(details["title"], indent=6)
        print("----------------")
        print("type : ", details_type)
        print("url : ", details_url)
        print("title : ", details_title)
        print("----------------")






def cve_simple(name, version):
    url = f"https://vulners.com/api/v3/search/lucene/?query={name}+{version}"
    
    response = requests.get(url)
    
    if response.status_code == 200:
        vuln = response.json()
        
        if vuln.get("data", {}).get("search", []):
            print(Fore.RED +"Vulnérabilités détectées " f"pour \n service : {name} \n version : {version} (disponible plus tard)")
        else:
            print(Fore.GREEN + f"Aucune vulnérabilité trouvée pour {name} version {version}.")
    else:
        print(f"Erreur lors de la recherche. Code de statut: {response.status_code}. Assure-toi que les paramètres sont corrects.")

    
def cve_details(cve_id):
    response = requests.get(f"https://cve.circl.lu/api/cve/{cve_id}")
    if response.status_code == 200:
        details = response.json() 
        formatted_details = json.dumps(details, indent=6)
        print("Détails trouvés : ", formatted_details)
    else:
        print("CVE inexistante, assure-toi d'avoir mis le bon ID.")


def long_time(iterations=2000, delay=1):
    for i in range(iterations):
        print("Waiting" + "." * ((i % 10) + 1), end="\r") 
        time.sleep(delay)
    print("\nTask completed!")

def refresh(iterations=100, delay=0.05, unit="unit"):
    print("Long time mode activated")
    with tqdm(total=iterations, desc="Processing", unit=unit) as pbar:
        for _ in range(iterations): 
            time.sleep(delay) 
            pbar.update(1)  
    print("Task completed!")

def scan_vuln():
    print("scanner de vuln choisit")

        
if __name__ == "__main__":
    print("mauvais fichier lancé")
