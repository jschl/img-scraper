import time
import os
import json

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
    base_url = f"https://www.google.com/search?site=&tbm=isch&source=hp&biw=1873&bih=990&q={search_term}"

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
                os.makedirs(os.path.join(export_folder + search_term), exist_ok=True)
                export_path = os.path.join(export_folder, search_term,  f"{search_term}{cnt}.jpg") 
                with open(export_path,"wb") as file:
                    file.write(reponse.content)

                ledger[src] = export_path
        else:
            break

        with open(os.path.join(export_folder, 'ledger.json'), 'w') as outfile:
            json.dump(ledger, outfile)

    return f'saved {len(ledger)} images to {export_folder}'

items = get_images('codiaeum petra', 3, '/opt/pjs/data/train/', headless=True)
