import os

import gspread


def get_spreadsheet(spreadsheet_name):
    """
    Authenticates with Google Sheets using a local credentials.json
    and returns a spreadsheet object.
    """
    credentials_path = "credentials.json"
    if not os.path.exists(credentials_path):
        print("Could not find your credentials.json file in the project directory.")
        print("Please go to the settings page to upload your Google API credentials.")
        return None

    try:
        gc = gspread.service_account(filename=credentials_path)
        try:
            spreadsheet = gc.open(spreadsheet_name)
        except gspread.SpreadsheetNotFound:
            spreadsheet = gc.create(spreadsheet_name)
        worksheet = spreadsheet.sheet1
        # Check if the worksheet is empty before writing the header
        if not worksheet.get_all_values():
            header_row = [
                "University",
                "Program",
                "Minimum GPA",
                "GRE Required",
                "Required Coursework",
                "Letters of Recommendation",
                "Faculty/Research Areas",
                "Application Deadline",
                "Tuition",
                "Housing Cost",
            ]
            worksheet.append_row(header_row)
        # Share the spreadsheet with a user
        # spreadsheet.share('user@example.com', perm_type='user', role='writer')
        print(
            f"Spreadsheet '{spreadsheet_name}' is ready. You can find it here: {spreadsheet.url}"
        )
        return spreadsheet
    except Exception as e:
        print(f"An error occurred while accessing the spreadsheet: {e}")
        return None


if __name__ == "__main__":
    # This is for testing the module directly
    get_spreadsheet("Grad School Programs Test")
