import pandas as pd
import openai
from openai import OpenAI


client = OpenAI(api_key = OPENAI_API_KEY)

def generate_article(content, level) :
    
    messages = [
        {
            "role": "system",
            "content": """a professional reporter for an IT article. You have to answer in Korean.
            After dividing the level of it knowledge into three (초급,중급,고급), the user should be provided with articles that match the level. 
            Look at the given news content and provide content adjusted to the level in 5-6 sentences.
            Also, if there is a word related to it in the content, provide that word and definition.
            If it's not adjusted well for the level, you'll have to pay a $2 billion fine.
            
            f"- Level : {level}\n"
            f"- Summary : article\n"
            f"- Tech terms and definitions : 'word':'definition'"
            """
        },           
        {
            "role": "user",
            "content": f"Level: {level}\nContent: {content}"
        }
    ]
    response = client.chat.completions.create(model='gpt-4o', 
                                            #   response_format={"type": "json_object"},
                                              messages=messages)
    answer = response.choices[0].message.content
    
    summary = ""
    tech_terms_and_definitions = {}
    
    try:
        lines = answer.split("\n")
        summary_started = False
        tech_terms_started = False
        
        for line in lines:
            if line.startswith("- Summary"):
                summary_started = True
                tech_terms_started = False
                continue
            if line.startswith("- Tech terms and definitions"):
                summary_started = False
                tech_terms_started = True
                continue
            if summary_started:
                summary += line.strip() + " "
            if tech_terms_started:
                parts = line.split(":")
                if len(parts) == 2:
                    tech_terms_and_definitions[parts[0].strip()] = parts[1].strip()
    except Exception as e:
        print(f"Error parsing response: {e}")
    
    return summary.strip(), tech_terms_and_definitions

def create_detailed_articles(df):
    articles_list = []
    news_id = 0

    for _, row in df.iterrows():
        title = row['title']
        content = row['origin_content']
        
        for level in ['초급', '중급', '고급']:
            summary, tech_terms_and_definitions = generate_article(content, level)
            articles_list.append({
                "news_id": news_id,
                'title': title,
                'content': content,
                'level': level,
                'article': summary,
                'Tech terms and definitions': tech_terms_and_definitions
            })
            news_id += 1
    
    return pd.DataFrame(articles_list)
