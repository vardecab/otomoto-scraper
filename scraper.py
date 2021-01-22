# === libs ===

import requests # HTTP requests
from urllib.request import urlopen # open URLs
from bs4 import BeautifulSoup # BeautifulSoup; parsing HTML
import re # regex; extract substrings
from datetime import datetime # calculate script's run time
from alive_progress import alive_bar, show_spinners  # progress bar
import time # delay execution; https://stackoverflow.com/questions/3327775/can-the-execution-of-statements-in-python-be-delayed
from termcolor import colored # colored input/output in terminal
import webbrowser # open browser and download file 
from win10toast import ToastNotifier # Windows 10 notifications # TODO
import sys # exit()
from sys import platform # check platform (Windows/Linux/macOS)

# workaround for encoding error (https://stackoverflow.com/questions/33444740/unicodedecodeerror-charmap-codec-cant-encode-character-x-at-position-y-char)
# from colorama import init # colored input/output in terminal
# from typing import Counter

# === start + run time ===

print (colored("Starting...", 'green'))
start = datetime.now()  # run time

toaster = ToastNotifier() # initialize win10toast

# === URLs to scrape ===

page_url_p1 = "https://www.otomoto.pl/osobowe/tarnow/?search%5Bfilter_float_price%3Ato%5D=12000&search%5Bfilter_float_engine_power%3Afrom%5D=80&search%5Bfilter_enum_damaged%5D=0&search%5Bfilter_enum_no_accident%5D=1&search%5Border%5D=filter_float_engine_power%3Adesc&search%5Bbrand_program_id%5D%5B0%5D=&search%5Bdist%5D=90&search%5Bcountry%5D="
page_url_p2 = 'https://www.otomoto.pl/osobowe/tarnow/?search%5Bfilter_float_price%3Ato%5D=12000&search%5Bfilter_float_engine_power%3Afrom%5D=80&search%5Bfilter_enum_damaged%5D=0&search%5Bfilter_enum_no_accident%5D=1&search%5Border%5D=filter_float_engine_power%3Adesc&search%5Bbrand_program_id%5D%5B0%5D=&search%5Bdist%5D=90&search%5Bcountry%5D=&view=list&page=2'
page_url_p3 = 'https://www.otomoto.pl/osobowe/tarnow/?search%5Bfilter_float_price%3Ato%5D=12000&search%5Bfilter_float_engine_power%3Afrom%5D=80&search%5Bfilter_enum_damaged%5D=0&search%5Bfilter_enum_no_accident%5D=1&search%5Border%5D=filter_float_engine_power%3Adesc&search%5Bbrand_program_id%5D%5B0%5D=&search%5Bdist%5D=90&search%5Bcountry%5D=&view=list&page=3'
page_url_p4 = 'https://www.otomoto.pl/osobowe/tarnow/?search%5Bfilter_float_price%3Ato%5D=12000&search%5Bfilter_float_engine_power%3Afrom%5D=80&search%5Bfilter_enum_damaged%5D=0&search%5Bfilter_enum_no_accident%5D=1&search%5Border%5D=filter_float_engine_power%3Adesc&search%5Bbrand_program_id%5D%5B0%5D=&search%5Bdist%5D=90&search%5Bcountry%5D=&view=list&page=4'
# *params:
# price_max = 12k
# bezwypadkowy, nieuszkodzony
# >= 80 KM
# Tarnów + 90 km
# sorted desc by KM

# TODO:
# url_base = 'https://www.otomoto.pl/'
# url_category = osobowe
# url_city = tarnow
# url_city_distance =
# url_power =
# url_price = %5Bfilter_float_price%3Ato%5D=12000
# url_damaged =
# url_accident =
# url_sort =
# url_
# osobowe/tarnow/?search%5Bfilter_float_price%3Ato%5D=12000&search%5Bfilter_float_engine_power%3Afrom%5D=80&search%5Bfilter_enum_damaged%5D=0&search%5Bfilter_enum_no_accident%5D=1&search%5Border%5D=filter_float_engine_power%3Adesc&search%5Bbrand_program_id%5D%5B0%5D=&search%5Bdist%5D=90&search%5Bcountry%5D='

# === function to scrape data ===

def pullData(page_url):

    # ? can't crawl too often? works better with Otomoto limits perhaps
    # !FIX - uncomment on production
    # pause_duration = 3 # seconds to wait 
    # print ("Waiting for", pause_duration, "seconds before opening URL...")
    # with alive_bar(pause_duration, bar="circles", spinner="dots_waves") as bar:
    #     for second in range(0,pause_duration): 
    #         time.sleep(1)
    #         bar()

    print (colored("Opening page...", 'green')) # green output in terminal
    print (page_url) # 🐛 debug
    page = urlopen(page_url)
    
    print (colored("Scraping page...", 'green'))
    soup = BeautifulSoup(page, 'html.parser')  # parse the page
    
    # local_file = r"output/bs_output.txt"

    with open(r"output/bs_output.txt", "a", encoding="utf-8") as bs_output:
        print (colored("Creating local file to store URLs...", 'green'))
        counter = 0 # counter to get # of URLs/cars
        with alive_bar(bar="circles", spinner="dots_waves") as bar: # progress bar
            for link in soup.find_all("a", {"class": "offer-title__link"}):
                bs_output.write(link.get('href'))
                counter += 1 # counter ++ 
                bar() # progress bar ++ 
                # print ("Adding", counter, "URL to file...")
        print ("Successfully added", counter, "cars to file.")
        # print ("File with URLs successfully created.")

    return counter # so we can sum up all URLs/cars later on 

# === run URLs in function ^ ===

counter_p1 = pullData(page_url_p1) # run 1st URL and get back # of URLs/cars
# counter_p2 = pullData(page_url_p2) # run 2nd URL and get back # of URLs/cars
# counter_p3 = pullData(page_url_p3) # run 3rd URL and get back # of URLs/cars 
# counter_p4 = pullData(page_url_p4) # run 4th URL and get back # of URLs/cars
# counter_sum = counter_p1+counter_p2+counter_p3+counter_p4 # sum # of all URLs/cars in the file
# print ("Cars in total:", counter_sum)

# === make file more pretty by adding new lines ===

with open(r"output/bs_output.txt", "r", encoding="utf-8") as local_file:  # open file...
    print (colored("Reading file to clean up...", 'green'))
    read_local_file = local_file.read()  # ... and read it
urls_line_by_line = re.sub(r"#[a-zA-Z0-9]+(?!https$)://", "\n", read_local_file) 
urls_line_by_line = urls_line_by_line.replace("www", "https://www") 

# === remove duplicates ===

with open(r"output/urls_line_by_line.txt", "w", encoding="utf-8") as file_urls_line_by_line:
    print (colored("Cleaning the file...", 'green'))
    file_urls_line_by_line.write(urls_line_by_line)
    lines_seen = set() # holds lines already seen
    outfile = open(r"output/urls_line_by_line_no_dupes.txt", "w")
    for line in open(r"output/urls_line_by_line.txt", "r"):
        if line not in lines_seen: # not a duplicate
            outfile.write(line)
            lines_seen.add(line)
    outfile.close()
    print (colored("File cleaned up. New lines added.", 'green'))

# === tailor the results by using a keyword: brand, model (possibly also engine size etc) ===

regex_user_input = input("Jak chcesz zawęzić wyniki? Możesz wpisać markę (np. BMW) albo model (np. E39) >>> ") # for now using brand as quesion but user can put any one-word keyword
# TODO: better input handling ^
regex_user_input = regex_user_input.strip() # strip front & back
reg = re.compile(regex_user_input) # matches "KEYWORD" in lines
print ("Opening file to search for keyword:", regex_user_input)
counter2 = 0 # another counter to get the # of search results
with open(r'output/search-output.txt', 'w') as output: # open file for writing
    print (colored("Searching for keyword...", 'green'))
    with open(r'output/urls_line_by_line_no_dupes.txt', 'r', encoding='UTF-8') as no_dupes_file:
        with alive_bar(bar="circles", spinner="dots_waves") as bar:
            for line in no_dupes_file:  # read file line by line
                if reg.search(line):  # if there is a match anywhere in a line
                    output.write(line)  # write the line into the new file
                    counter2 += 1 # counter ++
                    bar() # progress bar ++ 
                    # print ("Progress:", counter2)
        # print (counter2, "results left from", counter_sum, "when looking for", regex_user_input) # !FIX: uncomment
        print (counter2, "results left from when looking for", regex_user_input) # !FIX: remove
        print ("Found", counter2, "results.") # !FIX: which one to choose? 

# === open search results in browser ===

if counter2 != 0:
    user_choice_open_urls = input("Chcesz otworzyć linki w przeglądarce? [y/n] >>> ")   
    if user_choice_open_urls == 'y':
        with open(r'output/search-output.txt', 'r', encoding='UTF-8') as search_results:
            counter3 = 0
            print ("Opening URLs in browser...")
            with alive_bar(bar="circles", spinner="dots_waves") as bar:
                for line in search_results: # go through the file
                    webbrowser.open(line) # open URL in browser
                    counter3 += 1
                    bar()
        if counter3 != 1: # correct grammar for multiple (URLs; them; they)
            print ("Opened", counter3, "URLs in the browser. Go and check them before they go 404 ;)") 
            if platform == "win32":
                toaster.show_toast("otomoto-scraper", "Opened URLs",  icon_path="icons/www.ico", duration=3)
        else: # correct grammar for 1 (URL; it)
            print ("Opened", counter3, "URL in the browser. Go and check it before it goes 404 ;)") 
            if platform == "win32":
                toaster.show_toast("otomoto-scraper", "Opened URL",  icon_path="icons/www.ico", duration=3)
    else:
        print ("Script run time:", datetime.now()-start)
        sys.exit("Ok - URLs saved in 'output/search-output.txt' anyway.")
else:
    print ("No search results found.")

# === run time ===

print ("Script run time:", datetime.now()-start)