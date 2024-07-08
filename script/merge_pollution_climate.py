import pandas as pd
import glob 

# Define the bounds for the Rhône-Alpes region (example bounds, you may need to adjust them)
lat_min, lat_max = 44.0, 46.5
lon_min, lon_max = 4.0, 7.5

# Load the correspondence data
correspondence_df = pd.read_csv('C:/Users/Administrateur/Documents/correspondence_table.csv')

# Load the pollution data
pollution_df = pd.read_csv('C:/Users/Administrateur/Documents/pollution_rhone_alpe_data.csv')

# Merge the pollution data with the correspondence data on the id column
merged_pollution_df = pollution_df.merge(correspondence_df, left_on='id', right_on='Pollutant_Station_Code')

# Convert date-time columns in pollution data to the desired format
merged_pollution_df['date'] = pd.to_datetime(merged_pollution_df['start']).dt.strftime('%Y%m%d')
print("Merged Pollution Data:")
print(merged_pollution_df.columns.values)

# Extract unique dates from pollution data
pollution_dates = merged_pollution_df['date'].unique()
print(f"Unique Dates in Pollution Data: {pollution_dates}")

# Initialize a dataframe for the final merged data
final_merged_df = pd.DataFrame()

# Initialize a list to hold all climate data
climate_data_list = []

# Loop through all climate data files
climate_files = glob.glob('C:/Users/Administrateur/Documents/data_climate/data/data_climate*_cleaned.csv')  # Update the path as per your directory structure

for climate_file in climate_files:
    print(f"Processing Climate Data from {climate_file}:")
    
    # Load the climate data
    climate_df = pd.read_csv(climate_file)
    
    # Rename columns in climate data for easier merging
    climate_df.rename(columns={'LAT': 'Climate_Latitude', 'LON': 'Climate_Longitude', 'AAAAMMJJ': 'Climate_Date'}, inplace=True)
    
    # Filter the rows based on latitude and longitude bounds
    subset_climate_df = climate_df[(climate_df['Climate_Latitude'] >= lat_min) & 
                                    (climate_df['Climate_Latitude'] <= lat_max) & 
                                    (climate_df['Climate_Longitude'] >= lon_min) & 
                                    (climate_df['Climate_Longitude'] <= lon_max)]
    
    # Convert 'Climate_Date' to string format 'YYYYMMDD'
    subset_climate_df['Climate_Date'] = subset_climate_df['Climate_Date'].astype(str)
    
    # Filter climate data to keep only rows with dates present in pollution data
    filtered_climate_df = subset_climate_df[subset_climate_df['Climate_Date'].isin(pollution_dates)]
    
    # Append the filtered data to the list
    climate_data_list.append(subset_climate_df)
     

# Combine all climate data into a single DataFrame
all_climate_data_df = pd.concat(climate_data_list, ignore_index=True)
print(all_climate_data_df )

print("Combined Climate Data:")
print(all_climate_data_df.columns.values)

# Merge the combined data with the pollution data using date, latitude, and longitude coordinates
merged_climate_df = merged_pollution_df.merge(
    all_climate_data_df,
    left_on=['date', 'Climate_Latitude', 'Climate_Longitude'],
    right_on=['Climate_Date', 'Climate_Latitude', 'Climate_Longitude'],
    how='left'  # Adjust 'how' as needed
)

print("Merged Data:")
print(merged_climate_df.head())

# Save the final merged data to a CSV file
output = 'C:/Users/Administrateur/Documents/final_merged_data.csv'
merged_climate_df.to_csv(output, index=False)
print(f"Final merged data saved to '{output}'")