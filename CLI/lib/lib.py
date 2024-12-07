import requests
import pathlib
import json
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
    menu.append("\n5. ", style="bold yellow")
    menu.append("Perform services scan", style="cyan")

    console.rule()
    console.print(title, justify="left")
    console.print(subtitle, justify="left")
    console.print("\n")
    console.print(menu, justify="left")
    console.rule()

def scan(domain):
    print("Scanning domain ....")
    out = input("output file (y or n) :")
    if out == "y":
        pass
    else:
        pass

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

def service_vuln(name, version):
    url = f"https://vulners.com/api/v3/search/lucene/?query={name}+{version}"
    
    response = requests.get(url)
    
    if response.status_code == 200:
        vuln = response.json()
        
        if vuln.get("data", {}).get("search", []):
            print(Fore.RED +"Vulnerabilities detected " f"for \n service : {name} \n version : {version} (available later)")
        else:
            print(Fore.GREEN + f"No vulnerabilities found for {name} version {version}.")
    else:
        print(f"Error during search. Status code: {response.status_code}. Make sure the parameters are correct.")

def cve_details(cve_id):
    url = f"https://services.nvd.nist.gov/rest/json/cves/2.0?cveId={cve_id}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if "vulnerabilities" in data and data["vulnerabilities"]:
            cve_name = data["vulnerabilities"][0]["cve"]["cisaVulnerabilityName"]
            cve_score = data["vulnerabilities"][0]["cve"]["metrics"]["cvssMetricV31"][0]["cvssData"]["baseScore"]
            published = data["vulnerabilities"][0]["cve"]["published"]
            description = data["vulnerabilities"][0]["cve"]["descriptions"][0]["value"]
            metrics_vector = data["vulnerabilities"][0]["cve"]["metrics"]["cvssMetricV31"][0]["cvssData"]["attackVector"]
            metrics_complexity = data["vulnerabilities"][0]["cve"]["metrics"]["cvssMetricV31"][0]["cvssData"]["attackComplexity"]
            metrics_userinteract = data["vulnerabilities"][0]["cve"]["metrics"]["cvssMetricV31"][0]["cvssData"]["userInteraction"]
            metrics_exploitability = data["vulnerabilities"][0]["cve"]["metrics"]["cvssMetricV31"][0]["exploitabilityScore"]
            
            
            console = Console()
            table = Table(title=f"Détails de la CVE : {cve_id}")

            table.add_column("Champ", style="cyan", no_wrap=True)
            table.add_column("Valeur", style="magenta")
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
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if "vulnerabilities" in data and data["vulnerabilities"]:
            cve_name = data["vulnerabilities"][0]["cve"].get("cisaVulnerabilityName", "N/A")
            cve_score = data["vulnerabilities"][0]["cve"]["metrics"]["cvssMetricV31"][0]["cvssData"].get("baseScore", "N/A")
            published = data["vulnerabilities"][0]["cve"].get("published", "N/A")
            description = data["vulnerabilities"][0]["cve"]["descriptions"][0].get("value", "N/A")
            metrics_vector = data["vulnerabilities"][0]["cve"]["metrics"]["cvssMetricV31"][0]["cvssData"].get("attackVector", "N/A")

            console = Console()
            table = Table(title=f"Détails de la CVE : {cve_id}")

            table.add_column("Champ", style="cyan", no_wrap=True)
            table.add_column("Valeur", style="magenta")

            table.add_row("Nom de la vulnérabilité", cve_name)
            table.add_row("Score CVSS", str(cve_score))
            table.add_row("Date de publication", published)
            table.add_row("Description", description)
            table.add_row("Attack Vector", metrics_vector)

            console.print(table)

    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la requête: {e}")


def long_time():
    print("Long time mode activated")

if __name__ == "__main__":
    cve_details("CVE-2010-3333")
