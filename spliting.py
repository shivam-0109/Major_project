import pandas as pd
import os

def split_csv(input_file, chunk_size_mb=15):
    # Load the CSV file
    df = pd.read_csv(input_file)

    # Get the number of rows in the file
    total_rows = len(df)
    
    # Get the chunk size in rows (approximate)
    rows_per_chunk = int(chunk_size_mb * 1024 * 1024 / df.memory_usage(index=False).sum() * total_rows)
    
    # Create the output directory if it doesn't exist
    output_dir = 'split_csvs'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Split the CSV into smaller files
    for i, start_row in enumerate(range(0, total_rows, rows_per_chunk)):
        chunk = df.iloc[start_row:start_row + rows_per_chunk]
        chunk.to_csv(f'{output_dir}/part_{i+1}.csv', index=False)
        print(f'Saved part_{i+1}.csv')

# Example usage
input_file = 'Water Quality Prediction.csv'  # Replace with your file name
split_csv(input_file)
