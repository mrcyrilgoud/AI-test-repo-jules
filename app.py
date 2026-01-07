import os
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import helper modules
import auth
import gmail_service
import analyzer

app = Flask(__name__)
app.secret_key = os.urandom(24) # Used for session management

# Allow OAuth over HTTP for local testing
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

@app.route('/')
def index():
    if 'credentials' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/login')
def login():
    # Create the flow using the helper from auth.py
    # We use url_for to dynamically get the callback URL
    redirect_uri = url_for('callback', _external=True)
    flow = auth.get_flow(redirect_uri)

    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true'
    )

    session['state'] = state
    return redirect(authorization_url)

@app.route('/callback')
def callback():
    state = session.get('state')

    redirect_uri = url_for('callback', _external=True)
    flow = auth.get_flow(redirect_uri)

    flow.fetch_token(authorization_response=request.url)

    credentials = flow.credentials
    session['credentials'] = auth.credentials_to_dict(credentials)

    return redirect(url_for('index'))

@app.route('/api/emails')
def get_emails():
    if 'credentials' not in session:
        return jsonify({'error': 'Not authenticated'}), 401

    try:
        # 1. Rebuild the Gmail Service
        service = gmail_service.get_gmail_service(session['credentials'])

        # 2. Fetch Emails
        raw_emails = gmail_service.fetch_recent_emails(service, max_results=10)

        # 3. Analyze Emails
        analyzed_emails = analyzer.analyze_emails_batch(raw_emails)

        return jsonify(analyzed_emails)

    except Exception as e:
        print(f"API Error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
