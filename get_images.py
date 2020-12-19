import time
import os
import json
import argparse

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import requests

def get_images(search_term, limit, export_folder, headless=False):
    ledger = {}
    options = Options()
    if headless == True:
        options.headless = True
    else:
        options.headless = False

    browser = webdriver.Firefox(options=options, executable_path=r'geckodriver/geckodriver')
    base_url = f"https://www.google.de/search?site=&tbm=isch&source=hp&biw=1873&bih=990&q={search_term}"

    # go to url
    browser.get(base_url)

    for _ in range(5):
        browser.execute_script("window.scrollBy(0,10000)")

    # find all images
    elements = browser.find_elements_by_class_name('rg_i')

    for cnt, e in enumerate(elements, start=0):
        if cnt < limit:
            # click image
            e.click()
            # content reload
            time.sleep(4)
            # select source image
            element = browser.find_elements_by_class_name('v4dQwb')

            if cnt == 0:
                big_img = element[0].find_element_by_class_name('n3VNCb')
            else:
               big_img = element[1].find_element_by_class_name('n3VNCb')

            # retrieve and save image
            try:
                src = big_img.get_attribute("src")
                reponse = requests.get(src)
            except:
                continue

            if reponse.status_code == 200:
                os.makedirs(os.path.join(export_folder, search_term), exist_ok=True)
                export_path = os.path.join(export_folder, search_term,  f"{search_term}{cnt}.jpg") 
                with open(export_path,"wb") as file:
                    file.write(reponse.content)

                ledger[src] = export_path
        else:
            break

        with open(os.path.join(export_folder, search_term, 'ledger.json'), 'w') as outfile:
            json.dump(ledger, outfile)

    return f'{search_term}: saved {len(ledger)} images to {export_folder}'

parser = argparse.ArgumentParser(description='xDescription of your program')
parser.add_argument('-c','--cat_file', help='path to categories', required=True)
parser.add_argument('-l','--limit', help='how many images should be scraped per category?', required=True)
parser.add_argument('-e','--export', help='export folder path', required=True)
parser.add_argument('--headless', help='should browser be headless?', required=False)
args = vars(parser.parse_args())

cat_file = args['cat_file']
with open(cat_file, 'r') as infile:
    cats = infile.read().splitlines()

limit = int(args['limit'])
export = args['export']
headless = False if args['headless'] == None else True

for cat in cats:
    result = get_images(cat, limit, export, headless)
    print(result)
