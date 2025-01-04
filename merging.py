import pandas as pd
import os

def merge_csv(output_file, input_dir='split_csvs'):
    # Get all the CSV files in the directory
    files = sorted([f for f in os.listdir(input_dir) if f.endswith('.csv')])

    # Initialize an empty DataFrame to concatenate
    combined_df = pd.DataFrame()

    # Read and concatenate each CSV file
    for file in files:
        df = pd.read_csv(os.path.join(input_dir, file))
        combined_df = pd.concat([combined_df, df], ignore_index=True)
        print(f'Merged {file}')
    
    # Save the merged DataFrame to a new CSV
    combined_df.to_csv(output_file, index=False)
    print(f'Merged CSV saved to {output_file}')

# Example usage
output_file = 'merged_Water_Quality_Prediction.csv'  # Name of the merged file
merge_csv(output_file)
