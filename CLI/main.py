import requests
from lib.lib import *

get_latest_cves()

print("""
      
      hello to the newsletter automatisation ( check the readme page to see how to use it)
      
      
      1. See the news about cyber (single url).
      2. Search for CVE.
      3. Add new site.
      4. Enable the long time mode.
      
      """)

while True:
    choice = input("what's do you want to do ? : ")

    if choice == "1":
        url = input("url : ")
        print(scrape(url))
        
            
    elif choice == "2":
        adv = input("Do you wan't to search about cve with her details ? (Y/N)")
        if adv.lower() == "y":
            print("{ cve } with details ")
        
        elif adv.lower() == "n":
            print(" { cve } without details ")

        else:
            print("please choose beetwen yes or no ")   

    elif choice == "3":
        url = input("enter the site that you want to add (with http/https): ")
        if requests.get(url).status_code == 200:
            print('valid website')
        else:
            print("it's not a valid website")

    elif choice == "4":
        long_time()