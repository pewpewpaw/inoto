import requests
from lib.lib import *
from colorama import *

init(autoreset=True)


while True:
    display_menu()
    
    choice = input("what's do you want to do ? : ")

    if choice == "1":
        domain = input("domain/ip :")
        scan(domain)
        
            
    elif choice == "2":
        adv = input("Do you wan't to search about cve with her details ? (Y/N)")
        if adv.lower() == "y":
            cve_id = input("aliases of the cve (format : CVE-XXXX-XXXX ): ")
            print(Back.RED + "Warning : the description of cve use the 3.1 version of cvss for better, more reliable result.")
            cve_details(cve_id.upper())
        
        elif adv.lower() == "n":
            cve_id = input("aliases of the cve (format : CVE-XXXX-XXXX ): ")
            cve_simple(cve_id.upper())

        else:
            print("please choose beetwen yes or no ")   

    elif choice == "3":
        top_article()

    elif choice == "4":
        pass
    
    elif choice == "5":
        services = input("service : ")
        version = input("version : ")
        scan_serv(services, version)
        
        
    
    else:
        print("choice beetewen 1 and 5")
