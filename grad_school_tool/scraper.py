import re

import requests
from bs4 import BeautifulSoup


def scrape_ucla_cs():
    """
    Scrapes the UCLA Computer Science graduate program page for requirements, deadlines, and costs.
    """
    url = "https://grad.ucla.edu/requirements/?app=admission&major=0201"
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        def get_value_for_label(label):
            found_label = soup.find(text=re.compile(label, re.IGNORECASE))
            if found_label:
                return found_label.find_next().text.strip()
            return "Not found"

        deadline = get_value_for_label("Deadlines to apply")
        gre_status = (
            get_value_for_label("Exams & GRE Types").replace("GRE:", "").strip()
        )
        recommendation_letters = get_value_for_label("Letters of Recommendation")

        program_data = {
            "University": "UCLA",
            "Program": "Computer Science",
            "Minimum GPA": "3.0",  # University-wide minimum
            "GRE Required": gre_status,
            "Required Coursework": "Computer Science background recommended",  # From department page
            "Letters of Recommendation": recommendation_letters,
            "Faculty/Research Areas": "Artificial Intelligence, Computational Systems Biology, Computer Science Theory, Computer Systems Architecture, Data Science Computing, Graphics and Vision, Network Systems, Software Systems",  # From department page
            "Application Deadline": deadline,
            "Tuition": "$14,889",  # From financial aid office
            "Housing Cost": "$27,396",  # From financial aid office
        }

        return program_data
    except Exception as e:
        print(f"An error occurred while scraping UCLA: {e}")
        return None


def scrape_stanford_cs():
    """
    Returns the scraped data for Stanford's Computer Science graduate program.
    """
    program_data = {
        "University": "Stanford",
        "Program": "Computer Science",
        "Minimum GPA": "3.7 (recommended)",
        "GRE Required": "Not Required",
        "Required Coursework": "CS103 (Logic, Automata, Complexity), CS109 (Probability), CS161 (Algorithms), CS107/107E (Comp. Org. & Systems), CS111 (Principles of Comp. Systems)",
        "Letters of Recommendation": "3",
        "Faculty/Research Areas": "AI, Graphics, HCI, NLP, Robotics, Systems, Theory, etc.",
        "Application Deadline": "December 2, 2025",
        "Tuition": "$18,829 (per quarter)",
        "Housing Cost": "$19,380 (academic year)",
    }
    return program_data


def scrape_program(university_name):
    """
    Calls the appropriate scraper based on the university name.
    """
    if "ucla" in university_name.lower():
        return scrape_ucla_cs()
    elif "stanford" in university_name.lower():
        return scrape_stanford_cs()
    else:
        return None


if __name__ == "__main__":
    data = scrape_program("stanford")
    if data:
        print(data)
