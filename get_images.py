import time
import os
import json

from selenium import webdriver
import requests

def get_images(search_term, limit, export_folder, headless=False):
    browser = webdriver.Firefox(executable_path=r'geckodriver/geckodriver')
    base_url = f"https://www.google.com/search?site=&tbm=isch&source=hp&biw=1873&bih=990&q={search_term}"
    target_urls = []

    # go to url
    browser.get(base_url)

    for _ in range(5):
        browser.execute_script("window.scrollBy(0,10000)")

    # find all images
    elements = browser.find_elements_by_class_name('rg_i')

    for cnt, e in enumerate(elements, start=0):
        print(cnt, limit, cnt > limit)
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

            target_urls.append(big_img.get_attribute("src"))

            # retrieve and save image
            try:
                reponse = requests.get(target_urls[cnt])
            except:
                continue

            if reponse.status_code == 200:
                os.makedirs(export_folder, exist_ok=True)
                export_path = os.path.join(export_folder, f"{search_term}{cnt}.jpg") 
                with open(export_path,"wb") as file:
                    file.write(reponse.content)

    return target_urls

items = get_images('codiaeum petra', 20, '/opt/pjs/data/')
