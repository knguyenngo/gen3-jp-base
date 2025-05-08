import pandas as pd

# Import csv
pokemon = pd.read_csv('./scraped/pokemon.csv')
moves = pd.read_csv('./scraped/moves.csv')
jp_names = pd.read_csv('./scraped/jp_names.csv')
jp_moves = pd.read_csv('./scraped/jp_moves.csv')

# Drop forms of same species
pokemon.drop(pokemon[pokemon["name"] == "Deoxys-Attack"].index, inplace=True)
pokemon.drop(pokemon[pokemon["name"] == "Deoxys-Defense"].index, inplace=True)
pokemon.drop(pokemon[pokemon["name"] == "Deoxys-Speed"].index, inplace=True)
pokemon.drop(pokemon[pokemon["name"] == "Castform-Rainy"].index, inplace=True)
pokemon.drop(pokemon[pokemon["name"] == "Castform-Snowy"].index, inplace=True)
pokemon.drop(pokemon[pokemon["name"] == "Castform-Sunny"].index, inplace=True)

# Check if number of mons and moves are same
i, j = 0, 0

print("Checking if pokemon lists are equal")
eng_names = jp_names.eng_name.values

mon_passed = True
move_passed = True

for name in eng_names:
    i = i+1
    if name not in pokemon.name.values:
        mon_passed = False

# No mons missing and names matched up
if i == len(pokemon.name.values) and mon_passed:
    print("All names matched")

print("Checking if move lists are equal")
move_names = jp_moves.eng_name.values

for name in move_names:
    j = j+1
    if name not in moves.name.values:
        move_passed = False

# No moves missing and names matched up
if j == len(moves.name.values) and move_passed:
    print("All moves matched")

