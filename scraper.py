import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

# Définir le chemin d'accès absolu au dossier "data"
data_dir = os.path.abspath("data")

# Vérifier si le dossier "data" existe, sinon le créer
if not os.path.exists(data_dir):
    os.makedirs(data_dir)
    print('"data" directory created')

# Définir l'URL de la page ciblée
url = "https://www.zara.com/ej/en/preowned-resell/products/woman-l1/new-in--l154"

# Définir les options du driver Chrome
options = Options()
#options.add_argument("--headless")
#options.add_argument("--disable-gpu")

# Créer un driver Chrome
driver = webdriver.Chrome(options=options)

# Aller sur la page ciblée
driver.get(url)
print('Driver open')

# Attendre que l'élément "FILTERS" soit présent sur la page
wait = WebDriverWait(driver, 10)
print('Selecting filters')
filters_button = wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'FILTERS')]")))

# Cliquer sur l'élément "FILTERS"
filters_button.click()
print('Done in 3')
time.sleep(2)

# Attendre que l'élément "condition" soit présent sur la page
condition_button = wait.until(EC.presence_of_element_located((By.XPATH, "//button[.//span[contains(text(), 'condition')]]")))

# Cliquer sur l'élément "condition"
condition_button.click()
print('Done in 2')
time.sleep(2)

# Attendre que l'élément "NEW WITH TAGS" soit présent sur la page
new_with_tags_button = wait.until(EC.presence_of_element_located((By.XPATH, "//button[.//div[contains(text(), 'New with tags')]]")))

# Cliquer sur l'élément "NEW WITH TAGS"
new_with_tags_button.click()
print('Done in 1')
time.sleep(2)
print('Selection done')

# Faire défiler la page vers le bas 100 fois avec un délai de 5 secondes entre chaque défilement
count = 0
for i in range(100):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)
    count += 1
    print(f'Scrolling {count}')

# Sauvegarder la page web
with open(os.path.join(data_dir, "zara_resell_woman_newWithTags.html"), "w", encoding="utf-8") as f:
    f.write(driver.page_source)
    print('Page saved as "zara_resell_woman_newWithTags.html"')

# Fermer le driver
driver.quit()
print('Driver closed')

# Définir le DataFrame pour stocker les informations
result = pd.DataFrame(columns=["nom", "prix", "product_id", "etat", "marque"])

# Parser la page web et extraire les informations souhaitées
with open(os.path.join(data_dir, "zara_resell_woman_newWithTags.html"), "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f, "html.parser")
    print('Parsing')

# Trouver tous les éléments contenant les informations des articles
articles = soup.find_all("div", class_="generic-product-card")
print("Articles found :", len(articles))

# Parcourir chaque article et extraire les informations
for article in articles:
    nom_elem = article.find("p", class_="main-product-footer__detail__product-name-wrapper__name")
    prix_div = article.find("div", class_="main-product-footer__detail__product-price-wrapper")

    if nom_elem and prix_div:
        nom = nom_elem.text.strip()
        prix_elem = prix_div.find("p")

        if prix_elem:
            prix = prix_elem.text.strip()
            etat = "New with tags"
            marque = "Zara"

    # Créer un nouveau DataFrame avec les données à ajouter
    new_data = pd.DataFrame({"nom": [nom], "prix": [prix], "etat": [etat], "marque": [marque]})

    # Utiliser concat pour ajouter le nouveau DataFrame à la DataFrame existante
    result = pd.concat([result, new_data], ignore_index=True)

# Imprimer la taille du DataFrame pour vérifier s'il est vide
print("Articles in the DataFrame :", len(result))

# Vérifier si le DataFrame est vide, sinon exporter le DataFrame au format CSV dans le dossier "data"
if not result.empty:
    result.to_csv(os.path.join(data_dir, "articles.csv"), index=False)
    print('DataFrame successfully exported')
else:
    print("Empty Data Frame, export aborted")
