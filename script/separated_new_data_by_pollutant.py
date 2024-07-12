import glob
import os
import pandas as pd

csv_files = glob.glob( "C:/Users/Administrateur/Documents/talend/data/csv/*.csv" ) 


# Open the first csv file to get the pollutant list
df_init = pd.read_csv(csv_files[0], sep=";")
# Get unique pollutants in the file

pollutants = df_init['Polluant'].unique()

print( pollutants)

col = list(df_init.columns.values)
print( col )
# Remove 'Polluant' and 'value' from the columns name list
for i in [ 'Organisme', 'Polluant','type d\'influence','discriminant','type d\'évaluation', 'code zas', 'Zas',  'valeur', 'Réglementaire', 'procédure de mesure','type de valeur','valeur brute','unité de mesure','taux de saisie','couverture temporelle','couverture de données','code qualité','validité' ]:
    col.remove(i)


# Process each pollutant
for pollutant in pollutants:
    print(f"Process {pollutant}")
    pollutant_df = pd.DataFrame(columns=col)
    i = 0 
    for file in csv_files:
        print( f"{ i * 100 / len(csv_files)}%                       ", end="\r")
        i = i+1
        # Read the CSV file
        df = pd.read_csv(file, sep=";")
        
        # Filter the DataFrame for the specific pollutant
        df_with_only_pollutant = df[df['Polluant'] == pollutant]
        
        # Create a new column with the pollutant name and set its values
        df_with_only_pollutant = df_with_only_pollutant.loc[:, col]
        df_with_only_pollutant[pollutant] = df[df['Polluant'] == pollutant]['valeur'].values
        
        # Append the DataFrame to the corresponding pollutant DataFrame
        pollutant_df  = pd.concat([pollutant_df, df_with_only_pollutant], ignore_index=True)
    
    # Save the concatenated DataFrame to a new CSV file
    output_file = f"C:/Users/Administrateur/Documents/newdata{pollutant}_combined.csv"
    pollutant_df.to_csv(output_file, index=False)


print("Processing complete.")

