import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from streamlit_folium import st_folium
import folium

# Step 1: Create test data with latitude and longitude
df = pd.DataFrame({
    'region': ['Kowloon', 'Kowloon', 'Hong Kong Island', 'Hong Kong Island'],
    'car_park': ['Park A', 'Park B', 'Park C', 'Park D'],
    'timestamp': pd.date_range('2025-11-01', periods=4, freq='15min'),
    'vacancy': [10, 20, 15, 5],
    'latitude': [22.3167, 22.3231, 22.2800, 22.2750],
    'longitude': [114.1700, 114.1650, 114.1588, 114.1500]
})

# Ensure timestamp is datetime
df['timestamp'] = pd.to_datetime(df['timestamp'])

# Step 2: Create a Streamlit web app
st.title('Hong Kong Car Park Vacancy Viewer')

# Step 3: Dropdown for selecting region
regions = sorted(df['region'].unique())
selected_region = st.selectbox('Select Region', regions)

# Step 4: Filter car parks by selected region
region_data = df[df['region'] == selected_region]
car_parks = sorted(region_data['car_park'].unique())

# Step 5: Initialize session state for selected car park
if 'selected_car_park' not in st.session_state:
    st.session_state.selected_car_park = car_parks[0] if car_parks else None

# Step 6: Create Folium map
st.subheader(f'Car Parks in {selected_region}')
map_data = region_data[['latitude', 'longitude', 'car_park']].drop_duplicates(subset=['car_park'])
map_data = map_data[map_data['latitude'].notnull() & map_data['longitude'].notnull()]

if not map_data.empty:
    # Create Folium map centered on Hong Kong
    m = folium.Map(location=[22.3193, 114.1694], zoom_start=11, tiles='OpenStreetMap')
    
    # Add clickable markers
    for _, row in map_data.iterrows():
        folium.Marker(
            location=[row['latitude'], row['longitude']],
            popup=row['car_park'],
            tooltip=row['car_park'],
            icon=folium.Icon(color='blue')
        ).add_to(m)
    
    # Render map and capture click events
    map_output = st_folium(m, width=700, height=500, key=f"map_{selected_region}")
    
    # Check for clicked marker
    if map_output.get('last_clicked'):
        clicked_latlng = map_output['last_clicked']
        # Find the closest car park to the clicked location
        map_data['distance'] = ((map_data['latitude'] - clicked_latlng['lat'])**2 + 
                               (map_data['longitude'] - clicked_latlng['lng'])**2)**0.5
        closest_park = map_data.loc[map_data['distance'].idxmin(), 'car_park']
        st.session_state.selected_car_park = closest_park
else:
    st.write('No valid latitude/longitude data available for this region.')

# Step 7: Dropdown for selecting car park (syncs with map clicks)
selected_car_park = st.selectbox('Select Car Park', car_parks, 
                                 index=car_parks.index(st.session_state.selected_car_park) 
                                 if st.session_state.selected_car_park in car_parks else 0,
                                 key='car_park_select')
st.session_state.selected_car_park = selected_car_park

# Step 8: Plot bar chart for the selected car park
park_data = region_data[region_data['car_park'] == selected_car_park].sort_values('timestamp')
if not park_data.empty:
    st.subheader(f'Vacancy for {selected_car_park}')
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(park_data['timestamp'], park_data['vacancy'], width=0.01)
    ax.set_xlabel('Timestamp')
    ax.set_ylabel('Vacancy')
    ax.set_title(f'Vacancy Historical Record for {selected_car_park}')
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig)
else:
    st.write('No data available for the selected car park.')
