import sys
import os
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time
import random
import re

# # default settings
# start_page = 1 # default start scraping page
# num_pages = 10 # default number of scraped pages
# city = ""

# # you can pass the input in the command line. ie. the start page number
# if (len(sys.argv) == 1):
#     city = input("please specify the city: ") # prompt user to specify the city to crawl
#     start_page = int(input("please specify the page to start: ") ) # able to set custom start page, this is useful when the scraper stops halfway
#     num_pages = int(input("please specify how many pages to scrape: ") )

def scrape(city: str, start_page: int, num_pages: int):
    # Import the webdriver
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

    # visit tripvisor and search for the input city, get the designated url
    main_url = "https://www.tripadvisor.com/"
    driver.get(main_url)
    search_term = city + " restaurants" 
    driver.find_element(By.CSS_SELECTOR, ".EcFTp .R0").send_keys(search_term + Keys.ENTER) # find the input box, key in the search term, and hit enter
    time.sleep(8) # let the page to load
    get_url = driver.current_url
    print("The current url is: "+str(get_url))

    # Iterate through the pagingnation, and get all listing links
    listings = []
    for i in range(0, num_pages):

        page = start_page + i
        oa_number = (page - 1) * 30

        url_split = re.split("-", get_url, 3)
        url = url_split[0] + "-" + url_split[1] + "-oa" + str(oa_number) + "-" + url_split[2] + "#EATERY_LIST_CONTENTS"
        driver.get(url)

        # wait some time for the page to load and to prevent triggering website anticrawl mechanism
        time.sleep(random.randint(3,5))

        # get all listing links for that page
        elements = driver.find_elements(By.CLASS_NAME, "Lwqic")

        for element in elements:
            listings.append(element.get_attribute("href"))
        
    # sampling every 30th listing in the queue
    print(listings[0::30])

    # find the working directory
    # create output directory if not existed
    # set path to file to store data
    current_wd = os.getcwd()
    output = "output"
    output_wd = os.path.join(current_wd, output)
    isExist = os.path.exists(output_wd)
    if not isExist:
        os.mkdir(output_wd)     
    path_to_file = output_wd  + "/" + city + ".csv"

    # Open the file to save the output
    # for windows, use "w", newline ="" parameters to eliminate the empty line inbetween each record
    csvFile = open(path_to_file, 'w', newline='', encoding="utf-8")
    csvWriter = csv.writer(csvFile)

    # Iterate through each listing and crawl contact data
    for j in range(0, len(listings)):

        listing_url = listings[j]
        driver.get(listing_url)

        print(j , " ", listing_url)

        # wait some time for the page to load and to prevent triggering website anticrawl mechanism
        time.sleep(random.randint(2,5))    

        # get all data needed for that page
        # try/except method is used to catch ElementNotFound Error when some listing doesnt have email or contact number
        try:
            title = driver.find_element(By.CLASS_NAME, "HjBfq").text
        except:
            title = "NA"

        try:    
            website = driver.find_element(By.CSS_SELECTOR, ".sNsFa .FPPgD").get_attribute("href")
        except:
            website = "NA"

        try: 
            email = driver.find_element(By.CSS_SELECTOR, ".sNsFa+ .sNsFa a").get_attribute("href")
        except:
            email = "NA"  

        try: 
            phone = driver.find_element(By.CSS_SELECTOR, ".f+ .f a").get_attribute("href")
        except:
            phone = "NA" 

        csvWriter.writerow([title, website, email, phone]) 


    driver.close()
