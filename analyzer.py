import os
import json
import google.generativeai as genai

def analyze_emails_batch(emails_data):
    """
    Sends a batch of emails to the Gemini API for analysis.
    Returns a list of emails with added analysis fields.
    """
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY not found in environment variables.")
        return emails_data # Return original data if no key

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')

    analyzed_emails = []

    for email in emails_data:
        prompt = f"""
        You are an intelligent email assistant for a busy professional. Analyze the following email content and provide a structured assessment in JSON format.

        **Criteria:**
        1. **Content Value (1-10):** How valuable is this email? Consider VIP senders, important topics, financial opportunities, or urgent projects as high value.
        2. **Severity (1-10):** How critical is the impact on the user? High severity implies negative consequences if ignored (e.g., angry customer, system outage).
        3. **Recommended Response Time:** Suggest a timeframe (e.g., "Immediate", "By EOD", "Next Week", "No Action Needed").
        4. **Reasoning:** A brief explanation (1 sentence) for your assessment.

        **Email Content:**
        Subject: {email['subject']}
        Sender: {email['sender']}
        Body: {email['body'][:1000]} (truncated)

        **Output Format (Strict JSON):**
        {{
            "content_value": <int>,
            "severity": <int>,
            "response_time": "<string>",
            "reasoning": "<string>"
        }}
        """

        try:
            response = model.generate_content(prompt)
            # Basic cleanup to ensure we get just the JSON string if Gemini adds markdown
            text_response = response.text.strip()
            if text_response.startswith("```json"):
                text_response = text_response[7:-3]
            elif text_response.startswith("```"):
                text_response = text_response[3:-3]

            analysis = json.loads(text_response)

            # Merge analysis into the email object
            email.update(analysis)

            # Calculate a simple priority score
            email['urgency_score'] = email.get('content_value', 0) * email.get('severity', 0)

        except Exception as e:
            print(f"Error analyzing email {email['id']}: {e}")
            # Add default values on error
            email.update({
                "content_value": 0,
                "severity": 0,
                "response_time": "Analysis Failed",
                "reasoning": "Could not process this email.",
                "urgency_score": 0
            })

        analyzed_emails.append(email)

    # Sort by Urgency Score (Descending)
    analyzed_emails.sort(key=lambda x: x.get('urgency_score', 0), reverse=True)

    return analyzed_emails
