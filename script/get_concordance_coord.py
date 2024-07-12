import pandas as pd
import numpy as np
from math import radians, cos, sin, sqrt, atan2
import matplotlib.pyplot as plt
import glob

# Define the Haversine formula
def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0  # Earth radius in km

    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)

    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    return distance

# Define geographical boundaries for France Métropolitaine
lat_min, lat_max = 41.0, 51.5
lon_min, lon_max = -5.0, 10.0

# Function to filter coordinates within France Métropolitaine
def filter_france_metropolitaine(df, lat_col, lon_col):
    return df[(df[lat_col] >= lat_min) & (df[lat_col] <= lat_max) & (df[lon_col] >= lon_min) & (df[lon_col] <= lon_max)]

# Initialize lists to store matching coordinates
correspondence = []

# Load pollution station data
df2 = pd.read_excel('C:/Users/Administrateur/Documents/fr-2023-d-lcsqa-ineris-20230717.xls')
coord2 = df2[['EUStationCode', 'Latitude', 'Longitude']].drop_duplicates()
# Filter coord2 for France Métropolitaine
coord2 = filter_france_metropolitaine(coord2, 'Latitude', 'Longitude')

all_coords1 = pd.DataFrame()

# Iterate through each climate data file and gather coordinates
for file_path in glob.glob("C:/Users/Administrateur/Documents/data_climate/data/data_climate*"):
    df1 = pd.read_csv(file_path)
    coords1 = df1[['NOM_USUEL', 'LAT', 'LON']].drop_duplicates()
    coords1 = filter_france_metropolitaine(coords1, 'LAT', 'LON')
    all_coords1 = pd.concat([all_coords1, coords1], ignore_index=True)

# Remove duplicates
all_coords1 = all_coords1.drop_duplicates()

# Dictionary to store the closest coordinates
closest_pairs = {}

print("Start to create the correspondence table")

# Iterate through all climate coordinates and find the closest pollution stations
for index1, row1 in all_coords1.iterrows():
    lat1 = row1['LAT']
    lon1 = row1['LON']
    
    closest_distance = float('inf')
    closest_row = None
    
    for index2, row2 in coord2.iterrows():
        lat2 = row2['Latitude']
        lon2 = row2['Longitude']
        distance = haversine(lat1, lon1, lat2, lon2)
        
        if distance < closest_distance and distance <= 10:
            closest_distance = distance
            closest_row = row2
    
    # Store the closest match if one was found and the pollution station is not already assigned
    if closest_row is not None and closest_row['EUStationCode'] not in closest_pairs.values():
        closest_pairs[index1] = {
            'Climate_Name': row1['NOM_USUEL'],
            'Climate_Latitude': lat1,
            'Climate_Longitude': lon1,
            'Pollutant_Station_Code': closest_row['EUStationCode'],
            'Pollutant_Station_Latitude': closest_row['Latitude'],
            'Pollutant_Station_Longitude': closest_row['Longitude'],
            'Distance_km': closest_distance
        }
        print(f"{row1['NOM_USUEL']} ({lat1}, {lon1}) -> {closest_row['EUStationCode']} ({lat2}, {lon2}) | Distance: {closest_distance:.2f} km")

# Create a DataFrame from the closest pairs
correspondence_df = pd.DataFrame(list(closest_pairs.values()))

# Save the correspondence DataFrame to a CSV file
correspondence_df.to_csv('correspondence_table_one_to_one.csv', index=False)

# Print the DataFrame
print(correspondence_df)

# Plot the coordinates
plt.figure(figsize=(10, 8))
plt.scatter(all_coords1['LON'], all_coords1['LAT'], c='dimgrey', label='Station Climate Coordinates')
plt.scatter(coord2['Longitude'], coord2['Latitude'], c='darkgreen', label='Station Pollutant Coordinates')

plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.title('Coordinates from Climate and Pollutant Stations')
plt.legend()
plt.show()
