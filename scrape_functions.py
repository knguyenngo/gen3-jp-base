from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
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
        
        # Extract move data
        for move in moves:
            name = move.find_element(By.CSS_SELECTOR, "div.MoveRow-name").text
            move_type = move.find_element(By.CSS_SELECTOR, "div.MoveRow-type").text
            damage_type = move.find_element(By.CSS_SELECTOR, "div.damage-category-block").get_attribute("class").split()[-1]
            move_power = move.find_element(By.CSS_SELECTOR, "div.MoveRow-power > span").text
            move_accuracy = move.find_element(By.CSS_SELECTOR, "div.MoveRow-accuracy > span").text
            move_pp = move.find_element(By.CSS_SELECTOR, "div.MoveRow-pp > span").text
            move_desc = move.find_element(By.CSS_SELECTOR, "div.MoveRow-description").text
            print(name, move_type, damage_type, move_power, move_accuracy, move_pp, move_desc)
    finally:
        driver.quit()
