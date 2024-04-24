import pandas as pd

def calculate_mean_and_std(file_path):
    # Read Excel file into a pandas DataFrame
    df = pd.read_excel(file_path)
    
    # Iterate through each row in the DataFrame
    for index, row in df.iterrows():
        # Calculate mean and standard deviation for each row
        mean = row.mean()
        std_dev = row.std()
        
        # Print mean and standard deviation for each row
        print(f"Row {index + 1}: Mean = {mean}, Standard Deviation = {std_dev}")

# Example usage:
file_path = 'Data\Inverse_square_22_secondTakeNa.xlsx'  # Path to your Excel file
calculate_mean_and_std(file_path)