import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

# 한글 폰트 설정 (Windows: Malgun Gothic)
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

def show_boxplot(df):
    # 전공별 점수 분포 시각화
    fig, ax = plt.subplots()
    df.boxplot(column='점수', by='반', ax=ax)
    plt.title("반별 점수 분포")
    plt.suptitle("") # 자동 생성 제목 제거
    st.pyplot(fig)

if "scored_data" not in st.session_state:
    st.warning("먼저 홈화면에서 파일을 업로드해 주세요.")
    st.stop()

df = st.session_state.scored_data

# 사이드바에서 학생 선택
student_list = df['학번'].unique()
selected_std = st.sidebar.selectbox("학생 선택", student_list)

st.header(f"학생 상세 리포트: {selected_std}")

# 해당 학생 데이터 필터링
std_data = df[df['학번'] == selected_std]

# 2. 오답 항목 표시 (점수가 100점 미만인 경우)
st.subheader("오답 및 부분점수 항목")
wrong_items = std_data[std_data['점수'] < 100]
if not wrong_items.empty:
    st.table(wrong_items[['문항 번호', '학생 답', '정답 키워드', '점수']])
else:
    st.write("모든 문항 정답입니다.")

# 3. 해당 학생의 키워드 분석
st.subheader("추출된 주요 키워드")
for _, row in std_data.iterrows():
    st.write(f"문항 {row['문항 번호']}: {', '.join(row['추출된 키워드'])}")

# 4. 시각화 (박스도표)
st.subheader("전체 점수 분포 내 위치")
show_boxplot(df)