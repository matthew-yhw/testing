import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Simulate sample data
df = pd.DataFrame({
    'region': ['Kowloon', 'Kowloon', 'Hong Kong Island', 'Hong Kong Island'],
    'car_park': ['Park A', 'Park B', 'Park C', 'Park D'],
    'timestamp': pd.date_range('2025-11-01', periods=4, freq='15min'),
    'vacancy': [10, 20, 15, 5],
    'latitude': [22.3167, 22.3231, 22.2800, 22.2750],  # Approximate coordinates
    'longitude': [114.1700, 114.1650, 114.1588, 114.1500]
})

# Step 1: Load your car park data
# Replace 'your_car_park_data.csv' with your actual data source (e.g., CSV or database)
# Expected columns: 'region', 'car_park', 'timestamp', 'vacancy'

# Convert timestamp to datetime if not already
if not pd.api.types.is_datetime64_any_dtype(df['timestamp']):
    df['timestamp'] = pd.to_datetime(df['timestamp'])

# Step 2: Create a Streamlit web app
st.title('Hong Kong Car Park Vacancy Viewer')  # Web page title

# Step 3: Dropdown for selecting region
regions = sorted(df['region'].unique())
selected_region = st.selectbox('Select Region', regions)

# Step 4: Dropdown for selecting car park based on region
car_parks = sorted(df[df['region'] == selected_region]['car_park'].unique())
selected_car_park = st.selectbox('Select Car Park', car_parks)

# Step 5: Filter data for the selected car park
park_data = df[df['car_park'] == selected_car_park].sort_values('timestamp')

# Step 6: Display map of all car parks in the selected region
st.subheader(f'Car Parks in {selected_region}')
# Prepare data for the map
map_data = region_data[['latitude', 'longitude', 'car_park']].drop_duplicates(subset=['car_park'])
# Ensure lat/lon are numeric and drop invalid rows
map_data = map_data[map_data['latitude'].notnull() & map_data['longitude'].notnull()]
if not map_data.empty:
    st.map(map_data, latitude='latitude', longitude='longitude', zoom=10, tooltip='car_park')
else:
    st.write('No valid latitude/longitude data available for this region.')

# Step 7: Filter data for the selected car park and plot bar chart
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





