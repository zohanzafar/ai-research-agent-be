# AI Research Agent

This project helps users create research reports using an AI Agent. Users enter a topic, and the system creates a structured report with REST API endpoints for accessing and managing reports. The AI Agent uses OpenAI's API and Wikipedia to gather information.

## Features

- Generates research reports with sections like scope, design, literature, and ethics
- Saves all research reports in the database
- Exports research reports to PDF and CSV

## How It Works

1. User enters a keyword.
2. The system fetches related information from Wikipedia.
3. It sends a structured prompt to OpenAI to create the report.
4. The response is stored in the database.
5. Users can view, download, or export the research reports via REST API endpoints.

## AI Agent

The AI agent is in `agent.py`. It builds prompts using Wikipedia data and sends them to OpenAI. It also formats the response into sections.

## History

All reports are saved in the database. This allows users to see past results and export them if needed.

## Setup

```bash
git clone https://github.com/zohanzafar/ai_research_agent_be.git
cd ai_research_agent_be
python3 -m venv venv
source venv/bin/activate  # For Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

### Sample .env File

Create a `.env` file in the project root with the following content:

```
# Keys
OPENAI_API_KEY=your_openai_api_key
SECRET_KEY=your_secure_django_secret_key

# DEBUG
DEBUG=False

# Allowed Hosts
ALLOWED_HOSTS=yourdomain.com,localhost

# CORS Config
CORS_ALLOWED_ORIGINS=https://yourfrontend.com
CORS_ALLOW_CREDENTIALS=True

# PostgreSQL Database
POSTGRES_DB=your_database_name
POSTGRES_USER=your_database_user
POSTGRES_PASSWORD=your_database_password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

```

Replace `your_openai_api_key`, `your_secure_django_secret_key`, `postgres database_settings` and `yourdomain.com` with your actual values. For local development, you can use `DEBUG=True` and `CORS_ALLOWED_ORIGINS=http://localhost:3000`.

## Output Format

Each report has these fields:

- Keyword
- Scope
- Design
- Literature
- Analysis
- Discussion
- Ethics
- References

## API Endpoints

GET /api/v1/research/
→ List all research records.

POST /api/v1/research/
→ Create a new research record.

POST /api/v1/research/generate/
→ Generate research content using the AI agent (based on a keyword).

GET /api/v1/research/<id>/
→ Retrieve details of a single research record by ID.

DELETE /api/v1/research/<id>/
→ Delete a specific research record by ID.

GET /api/v1/research/<id>/download-pdf/
→ Download the research report as a structured PDF file.

GET /api/v1/research/download-csv/
→ Download all research records as a CSV file.

## Notes

This project only contains the backend. The backend includes REST API endpoints for report management, and the logic is organized in functions that can be used in any interface.