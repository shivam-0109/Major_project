import pandas as pd

def compare_csv(file1, file2):
    # Read both CSV files into DataFrames
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)

    # Find rows that are in df1 but not in df2
    diff1 = pd.concat([df1, df2, df2]).drop_duplicates(keep=False)

    # Find rows that are in df2 but not in df1
    diff2 = pd.concat([df2, df1, df1]).drop_duplicates(keep=False)

    # Combine both differences into one DataFrame
    diff = pd.concat([diff1, diff2], ignore_index=True)

    return diff

# Example usage
file1 = 'merged_Water_Quality_Prediction.csv'  # Replace with your first CSV file
file2 = 'Water Quality Prediction.csv'  # Replace with your second CSV file

difference = compare_csv(file1, file2)

# Save the differences to a new CSV
difference.to_csv('differences.csv', index=False)

print("Differences have been saved to 'differences.csv'")
