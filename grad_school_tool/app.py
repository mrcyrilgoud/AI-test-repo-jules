import json

from flask import Flask, redirect, render_template, request, url_for
from scraper import scrape_program
from sheets import get_spreadsheet

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/settings")
def settings():
    return render_template("settings.html")


@app.route("/save_settings", methods=["POST"])
def save_settings():
    credentials = request.form["credentials"]
    try:
        # Validate that the credentials are valid JSON
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

    scraped_results = []
    for university in universities_list:
        data = scrape_program(university)
        if data:
            scraped_results.append(data)

    if action == "visualize":
        return render_template("results.html", results=scraped_results)
    
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
