import pandas as pd
import glob

# Get a list of all CSV files
csv_files = glob.glob("C:/Users/Administrateur/Documents/intermediate_csvs/intermediate_*.csv")

# Bip bip init
# Open the first csv file to get the pollutant list
df_init = pd.read_csv(csv_files[0])
# Get unique pollutants in the file
pollutants = df_init['Polluant'].unique()
col = list(df_init.columns.values)
# Remove 'Polluant' and 'value' from the columns name list
col.remove('Polluant')
col.remove('value')

# Process each pollutant
for pollutant in pollutants:
    print(f"Process {pollutant}")
    pollutant_df = pd.DataFrame(columns=col)
    for file in csv_files:
        print(f"Read {file}")
        # Read the CSV file
        df = pd.read_csv(file)
        
        # Filter the DataFrame for the specific pollutant
        df_with_only_pollutant = df[df['Polluant'] == pollutant]
        
        # Create a new column with the pollutant name and set its values
        df_with_only_pollutant = df_with_only_pollutant.loc[:, col]
        df_with_only_pollutant[pollutant] = df[df['Polluant'] == pollutant]['value'].values
        
        # Append the DataFrame to the corresponding pollutant DataFrame
        pollutant_df  = pd.concat([pollutant_df, df_with_only_pollutant], ignore_index=True)
    
    # Save the concatenated DataFrame to a new CSV file
    output_file = f"C:/Users/Administrateur/Documents/intermediate_csvs/{pollutant}_combined.csv"
    pollutant_df.to_csv(output_file, index=False)

print("Processing complete.")