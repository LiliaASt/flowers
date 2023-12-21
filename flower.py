import os
import requests
import shutil
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

def creating_folder(name: str) -> None:
    if not os.path.isdir(name):
        os.mkdir(name)
        print("The folder has been created")
    else:
        print("The folder already exists")

def getting_links(query:str, quantity:int) -> None:
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    time.sleep(2)
    url = f"https://yandex.ru/images/search?text={query}"
    driver.get(url=url)
    time.sleep(2)
    driver.maximize_window()
    time.sleep(8)
    view_all_button = driver.find_element(By.CSS_SELECTOR, "a.Link.SimpleImage-Cover")
    view_all_button.click()

    with open(f"{query}.txt", "w") as file:
        for link in range(quantity):
            try:
                time.sleep(1)
                link = driver.find_element(By.CSS_SELECTOR, "a.Button2_view_action").get_attribute("href")
                file.write(link + "\n")
                driver.find_element(By.CSS_SELECTOR, "div.CircleButton:nth-child(4)").click()
            except:
                continue
    driver.close()
    driver.quit()
    print("The files are ready")

def download_images(query:str) -> None:

    img_count=0

    creating_folder("dataset")
    creating_folder(os.path.join("dataset", f"{query}"))

    with open(f"{query}.txt", "r") as file:
        for line in file:
            try:
                url = line.strip()
                time.sleep(4)
                response = requests.get(url, stream=True)
                if response.status_code == 200:
                    img_count += 1
                    with open(os.path.join("dataset", f"{query}", f"{str(img_count).zfill(4)}.jpg"), "wb") as image_file:
                        shutil.copyfileobj(response.raw, image_file)
                else:
                    continue
            except:
                continue
    print(f'{img_count} images downloaded')

def main() -> None:
    if os.path.isdir("dataset"):
        shutil.rmtree("dataset")

    query = "rose"
    getting_links(query , 3)
    download_images(query)
    time.sleep(4)

    query  = "tulip"
    getting_links(query , 3)
    download_images(query)
