import gspread
import os

def get_spreadsheet(spreadsheet_name):
    """
    Authenticates with Google Sheets and returns a spreadsheet object.
    """
    credentials_path = os.path.join(os.path.expanduser('~'), '.config', 'gspread', 'credentials.json')
    if not os.path.exists(credentials_path):
        print("Could not find your Google API credentials.")
        print("Please follow these steps to get your credentials.json file:")
        print("1. Go to https://console.developers.google.com/ and create a new project.")
        print("2. Enable the Google Drive API and the Google Sheets API.")
        print("3. Create an OAuth 2.0 client ID for a Desktop application.")
        print("4. Download the JSON file and save it as credentials.json in this directory: ~/.config/gspread/")
        return None

    try:
        gc = gspread.oauth()
        spreadsheet = gc.create(spreadsheet_name)
        worksheet = spreadsheet.sheet1
        header_row = ["University", "Program", "Minimum GPA", "GRE Required", "Required Coursework", "Letters of Recommendation", "Faculty/Research Areas", "Application Deadline", "Tuition", "Housing Cost"]
        worksheet.append_row(header_row)
        return spreadsheet
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

if __name__ == '__main__':
    get_spreadsheet("Grad School Programs")
