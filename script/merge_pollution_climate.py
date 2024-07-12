import pandas as pd
import glob

# Load the correspondence data
correspondence_df = pd.read_csv('C:/Users/Administrateur/Documents/correspondence_table.csv')

# Load the pollution data
pollution_df_old = pd.read_csv('C:/Users/Administrateur/Documents/pollution_rhone_alpe_data.csv')
pollution_df_new = pd.read_csv('C:/Users/Administrateur/Documents/rhone_alpes_filtered_data_new.csv')

# Function to standardize datetime formats to ISO 8601
def standardize_datetime_format(df, column_name):
    # Parse the datetime column with errors='coerce' to handle any parsing issues
    df[column_name] = pd.to_datetime(df[column_name], errors='coerce', utc=True)
    # Convert to ISO 8601 format with timezone information
    df[column_name] = df[column_name].dt.strftime('%Y-%m-%dT%H:%M:%S%z')
    return df

# Apply the function to both DataFrames
pollution_df_old = standardize_datetime_format(pollution_df_old, 'start')
pollution_df_new = standardize_datetime_format(pollution_df_new, 'start')

# Concatenate old and new pollution data
pollution_df = pd.concat([pollution_df_old, pollution_df_new])
print(pollution_df)

# Merge the pollution data with the correspondence data on the id column
merged_pollution_df = pollution_df.merge(correspondence_df, left_on='id', right_on='Pollutant_Station_Code')

# Convert 'start' column to datetime format and then format it to 'YYYYMMDD'
merged_pollution_df['date'] = pd.to_datetime(merged_pollution_df['start'], errors='coerce').dt.strftime('%Y%m%d')
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
     
    # Convert 'Climate_Date' to string format 'YYYYMMDD'
    climate_df['Climate_Date'] = climate_df['Climate_Date'].astype(str)
    
    # Filter climate data to keep only rows with dates present in pollution data
    filtered_climate_df = climate_df[climate_df['Climate_Date'].isin(pollution_dates)]
    
    # Append the filtered data to the list
    climate_data_list.append(filtered_climate_df)

# Combine all climate data into a single DataFrame
all_climate_data_df = pd.concat(climate_data_list, ignore_index=True)
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
