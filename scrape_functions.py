from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
import json
import time

# Return soup from file
def convert_soup(file_name):
    with open(file_name) as original:
        soup = BeautifulSoup(original, 'html.parser')
    return soup

# Prettify html files for readability
def format_html(soup, write_file):
    with open(write_file, "w", encoding = 'utf-8') as formatted:
        formatted.write(str(soup.prettify()))

# Grab move data-reactid
def grab_moves(soup):
    move_links = soup.find_all('a', class_="MoveLink")
    return move_links

# Scrape smogon url by scrolling
def scrape_by_scroll(url):
    # Set options for Firefox to run in background
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")

    # Run Firefox in background
    driver = webdriver.Firefox(options=options)

    # Testing purposes
    captured_first_moves = []
    captured_last_moves = []

    try:
        driver.get(url)
        
        # Wait for spinner to disappear
        WebDriverWait(driver, 10).until(
            EC.invisibility_of_element_located((By.CLASS_NAME, "spinner"))
        )

        # Begin scrolling
        print("Scrolling to load all moves...")
        num_scrolls = 0
        scroll_lengths = [
            705, 700, 700, 695, 700, 700, 700, 700, 700, 700,  # 0-9
            695, 700, 700, 700, 700, 700, 695, 700           # 10-17
        ]

        while True:
            # Wait for page to load
            time.sleep(3)
            # Grab current .html and convert to soup object
            page_source = driver.page_source
            soup = BeautifulSoup(page_source, "html.parser")

            # Grab all move links
            move_links = grab_moves(soup)
            captured_first_moves.append(move_links[0].text)
            captured_last_moves.append(move_links[-1].text)

            # Stop scrolling when captured end of move list
            if (num_scrolls == 18):
                break
            
            # Determine scroll length for current iteration and scroll by length
            scroll_length = scroll_lengths[num_scrolls]
            driver.execute_script("window.scrollBy(0, arguments[0]);", scroll_length)

            num_scrolls = num_scrolls+1
    finally:
        driver.quit()
    
    return captured_first_moves, captured_last_moves

# Scrape smogon url for move list
def scrape_moves(url):
    # Set options for Firefox to run in background
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")

    # Run Firefox in background
    total_moves = 0
    driver = webdriver.Firefox(options=options)
    driver.get(url)
    driver.set_window_size(1920, 20000)
    time.sleep(5)

    moves = driver.find_elements(By.CLASS_NAME, "MoveRow")

    for move in moves:
        name = move.find_element(By.CSS_SELECTOR, "div.MoveRow-name").text
        move_type = move.find_element(By.CSS_SELECTOR, "div.MoveRow-type").text
        damage_type = move.find_element(By.CSS_SELECTOR, "div.damage-category-block").get_attribute("class").split()[-1]
        move_power = move.find_element(By.CSS_SELECTOR, "div.MoveRow-power > span").text
        move_accuracy = move.find_element(By.CSS_SELECTOR, "div.MoveRow-accuracy > span").text
        move_pp = move.find_element(By.CSS_SELECTOR, "div.MoveRow-pp > span").text
        move_desc = move.find_element(By.CSS_SELECTOR, "div.MoveRow-description").text
        print(name, move_type, damage_type, move_power, move_accuracy, move_pp, move_desc)

    driver.quit()
