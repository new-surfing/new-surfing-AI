import tensorflow as tf
from transformers import BertTokenizer, TFBertForSequenceClassification
import numpy as np
import re
import logging
from sklearn.preprocessing import LabelEncoder

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 모델과 토크나이저 로드
model = TFBertForSequenceClassification.from_pretrained('./kobert_news_classifier')
tokenizer = BertTokenizer.from_pretrained('./kobert_news_classifier')

# 라벨 인코더 로드
label_encoder = LabelEncoder()
label_encoder.classes_ = np.load('./kobert_news_classifier/label_classes.npy', allow_pickle=True)

def preprocess_text(text):
    """
    텍스트 전처리 함수
    """
    if isinstance(text, str):
        text = re.sub(r'\[.*?\]', '', text)  # 대괄호로 둘러싸인 텍스트 제거
        text = re.sub(r'\W+', ' ', text)  # 특수 문자 제거
        text = re.sub(r'\s+', ' ', text).strip()  # 여분의 공백 제거
    else:
        text = ''
    return text

def classify_article(article_text):
    """
    주어진 기사 텍스트를 분류하고 디코딩된 라벨 값을 반환합니다.
    """
    try:
        # 텍스트 전처리
        processed_text = preprocess_text(article_text)
        
        # 기사 분류
        inputs = tokenizer(processed_text, return_tensors='tf', max_length=128, truncation=True, padding='max_length')
        outputs = model(inputs)
        logits = outputs.logits
        scores = tf.nn.softmax(logits, axis=-1).numpy()[0]
        
        # 50% 이상인 라벨 필터링
        filtered_labels = {label_encoder.inverse_transform([i])[0]: score for i, score in enumerate(scores) if score >= 0.2}
        
        # 최소 하나의 라벨 보장
        if not filtered_labels:
            max_score_idx = np.argmax(scores)
            filtered_labels[label_encoder.inverse_transform([max_score_idx])[0]] = scores[max_score_idx]
        
        # 디코딩된 라벨 값만 반환
        decoded_labels = list(filtered_labels.keys())
        return decoded_labels
    except Exception as e:
        logger.error(f"Error in classifying article with scores: {e}")
        return None
