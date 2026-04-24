import streamlit as st
import pandas as pd
from utils_scoring import calculate_score

st.title("학생 서논술형 평가 시스템")

# 1. 파일 업로드 섹션
ans_file = st.file_uploader("정답 예시 파일 업로드 (CSV)", type=["csv"])
std_file = st.file_uploader("학생 답안 파일 업로드 (CSV)", type=["csv"])

if ans_file and std_file:
    df_ans = pd.read_csv(ans_file)
    df_std = pd.read_csv(std_file)

    # 채점 로직 수행
    results = []
    for _, row in df_std.iterrows():
        # 문항 번호가 일치하는 정답 키워드 추출
        correct_row = df_ans[df_ans['문항 번호'] == row['문항 번호']]
        if not correct_row.empty:
            correct_keywords = correct_row.iloc[0]['핵심 키워드']
            score, found = calculate_score(row['학생 답'], correct_keywords)

            res_dict = row.to_dict()
            res_dict.update({'점수': score, '추출된 키워드': found, '정답 키워드': correct_keywords})
            results.append(res_dict)

    # 세션 상태에 결과 저장
    st.session_state.scored_data = pd.DataFrame(results)
    st.success("채점이 완료되었습니다. 사이드바에서 학생별 상세 결과를 확인하세요.")