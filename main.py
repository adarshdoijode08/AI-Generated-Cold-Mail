from app.main import create_streamlit_app
from app.chains import Chain
from app.portfolio import Portfolio
from app.utils import clean_text

if __name__ == '__main__':
    chain = Chain()
    portfolio = Portfolio()
    create_streamlit_app(chain, portfolio, clean_text)
