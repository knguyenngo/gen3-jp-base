# Generation III Pokémon Explorer

A bilingual Streamlit web app that lets you search and filter Generation III Pokémon and moves by English name, Japanese Kanji, or Hepburn transliteration. Features color‑coded type badges, custom HTML tables, inline sprites, and detailed stat‑bar visualizations.

## 🚀 Features
- **All Moves**: Searchable table of 165 moves with bilingual names, categories, stats, and descriptions.
- **All Pokémon**: Searchable table of 386 Pokémon with English & Japanese names, type badges, abilities, and base stats.
- **Lookup a Pokémon**: Detail view showing sprite, bilingual labels, and horizontal stat bars.
- **Dark‑mode styling** with custom HTML/CSS and fixed‑width columns.
- **AI‑powered development**: Claude for scaffolding/CSS, GPT‑4 for creative UI ideas & debugging.

## 📦 Installation

1. **Create a virtual environment**  
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. **Install dependencies**  
   ```bash
   pip install -r requirements.txt
   ```

3. **Scrape data**  
   ```bash
   python scrape_functions.py
   # Produces CSVs in ./scraped/
   ```

## ▶️ Usage

Run the Streamlit app:
```bash
streamlit run app.py
```
App will automatically open in your browser to explore Pokémon and moves!

## 📁 File Structure
```
.
├── app.py               # Main Streamlit application
├── scrape_functions.py  # Selenium scraping helpers
├── requirements.txt     # Python dependencies
├── scraped/             # Generated CSV data
│   ├── moves.csv
│   ├── jp_moves.csv
│   ├── pokemon.csv
│   └── jp_names.csv
├── test.py              # Basic data-loading and merge tests
└── README.md            # This file
```

## 📄 License
This project is licensed under the MIT License. See `LICENSE` for details.
