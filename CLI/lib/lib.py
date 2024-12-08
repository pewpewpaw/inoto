import requests
from pathlib import Path
from tqdm import *
import json
import requests
from rich.table import Table
from rich.table import Text
from rich.console import Console
from datetime import *
from colorama import *
from nmap import *


init(autoreset=True)

  
def json_to_plain_text(data, indent=1):
    result = ""
    indent_space = " " * indent
    if isinstance(data, dict):
            for key, value in data.items():
                result += f"{indent_space}{key}:{json_to_plain_text(value, indent + 4)}\n"
    elif isinstance(data, list):
            for item in data:
                result = f"{json_to_plain_text(item, indent + 2).strip()}\n"
    else:
        result += f"{indent_space}{data}"
    return result


def display_menu():
    console = Console()

    title = Text("Hello to the Newsletter Automation", style="bold magenta")
    subtitle = Text("(Check the README page to see how to use it)", style="dim cyan")

    menu = Text()
    menu.append("1. ", style="bold yellow")
    menu.append("Scan for vulnerabilities", style="cyan")
    menu.append("\n2. ", style="bold yellow")
    menu.append("Search for CVE", style="cyan")
    menu.append("\n3. ", style="bold yellow")
    menu.append("10 latest news", style="cyan")
    menu.append("\n4. ", style="bold yellow")
    menu.append("Enable the long time mode", style="cyan")

    console.rule()
    console.print(title, justify="left")
    console.print(subtitle, justify="left")
    console.print("\n")
    console.print(menu, justify="left")
    console.rule()

def scan(domain):
    print("Scanning domain ....")
    out = input("output file (y or n) :")
    if out.lower() == "y":
        pass
    elif out.lower() == "n":
        pass
    else:
        print("choose beetwen y / n ")

def top_article():
    console = Console()
    liste = []
    
    response = requests.get("https://hacker-news.firebaseio.com/v0/topstories.json")
    if response.status_code == 200:
        top = response.json()
    else:
        console.print("[bold red]Error retrieving Hacker News data[/bold red]")
        return

    for tops in top[:10]:
        liste.append(tops)
    
    table = Table(title="Top Articles from Hacker News", show_lines=True)
    table.add_column("Type", style="cyan", justify="center")
    table.add_column("Title", style="green", justify="left")
    table.add_column("URL", style="magenta", justify="left")

    for id in liste:
        article = requests.get(f"https://hacker-news.firebaseio.com/v0/item/{id}.json")
        if article.status_code == 200:
            details = article.json()
            details_type = details.get("type", "N/A")
            details_title = details.get("title", "No Title")
            details_url = details.get("url", "No URL")
            table.add_row(details_type, details_title, details_url)
        else:
            console.print(f"[bold red]Error retrieving details for article ID {id}[/bold red]")

    console.print(table)

def cve_details(cve_id):
    url = f"https://services.nvd.nist.gov/rest/json/cves/2.0?cveId={cve_id}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if "vulnerabilities" in data and data["vulnerabilities"]:
            vulnerability = data["vulnerabilities"][0]["cve"]

            cve_name = vulnerability.get("cisaVulnerabilityName", "Indisponible")

            try:
                cve_score = vulnerability["metrics"]["cvssMetricV31"][0]["cvssData"]["baseScore"]
            except (KeyError, IndexError):
                cve_score = "Indisponible"

            published = vulnerability.get("published", "Indisponible")

            try:
                description = vulnerability["descriptions"][0]["value"]
            except (KeyError, IndexError):
                description = "Indisponible"

            try:
                metrics_vector = vulnerability["metrics"]["cvssMetricV31"][0]["cvssData"]["attackVector"]
            except (KeyError, IndexError):
                metrics_vector = "Indisponible"

            try:
                metrics_complexity = vulnerability["metrics"]["cvssMetricV31"][0]["cvssData"]["attackComplexity"]
            except (KeyError, IndexError):
                metrics_complexity = "Indisponible"

            try:
                metrics_userinteract = vulnerability["metrics"]["cvssMetricV31"][0]["cvssData"]["userInteraction"]
            except (KeyError, IndexError):
                metrics_userinteract = "Indisponible"

            try:
                metrics_exploitability = vulnerability["metrics"]["cvssMetricV31"][0]["exploitabilityScore"]
            except (KeyError, IndexError):
                metrics_exploitability = "Indisponible"
    
            
            console = Console()
            table = Table(title=f"Détails de la CVE : {cve_id}")

            table.add_column("Champ", style="cyan", no_wrap=True)
            table.add_column("Valeur", style="red")
            table.add_row("Nom de la vulnérabilité", cve_name)
            table.add_row("Score CVSS", str(cve_score))
            table.add_row("Date de publication", published)
            table.add_row("Description", description)
            table.add_row("Attack Vector", metrics_vector)
            table.add_row("Attack Complexity", metrics_complexity)
            table.add_row("User Interaction", metrics_userinteract)
            table.add_row("Exploitabilité", str(metrics_exploitability))
            console.print(table)

    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la requête: {e}")


def cve_simple(cve_id):
    url = f"https://services.nvd.nist.gov/rest/json/cves/2.0?cveId={cve_id}"
    try:
        response = requests.get(url, timeout=10) 
        response.raise_for_status() 
        data = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la requête: {e}")
        return
    except ValueError:
        print("Erreur : Réponse JSON invalide.")
        return

    try:
        if "vulnerabilities" in data and data["vulnerabilities"]:
            cve = data["vulnerabilities"][0]["cve"]

            cve_name = cve.get("cisaVulnerabilityName", "Indisponible")
            cve_score = (
                cve.get("metrics", {})
                .get("cvssMetricV31", [{}])[0]
                .get("cvssData", {})
                .get("baseScore", "Indisponible")
            )
            published = cve.get("published", "Indisponible")
            description = (
                cve.get("descriptions", [{}])[0].get("value", "Indisponible")
            )
            metrics_vector = (
                cve.get("metrics", {})
                .get("cvssMetricV31", [{}])[0]
                .get("cvssData", {})
                .get("attackVector", "Indisponible")
            )

            console = Console()
            table = Table(title=f"Détails de la CVE : {cve_id}")

            table.add_column("Champ", style="cyan", no_wrap=True)
            table.add_column("Valeur", style="red")

            table.add_row("Nom de la vulnérabilité", cve_name)
            table.add_row("Score CVSS", str(cve_score))
            table.add_row("Date de publication", published)
            table.add_row("Description", description)
            table.add_row("Attack Vector", metrics_vector)

            console.print(table)
        else:
            print("Erreur : Aucune vulnérabilité trouvée pour cet ID CVE.")

    except (KeyError, IndexError, TypeError) as e:
        print(f"Erreur lors de l'extraction des données : {e}")

def scan_serv(services, version):
    pass
    


if __name__ == "__main__":
    pass
