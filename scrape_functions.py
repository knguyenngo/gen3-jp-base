from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
import pandas as pd
import json
import time

# Scrape smogon url for move list
def scrape_moves(url):
    # Set options for Firefox to run in background
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")

    driver = webdriver.Firefox(options=options)
    try:
        # Go to url
        driver.get(url)

        # Expand window size to capture all dynamically generated elements
        driver.set_window_size(1920, 13500)
        time.sleep(5)

        moves = driver.find_elements(By.CLASS_NAME, "MoveRow")
        move_list = []

        # Extract move data
        for move in moves:
            name = move.find_element(By.CSS_SELECTOR, "div.MoveRow-name").text
            move_type = move.find_element(By.CSS_SELECTOR, "div.MoveRow-type").text
            damage_type = move.find_element(By.CSS_SELECTOR, "div.damage-category-block").get_attribute("class").split()[-1]
            move_power = move.find_element(By.CSS_SELECTOR, "div.MoveRow-power > span").text
            move_accuracy = move.find_element(By.CSS_SELECTOR, "div.MoveRow-accuracy > span").text
            move_pp = move.find_element(By.CSS_SELECTOR, "div.MoveRow-pp > span").text
            move_desc = move.find_element(By.CSS_SELECTOR, "div.MoveRow-description").text
 
            # Create move dictionary
            move = {
                'name': name,
                'type': move_type,
                'damage_type': damage_type,
                'power': move_power,
                'accuracy': move_accuracy,
                'pp': move_pp,
                'description': move_desc 
            }

            # Add move to list
            move_list.append(move)
    finally:
        driver.quit()

        df = pd.DataFrame(move_list)
        return df # Return dataframe

# Scrape smogon url for pokemon data
def scrape_pokemon(url):
    # Set options for Firefox to run in background
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")

    driver = webdriver.Firefox(options=options)
    try:
        # Go to url
        driver.get(url)

        # Expand window size to capture all dynamically generated elements
        driver.set_window_size(1920, 14800)
        time.sleep(5)

        pokemons = driver.find_elements(By.CLASS_NAME, "PokemonAltRow")
        pokemon_list = []

        # Extract pokemon data
        for mon in pokemons:
            name = mon.find_element(By.CSS_SELECTOR, "div.PokemonAltRow-name").text
            type_list = mon.find_element(By.CSS_SELECTOR, "div.PokemonAltRow-types").text.splitlines()
            ability_list = mon.find_elements(By.CLASS_NAME, "AbilityList")
            base_hp = mon.find_element(By.CSS_SELECTOR, "div.PokemonAltRow-hp").text.split("\n")[1]
            base_atk = mon.find_element(By.CSS_SELECTOR, "div.PokemonAltRow-atk").text.split("\n")[1]
            base_def = mon.find_element(By.CSS_SELECTOR, "div.PokemonAltRow-def").text.split("\n")[1]
            base_spa = mon.find_element(By.CSS_SELECTOR, "div.PokemonAltRow-spa").text.split("\n")[1]
            base_spd = mon.find_element(By.CSS_SELECTOR, "div.PokemonAltRow-spd").text.split("\n")[1]
            base_spe = mon.find_element(By.CSS_SELECTOR, "div.PokemonAltRow-spe").text.split("\n")[1]
            
            # Check for multiple typings
            if len(type_list) == 1:
                type_list = type_list[0]

            # Check for multiple abilities
            if len(ability_list) > 1 and ability_list[1].text != "":
                ability_list = [ability_list[0].text, ability_list[1].text]
            else:
                ability_list = ability_list[0].text

            # Create pokemon dictionary
            pokemon = {
                'name': name,
                'type': type_list,
                'ability': ability_list,
                'hp': base_hp,
                'attack': base_atk,
                'defense': base_def,
                'special_attack': base_spa,
                'special_defense': base_spd,
                'speed': base_spe
            }

            # Add pokemon to list
            pokemon_list.append(pokemon)
    finally:
        driver.quit()

        df = pd.DataFrame(pokemon_list)
        return df # Return dataframe

# Scrape smogon url for abilities list
def scrape_abilities(url):
    # Set options for Firefox to run in background
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")

    driver = webdriver.Firefox(options=options)
    try:
        # Go to url
        driver.get(url)

        # Expand window size to capture all dynamically generated elements
        driver.set_window_size(1920, 3150)
        time.sleep(5)

        abilities = driver.find_elements(By.CLASS_NAME, "AbilityRow")
        ability_list = []

        # Extract ability data
        for ab in abilities:
            name = ab.find_element(By.CSS_SELECTOR, "div.AbilityRow-name").text
            ability_desc = ab.find_element(By.CSS_SELECTOR, "div.AbilityRow-description").text
 
            # Create ability dictionary
            ability = {
                'name': name,
                'description': ability_desc
            }

            # Add ability to list
            ability_list.append(ability)
    finally:
        driver.quit()

        df = pd.DataFrame(ability_list)
        return df # Return dataframe

# Scrape smogon url for items list
def scrape_items(url):
    # Set options for Firefox to run in background
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")

    driver = webdriver.Firefox(options=options)
    try:
        # Go to url
        driver.get(url)

        # Expand window size to capture all dynamically generated elements
        driver.set_window_size(1920, 4650)
        time.sleep(5)

        items = driver.find_elements(By.CLASS_NAME, "ItemRow")
        item_list = []

        # Extract item data
        for it in items:
            name = it.find_element(By.CSS_SELECTOR, "div.ItemRow-name").text
            item_desc = it.find_element(By.CSS_SELECTOR, "div.ItemRow-description").text
 
            # Create item dictionary
            item = {
                'name': name,
                'description': item_desc
            }

            # Add item to list
            item_list.append(item)
    finally:
        driver.quit()

        df = pd.DataFrame(item_list)
        return df # Return dataframe

# Scrape dex number, kanji and hepburn for pokemon
def scrape_pokemon_jp(url):
# Set options for Firefox to run in background
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")

    driver = webdriver.Firefox(options=options)
    try:
        # Go to url
        driver.get(url)

        # Expand window size to capture all dynamically generated elements
        driver.set_window_size(1920, 13000)
        time.sleep(5)

        # Find tables for gen 1 - 3
        tables = driver.find_elements(By.XPATH, "/html/body/div[1]/div[2]/div[1]/div[3]/div[4]/div[1]/table")

        pokemons = []
        pokemon_list = []    

        # Extract rows from tables and combine into one list
        for i, table in enumerate(tables[:3], start=1):
            curr_gen = table.find_elements(By.TAG_NAME, "tr")
            pokemons = pokemons + curr_gen[2:]
            time.sleep(5)

        # Extract pokemon name data
        for mon in pokemons:
            name_str = mon.text

            # Check if "Mr. Mime" is in the string
            if "Mr. Mime" in name_str:
                # Replace "Mr. Mime" with a placeholder
                name_str = name_str.replace("Mr. Mime", "Mr_Mime")

            # Split string
            names = name_str.split(" ")

            # Restore "Mr. Mime" for eng name
            names = [name.replace("Mr_Mime", "Mr. Mime") for name in names]
            
            # Create pokemon names dictionary
            pokemon = {
                'dex_entry': names[0],
                'eng_name': names[1],
                'kanji': names[2],
                'hepburn': names[3]
            }

            # Add pokemon to list
            pokemon_list.append(pokemon)
    finally:
        driver.quit()

        df = pd.DataFrame(pokemon_list)
        return df # Return dataframe
