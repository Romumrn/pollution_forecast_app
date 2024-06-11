import glob
import pandas as pd

# Directory where the data files are stored
dir = "data"

for i in range(1, 96):
    # Pad the number with a leading zero if it's a single digit
    if len(str(i)) == 1:
        i = "0" + str(i)
    else:
        i = str(i)
    
    print(f"Process department {i}")

    # Initialize an empty list to hold DataFrames for 'Vent' files
    dataframes_vent = []

    # Process each .csv.gz file for the current number (Vent data)
    for file in glob.glob(f"{dir}/Q_{i}*Vent.csv.gz"):
        # Read the CSV file with gzip compression
        data = pd.read_csv(file, sep=';', compression='gzip')
        
        # Convert the 'AAAAMMJJ' column to string to ensure proper filtering
        data['AAAAMMJJ'] = data['AAAAMMJJ'].astype(str)
        
        # Remove rows recorded before 2017
        data = data[data['AAAAMMJJ'].str[:4].astype(int) >= 2017]
        
        # Append the filtered data to the list
        dataframes_vent.append(data)
    
    # Concatenate all DataFrames in the list into a single DataFrame
    result_vent = pd.concat(dataframes_vent)
    

    # Initialize an empty list to hold DataFrames for 'autres-parametres' files
    dataframes_autre = []

    # Process each .csv.gz file for the current number (autres-parametres data)
    for file in glob.glob(f"{dir}/Q_{i}*autres-parametres.csv.gz"):
        # Read the CSV file with gzip compression
        data = pd.read_csv(file, sep=';', compression='gzip')
        
        # Convert the 'AAAAMMJJ' column to string to ensure proper filtering
        data['AAAAMMJJ'] = data['AAAAMMJJ'].astype(str)
        
        # Remove rows recorded before 2017
        data = data[data['AAAAMMJJ'].str[:4].astype(int) >= 2017]
        
        # Append the filtered data to the list
        dataframes_autre.append(data)
    
    # Concatenate all DataFrames in the list into a single DataFrame
    result_autre = pd.concat(dataframes_autre)
    
    # Merge the two DataFrames on the specified columns
    combined_df = pd.merge(result_autre, result_vent, how="right", on=["NUM_POSTE", "NOM_USUEL", "LAT", "LON", "ALTI", "AAAAMMJJ"])

    # Save the combined DataFrame to a CSV file
    combined_df.to_csv(f"{dir}/data_climate{i}_cleaned.csv", index=False)
