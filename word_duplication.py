import pandas as pd
import mysql.connector

# MySQL 데이터베이스 연결 설정
db_config = {
    'user': 'your_username',
    'password': 'your_password',
    'host': 'your_host',
    'database': 'your_database'
}

db_config = {
        host : 'newsurfing-webservice.c5oa8musk0ga.ap-northeast-2.rds.amazonaws.com',
        port  : '3306', 
        database : 'api',
        user : 'ysjo123',
        password : '!Newnew240628'
}

# url : jdbc:mysql://newsurfing-webservice.c5oa8musk0ga.ap-northeast-2.rds.amazonaws.com:3306
# username: ysjo123
# password: "!Newnew240628"


def check_and_remove_terms(df):

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # 조회할 테이블 및 컬럼명 설정
    table_name = 'FORBIDDEN'
    column_name = 'text'
    
    for index, row in df.iterrows():
        terms = row['Tech terms and definitions']
        if terms:
            # 용어를 분할하여 리스트로 변환
            term_list = [term.split(":")[0].strip() for term in terms.split(",")]
            for term in term_list:
                # MySQL 쿼리를 통해 용어 존재 여부 확인
                query = f"SELECT EXISTS(SELECT 1 FROM {table_name} WHERE {column_name} = %s)"
                cursor.execute(query, (term,))
                exists = cursor.fetchone()[0]
                if exists:
                    # 데이터프레임에서 해당 용어 제거
                    term_list.remove(term)
            
            # 수정된 용어 리스트를 다시 합쳐서 데이터프레임에 반영
            df.at[index, 'Tech terms and definitions'] = ", ".join(term_list)
    
    # MySQL 연결 닫기
    cursor.close()
    conn.close()

    return df

# # 예제 사용
# data = [
#     {'news_id': 1, 'title': '전북자치도, AI 시스템 Chat GPT 시범도입...업무 효율성 기대', 'content': '전북자치도가 행정업무 효율성 향상을 위해 인공지능 챗봇인 Chat GPT를 도입했다. 13일 도에 따르면...', 'level': '초급', 'article': 'example article 1', 'Tech terms and definitions': '싸이벡스: 독일 프리미엄 유아용품 브랜드, 프리암: 싸이벡스의 프리미엄 유모차 모델'},
#     {'news_id': 2, 'title': '제목예시1', 'content': '이러쿵 저러쿵 쿵짝쿵짝 AI 딥러닝...', 'level': '중급', 'article': 'example article 2', 'Tech terms and definitions': '싸이벡스: 독일 프리미엄 유아용품 브랜드'}
# ]

# df = pd.DataFrame(data)
# result_df = check_and_remove_terms(df)
# print(result_df)
