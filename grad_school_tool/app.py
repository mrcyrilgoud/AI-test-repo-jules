from flask import Flask, render_template, request
from sheets import get_spreadsheet
from scraper import scrape_program

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    universities_input = request.form['universities']
    universities_list = [uni.strip() for uni in universities_input.split('\\n') if uni.strip()]

    spreadsheet = get_spreadsheet("Grad School Programs")
    if spreadsheet:
        worksheet = spreadsheet.sheet1
        for university in universities_list:
            scraped_data = scrape_program(university)
            if scraped_data:
                worksheet.append_row(list(scraped_data.values()))
        return f"Successfully created and updated spreadsheet: {spreadsheet.title}"
    else:
        return "Failed to create spreadsheet."


if __name__ == '__main__':
    app.run(debug=True)
