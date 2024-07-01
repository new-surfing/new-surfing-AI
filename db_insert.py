import pandas as pd
import mysql.connector
from mysql.connector import Error


'''
condition : FORBIDDEN - text
insert table : 
- TAG(mainCategory, detail, 사용여부)
- ARTICLE(title, author, publishedAt, urlLink, description, sourceId, tagId) 
- VOCABULARY(name, content, Field)
- SUMMARY_INFERENCE(content, level, articleId)


'''


def insert_data_to_db(df, host, port, database, user, password):
    try:
        conn = mysql.connector.connect(
            host=host,
            port=port,
            database=database,
            user=user,
            password=password
        )

        if conn.is_connected():
            print('MySQL에 성공적으로 연결되었습니다.')

        cursor = conn.cursor()

        # Source와 Tag 데이터 삽입
        source_ids = {}
        tag_ids = {}

        for source_name in df['source_name'].unique():
            cursor.execute("INSERT INTO SOURCE (name, displayName) VALUES (%s, %s)", (source_name, source_name))
            conn.commit()
            source_ids[source_name] = cursor.lastrowid

        for tag_name in df['tag_name'].unique():
            cursor.execute("INSERT INTO TAG (detail, isUse) VALUES (%s, %s)", (tag_name, True))
            conn.commit()
            tag_ids[tag_name] = cursor.lastrowid

        # Article, Summary_Inference, Vocabulary, Article_Vocabulary_Mapping 데이터 삽입
        for idx, row in df.iterrows():
            # Article 삽입
            cursor.execute("""
                INSERT INTO ARTICLE (title, author, publishedAt, urlLink, description, sourceId, tagId)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (row['title'], row['author'], row['publishedAt'], row['urlLink'], row['description'], source_ids[row['source_name']], tag_ids[row['tag_name']]))
            conn.commit()
            article_id = cursor.lastrowid

            # Summary_Inference 삽입
            cursor.execute("""
                INSERT INTO SUMMARY_INFERENCE (content, level, articleId)
                VALUES (%s, %s, %s)
            """, (row['summary_content'], row['level'], article_id))
            conn.commit()

            # Vocabulary 및 Article_Vocabulary_Mapping 삽입
            for vocab_name, vocab_content in row['voca'].items():
                # Vocabulary 삽입
                cursor.execute("SELECT id FROM VOCABULARY WHERE name = %s", (vocab_name,))
                vocab_result = cursor.fetchone()

                if vocab_result:
                    vocabulary_id = vocab_result[0]
                else:
                    cursor.execute("INSERT INTO VOCABULARY (name, content) VALUES (%s, %s)", (vocab_name, vocab_content))
                    conn.commit()
                    vocabulary_id = cursor.lastrowid

                # Article_Vocabulary_Mapping 삽입
                cursor.execute("INSERT INTO ARTICLE_VOCABULARY_MAPPING (articleId, vocabularyId) VALUES (%s, %s)", (article_id, vocabulary_id))
                conn.commit()

        print('데이터프레임이 성공적으로 MySQL 테이블에 삽입되었습니다.')

    except Error as e:
        print(f'MySQL 연결 에러 발생: {e}')

    finally:
        # 연결 닫기
        if conn.is_connected():
            cursor.close()
            conn.close()
            print('MySQL 연결이 닫혔습니다.')


