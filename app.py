from fastapi import FastAPI, HTTPException
import logging
import pandas as pd

from naver_api import fetch_news_data
from crawler import crawl_article_content
from tech_classifier import filter_tech_articles
from similarity import similarity
from job_classifier import classify_article
from summarizer import create_detailed_articles
# from word_duplication import check_and_remove_terms

app = FastAPI()


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_tech_words(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        tech_words = [line.strip() for line in f.readlines()]
    return tech_words

tech_words = load_tech_words('tech_words.txt')

@app.get("/")
def read_root():
    return {"message": "Welcome to the tech news classifier API"}


@app.get("/process_articles/")
def process_articles():
    try:
        # 뉴스 데이터 가져오기
        news = fetch_news_data(client_id, client_secret)
        logger.info(f"Fetched news data: {news.head()}")
        if news.empty:
            raise HTTPException(status_code=404, detail="No News")

        # 제목을 통한 유사도 필터
        unique_news = similarity(news)
        logger.info(f"Unique news data: {unique_news.head()}")
        if unique_news.empty:
            raise HTTPException(status_code=404, detail="No News")

        # 본문 가져오기
        origin_content = [''] * len(unique_news)
        for i in range(len(unique_news)):
            origin_content[i] = crawl_article_content(unique_news.loc[i, 'link'])
        unique_news['origin_content'] = origin_content
        logger.info(f"News with content: {unique_news.head()}")

        # 테크 기사 분류
        filter_news = filter_tech_articles(unique_news, tech_words)
        logger.info(f"Filtered tech news: {filter_news.head()}")
        if filter_news.empty:
            raise HTTPException(status_code=404, detail="No News")

        # 라벨 분류
        job_label = [''] * len(filter_news)
        for i in range(len(filter_news)):
            job_label[i] = classify_article(filter_news.loc[i, 'origin_content'])
        filter_news['label'] = job_label
        logger.info(f"Labeled news: {filter_news.head()}")

        # 아티클 생성
        articles = create_detailed_articles(filter_news)
        logger.info(f"Created articles: {articles.head()}")

        # # DB조회 및 중복 용어 제거
        # articles = check_and_remove_terms(articles)
        # logger.info(f"Articles after removing duplicates: {articles.head()}")

        # JSON 변환
        result_json = articles.to_json(orient='records', force_ascii=False)

        return result_json

    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

