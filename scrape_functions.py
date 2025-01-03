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
 
            # Create move dataframe
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
        return move_list # Return list of moves

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

            # Create pokemon dataframe
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
        return pokemon_list # Return list of pokemon 