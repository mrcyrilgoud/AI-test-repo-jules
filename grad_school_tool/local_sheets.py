import csv
import os

def save_to_csv(data_list, file_path):
    """
    Appends a list of dictionaries to a CSV file.
    Creates the file with headers if it doesn't exist.
    """
    if not data_list:
        return False, "No data to save."

    try:
        # Check if file exists to determine if we need to write headers
        file_exists = os.path.isfile(file_path)
        
        # Get headers from the first dictionary
        headers = list(data_list[0].keys())

        with open(file_path, mode='a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=headers)

            if not file_exists:
                writer.writeheader()

            for data in data_list:
                writer.writerow(data)
                
        return True, f"Successfully saved to {file_path}"
    except Exception as e:
        return False, f"Error saving to local file: {str(e)}"
