import newspaper
from openai import OpenAI
import os
import streamlit as st
from dotenv import load_dotenv, find_dotenv
from datetime import datetime

load_dotenv(find_dotenv('.env'))

api_key = os.environ.get("OPENAI_API_KEY")
MODEL="gpt-4o-mini"


def generate_analysis(article_date, article_text):
    client = OpenAI(api_key=api_key)
    completion = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are an expert financial analyst with deep knowledge of market trends and stock price predictions."},
            {"role": "user", "content": f"Please analyze the following news article published on {article_date} if the news article is too old from the current date {datetime.now()} so avoid replying politely. Provide a detailed impact analysis of the news on the stock price of the company. Please explain in the simple language Finally, based on your analysis, recommend whether to Buy, Sell, or Hold the stock: \n\n{article_text}"
                                        f"Provide details in separate section"
                                        f"Company Name, Published Date"}
        ]
    )

    return completion.choices[0].message.content


def scrape_article(url):
    article = newspaper.article(url)
    published_date = article.publish_date
    published_text = article.text
    return published_text, published_date


def main():
    st.title("Stock News Analysis")
    url = st.text_input("Enter News Article URL:")
    if url:
        with st.spinner("Scraping and analyzing..."):
            try:
                article_date, article_text = scrape_article(url)
                analysis = generate_analysis(article_date, article_text)
                st.subheader("Detailed Analysis")
                st.write(analysis)
            except Exception as e:
                st.error(f"Error: {str(e)}")


if __name__ == "__main__":
    main()