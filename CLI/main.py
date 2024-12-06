import requests
from lib.lib import *
from colorama import *

init(autoreset=True)

get_latest_cves()

print("""
      
      hello to the newsletter automatisation ( check the readme page to see how to use it)
      
      
      1. See the news about cyber (single url).
      2. Search for CVE.
      3. 10 latest news.
      4. Enable the long time mode.
      5. scan for vulnerabilities.
      
      """)

while True:
    choice = input("what's do you want to do ? : ")

    if choice == "1":
        news_single()
        
            
    elif choice == "2":
        adv = input("Do you wan't to search about cve with her details or scan about service version ? (CVE/SERV)")
        if adv.lower() == "cve":
            cve_id = input("aliases of the cve (format : CVE-XXXX-XXXX ): ")
            cve_details(cve_id)
        
        elif adv.lower() == "serv":
            service = input("service : ")
            version = input ("version : ")
            cve_simple(service, version)

        else:
            print("please choose beetwen cve or serv ")   

    elif choice == "3":
        top_article()

    elif choice == "4":
        long_time()
        
    elif choice == "5":
        scan_vuln()
    
    else:
        print("choisit entre 1 et 5")
