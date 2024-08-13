from selenium import webdriver as opselenium
from selenium.webdriver.common.by import By

import pyautogui as waitTime
from flask import  Flask, jsonify
import pandas as pd

app = Flask(__name__)

@app.route('/')
def home():
    return  'API ON!'

@app.route('/components-kabum/<item>/', defaults={'param': None})
@app.route('/components-kabum/<item>/<param>')
def componentsKabum(item, param):
    browser = opselenium.Chrome()
    browser.maximize_window()

    # search_item_name_cpu_amd = "processadores/processador-amd"
    # search_item_name_cpu_intel = "processadores/processador-intel"
    # search_item_name = "placas-mae/placa-mae-intel"
    # search_item_name = "placas-mae/placa-mae-amd"
    # search_item_name_memoria = "memoria-ram/ddr-4"
    # search_item_name = "placa-de-video-vga/placa-de-video-amd"
    # search_item_name = "placa-de-video-vga/placa-de-video-nvidia"
    # search_item_name_fontes = "fontes"
    # search_item_name_ssd = "ssd-2-5"
    # search_item_name_hd = "disco-rigido-hd"

    if type(param) is not str:
        browser.get(f"https://www.kabum.com.br/hardware/{item}")
    else:
        browser.get(f"https://www.kabum.com.br/hardware/{item}/{param}")

    waitTime.sleep(1)

    browser.find_element(By.XPATH, '//*[@id="Filter"]/label/select').click()
    waitTime.sleep(1)

    browser.find_element(By.XPATH, '//*[@id="Filter"]/label/select/option[5]').click()
    waitTime.sleep(1)

    content_pages = browser.find_element(By.CLASS_NAME, 'pagination').text.split('\n')
    content_pages = content_pages[:-1]

    data_item_search = []

    n_max_pages = 1
    i = 1

    if len(content_pages) > 1:
        n_max_pages = content_pages[-1]

    while i <= int(n_max_pages):

        main_card = browser.find_element(By.TAG_NAME, 'main')
        card = main_card.find_elements(By.CLASS_NAME, 'productCard')

        print(f"{i}/{n_max_pages}")

        for item in card:
            try:
                nome = item.find_element(By.CLASS_NAME, 'nameCard').text
                preco = item.find_element(By.CLASS_NAME, 'priceCard').text
                url_item = item.find_element(By.TAG_NAME, 'a').get_attribute('href')
                link_img = item.find_element(By.TAG_NAME, 'img').get_attribute('srcset')

                data = {
                    'name': nome,
                    'price': preco,
                    'url': url_item,
                    'link': "https://www.kabum.com.br" + link_img
                }

                data_item_search.append(data)
            except Exception:
                pass

        try:
            i += 1
            browser.execute_script("""
                    var scrollHeight = document.body.scrollHeight;
                    var scrollPosition = scrollHeight * 0.77;
                    window.scrollTo(0, scrollPosition);
                """)
            waitTime.sleep(1)
            browser.find_element(By.CLASS_NAME, 'nextLink').click()
            print("Encontrou")
            waitTime.sleep(1)
        except Exception as e:
            pass
    else:
        print("DADOS COLETADOS COM SUCESSO!!")

    return jsonify(data_item_search)


# rodar a api
app.run(host='0.0.0.0')