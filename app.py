import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import json

st.set_page_config(layout="wide")

@st.cache_data
def load_csv(path):
    return pd.read_csv(path)

# Load your CSVs
japanese_moves = load_csv("./scraped/jp_moves.csv")  # eng_name, kanji, hepburn
move_details = load_csv("./scraped/moves.csv")  # name, type, damage_type, power, accuracy, pp, description
pokemon_data = load_csv("./scraped/pokemon.csv")  # name,type,ability,hp,attack,defense,special_attack,special_defense,speed
pokemon_japanese = load_csv("./scraped/jp_names.csv")  # dex_entry,eng_name,kanji,hepburn

# Merge move data on the English name
moves_df = pd.merge(
    japanese_moves,
    move_details,
    left_on="eng_name",
    right_on="name",
    how="right"
).drop(columns=["eng_name"]) \
.rename(columns={"name": "move"})

# Merge pokemon data with Japanese names
pokemon_df = pd.merge(
    pokemon_japanese,
    pokemon_data,
    left_on="eng_name",
    right_on="name",
    how="right"
).drop(columns=["eng_name"]) \
.rename(columns={"name": "pokemon"})

# Process the ability and type columns to handle list format
# Instead of keeping as Python lists, convert to string representations for display
pokemon_df['ability_orig'] = pokemon_df['ability'].copy()
pokemon_df['type_orig'] = pokemon_df['type'].copy()

# Convert lists to strings for dataframe display
pokemon_df['ability'] = pokemon_df['ability'].apply(
    lambda x: ', '.join(eval(x)) if isinstance(x, str) and x.startswith('[') else 
              (', '.join(x) if isinstance(x, list) else str(x))
)
pokemon_df['type'] = pokemon_df['type'].apply(
    lambda x: ', '.join(eval(x)) if isinstance(x, str) and x.startswith('[') else 
              (', '.join(x) if isinstance(x, list) else str(x))
)

# Main navigation
view = st.sidebar.radio("Choose view", ["All Moves", "All Pokémon", "Lookup a Pokémon"])

if view == "All Moves":
    st.header("Moves Database")
    query = st.text_input("🔎 Search moves by name").strip().lower()
    if query:
        df_filtered = moves_df[moves_df["move"].str.lower().str.contains(query)]
    else:
        df_filtered = moves_df

    # Pre‑define your type colours
    type_colors = {
        "Normal": "#A8A878", "Fire": "#F08030", "Water": "#6890F0",
        "Electric": "#F8D030", "Grass": "#78C850", "Ice": "#98D8D8",
        "Fighting": "#C03028", "Poison": "#A040A0", "Ground": "#E0C068",
        "Flying": "#A890F0", "Psychic": "#F85888", "Bug": "#A8B820",
        "Rock": "#B8A038", "Ghost": "#705898", "Dragon": "#7038F8",
        "Dark": "#705848", "Steel": "#B8B8D0", "Fairy": "#EE99AC"
    }

    html = """
    <style>
    .moves-table {
        table-layout: fixed;      /* honor the colgroup widths */
        width: 100%;
        border-collapse: collapse;
        background:#121212;
        color:#e0e0e0;
    }
    .moves-table th {
        background:#1f1f1f;
        color:#fff;
        padding:8px;
        border-bottom:2px solid #444;
        text-align:left;
    }
    .moves-table td {
        padding:8px;
        border-bottom:1px solid #333;
        vertical-align: top;
    }
    .moves-table tr:hover {
        background:#2a2a2a;
    }
    .type-badge {
        display:inline-block;
        padding:2px 6px;
        border-radius:4px;
        margin-right:4px;
        color:#fff;
        font-size:0.85em;
    }
    </style>

    <table class="moves-table">
    <!-- 👇 define exact widths for every column except Description -->
    <colgroup>
        <col style="width:80px">   <!-- Kanji -->
        <col style="width:100px">  <!-- Hepburn -->
        <col style="width:120px">  <!-- Move -->
        <col style="width:100px">  <!-- Type -->
        <col style="width:100px">  <!-- Category -->
        <col style="width:50px">   <!-- Power -->
        <col style="width:50px">   <!-- Acc -->
        <col style="width:50px">   <!-- PP -->
        <col>                     <!-- Description (gets leftover space) -->
    </colgroup>

    <thead>
        <tr>
        <th>Kanji</th>
        <th>Hepburn</th>
        <th>Move</th>
        <th>Type</th>
        <th>Category</th>
        <th>Power</th>
        <th>Acc</th>
        <th>PP</th>
        <th>Description</th>
        </tr>
    </thead>
    <tbody>
    """

    for _, r in df_filtered.iterrows():
        # render type badges
        raw_type = r["type"]
        # handle list vs string
        types = eval(raw_type) if isinstance(raw_type, str) and raw_type.startswith("[") else [raw_type]
        badges = "".join(
            f'<span class="type-badge" style="background:{type_colors.get(t, "#777")}">{t}</span>'
            for t in types
        )

        html += f"""
        <tr>
          <td>{r['kanji'] or ''}</td>
          <td>{r['hepburn'] or ''}</td>
          <td>{r['move']}</td>
          <td>{badges}</td>
          <td>{r['damage_type']}</td>
          <td>{r['power']}</td>
          <td>{r['accuracy']}</td>
          <td>{r['pp']}</td>
          <td>{r['description']}</td>
        </tr>
        """

    html += """
      </tbody>
    </table>
    """

    # render as HTML component
    components.html(
      html,
      height=400 + 30 * len(df_filtered),
      scrolling=True
    )

elif view == "All Pokémon":
    st.header("Pokémon Database")
    
    # Search and filter options
    col1, col2 = st.columns([2, 1])
    with col1:
        query = st.text_input("Search Pokémon by name or Pokédex number").strip().lower()
    
    # Additional filters
    col1, col2 = st.columns(2)
    with col1:
        all_types_flat = set()
        for t in pokemon_df['type_orig']:
            if isinstance(t, list):
                all_types_flat.update(t)
            elif isinstance(t, str) and t.startswith('['):
                all_types_flat.update(eval(t))
            else:
                all_types_flat.add(str(t))
        all_types = sorted(all_types_flat)
        type_filter = st.multiselect("Filter by type", options=["All"] + all_types, default="All")
    
    with col2:
        stat_options = ["HP", "Attack", "Defense", "Special Attack", "Special Defense", "Speed"]
        sort_by = st.selectbox("Sort by", options=["Pokédex #", "Name"] + stat_options, index=0)
    
    # Filter by name or Pokédex number
    if query:
        # Search in both name and Pokédex number
        name_matches = pokemon_df["pokemon"].str.lower().str.contains(query)
        dex_matches = pokemon_df["dex_entry"].str.lower().str.contains(query)
        pokemon_filtered = pokemon_df[name_matches | dex_matches]
    else:
        pokemon_filtered = pokemon_df.copy()
    
    # Filter by type
    if "All" not in type_filter and type_filter:
        # Filter Pokémon that have at least one of the selected types
        def has_type(type_value, filter_types):
            if isinstance(type_value, list):
                return any(t in filter_types for t in type_value)
            elif isinstance(type_value, str) and type_value.startswith('['):
                return any(t in filter_types for t in eval(type_value))
            else:
                return str(type_value) in filter_types
        
        type_mask = pokemon_filtered['type_orig'].apply(lambda x: has_type(x, type_filter))
        pokemon_filtered = pokemon_filtered[type_mask]
    
    # Sort by selected option
    if sort_by == "Pokédex #":
        pokemon_filtered = pokemon_filtered.sort_values("dex_entry")
    elif sort_by == "Name":
        pokemon_filtered = pokemon_filtered.sort_values("pokemon")
    elif sort_by == "HP":
        pokemon_filtered = pokemon_filtered.sort_values("hp", ascending=False)
    elif sort_by == "Attack":
        pokemon_filtered = pokemon_filtered.sort_values("attack", ascending=False)
    elif sort_by == "Defense":
        pokemon_filtered = pokemon_filtered.sort_values("defense", ascending=False)
    elif sort_by == "Special Attack":
        pokemon_filtered = pokemon_filtered.sort_values("special_attack", ascending=False)
    elif sort_by == "Special Defense":
        pokemon_filtered = pokemon_filtered.sort_values("special_defense", ascending=False)
    elif sort_by == "Speed":
        pokemon_filtered = pokemon_filtered.sort_values("speed", ascending=False)
    
    # Display columns in a specific order with Pokédex number first
    # Drop the original columns we used for filtering
    display_df = pokemon_filtered.drop(columns=["type_orig", "ability_orig"])
    
    columns_order = ["dex_entry", "pokemon", "type", "ability", "hp", "attack", "defense", 
                     "special_attack", "special_defense", "speed"]
    
    # Only include columns that exist in the dataframe
    valid_columns = [col for col in columns_order if col in display_df.columns] + [
        col for col in display_df.columns if col not in columns_order
    ]
    
    type_colors = {
        "Normal": "#A8A878", "Fire": "#F08030", "Water": "#6890F0",
        "Electric": "#F8D030", "Grass": "#78C850", "Ice": "#98D8D8",
        "Fighting": "#C03028", "Poison": "#A040A0", "Ground": "#E0C068",
        "Flying": "#A890F0", "Psychic": "#F85888", "Bug": "#A8B820",
        "Rock": "#B8A038", "Ghost": "#705898", "Dragon": "#7038F8",
        "Dark": "#705848", "Steel": "#B8B8D0", "Fairy": "#EE99AC"
    }

    html = """
    <style>
      .pokemon-table { table-layout: fixed; width:100%; border-collapse:collapse;
        background:#121212; color:#e0e0e0; }
      .pokemon-table th, .pokemon-table td {
        padding:8px; border-bottom:1px solid #333; vertical-align:middle;
      }
      .pokemon-table th {
        background:#1f1f1f; color:#fff; border-bottom:2px solid #444;
        text-align:left;
      }
      .pokemon-table tr:hover { background:#2a2a2a; }
      .sprite-cell { width:50px; text-align:center; }
      .sprite-img { width:40px; height:40px; image-rendering:pixelated; }
      .type-badge {
        display:inline-block; padding:2px 6px; border-radius:4px;
        margin-right:4px; color:#fff; font-size:0.85em;
      }
    </style>

    <table class="pokemon-table">
      <colgroup>
        <col style="width:50px">   <!-- sprite -->
        <col style="width:50px">   <!-- Dex # -->
        <col style="width:100px">  <!-- Eng Name -->
        <col style="width:100px">  <!-- Kanji -->
        <col style="width:100px">  <!-- Hepburn -->
        <col style="width:100px">  <!-- Type badges -->
        <col style="width:100px">  <!-- Ability -->
        <col style="width:50px">   <!-- HP -->
        <col style="width:50px">   <!-- Atk -->
        <col style="width:50px">   <!-- Def -->
        <col style="width:60px">   <!-- Sp.Atk -->
        <col style="width:60px">   <!-- Sp.Def -->
        <col style="width:50px">   <!-- Speed -->
      </colgroup>
      <thead>
        <tr>
          <th class="sprite-cell"></th>
          <th>Dex #</th>
          <th>Eng Name</th>
          <th>Kanji</th>
          <th>Hepburn</th>
          <th>Type</th>
          <th>Ability</th>
          <th>HP</th><th>Atk</th><th>Def</th>
          <th>Sp.Atk</th><th>Sp.Def</th><th>Speed</th>
        </tr>
      </thead>
      <tbody>
    """

    for _, row in pokemon_filtered.iterrows():
        dex_num = str(row["dex_entry"]).lstrip('#').lstrip('0') or "1"

        # build type badges
        raw = row["type_orig"]
        types = eval(raw) if isinstance(raw, str) and raw.startswith('[') else \
                (raw if isinstance(raw, list) else [str(raw)])
        badge_html = "".join(
            f'<span class="type-badge" style="background:{type_colors.get(t,"#777")}">{t}</span>'
            for t in types
        )

        sprite_url = (
          f"https://raw.githubusercontent.com/PokeAPI/sprites"
          f"/master/sprites/pokemon/versions/generation-iii/emerald/{dex_num}.png"
        )

        html += f"""
        <tr>
          <td class="sprite-cell">
            <img src="{sprite_url}" class="sprite-img" alt="{row['pokemon']}">
          </td>
          <td>{row['dex_entry']}</td>
          <td>{row['pokemon']}</td>
          <td>{row['kanji'] or ''}</td>
          <td>{row['hepburn'] or ''}</td>
          <td>{badge_html}</td>
          <td>{row['ability']}</td>
          <td>{row['hp']}</td>
          <td>{row['attack']}</td>
          <td>{row['defense']}</td>
          <td>{row['special_attack']}</td>
          <td>{row['special_defense']}</td>
          <td>{row['speed']}</td>
        </tr>
        """

    html += "</tbody></table>"

    components.html(
      html,
      height=400 + 30 * len(pokemon_filtered),
      scrolling=True
    )

elif view == "Lookup a Pokémon":
    st.header("Pokémon Details")
    
    # Option to search by Pokédex number or name
    search_by = st.radio("Search by", ["Name", "Pokédex Number"], horizontal=True)
    
    if search_by == "Name":
        pokemon_list = pokemon_df["pokemon"].sort_values().unique()
        choice = st.selectbox("Select a Pokémon", pokemon_list)
        row = pokemon_df[pokemon_df["pokemon"] == choice].iloc[0]
    else:
        dex_list = pokemon_df["dex_entry"].sort_values().unique()
        choice = st.selectbox("Select a Pokédex Number", dex_list)
        row = pokemon_df[pokemon_df["dex_entry"] == choice].iloc[0]
        
    # Get the Pokémon name for display
    pokemon_name = row["pokemon"]
    dex_number = row["dex_entry"]
    kanji = row["kanji"]
    hepburn = row["hepburn"]
    
    # Display Pokémon information in a more visual format
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # Try to get the numeric part of the dex entry for image
        dex_num = dex_number.replace('#', '').lstrip('0')
        if not dex_num:
            dex_num = "1"  # Fallback
            
        # Display Pokémon image using Pokédex number
        sprite_url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-iii/emerald/{dex_num}.png"
        st.markdown(f"""
        <div style="display: flex; justify-content: center; margin-bottom: 20px;">
            <img src="{sprite_url}" width="200" style="image-rendering: pixelated;">
        </div>
        """, unsafe_allow_html=True)
        
        # Show Pokédex number prominently
        st.markdown(f"<h2 style='text-align: left;'>{dex_number}</h2>", unsafe_allow_html=True)
        st.markdown(f"""
        <h3 style='text-align: left;'>
            {pokemon_name} 
            <span style='font-weight: normal; font-size: 0.9em;'>
                • {kanji} • {hepburn}
            </span>
        </h3>
        """, unsafe_allow_html=True)
    
    with col2:
        # Type badges - use type_orig which has the original list format
        types = row['type_orig']
        if isinstance(types, str) and types.startswith('['):
            types = eval(types)
        if not isinstance(types, list):
            types = [str(types)]
            
        type_colors = {
            "Normal": "#A8A878", "Fire": "#F08030", "Water": "#6890F0",
            "Electric": "#F8D030", "Grass": "#78C850", "Ice": "#98D8D8",
            "Fighting": "#C03028", "Poison": "#A040A0", "Ground": "#E0C068",
            "Flying": "#A890F0", "Psychic": "#F85888", "Bug": "#A8B820",
            "Rock": "#B8A038", "Ghost": "#705898", "Dragon": "#7038F8",
            "Dark": "#705848", "Steel": "#B8B8D0", "Fairy": "#EE99AC"
        }
        
        type_html = " ".join([f'<span style="background-color: {type_colors.get(t, "#999999")}; padding: 2px 8px; border-radius: 4px; color: white; margin-right: 4px;">{t}</span>' for t in types])
        st.markdown(f"**Types:** {type_html}", unsafe_allow_html=True)
        
        # Abilities - use ability_orig which has the original list format
        abilities = row['ability_orig']
        if isinstance(abilities, str) and abilities.startswith('['):
            abilities = eval(abilities)
        if not isinstance(abilities, list):
            abilities = [str(abilities)]
            
        st.markdown(f"**Abilities:** {', '.join(abilities)}")
        
        # Base stats with visual bars
        st.subheader("Base Stats")
        max_stat = 255  # Maximum possible stat value
        
        stats = {
            "HP": row['hp'],
            "Attack": row['attack'], 
            "Defense": row['defense'],
            "Special Attack": row['special_attack'],
            "Special Defense": row['special_defense'],
            "Speed": row['speed']
        }
        
        for stat, value in stats.items():
            # Calculate percentage for bar width
            percentage = min(int(value) / max_stat * 100, 100)
            bar_color = "green" if percentage > 70 else "orange" if percentage > 40 else "red"
            
            st.markdown(f"""
            <div style="margin-bottom: 5px;">
                <div style="display: flex; align-items: center;">
                    <div style="width: 120px; font-weight: bold;">{stat}:</div>
                    <div style="flex-grow: 1; background-color: #eee; border-radius: 5px; height: 20px;">
                        <div style="width: {percentage}%; background-color: {bar_color}; height: 100%; border-radius: 5px; display: flex; align-items: center; justify-content: flex-end; padding-right: 5px; color: white;">
                            {int(value)}
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Total stats
        total = sum(stats.values())
        st.markdown(f"**Total:** {total}")