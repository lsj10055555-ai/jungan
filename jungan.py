import pandas as pd
from konlpy.tag import Okt

# 형태소 분석기 초기화
okt = Okt()


def analyze_keywords(text):
    # 문장에서 명사만 추출하여 반환
    if pd.isna(text):
        return []
    return okt.nouns(text)


def calculate_score(student_ans, correct_keywords):
    # 학생 답안의 명사와 정답 키워드 대조
    student_keywords = analyze_keywords(student_ans)
    # 정답 키워드는 쉼표로 구분된 문자열로 가정
    keywords_list = [k.strip() for k in correct_keywords.split(',')]
    found_keywords = [k for k in keywords_list if k in student_keywords]

    # 채점 결과: 모든 키워드 포함 시 100점, 아니면 비율대로 계산
    score = (len(found_keywords) / len(keywords_list)) * 100 if keywords_list else 0
    return round(score, 2), found_keywords