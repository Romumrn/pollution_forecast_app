import pandas as pd
import glob

# Define the bounds for the Rhône-Alpes region (example bounds, you may need to adjust them)
lat_min, lat_max = 44.0, 46.5
lon_min, lon_max = 4.0, 7.5

# Get the list of CSV files
csv_files = glob.glob("C:/Users/Administrateur/Documents/intermediate_csvs/*combined.csv")

# Check if any files are found
if not csv_files:
    print("No CSV files found.")
else:
    print(f"Found {len(csv_files)} files.")

# Initialize an empty list to store DataFrames
dfs = []

for file in csv_files:
    # Read the CSV file
    df = pd.read_csv(file)
    print(f"Processing file: {file}, total rows: {len(df)}")

    # Filter the rows based on latitude and longitude bounds
    subset_df = df[(df['latitude'] >= lat_min) & (df['latitude'] <= lat_max) & 
                   (df['longitude'] >= lon_min) & (df['longitude'] <= lon_max)]

    print(f"Filtered rows: {len(subset_df)}")

    # Append the filtered DataFrame to the list if it's not empty
    if not subset_df.empty:
        dfs.append(subset_df)

# Check if there are any DataFrames to concatenate
if not dfs:
    print("No data to concatenate after filtering.")
else:
    # Concatenate all DataFrames, combining any unique columns
    concatenated_df = pd.concat(dfs, ignore_index=True)

    # Group by id, start, end, measure_unit, verif, valid, name, municipality, latitude, longitude, altitude
    group_columns = ['id', 'start', 'end']
    
    # Aggregate the pollutant values using mean
    aggregated_df = concatenated_df.groupby(group_columns).agg({
        'CO': 'mean',
        'NO2': 'mean',
        'O3': 'mean',
        'PM10': 'mean',
        'PM2.5': 'mean',
        'SO2': 'mean'
    }).reset_index()

    # Replace zeros with NaN
    aggregated_df.replace(0, pd.NA, inplace=True)

    # Write the concatenated data to a new CSV file
    output='pollution_rhone_alpe_data.csv'
    aggregated_df.to_csv(output, index=False)

    print(f"Filtered and combined data saved to '{output}'")
