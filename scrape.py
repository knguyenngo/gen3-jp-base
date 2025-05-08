import scrape_functions as sf
import time

move_url = 'https://www.smogon.com/dex/rs/moves/'
mon_url = 'https://www.smogon.com/dex/rs/pokemon/'
ab_url = 'https://www.smogon.com/dex/rs/abilities/'
it_url = 'https://www.smogon.com/dex/rs/items/'
jp_url = 'https://bulbapedia.bulbagarden.net/wiki/List_of_Japanese_Pok%C3%A9mon_names'
jp_move_url = 'https://bulbapedia.bulbagarden.net/wiki/List_of_moves_in_other_languages'

moves = sf.scrape_moves(move_url)
pokemon = sf.scrape_pokemon(mon_url)
abilities = sf.scrape_abilities(ab_url)
items = sf.scrape_items(it_url)

moves.to_csv('./scraped/moves.csv', index=False)
pokemon.to_csv('./scraped/pokemon.csv', index=False)
abilities.to_csv('./scraped/abilities.csv', index=False)
items.to_csv('./scraped/items.csv', index=False)

jp_names = sf.scrape_pokemon_jp(jp_url)
jp_names.to_csv('./scraped/jp_names.csv', index=False)

time.sleep(30)

jp_moves = sf.scrape_moves_jp(jp_move_url, moves)
jp_moves.to_csv('./scraped/jp_moves.csv', index=False)