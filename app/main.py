import requests
import streamlit as st
from bs4 import BeautifulSoup
from langchain_community.document_loaders import WebBaseLoader
from app.chains import Chain
from app.portfolio import Portfolio
from app.utils import clean_text


def render_portfolio_links(links):
    if not links:
        st.write('No matching portfolio links found.')
        return
    for index, link in enumerate(links, start=1):
        st.markdown(f'{index}. [{link}]({link})')


def load_url_text(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (compatible; Bot/1.0)'}
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        page = BeautifulSoup(response.text, 'html.parser')
        return page.get_text(separator=' ', strip=True)
    except Exception:
        return ''


def create_streamlit_app(llm, portfolio, clean_text):
    st.set_page_config(layout='wide', page_title='Cold Email Generator', page_icon='📧')
    st.title('📧 Cold Email Generator')
    st.write('Generate a personalized cold email by entering a job page URL or pasting the job description text.')

    with st.form('cold_email_form'):
        source_type = st.radio('Input type', ['URL', 'Text'], horizontal=True)
        if source_type == 'URL':
            url_input = st.text_input('Job page URL', value='https://jobs.nike.com/job/R-33460')
            text_input = ''
        else:
            url_input = ''
            text_input = st.text_area('Paste the job description text', height=240)

        company_name = st.text_input('Your company name', value='ABC')
        recipient_role = st.text_input('Recipient role', value='Hiring Manager')
        submit_button = st.form_submit_button('Generate email')

    if submit_button:
        if source_type == 'URL' and not url_input:
            st.error('Please enter a valid URL.')
            return
        if source_type == 'Text' and not text_input:
            st.error('Please paste the job description text.')
            return

        try:
            raw_content = ''
            if source_type == 'URL':
                try:
                    loader = WebBaseLoader([url_input])
                    pages = loader.load()
                    raw_content = pages[0].page_content if pages else ''
                except Exception:
                    raw_content = ''

                if not raw_content:
                    raw_content = load_url_text(url_input)
            else:
                raw_content = text_input

            cleaned = clean_text(raw_content)
            if not cleaned:
                st.error('No readable text was found. Please provide a valid URL or job description.')
                return

            portfolio.load_portfolio()
            jobs = llm.extract_jobs(cleaned)

            if not jobs:
                st.warning('No jobs were extracted from the provided content.')
                return

            for idx, job in enumerate(jobs, start=1):
                st.markdown('---')
                st.subheader(f'Job #{idx}: {job.get("role", "Unknown role")}')
                cols = st.columns([2, 1])
                with cols[0]:
                    st.markdown('**Experience**')
                    st.write(job.get('experience', 'N/A'))
                    st.markdown('**Skills**')
                    skills = job.get('skills', [])
                    st.write(', '.join(skills) if skills else 'N/A')
                    st.markdown('**Description**')
                    st.write(job.get('description', 'N/A'))
                with cols[1]:
                    st.markdown('**Suggested portfolio links**')
                    links = portfolio.query_links(skills if skills else job.get('description', ''))
                    render_portfolio_links(links)

                email = llm.write_mail(job, links, company_name, recipient_role)
                st.markdown('**Generated cold email**')
                st.code(email, language='markdown')

        except Exception as exc:
            st.error(f'An Error Occurred: {exc}')


if __name__ == '__main__':
    chain = Chain()
    portfolio = Portfolio()
    create_streamlit_app(chain, portfolio, clean_text)
