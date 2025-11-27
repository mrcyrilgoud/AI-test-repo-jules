import json

from flask import Flask, redirect, render_template, request, url_for, Response
from scraper import scrape_program
from sheets import get_spreadsheet
from local_sheets import save_to_csv
import io
import csv

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/settings")
def settings():
    local_path = ""
    gemini_api_key = ""
    try:
        with open("settings.json", "r") as f:
            settings_data = json.load(f)
            local_path = settings_data.get("local_path", "")
            gemini_api_key = settings_data.get("gemini_api_key", "")
    except FileNotFoundError:
        pass
    return render_template("settings.html", local_path=local_path, gemini_api_key=gemini_api_key)


@app.route("/save_settings", methods=["POST"])
def save_settings():
    credentials = request.form.get("credentials", "")
    local_path = request.form.get("local_path", "")
    gemini_api_key = request.form.get("gemini_api_key", "")
    
    # Save local settings
    settings_data = {
        "local_path": local_path,
        "gemini_api_key": gemini_api_key
    }
    with open("settings.json", "w") as f:
        json.dump(settings_data, f)

    try:
        # Validate that the credentials are valid JSON if provided
        if credentials.strip():
            json.loads(credentials)
            with open("credentials.json", "w") as f:
                f.write(credentials)
        return redirect(url_for("index"))
    except json.JSONDecodeError:
        return (
            "Invalid JSON format. Please go back and paste the correct content from your credentials.json file.",
            400,
        )


@app.route("/submit", methods=["POST"])
def submit():
    universities_input = request.form["universities"]
    action = request.form.get("action", "visualize")
    
    universities_list = [
        uni.strip() for uni in universities_input.splitlines() if uni.strip()
    ]

    # Load API Key
    gemini_api_key = ""
    try:
        with open("settings.json", "r") as f:
            settings_data = json.load(f)
            gemini_api_key = settings_data.get("gemini_api_key", "")
    except FileNotFoundError:
        pass

    scraped_results = []
    for university in universities_list:
        data = scrape_program(university, gemini_api_key)
        if data:
            scraped_results.append(data)

    if action == "visualize":
        return render_template("results.html", results=scraped_results)
    
    elif action == "download":
        if not scraped_results:
             return "No data found to download."
        
        # Create CSV in memory
        output = io.StringIO()
        if scraped_results:
            writer = csv.DictWriter(output, fieldnames=scraped_results[0].keys())
            writer.writeheader()
            writer.writerows(scraped_results)
        
        return Response(
            output.getvalue(),
            mimetype="text/csv",
            headers={"Content-disposition": "attachment; filename=grad_school_results.csv"}
        )

    elif action == "save_local":
        local_path = ""
        try:
            with open("settings.json", "r") as f:
                local_path = json.load(f).get("local_path", "")
        except FileNotFoundError:
            pass
            
        if not local_path:
             return "No local path configured. Please go to <a href='/settings'>Settings</a> to set a local spreadsheet path."
        
        success, message = save_to_csv(scraped_results, local_path)
        return message

    elif action == "save":
        spreadsheet = get_spreadsheet("Grad School Programs")
        if spreadsheet:
            worksheet = spreadsheet.sheet1
            for data in scraped_results:
                worksheet.append_row(list(data.values()))
            return f"Successfully created and updated spreadsheet: <a href='{spreadsheet.url}' target='_blank'>{spreadsheet.title}</a>"
        else:
            return "Failed to create spreadsheet. Please make sure your Google Drive credentials are set correctly in the <a href='/settings'>settings page</a>."


if __name__ == "__main__":
    app.run(debug=True)
