# Pet Cost Estimator

An interactive pet care cost estimation tool based on real pet store sales data. Helps prospective pet owners estimate annual pet care costs with personalised advice, supporting all seven continents with economy-adjusted pricing.

## Data Source
- **Dataset**: Pet Store Records 2020 (Kaggle)
- **URL**: https://www.kaggle.com/datasets/ippudkiippude/pet-store-records-2020
- **Data Year**: 2020
- **Currency**: USD ($)

## Quick Start

### Local Setup

1. Install dependencies
```bash
pip install -r requirements.txt
```

2. Run the app
```bash
streamlit run app.py
```

3. Open http://localhost:8501 in your browser

## Features

### 1. Personalised Pet Naming
Give your future pet a name! The app personalises the cost estimate and tips with your pet's name.

### 2. Detailed Pet Type Selection
Supports 7 categories with 12 specific types, with logically ordered costs:

| Pet Type | Monthly (Global) | Annual (Global) | Level |
|----------|-----------------|-----------------|-------|
| 🦎 Reptile | ~$43 | ~$516 | Lowest |
| 🐠 Fish | ~$45 | ~$540 | Very Low |
| 🐹 Hamster | ~$51 | ~$612 | Low |
| 🦜 Bird | ~$93 | ~$1,116 | Medium-Low |
| 🐰 Rabbit | ~$130 | ~$1,560 | Medium |
| 🐶 Small Dog | ~$160 | ~$1,920 | Medium |
| 🐱 Short-haired Cat | ~$170 | ~$2,040 | Medium |
| 🐱 Long-haired Cat | ~$190 | ~$2,280 | Medium-High |
| 🐶 Medium Dog | ~$200 | ~$2,400 | High |
| 🐶 Large Dog | ~$265 | ~$3,180 | Highest |

### 3. All Seven Continents
Supports all 7 continents with economy-adjusted pricing:

| Continent | Economy | Price Multiplier |
|-----------|---------|-----------------|
| 🌎 North America | Developed | 1.35x |
| 🌏 Oceania | Developed | 1.30x |
| 🌍 Europe | Developed | 1.25x |
| 🌏 Asia | Mixed | 0.85x |
| 🌎 South America | Developing | 0.75x |
| 🌍 Africa | Developing | 0.65x |
| 🧊 Antarctica | Research Only | 2.00x |

### 4. Adjustable Spending Levels
Each category can be adjusted with a slider (0.5x - 2.0x, step 0.1):

| Level | Multiplier | Color |
|-------|-----------|-------|
| Basic | 0.5x - 0.7x | 🟢 |
| Standard | 0.8x - 1.2x | 🔵 |
| Premium | 1.3x - 2.0x | 🔴 |

### 5. Cost Categories
| Category | Description |
|----------|-------------|
| Grooming | Bathing, grooming, cleaning |
| Food | Main food, treats, supplements |
| Toys & Supplies | Toys, cages, bowls, etc. |
| Medical | Vaccinations, checkups, medications |

### 6. Personalised Care Tips
Breed-specific recommendations for all 12 pet types across 4 categories.

### 7. Centred Layout
All controls are in the main content area for a cleaner, more intuitive experience.

## Files

| File | Description |
|------|-------------|
| `app.py` | Main Streamlit application |
| `pet_price_data.json` | Processed price data (USD, 7 continents) |
| `requirements.txt` | Python dependencies |

## Tech Stack

- **Frontend**: Streamlit
- **Visualisation**: Plotly
- **Data Processing**: Pandas, NumPy
- **Currency**: USD ($)

## Usage

1. **Name your pet** (optional)
2. Select **pet category** and **specific type**
3. Choose your **continent**
4. Adjust **spending sliders** for each category
5. Click **"Calculate Annual Cost"**
6. View personalised cost estimate and care tips

## Disclaimer

- Data is for reference only; actual costs may vary
- Antarctica pricing reflects extreme logistics costs for research stations
- Budget extra for emergency medical expenses
- Pet ownership is a long-term commitment

---

**Pet Cost Estimator** - Made with love for future pet owners
