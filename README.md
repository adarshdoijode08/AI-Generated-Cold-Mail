# AI-Generated-Cold-Mail

# Cold Sales Email Generator

A Streamlit application that generates professional cold emails based on a job posting URL or pasted job description text. The app extracts relevant job details, matches skills with portfolio links from a CSV dataset, and produces a polished outreach email.

## Features

- Accepts a job posting URL or manual job description text
- Uses `WebBaseLoader` from `langchain_community` to scrape URL text
- Falls back to raw HTML scraping via `requests` and `BeautifulSoup` when needed
- Extracts role, experience, and skills from the job description
- Queries a portfolio dataset (`app/resource/my_portfolio.csv`) to recommend related links
- Generates a professional cold email template

## Repository structure

- `main.py` - Launches the Streamlit app
- `app/main.py` - Streamlit application UI and workflow
- `app/chains.py` - Job extraction and email generation logic
- `app/portfolio.py` - Portfolio loading and matching logic using ChromaDB
- `app/utils.py` - Text cleaning helper
- `app/resource/my_portfolio.csv` - Portfolio dataset used for link recommendations
- `.gitignore` - Local files excluded from version control

## Setup

1. Create and activate a Python virtual environment in the project folder:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
python3 -m pip install -r requirements.txt
```

> If `requirements.txt` is not present, install at least:
> `streamlit`, `beautifulsoup4`, `lxml`, `langchain-community`, `chromadb`, `pandas`, `requests`

3. Install additional dependencies if needed:

```bash
python3 -m pip install streamlit beautifulsoup4 lxml langchain-community chromadb pandas requests
```

## Run the app

From the project root:

```bash
.venv/bin/streamlit run main.py
```

Then open the URL shown in the Streamlit console output.

## Usage

1. Choose `URL` or `Text` input mode.
2. Enter a job posting URL or paste the job description.
3. Enter your company name (default: `ABC`).
4. Enter the recipient role.
5. Click `Generate email`.

The app will:

- scrape the job posting text
- clean the text
- extract job role, experience, and skills
- query the portfolio dataset for related links
- display portfolio link suggestions
- generate a professional cold email

## Notes

- The portfolio matching uses a local ChromaDB collection stored in `vectorstore/`.
- `langchain-community` is used for `WebBaseLoader`, but the package is currently deprecated in favor of more modern standalone integrations. Use it with that in mind.
- The app falls back to HTML scraping if `WebBaseLoader` fails to load a URL.
- `company_name` default is set to `ABC`.

## Troubleshooting

- If the app cannot import `langchain_community`, install it in the active environment:
  `python3 -m pip install langchain-community`
- If `bs4` is missing, install `beautifulsoup4`:
  `python3 -m pip install beautifulsoup4 lxml`
- If portfolio links do not show, ensure `app/resource/my_portfolio.csv` contains valid `Techstack` and `Links` columns.

## Development

- Update `app/chains.py` to improve email generation quality
- Update `app/portfolio.py` to change portfolio matching logic
- Update `app/utils.py` to refine text cleaning rules

## License

This repository does not include a formal license file. Add one if you want to share this project publicly.
