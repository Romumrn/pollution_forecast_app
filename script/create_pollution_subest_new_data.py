import pandas as pd
import os
import glob

# Load the concorence table
concorence_table = pd.read_csv('C:/Users/Administrateur/Documents/correspondence_table.csv')

# Filter for Rhône-Alpes region based on some criteria (example: latitude and longitude range)
# Assuming 'Climate_Latitude' and 'Climate_Longitude' columns represent the coordinates for Rhône-Alpes
rhone_alpes_stations = concorence_table[
    (concorence_table['Climate_Latitude'] >= 45) & 
    (concorence_table['Climate_Latitude'] <= 46.5) & 
    (concorence_table['Climate_Longitude'] >= 4.5) & 
    (concorence_table['Climate_Longitude'] <= 6)
]

# Get the list of pollutant station codes for Rhône-Alpes
rhone_alpes_station_codes = rhone_alpes_stations['Pollutant_Station_Code'].tolist()


# Function to load and filter data based on station codes
def load_and_filter_data(file_path, station_codes):
    df = pd.read_csv(file_path, delimiter=';', encoding='utf-8')
    filtered_df = df[df['code site'].isin(station_codes)]
    return filtered_df

# Function to restructure data to the desired format
def restructure_data(df):
    pollutants = ['CO', 'NO2', 'O3', 'PM10', 'PM2.5', 'SO2']
    df['start'] = pd.to_datetime(df['Date de début'])
    df['end'] = pd.to_datetime(df['Date de fin'])
    df['id'] = df['code site']
    
    # Initialize an empty DataFrame for the final structure
    final_df = pd.DataFrame(columns=['id', 'start', 'end'] + pollutants)
    
    for pollutant in pollutants:
        pollutant_data = df[df['Polluant'] == pollutant]
        pollutant_data = pollutant_data[['id', 'start', 'end', 'valeur']]
        pollutant_data.rename(columns={'valeur': pollutant}, inplace=True)
        if final_df.empty:
            final_df = pollutant_data
        else:
            final_df = pd.merge(final_df, pollutant_data, on=['id', 'start', 'end'], how='outer')
    
    final_df = final_df.sort_values(by=['id', 'start']).reset_index(drop=True)
    return final_df

# List of your data files
data_files = glob.glob('C:/Users/Administrateur/Documents/talend/data/csv/*csv')  # Replace with your actual file names

# Load, filter, and restructure data
all_data = pd.DataFrame()
for file in data_files:
    df = load_and_filter_data(file, rhone_alpes_station_codes)
    print(file.split("/")[-1], df.shape)
    if not df.empty:
        restructured_df = restructure_data(df)
        all_data = pd.concat([all_data, restructured_df], ignore_index=True)

# Save the final dataset to a CSV file
all_data.to_csv('rhone_alpes_filtered_data_new.csv', index=False)
