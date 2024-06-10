import glob
import pandas as pd
import pickle
import os

print("Go")
# List pickle files
list_chunk = glob.glob("data_chunk*.pkl")
print(len(list_chunk))

# Directory for intermediate CSV files
intermediate_dir = "intermediate_csvs"
os.makedirs(intermediate_dir, exist_ok=True)

# Parameters for intermediate saving
max_rows_per_file = 3000000  # Adjust this number based on your memory limits
current_rows = 0
file_count = 0

# Initialize an empty DataFrame for combining chunks
combined_df = pd.DataFrame()

# Process each pickle file one at a time
for i, file in enumerate(list_chunk):
    with open(file, 'rb') as f:
        chunk_data = pickle.load(f)
        chunk_df = pd.DataFrame(chunk_data)
        combined_df = pd.concat([combined_df, chunk_df], ignore_index=True)
        current_rows += len(chunk_df)

    # If current combined data exceeds the maximum rows, save it to a CSV file
    if current_rows >= max_rows_per_file:
        combined_df.to_csv(os.path.join(intermediate_dir, f"intermediate_{file_count}.csv"), index=False)
        combined_df = pd.DataFrame()  # Reset combined DataFrame
        current_rows = 0
        file_count += 1
        print(f"Saved intermediate file {file_count}")

# Save any remaining data after processing all files
if not combined_df.empty:
    combined_df.to_csv(os.path.join(intermediate_dir, f"intermediate_{file_count}.csv"), index=False)
    print(f"Saved final intermediate file {file_count} (last)")

# Combine all intermediate CSV files into the final DataFrame
print("Create final Dataframe")
all_data = []
for csv_file in glob.glob(os.path.join(intermediate_dir, "*.csv")):
    print( f"Loading {csv_file}")
    all_data.append(pd.read_csv(csv_file))

final_df = pd.concat(all_data, ignore_index=True)


# Sort the final DataFrame
final_df = final_df.sort_values(by=['id', 'Polluant', "start"])

# Save the final DataFrame to a CSV file
final_df.to_csv("data_pollutant_from_xml.csv", index=False)

# Clean up intermediate files
for csv_file in glob.glob(os.path.join(intermediate_dir, "*.csv")):
    os.remove(csv_file)
os.rmdir(intermediate_dir)
