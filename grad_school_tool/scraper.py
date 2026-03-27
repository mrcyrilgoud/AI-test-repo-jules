import re
import os
import json
import requests
import certifi
from bs4 import BeautifulSoup
from googlesearch import search
import google.generativeai as genai

# Fix for SSL certificate issues on macOS
os.environ["SSL_CERT_FILE"] = certifi.where()

# Custom Brave Search scraper to avoid library issues and blocking
def search_program_url(university, program):
    """
    Searches for the official graduate program page using Brave Search.
    """
    query = f"{university} {program} graduate program requirements admission"
    print(f"Searching for: {query}")
    
    url = "https://search.brave.com/search"
    params = {'q': query}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        # verify=False is used here because of persistent SSL certificate issues on macOS in this environment
        requests.packages.urllib3.disable_warnings()
        response = requests.get(url, params=params, headers=headers, timeout=10, verify=False)
        print(f"Search Status: {response.status_code}")
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find result links. Brave structure varies, so we look for valid external links.
        links = soup.find_all('a')
        
        for link in links:
            href = link.get('href')
            if href and href.startswith('http'):
                # Filter out internal Brave links and common ads/trackers if obvious
                if 'brave.com' not in href and 'search.brave.com' not in href:
                    print(f"Found link: {href}")
                    return href
                    
    except Exception as e:
        print(f"Search failed: {e}")
        
    return None

def extract_data_from_html(html_content, api_key, university, program):
    """
    Uses Google Gemini to extract structured data from HTML content.
    """
    if not api_key:
        print("No API key provided for extraction.")
        return None

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.0-flash')

    prompt = f"""
    You are an expert research assistant. I will provide you with the HTML content of a university graduate program page.
    Your task is to extract specific information about the {program} program at {university}.
    
    Please extract the following fields and return them as a JSON object:
    - "University": The name of the university (e.g., "{university}")
    - "Program": The name of the program (e.g., "{program}")
    - "Minimum GPA": The minimum GPA required for admission.
    - "GRE Required": Whether the GRE is required, optional, or not required.
    - "Required Coursework": Any specific prerequisite courses mentioned.
    - "Letters of Recommendation": The number of letters required.
    - "Faculty/Research Areas": Key research areas or faculty mentioned (summarize if list is long).
    - "Application Deadline": The application deadline for the next intake.
    - "Tuition": The cost of tuition (per year or total).
    - "Housing Cost": Estimated housing cost if available.

    If a piece of information is not found in the text, set the value to "Not found".
    Do not hallucinate. Only use information present in the text.
    
    HTML Content:
    {html_content[:30000]}  # Truncate to avoid token limits if necessary, though Flash has a large context window.
    """

    try:
        response = model.generate_content(prompt)
        # Clean up the response to ensure it's valid JSON
        text = response.text.strip()
        if text.startswith("```json"):
            text = text[7:-3]
        elif text.startswith("```"):
            text = text[3:-3]
        
        return json.loads(text)
    except Exception as e:
        print(f"LLM extraction failed: {e}")
        return None

def scrape_program(university_name, api_key=None):
    """
    Orchestrates the research process: Search -> Fetch -> Extract.
    """
    # Simple parsing of the input string to separate university and program if possible
    # This is a basic heuristic; the user input might be just "Stanford" or "Stanford CS"
    parts = university_name.split(" ", 1)
    university = parts[0]
    program = parts[1] if len(parts) > 1 else "Graduate Program"

    print(f"Researching: {university} - {program}")

    url = search_program_url(university, program)
    if not url:
        print("Could not find a URL for this program.")
        return {
            "University": university,
            "Program": program,
            "Error": "Could not find program page."
        }
    
    print(f"Found URL: {url}")

    try:
        # User-Agent header to avoid being blocked by some sites
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        # verify=False due to persistent SSL issues in this environment
        response = requests.get(url, headers=headers, timeout=10, verify=False)
        response.raise_for_status()
        
        # Parse HTML to remove scripts and styles for cleaner LLM input
        soup = BeautifulSoup(response.content, "html.parser")
        for script in soup(["script", "style"]):
            script.decompose()
        text_content = soup.get_text(separator=" ", strip=True)
        
        if api_key:
            data = extract_data_from_html(text_content, api_key, university, program)
            if data:
                data["Source URL"] = url # Add the source URL for reference
                return data
            else:
                 return {
                    "University": university,
                    "Program": program,
                    "Source URL": url,
                    "Error": "Failed to extract data with LLM."
                }
        else:
             return {
                "University": university,
                "Program": program,
                "Source URL": url,
                "Error": "Gemini API Key is missing. Please add it in Settings."
            }

    except Exception as e:
        print(f"Error fetching page: {e}")
        return {
            "University": university,
            "Program": program,
            "Source URL": url,
            "Error": f"Failed to fetch page: {str(e)}"
        }

if __name__ == "__main__":
    pass
