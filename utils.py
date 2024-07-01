import os
from dotenv import load_dotenv

def load_environment_variables():
    load_dotenv()
    naver_client_id = os.getenv('NAVER_CLIENT_ID')
    naver_client_secret = os.getenv('NAVER_CLIENT_SECRET')
    openai_api_key = os.getenv('OPENAI_API_KEY')
    sql_host = os.getenv('SQL_HOST')
    sql_port = os.getenv('SQL_PORT')
    sql_db = os.getenv('SQL_DB')
    sql_username = os.getenv('SQL_USERNAME')
    sql_password = os.getenv('SQL_PASSWORD')
    
    
    return {
        'NAVER_CLIENT_ID': naver_client_id,
        'NAVER_CLIENT_SECRET': naver_client_secret,
        'OPENAI_API_KEY': openai_api_key,
        'SQL_HOST' : sql_host, 
        'SQL_PORT' : sql_port, 
        'SQL_DB' : sql_db, 
        'SQL_USERNAME' : sql_username, 
        'SQL_PASSWORD' : sql_password
    }