# JARVISH - AI Powered Naukri Job Applier

JARVISH is an automated, AI-driven bot that logs into [Naukri.com](https://www.naukri.com/), browses recommended jobs, and automatically applies on your behalf. 

What makes JARVISH special is its **AI Brain** (powered by LangChain and Groq). When it encounters a recruiter's questionnaire during the application process, it reads your `resume.txt` and uses an LLM to automatically read, reason, and answer the questions with the best possible options (or type out short answers). It also includes human-simulation features like random typing speeds, mouse movements, and hesitations to avoid bot detection.

## Features

- **Automated Job Applications**: Automatically scrolls, selects, and applies to jobs from your recommended feed.
- **AI Questionnaire Engine**: Detects dynamic recruiter questionnaires and uses AI to answer them intelligently based on your resume.
- **Human Simulation**: Simulates human mouse movements, scrolling, typing delays, and hesitations to stay undetected.
- **Caching**: Remembers answers to previously asked questions using a local SQLite cache to save on API usage.

## Prerequisites

- Python 3.8+
- A Groq API Key (for the LLM)
- A Naukri.com account

## Initial Setup

Follow these steps to set up the project on your local machine:

### 1. Configure Environment Variables
You need to provide the bot with your Naukri login credentials and your Groq API key.
1. Copy the `.env.template` file and rename it to `.env` (or just create a new `.env` file in the root directory).
2. Fill in your details:
   ```env
   NAUKRI_EMAIL="your_email@example.com"
   NAUKRI_PASSWORD="your_naukri_password"
   GROQ_API_KEY="your_groq_api_key"
   ```

### 2. Add Your Resume Context
Open the `resume.txt` file in the `data` folder and paste the plain text of your up-to-date resume. The AI will use this text to answer recruiter questions automatically during the application process.
If required adjust the `system_prompt.txt` file in the `data` folder according to your needs. This file contains the system prompt for the AI.

### 3. Setup Caching Database
To reduce calls to the LLM API and save costs, create an empty `db.json` file in the `data` folder. The bot will use this file to cache and reuse answers to previously asked recruiter questions.

### 4. Install Dependencies
It is highly recommended to use a Python virtual environment. Open your terminal in the project directory and run:

**On Windows:**
```powershell
# Create a virtual environment
python -m venv venv

# Activate it
.\venv\Scripts\activate

# Install the required Python packages
pip install -r requirements.txt

# Install Playwright browsers (required for web automation)
playwright install chromium
```

**On macOS/Linux:**
```bash
# Create a virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate

# Install the required Python packages
pip install -r requirements.txt

# Install Playwright browsers
playwright install chromium
```

## Running the Bot

Once your `.env` is configured and your dependencies are installed, make sure your virtual environment is activated, and start the bot:

```bash
python main.py
```

Sit back and watch the terminal logs as JARVISH logs in, navigates to your recommended jobs, and starts applying!
