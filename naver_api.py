import requests
import datetime
import pandas as pd
from urllib.parse import urlparse

def fetch_news_data(client_id, client_secret):

    today = datetime.datetime.now().strftime('%a, %d %b %Y')  # 뉴스의 pubDate 형식과 일치시킴

    url = 'https://openapi.naver.com/v1/search/news.json'
    

    headers = {
        'X-Naver-Client-Id': client_id,
        'X-Naver-Client-Secret': client_secret
    }

    params = {
        'query': '이', 
        'display': 100,
        'start': 1, 
        'sort': 'date' 
    }

    news_list = []

    start = 1
    while True:
        params['start'] = start
        response = requests.get(url, headers=headers, params=params)
        if response.status_code != 200:
            print(f"Error: {response.status_code}")
            break

        data = response.json()
        items = data.get('items', [])
        if not items:
            break

        for item in items:
            pub_date = item['pubDate']
            if today in pub_date:
                news_list.append(item)
            else:
                break 

        start += 100
        if start > 1000: 
            break


    news_data = [{'title': news['title'], 'link': news['link'], 'Description': news['description'], 
                  'Publication Date': news['pubDate'], 'source': news['originallink']} for news in news_list]

    df = pd.DataFrame(news_data)
    
    df['source'] = df['source'].apply(lambda x: urlparse(x).netloc)
    # df = df[(df['source'] == 'news.kbs.co.kr') & (df['title'] == '') & (df['title'].notna()) & df['link'].notna() & (df['link'] == '')]
    # df = df[(df['source'] == 'news.kbs.co.kr') & (df['title'] != '') & df['title'].notna() & df['link'].notna() & (df['link'] != '')]
    df = df[(df['source'] == 'www.ytn.co.kr') & (df['title'] != '') & df['title'].notna() & df['link'].notna() & (df['link'] != '')]
    # df = df[(df['title'] != '') & df['title'].notna() & df['link'].notna() & (df['link'] != '')]
    
    return df

from utils import load_environment_variables#, check_and_remove_terms

# 환경 변수 로드
env_vars = load_environment_variables()
naver_client_id = env_vars['NAVER_CLIENT_ID']
naver_client_secret = env_vars['NAVER_CLIENT_SECRET']
openai_api_key = env_vars['OPENAI_API_KEY']

if __name__ == "__main__":
    client_id = naver_client_id
    client_secret = naver_client_secret
    df = fetch_news_data(client_id, client_secret)
    print(df)
