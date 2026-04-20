"""
Pet Cost Estimator - Streamlit App
==================================
Helps prospective pet owners estimate annual pet care costs
"""

import streamlit as st
import pandas as pd
import json
import plotly.graph_objects as go
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Pet Cost Estimator",
    page_icon="🐾",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #FF6B6B;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .result-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2.5rem;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin: 1.5rem 0;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
    }
    .advice-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #e4e8ec 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border-top: 4px solid #667eea;
        margin: 0.5rem 0;
    }
    .select-box {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 12px;
        border: 2px solid #e9ecef;
        margin: 0.5rem 0;
    }
    .select-box:hover {
        border-color: #667eea;
        box-shadow: 0 2px 8px rgba(102, 126, 234, 0.1);
    }
    .slider-section {
        background: #ffffff;
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #dee2e6;
        margin: 0.5rem 0;
    }
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 1rem 3rem;
        border-radius: 30px;
        font-size: 1.2rem;
        font-weight: bold;
        width: 100%;
    }
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 5px 20px rgba(102, 126, 234, 0.4);
    }
    .section-title {
        font-size: 1.3rem;
        font-weight: bold;
        color: #333;
        margin: 1.5rem 0 0.5rem 0;
    }
    .pet-name-display {
        font-size: 1.5rem;
        color: #667eea;
        font-weight: bold;
        text-align: center;
        margin: 0.5rem 0;
    }
    .cost-badge {
        display: inline-block;
        background: #667eea;
        color: white;
        padding: 0.2rem 0.8rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: bold;
    }
    div[data-testid="stExpander"] {
        border: 1px solid #dee2e6;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    with open('pet_price_data.json', 'r', encoding='utf-8') as f:
        return json.load(f)

# Pet category structure
PET_CATEGORIES = {
    '🐱 Cat': {
        'icon': '🐱',
        'types': {
            'Short-haired Cat': {'desc': 'British Shorthair, Siamese, etc.', 'icon': '🐱'},
            'Long-haired Cat': {'desc': 'Ragdoll, Persian, Maine Coon, etc.', 'icon': '🐱'}
        }
    },
    '🐶 Dog': {
        'icon': '🐶',
        'types': {
            'Small Dog': {'desc': 'Poodle, Pomeranian, Chihuahua, etc.', 'icon': '🐕'},
            'Medium Dog': {'desc': 'Corgi, Shiba Inu, Border Collie, etc.', 'icon': '🐕'},
            'Large Dog': {'desc': 'Golden Retriever, Husky, German Shepherd, etc.', 'icon': '🐕'}
        }
    },
    '🐠 Fish': {
        'icon': '🐠',
        'types': {
            'fish': {'desc': 'Tropical fish, Goldfish, etc.', 'icon': '🐠'}
        }
    },
    '🦜 Bird': {
        'icon': '🦜',
        'types': {
            'bird': {'desc': 'Parrots, Finches, Budgies, etc.', 'icon': '🦜'}
        }
    },
    '🐹 Hamster': {
        'icon': '🐹',
        'types': {
            'hamster': {'desc': 'Syrian, Dwarf, Roborovski, etc.', 'icon': '🐹'}
        }
    },
    '🐰 Rabbit': {
        'icon': '🐰',
        'types': {
            'rabbit': {'desc': 'Lop-eared, Netherland Dwarf, etc.', 'icon': '🐰'}
        }
    },
    '🦎 Reptile': {
        'icon': '🦎',
        'types': {
            'Reptile': {'desc': 'Geckos, Snakes, Tortoises, etc.', 'icon': '🦎'}
        }
    }
}

# Seven continents
REGIONS = {
    'Africa': '🌍 Africa',
    'Antarctica': '🧊 Antarctica',
    'Asia': '🌏 Asia',
    'Europe': '🌍 Europe',
    'North America': '🌎 North America',
    'Oceania': '🌏 Oceania',
    'South America': '🌎 South America'
}

# Economic level indicators
REGION_ECONOMY = {
    'Africa': 'Developing',
    'Antarctica': 'Research Only',
    'Asia': 'Mixed Economy',
    'Europe': 'Developed',
    'North America': 'Developed',
    'Oceania': 'Developed',
    'South America': 'Developing'
}

CATEGORY_ICONS = {
    'Grooming': '🛁',
    'Food': '🍖',
    'Toys & Supplies': '🎾',
    'Medical': '💊'
}

# Personalized pet care tips
PET_TIPS = {
    'Short-haired Cat': {
        'grooming': 'Short-haired cats are low-maintenance. Brush weekly to reduce shedding. Bathing is rarely needed.',
        'food': 'High-protein diet is essential. Consider wet food for hydration. Monitor weight to prevent obesity.',
        'supplies': 'Invest in a quality scratching post, interactive toys, and a comfortable cat tree.',
        'medical': 'Regular vaccinations and annual checkups. Prone to dental issues - consider dental treats.'
    },
    'Long-haired Cat': {
        'grooming': 'Daily brushing is essential to prevent matting. Professional grooming every 6-8 weeks recommended.',
        'food': 'High-quality protein-rich diet. Omega fatty acids help maintain coat health. Watch for hairballs.',
        'supplies': 'Multiple scratching posts, detangling brushes, and elevated perches for coat airflow.',
        'medical': 'Higher grooming costs. Watch for skin issues under fur. Regular dental care important.'
    },
    'Small Dog': {
        'grooming': 'Professional grooming every 4-6 weeks. Daily brushing for long-haired breeds.',
        'food': 'Small breed formula with smaller kibble. Prone to dental issues - dental chews recommended.',
        'supplies': 'Small toys (avoid choking hazards), harness for walks, and a cozy bed.',
        'medical': 'Watch for dental disease, patellar luxation, and tracheal issues. Regular teeth cleaning.'
    },
    'Medium Dog': {
        'grooming': 'Brush 2-3 times per week. Professional grooming every 6-8 weeks for long-haired breeds.',
        'food': 'Balanced diet matching activity level. Joint supplements can be beneficial for active breeds.',
        'supplies': 'Durable toys, comfortable leash and collar, and outdoor gear for exercise.',
        'medical': 'Hip dysplasia screening recommended. Keep up with vaccinations and parasite prevention.'
    },
    'Large Dog': {
        'grooming': 'Regular brushing, especially during shedding seasons. Larger dogs = higher grooming costs.',
        'food': 'Large breed formula to support joint health. Higher food consumption - budget accordingly.',
        'supplies': 'Heavy-duty toys, large bed, sturdy leash/harness. Consider elevated feeding bowls.',
        'medical': 'Hip and elbow dysplasia screening essential. Bloat prevention - use slow feeders. Higher medication doses = higher costs.'
    },
    'fish': {
        'grooming': 'Tank maintenance is key. Weekly water changes, filter cleaning, and algae control.',
        'food': 'Species-specific food - flakes, pellets, or frozen. Avoid overfeeding to maintain water quality.',
        'supplies': 'Quality filter, heater, lighting, water testing kit, and decorations. Tank size matters!',
        'medical': 'Quarantine new fish. Monitor water parameters (pH, ammonia, nitrites). Have a hospital tank ready.'
    },
    'bird': {
        'grooming': 'Regular wing/nail trimming. Bathing options (mist spray or shallow dish). Clean cage weekly.',
        'food': 'Pelleted diet supplemented with fresh fruits/vegetables. Avoid avocado and chocolate (toxic!).',
        'supplies': 'Large cage (bigger is better), perches of varying sizes, foraging toys, and flight time outside cage.',
        'medical': 'Annual avian vet checkup. Watch for respiratory issues. Feather plucking can indicate stress.'
    },
    'hamster': {
        'grooming': 'Minimal grooming needed. Provide sand bath for dwarf hamsters. Clean cage weekly.',
        'food': 'Hamster pellets with occasional seeds/fruits. Small amounts - they hoard food!',
        'supplies': 'Spacious cage with deep bedding for burrowing, exercise wheel, hideouts, and chew toys.',
        'medical': 'Short lifespan (2-3 years). Watch for wet tail (stress-related illness). Keep environment stable.'
    },
    'rabbit': {
        'grooming': 'Brush regularly, especially long-haired breeds. Nail trimming every 4-6 weeks.',
        'food': 'Unlimited hay is essential! Fresh vegetables daily. Limited pellets. No iceberg lettuce.',
        'supplies': 'Large enclosure or free-roam setup, litter box, hideouts, and toys for chewing.',
        'medical': 'Spay/neuter recommended to prevent reproductive cancers. Watch for GI stasis - critical condition.'
    },
    'Reptile': {
        'grooming': 'Enclosure cleaning and substrate changes. UVB lighting replacement every 6-12 months.',
        'food': 'Species-specific - live insects, rodents, or vegetables. Calcium and vitamin supplements essential.',
        'supplies': 'Proper enclosure with heating gradient, UVB lighting, hides, and humidity control. Thermostat essential!',
        'medical': 'Find an exotic vet before getting a reptile. Metabolic bone disease prevention with proper UVB.'
    }
}

data = load_data()

# ===================== HEADER =====================
st.markdown('<p class="main-header">🐾 Pet Cost Estimator</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Estimate your annual pet care costs based on real pet store data</p>', unsafe_allow_html=True)

# ===================== MAIN SELECTION AREA (CENTERED) =====================
# Use columns to center the selection area
left_spacer, main_area, right_spacer = st.columns([1, 4, 1])

with main_area:
    
    st.markdown("---")
    
    # STEP 1: Pet Name
    st.markdown("<p class='section-title'>💝 Step 1: Name Your Pet</p>", unsafe_allow_html=True)
    pet_name = st.text_input(
        "Give your future pet a name (optional)",
        value="",
        placeholder="e.g., Buddy, Luna, Coco...",
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    # STEP 2: Pet Type Selection
    st.markdown("<p class='section-title'>🐾 Step 2: Choose Your Pet</p>", unsafe_allow_html=True)
    
    cat_col1, cat_col2 = st.columns(2)
    
    with cat_col1:
        selected_category = st.selectbox(
            "Pet Category",
            options=list(PET_CATEGORIES.keys()),
            help="Select the type of pet you want"
        )
    
    with cat_col2:
        pet_types = PET_CATEGORIES[selected_category]['types']
        if len(pet_types) > 1:
            selected_pet = st.selectbox(
                "Specific Type",
                options=list(pet_types.keys()),
                format_func=lambda x: f"{pet_types[x]['icon']} {x}",
                help="Select a more specific type"
            )
        else:
            selected_pet = list(pet_types.keys())[0]
            st.selectbox("Specific Type", [f"{pet_types[selected_pet]['icon']} {selected_pet}"], disabled=True)
    
    # Show pet description
    if selected_pet in pet_types:
        st.caption(f"📝 {pet_types[selected_pet]['desc']}")
    
    st.markdown("---")
    
    # STEP 3: Region Selection
    st.markdown("<p class='section-title'>🌍 Step 3: Choose Your Region</p>", unsafe_allow_html=True)
    
    region_col1, region_col2 = st.columns(2)
    
    with region_col1:
        selected_region = st.selectbox(
            "Continent",
            options=list(REGIONS.keys()),
            format_func=lambda x: REGIONS[x],
            help="Select your continent"
        )
    
    with region_col2:
        # Show economic indicator
        economy = REGION_ECONOMY.get(selected_region, '')
        if economy == 'Developed':
            st.markdown(f"<br><span class='cost-badge' style='background:#28a745;'>{economy}</span>", unsafe_allow_html=True)
        elif economy == 'Developing':
            st.markdown(f"<br><span class='cost-badge' style='background:#ffc107;color:#333;'>{economy}</span>", unsafe_allow_html=True)
        elif economy == 'Research Only':
            st.markdown(f"<br><span class='cost-badge' style='background:#6c757d;'>{economy}</span>", unsafe_allow_html=True)
        else:
            st.markdown(f"<br><span class='cost-badge' style='background:#17a2b8;'>{economy}</span>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # STEP 4: Spending Sliders
    st.markdown("<p class='section-title'>⚡ Step 4: Adjust Spending Levels</p>", unsafe_allow_html=True)
    st.caption("Drag sliders to adjust spending for each category (0.5x - 2.0x)")
    
    slider_cols = st.columns(4)
    demand_multipliers = {}
    
    categories = ['Grooming', 'Food', 'Toys & Supplies', 'Medical']
    
    for idx, category in enumerate(categories):
        with slider_cols[idx]:
            st.markdown(f"<div style='text-align:center;font-size:1.5rem;'>{CATEGORY_ICONS[category]}</div>", unsafe_allow_html=True)
            st.markdown(f"<div style='text-align:center;font-weight:bold;'>{category}</div>", unsafe_allow_html=True)
            
            demand_multipliers[category] = st.slider(
                f"{category}_slider",
                min_value=0.5,
                max_value=2.0,
                value=1.0,
                step=0.1,
                key=f"slider_{category}",
                label_visibility="collapsed"
            )
            
            # Show level indicator
            val = demand_multipliers[category]
            if val < 0.8:
                level, color = "Basic", "🟢"
            elif val < 1.2:
                level, color = "Standard", "🔵"
            else:
                level, color = "Premium", "🔴"
            st.caption(f"{color} {level} ({val:.1f}x)")
    
    st.markdown("---")
    
    # CALCULATE BUTTON
    calculate = st.button("💰 Calculate Annual Cost", use_container_width=True)

# ===================== RESULTS AREA =====================
if calculate:
    display_name = pet_name.strip() if pet_name.strip() else selected_pet
    
    # Calculate
    region_data = data['region_data'].get(selected_region, {})
    pet_data = region_data.get(selected_pet, {})
    
    if not pet_data:
        pet_data = data['global_data'].get(selected_pet, {})
        st.warning(f"⚠️ Limited data for {REGIONS[selected_region]}. Using global average.")
    
    monthly_costs = {}
    for category in categories:
        if category in pet_data:
            base_price = pet_data[category]['avg_price']
            multiplier = demand_multipliers[category]
            monthly_costs[category] = round(base_price * multiplier, 2)
        else:
            global_price = data['global_data'].get(selected_pet, {}).get(category, {}).get('avg_price', 20)
            multiplier = demand_multipliers[category]
            monthly_costs[category] = round(global_price * multiplier, 2)
    
    monthly_total = sum(monthly_costs.values())
    annual_total = monthly_total * 12
    
    # Show results in centered layout
    st.markdown("---")
    
    # Pet name banner
    if pet_name.strip():
        st.markdown(f'<p class="pet-name-display">💝 Cost Estimate for {pet_name}</p>', unsafe_allow_html=True)
    
    # Annual Cost - Big Display
    result_spacer, result_center, result_spacer2 = st.columns([1, 3, 1])
    with result_center:
        st.markdown(f"""
        <div class="result-card">
            <h3 style="margin-bottom: 0.5rem; font-size: 1.5rem;">🐾 {display_name}'s Annual Cost</h3>
            <h1 style="font-size: 5rem; margin: 1rem 0; color: #FFD93D; text-shadow: 2px 2px 4px rgba(0,0,0,0.2);">${annual_total:,.0f}</h1>
            <p style="font-size: 1.1rem; opacity: 0.9;">
                📍 {REGIONS[selected_region]} | 
                📅 ${monthly_total:,.0f}/month
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Charts and breakdown
    chart_spacer, chart_area, chart_spacer2 = st.columns([1, 6, 1])
    
    with chart_area:
        col_chart1, col_chart2 = st.columns([1, 1])
        
        with col_chart1:
            st.markdown("### 📊 Monthly Breakdown")
            
            cost_df = pd.DataFrame({
                'Category': [f"{CATEGORY_ICONS[cat]} {cat}" for cat in monthly_costs.keys()],
                'Level': [f"{demand_multipliers[cat]:.1f}x" for cat in monthly_costs.keys()],
                'Monthly': [f"${cost:,.0f}" for cost in monthly_costs.values()]
            })
            st.dataframe(cost_df, use_container_width=True, hide_index=True)
        
        with col_chart2:
            st.markdown("### 📈 Distribution")
            
            fig_pie = go.Figure(data=[go.Pie(
                labels=list(monthly_costs.keys()),
                values=list(monthly_costs.values()),
                hole=0.45,
                marker_colors=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4'],
                textinfo='label+percent',
                textfont_size=13
            )])
            fig_pie.update_layout(
                showlegend=False,
                margin=dict(t=10, b=10, l=10, r=10),
                height=280
            )
            st.plotly_chart(fig_pie, use_container_width=True)
    
    # Personalized Tips
    st.markdown("---")
    st.markdown(f"### 💡 Personalized Tips for {display_name} ({selected_pet})")
    
    tips = PET_TIPS.get(selected_pet, PET_TIPS['Short-haired Cat'])
    
    tip_spacer, tip_area, tip_spacer2 = st.columns([1, 6, 1])
    with tip_area:
        tc1, tc2 = st.columns(2)
        with tc1:
            st.markdown(f"""
            <div class="advice-card">
                <h4>🛁 Grooming</h4>
                <p style="font-size:0.95rem;">{tips['grooming']}</p>
            </div>
            """, unsafe_allow_html=True)
            st.markdown(f"""
            <div class="advice-card">
                <h4>🍖 Food & Diet</h4>
                <p style="font-size:0.95rem;">{tips['food']}</p>
            </div>
            """, unsafe_allow_html=True)
        with tc2:
            st.markdown(f"""
            <div class="advice-card">
                <h4>🎾 Supplies</h4>
                <p style="font-size:0.95rem;">{tips['supplies']}</p>
            </div>
            """, unsafe_allow_html=True)
            st.markdown(f"""
            <div class="advice-card">
                <h4>💊 Health & Medical</h4>
                <p style="font-size:0.95rem;">{tips['medical']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.caption("📊 Data: Pet Store Records 2020 (Kaggle) | 💵 Currency: USD | Prices adjusted by regional economy level")

else:
    # Welcome state
    st.markdown("---")
    
    welcome_spacer, welcome_center, welcome_spacer2 = st.columns([1, 4, 1])
    
    with welcome_center:
        st.markdown("""
        <div style="text-align: center; padding: 2rem;">
            <div style="font-size: 4rem; margin-bottom: 1rem;">🐾</div>
            <h2 style="margin-bottom: 1rem;">Welcome to Pet Cost Estimator!</h2>
            <p style="font-size: 1.1rem; color: #666;">
                Fill out the form above to estimate your annual pet care costs.<br>
                Select your pet type, continent, and adjust spending levels.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Pet comparison table
    table_spacer, table_area, table_spacer2 = st.columns([1, 5, 1])
    with table_area:
        st.markdown("### 📋 Estimated Monthly Cost by Pet Type (Global Average)")
        
        comparison_data = []
        pet_order = ['Reptile', 'fish', 'hamster', 'bird', 'rabbit', 
                     'Small Dog', 'Short-haired Cat', 'Long-haired Cat', 'Medium Dog', 'Large Dog']
        
        for pet in pet_order:
            costs = data['global_data'].get(pet, {})
            total = sum(v['avg_price'] for v in costs.values())
            comparison_data.append({
                'Pet Type': pet,
                'Monthly': f"${total:.0f}",
                'Annual': f"${total*12:.0f}"
            })
        
        df_compare = pd.DataFrame(comparison_data)
        st.dataframe(df_compare, use_container_width=True, hide_index=True)
        
        st.info("💡 **Tip:** Costs vary by continent due to economic differences. Antarctica has the highest costs due to extreme logistics!")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #999; padding: 1rem;">
    <p>🐾 Pet Cost Estimator | Made with ❤️ for future pet owners</p>
    <p style="font-size: 0.8rem;">Data Source: Kaggle - Pet Store Records 2020 | Currency: USD | 7 Continents Supported</p>
</div>
""", unsafe_allow_html=True)
