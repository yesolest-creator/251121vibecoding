import streamlit as st
import pandas as pd
import altair as alt

# 🧠 기본 설정
st.set_page_config(
    page_title="MBTI World Explorer",
    page_icon="🌍",
    layout="centered",
)

@st.cache_data
def load_data():
    # 👉 CSV 파일 이름은 반드시 countriesMBTI_16types.csv 로 맞춰 주세요
    df = pd.read_csv("countriesMBTI_16types.csv")
    return df

df = load_data()

# MBTI 타입 목록 (Country 열 제외)
mbti_types = [col for col in df.columns if col != "Country"]

# 🎨 제목 & 소개
st.title("🌍 MBTI World Explorer")
st.markdown(
    """
    MBTI 유형별로 **전 세계 어떤 나라에서 비율이 높은지 / 낮은지** 한눈에 보는 웹앱이에요 😊  

    1️⃣ 위에서 MBTI 유형을 고르면  
    2️⃣ 해당 유형의 비율이 **높은 나라 TOP 10 🔝**  
    3️⃣ 그리고 **낮은 나라 BOTTOM 10 🔻** 를  
    인터랙티브한 Altair 막대 그래프로 보여줍니다!  
    """
)

# 🧩 MBTI 선택
default_index = mbti_types.index("INFP") if "INFP" in mbti_types else 0
selected_type = st.selectbox("🧠 보고 싶은 MBTI 유형을 골라 주세요", mbti_types, index=default_index)

st.markdown(
    f"""
    ### ✨ 선택한 유형: **{selected_type}**
    아래 그래프에서 막대에 마우스를 올리면 나라 이름과 정확한 비율(%)을 볼 수 있어요 👀  
    """
)

# 📊 데이터 정렬: 상위 / 하위 10개 나라
view_df = df[["Country", selected_type]].dropna()

top10 = (
    view_df.sort_values(by=selected_type, ascending=False)
    .head(10)
)

bottom10 = (
    view_df.sort_values(by=selected_type, ascending=True)
    .head(10)
)

# 🔝 TOP 10 그래프 (Altair)
top_chart = (
    alt.Chart(top10)
    .mark_bar()
    .encode(
        x=alt.X(
            f"{selected_type}:Q",
            title=f"{selected_type} 비율(%)",
            axis=alt.Axis(format=".1%")
        ),
        y=alt.Y(
            "Country:N",
            sort="-x",
            title=None
        ),
        tooltip=[
            alt.Tooltip("Country:N", title="나라"),
            alt.Tooltip(f"{selected_type}:Q", title="비율", format=".2%")
        ]
    )
    .properties(
        title=f"🔝 {selected_type} 비율이 높은 나라 TOP 10",
        height=350
    )
    .interactive()
)

st.altair_chart(top_chart, use_container_width=True)

st.markdown("---")

# 🔻 BOTTOM 10 그래프 (Altair)
st.markdown(
    f"""
    ### 🔻 {selected_type} 유형이 **상대적으로 적은** 나라들도 궁금하다면?
    아래 BOTTOM 10 그래프를 확인해 보세요 👇  
    """
)

bottom_chart = (
    alt.Chart(bottom10)
    .mark_bar()
    .encode(
        x=alt.X(
            f"{selected_type}:Q",
            title=f"{selected_type} 비율(%)",
            axis=alt.Axis(format=".1%")
        ),
        y=alt.Y(
            "Country:N",
            sort="x",
            title=None
        ),
        tooltip=[
            alt.Tooltip("Country:N", title="나라"),
            alt.Tooltip(f"{selected_type}:Q", title="비율", format=".2%")
        ]
    )
    .properties(
        title=f"🔻 {selected_type} 비율이 낮은 나라 BOTTOM 10",
        height=350
    )
    .interactive()
)

st.altair_chart(bottom_chart, use_container_width=True)

# 📝 작은 요약
st.markdown(
    f"""
    ---
    🧾 **요약 한 줄**  
    - 선택한 MBTI: **{selected_type}**  
    - 가장 비율이 높은 나라는: **{top10.iloc[0]['Country']}**  
    - 가장 비율이 낮은 나라는: **{bottom10.iloc[0]['Country']}**  

    전 세계 MBTI 분포를 보면서  
    📚 수업 자료로 쓰거나,  
    🎲 친구들과 MBTI 토론 소재로 써도 재밌게 활용할 수 있어요!
    """
)
