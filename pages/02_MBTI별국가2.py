import streamlit as st
import pandas as pd
import plotly.express as px

# 페이지 기본 설정
st.set_page_config(
    page_title="MBTI 세계 지도 🌍",
    page_icon="🧠",
    layout="wide"
)

@st.cache_data
def load_data():
    # 같은 폴더에 있는 CSV 파일 읽기
    df = pd.read_csv("countriesMBTI_16types.csv")
    return df

df = load_data()

# MBTI 타입 리스트 (첫 번째 열 'Country' 제외)
mbti_types = df.columns[1:].tolist()

# 상단 제목/설명
st.markdown(
    """
    # 🌍 MBTI World Explorer 🧠✨  
    전 세계 국가별 MBTI 비율을 한눈에 보는 귀여운 데이터 놀이터예요!  

    1. 좋아하는 **MBTI 유형**을 선택하면  
    2. 그 유형 비율이 **가장 높은 10개 나라**와  
    3. **가장 낮은 10개 나라**를 예쁜 막대 그래프로 보여줄게요 📊  

    아래에서 유형을 골라볼까요? 👇
    """
)

# MBTI 선택 위젯
selected_mbti = st.selectbox(
    "🔎 알고 싶은 MBTI 유형을 선택해 주세요:",
    options=mbti_types,
    index=mbti_types.index("INFP") if "INFP" in mbti_types else 0,
    help="드롭다운에서 MBTI 유형을 골라보세요! 😄"
)

st.markdown(f"### 📌 현재 선택한 유형: **{selected_mbti}**")

# 선택한 MBTI 기준 정렬
sorted_df = df[["Country", selected_mbti]].dropna()

# 값이 높은 순 & 낮은 순
top10 = sorted_df.sort_values(by=selected_mbti, ascending=False).head(10)
bottom10 = sorted_df.sort_values(by=selected_mbti, ascending=True).head(10)

# 비율을 % 로 보기 좋게 표시할 컬럼 추가 (선택 사항)
top10_display = top10.copy()
bottom10_display = bottom10.copy()
top10_display["percentage"] = top10_display[selected_mbti] * 100
bottom10_display["percentage"] = bottom10_display[selected_mbti] * 100

# -------------------------
# TOP 10 막대 그래프
# -------------------------
st.markdown("---")
st.markdown(
    f"## 🏆 {selected_mbti} 비율이 가장 높은 나라 TOP 10 ✨"
)

fig_top = px.bar(
    top10_display,
    x="Country",
    y="percentage",
    text="percentage",
    labels={"Country": "Country", "percentage": f"{selected_mbti} 비율(%)"},
    title=f"🌟 {selected_mbti} 유형이 많은 나라 TOP 10"
)

fig_top.update_traces(
    texttemplate="%{text:.2f}%",
    hovertemplate="<b>%{x}</b><br>" + selected_mbti + " 비율: %{y:.2f}%<extra></extra>"
)
fig_top.update_layout(
    xaxis_title="나라",
    yaxis_title=f"{selected_mbti} 비율(%)",
    title_x=0.5
)

st.plotly_chart(fig_top, use_container_width=True)

# -------------------------
# BOTTOM 10 막대 그래프
# -------------------------
st.markdown("---")
st.markdown(
    f"## 🐢 {selected_mbti} 비율이 가장 낮은 나라 BOTTOM 10 (그래도 소중해요 💖)"
)

fig_bottom = px.bar(
    bottom10_display,
    x="Country",
    y="percentage",
    text="percentage",
    labels={"Country": "Country", "percentage": f"{selected_mbti} 비율(%)"},
    title=f"🍀 {selected_mbti} 유형이 상대적으로 적은 나라 10곳"
)

fig_bottom.update_traces(
    texttemplate="%{text:.2f}%",
    hovertemplate="<b>%{x}</b><br>" + selected_mbti + " 비율: %{y:.2f}%<extra></extra>"
)
fig_bottom.update_layout(
    xaxis_title="나라",
    yaxis_title=f"{selected_mbti} 비율(%)",
    title_x=0.5
)

st.plotly_chart(fig_bottom, use_container_width=True)

# -------------------------
# 하단 귀여운 푸터
# -------------------------
st.markdown("---")
st.markdown(
    """
    ### 🧸 작은 팁  
    - 막대 위에 마우스를 올리면 **정확한 비율**을 확인할 수 있어요.  
    - MBTI를 바꿔가며 어떤 나라에 어떤 성향이 많은지 비교해 보세요! 🔁  
    - 수업에서 **진로·성격·문화 차이**를 이야기할 때 자료로 쓰기 딱 좋아요 📚  

    행복한 데이터 탐험 되세요 🌈
    """
)
