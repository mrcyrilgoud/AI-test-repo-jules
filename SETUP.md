# Email Command Center Setup Guide

This guide will help you set up the AI Email Command Center prototype on your local machine.

## Prerequisites
- **Python 3.8+** installed.
- A **Google Cloud Platform (GCP)** account.
- A **Gemini API Key**.

---

## Step 1: Google Cloud Project Setup (for Gmail API)

1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project (e.g., "Email-Command-Center").
3. **Enable Gmail API:**
   - In the search bar, type "Gmail API" and select it.
   - Click **Enable**.
4. **Configure OAuth Consent Screen:**
   - Go to **APIs & Services > OAuth consent screen**.
   - Select **External** (unless you have a Google Workspace organization, then Internal is fine).
   - Fill in the required fields (App Name, Support Email).
   - **Scopes:** Add `https://www.googleapis.com/auth/gmail.readonly`.
   - **Test Users:** Add your own email address so you can log in during development.
5. **Create Credentials:**
   - Go to **APIs & Services > Credentials**.
   - Click **Create Credentials > OAuth client ID**.
   - Application Type: **Web application**.
   - **Authorized redirect URIs:** Add `http://localhost:5000/callback`.
   - Click **Create**.
   - Copy the **Client ID** and **Client Secret**.

## Step 2: Gemini API Setup

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey).
2. Click **Create API Key**.
3. Copy the key.

## Step 3: Local Configuration

1. Create a `.env` file in the root directory (you can copy `.env.template`):
   ```bash
   cp .env.template .env
   ```
2. Open `.env` and paste your credentials:
   ```
   GOOGLE_CLIENT_ID=your_client_id_from_step_1
   GOOGLE_CLIENT_SECRET=your_client_secret_from_step_1
   GEMINI_API_KEY=your_api_key_from_step_2
   ```

## Step 4: Install Dependencies & Run

1. Install the Python packages:
   ```bash
   pip install -r requirements.txt
   ```
2. Start the application:
   ```bash
   python app.py
   ```
3. Open your browser and go to `http://localhost:5000`.
4. Click the **Connect with Gmail** button (or it will redirect you automatically) and log in.

**Note:** Since this is a test app, Google might show a "Google hasn't verified this app" warning screen. Click **Advanced > Go to (App Name) (unsafe)** to proceed.
