import streamlit as st

# ---------------- 기본 설정 ----------------
st.set_page_config(
    page_title="MBTI 고전 추천 진로 상담실",
    page_icon="📚",
    layout="wide"
)

# ----------------- 간단 스타일 -----------------
st.markdown(
    """
    <style>
    .big-title {
        font-size: 2.2rem;
        font-weight: 700;
        margin-bottom: 0.2rem;
    }
    .subtitle {
        font-size: 1rem;
        color: #555;
        margin-bottom: 1.2rem;
    }
    .tag {
        display: inline-block;
        padding: 0.1rem 0.55rem;
        border-radius: 999px;
        font-size: 0.75rem;
        margin-right: 0.2rem;
        margin-bottom: 0.2rem;
        background-color: #f1f3f6;
    }
    .book-card {
        border-radius: 1rem;
        padding: 1rem 1.1rem;
        margin-bottom: 0.9rem;
        background: white;
        box-shadow: 0 4px 10px rgba(15, 23, 42, 0.06);
        border: 1px solid #eef0f3;
    }
    .book-title {
        font-size: 1.0rem;
        font-weight: 700;
        margin-bottom: 0.15rem;
    }
    .book-meta {
        font-size: 0.78rem;
        color: #666;
        margin-bottom: 0.5rem;
    }
    .section-title {
        font-size: 1.1rem;
        font-weight: 700;
        margin: 1.0rem 0 0.5rem 0;
    }
    .pill {
        display: inline-flex;
        align-items: center;
        gap: 0.3rem;
        padding: 0.25rem 0.7rem;
        border-radius: 999px;
        font-size: 0.8rem;
        background: #eef4ff;
        color: #2c4bff;
        margin-right: 0.3rem;
        margin-top: 0.2rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ----------------- 데이터 정의 -----------------
MBTI_ICONS = {
    "INTJ": "🧠",
    "INTP": "🧪",
    "ENTJ": "🏁",
    "ENTP": "💡",
    "INFJ": "🌌",
    "INFP": "🎨",
    "ENFJ": "🤝",
    "ENFP": "✨",
    "ISTJ": "📏",
    "ISFJ": "🪴",
    "ESTJ": "🏗️",
    "ESFJ": "🎈",
    "ISTP": "🛠️",
    "ISFP": "🍃",
    "ESTP": "🏎️",
    "ESFP": "🎭",
}

# MBTI별 고전 추천 (간단 2권씩)
RECOMMENDATIONS = {
    "INTJ": [
        {
            "title": "군주론",
            "author": "니콜로 마키아벨리",
            "vibe": "전략 · 구조 · 권력 분석",
            "why": "INTJ의 장기 계획 세우는 힘과 분석력을 자극해 주는 책으로, 조직과 사회 구조를 전략적으로 바라보는 시각을 키워 줌.",
            "career": ["정책분석가", "경영전략가", "연구원", "기획자"],
        },
        {
            "title": "국가",
            "author": "플라톤",
            "vibe": "이상적 사회 · 철학적 사고",
            "why": "추상적 이론과 이상적인 시스템을 설계하는 데 흥미를 느끼는 INTJ에게 철학적·정치적 사고의 기반을 제공함.",
            "career": ["철학 · 인문학자", "공공정책", "교육기획", "데이터 기반 정책"],
        },
    ],
    "INTP": [
        {
            "title": "수학의 정석(아니고) → 『논어』",
            "author": "공자",
            "vibe": "개념 · 원리 · 인간 이해",
            "why": "원리와 개념을 좋아하는 INTP에게 인간 관계와 사회 규범을 구조적으로 바라볼 수 있게 해줌.",
            "career": ["연구자", "데이터 분석가", "개발자", "철학 · 인문 연구"],
        },
        {
            "title": "소크라테스의 변명",
            "author": "플라톤",
            "vibe": "비판적 사고 · 질문",
            "why": "끊임없이 ‘왜?’를 던지는 INTP에게 질문하는 태도와 비판적 사고의 중요성을 일깨워 줌.",
            "career": ["법조인", "학자", "기획자", "컨설턴트"],
        },
    ],
    "ENTJ": [
        {
            "title": "손자병법",
            "author": "손무",
            "vibe": "전략 · 리더십",
            "why": "목표를 향해 자원을 효율적으로 배치하는 ENTJ의 리더십 기질을 더욱 날카롭게 만들어 줄 전략서.",
            "career": ["경영자", "프로덕트 매니저", "조직 리더", "정치 · 행정"],
        },
        {
            "title": "자본론 (발췌/축약본 추천)",
            "author": "카를 마르크스",
            "vibe": "경제 구조 이해",
            "why": "큰 시스템과 구조를 파악하는 데 강한 ENTJ에게 경제·사회 구조를 입체적으로 보는 관점을 제공함.",
            "career": ["경영 · 금융", "정책 기획", "경제 분석"],
        },
    ],
    "ENTP": [
        {
            "title": "도둑맞은 집중",
            "author": "요한 하리 (현대 고전 계열)",
            "vibe": "현대 사회 · 비판",
            "why": "아이디어가 넘치는 ENTP에게, 정보 과부하 시대의 현실과 변화를 고민할 거리를 던져 주는 책.",
            "career": ["창업가", "크리에이터", "기획자", "마케터"],
        },
        {
            "title": "걸리버 여행기",
            "author": "조너선 스위프트",
            "vibe": "풍자 · 상상력",
            "why": "상상력과 풍자를 좋아하는 ENTP에게 사회를 유쾌하게 비틀어 보는 시선을 제공함.",
            "career": ["콘텐츠 제작", "광고 · 마케팅", "미디어"],
        },
    ],
    "INFJ": [
        {
            "title": "데미안",
            "author": "헤르만 헤세",
            "vibe": "자아 탐색 · 성장",
            "why": "내면 성찰과 가치 중심의 삶을 중시하는 INFJ에게 자기 정체성을 깊이 탐구하게 하는 성장 소설.",
            "career": ["상담가", "교사", "작가", "심리 · 사회복지"],
        },
        {
            "title": "이방인",
            "author": "알베르 카뮈",
            "vibe": "부조리 · 존재 의미",
            "why": "세상과 개인의 의미를 고민하는 INFJ에게 인간과 사회의 관계를 다시 생각하게 만드는 책.",
            "career": ["인문·사회 연구", "다문화 · 인권 분야", "예술"],
        },
    ],
    "INFP": [
        {
            "title": "어린 왕자",
            "author": "앙투안 드 생텍쥐페리",
            "vibe": "감성 · 상상력 · 순수함",
            "why": "감정과 상상력이 풍부한 INFP에게, 진짜 중요한 것이 무엇인지 질문을 던지는 따뜻한 고전.",
            "career": ["작가", "디자이너", "예술 · 문화 기획", "교육"],
        },
        {
            "title": "위대한 개츠비",
            "author": "F. 스콧 피츠제럴드",
            "vibe": "이상 · 현실 · 사랑",
            "why": "이상과 현실 사이의 갈등을 섬세하게 느끼는 INFP에게, 꿈과 진실을 돌아보게 하는 작품.",
            "career": ["콘텐츠 기획", "영상 · 문학", "브랜딩"],
        },
    ],
    "ENFJ": [
        {
            "title": "죄와 벌",
            "author": "도스토옙스키",
            "vibe": "도덕 · 죄책감 · 구원",
            "why": "사람과 사람 사이의 감정과 도덕을 중요하게 여기는 ENFJ에게 인간 이해의 깊이를 더해 줌.",
            "career": ["교사", "상담가", "인사관리(HR)", "사회운동"],
        },
        {
            "title": "시민불복종",
            "author": "헨리 데이비드 소로",
            "vibe": "가치 · 신념 · 사회 변화",
            "why": "공동체를 더 나은 방향으로 이끌고 싶은 ENFJ에게, 신념을 행동으로 옮기는 용기를 주는 글.",
            "career": ["교육", "사회운동", "정책", "비영리 단체"],
        },
    ],
    "ENFP": [
        {
            "title": "월든",
            "author": "헨리 데이비드 소로",
            "vibe": "자유 · 자연 · 라이프스타일",
            "why": "새로운 삶의 방식을 상상하는 ENFP에게 ‘어떻게 살 것인가’를 자유롭게 고민하게 만드는 책.",
            "career": ["프리랜서", "크리에이터", "기획자", "홍보·마케팅"],
        },
        {
            "title": "변신",
            "author": "프란츠 카프카",
            "vibe": "상징 · 상상 · 자아",
            "why": "기발한 상상과 상징 세계를 좋아하는 ENFP에게, ‘나’와 ‘타인’을 색다르게 보게 하는 작품.",
            "career": ["예술", "콘텐츠 제작", "스토리텔링"],
        },
    ],
    "ISTJ": [
        {
            "title": "법의 정신",
            "author": "몽테스키외",
            "vibe": "질서 · 제도 · 구조",
            "why": "논리적이고 책임감 있는 ISTJ에게 사회 제도와 법의 구조를 이해할 수 있는 탄탄한 인문 고전.",
            "career": ["공무원", "법조인", "회계사", "행정"],
        },
        {
            "title": "회사와 노동에 대한 책 (예: 『프로테스탄트 윤리와 자본주의 정신』 발췌)",
            "author": "막스 베버",
            "vibe": "성실 · 직업 윤리",
            "why": "근면과 성실을 중시하는 ISTJ가 자신의 일과 책임을 더 넓은 사회 구조 속에서 바라볼 수 있게 함.",
            "career": ["경영 관리", "행정", "재무"],
        },
    ],
    "ISFJ": [
        {
            "title": "작은 아씨들",
            "author": "루이자 메이 올컷",
            "vibe": "가족 · 헌신 · 성장",
            "why": "타인을 돌보고 배려하는 ISFJ의 따뜻한 면을 잘 보여 주고, 관계 속에서 성장하는 모습을 그려 줌.",
            "career": ["간호·보건", "교육", "사회복지", "서비스"],
        },
        {
            "title": "안네의 일기",
            "author": "안네 프랑크",
            "vibe": "공감 · 기록 · 희망",
            "why": "섬세한 마음을 지닌 ISFJ에게 기록과 공감, 희망의 힘을 전해 주는 작품.",
            "career": ["기록연구사", "교사", "상담", "인권 관련 직무"],
        },
    ],
    "ESTJ": [
        {
            "title": "국부론 (발췌·해설본 추천)",
            "author": "애덤 스미스",
            "vibe": "경제 · 시스템 · 효율",
            "why": "현실적이고 실용적인 ESTJ에게 경제 시스템과 조직 운영 원리를 이해하는 기반이 되는 고전.",
            "career": ["경영", "재무", "공공행정", "프로젝트 매니저"],
        },
        {
            "title": "토지",
            "author": "박경리",
            "vibe": "역사 · 공동체 · 책임",
            "why": "큰 틀에서 사회와 역사를 바라보고 책임감을 느끼는 ESTJ에게 우리 사회의 변화 과정을 보여 줌.",
            "career": ["행정", "조직 리더", "공공기관"],
        },
    ],
    "ESFJ": [
        {
            "title": "톰 소여의 모험",
            "author": "마크 트웨인",
            "vibe": "모험 · 우정 · 공동체",
            "why": "사람들과 어울리고 함께하는 것을 좋아하는 ESFJ에게 관계와 공동체의 즐거움을 다시 느끼게 함.",
            "career": ["행사 기획", "교육", "서비스", "관광"],
        },
        {
            "title": "제인 에어",
            "author": "샬럿 브론테",
            "vibe": "자립 · 사랑 · 도덕",
            "why": "주변 사람을 챙기면서도 자신의 가치를 지키고 싶은 ESFJ에게 자존감과 관계의 균형을 보여줌.",
            "career": ["교육", "상담", "HR", "고객 관계"],
        },
    ],
    "ISTP": [
        {
            "title": "로빈슨 크루소",
            "author": "다니엘 디포",
            "vibe": "생존 · 실용 · 문제 해결",
            "why": "손으로 부딪치고 해결하는 걸 좋아하는 ISTP에게 현실적인 문제 해결과 창의력의 재미를 보여주는 작품.",
            "career": ["공학 · 기술직", "개발자", "정비 · 설비", "디자인·제작"],
        },
        {
            "title": "해커와 화가",
            "author": "폴 그레이엄 (현대 고전 계열)",
            "vibe": "기술 · 창의 · 만들기",
            "why": "무언가를 직접 만들어 내는 걸 좋아하는 ISTP에게 기술과 예술의 만남을 보여주는 에세이.",
            "career": ["개발자", "메이커", "스타트업"],
        },
    ],
    "ISFP": [
        {
            "title": "나무",
            "author": "베른하르트 잘린스키 등(자연·에세이 계열 책들)",
            "vibe": "자연 · 감성 · 관찰",
            "why": "감각이 섬세한 ISFP에게 자연과 일상을 바라보는 시선을 깊게 만들어 주는 책.",
            "career": ["디자이너", "사진가", "예술가", "조경·환경"],
        },
        {
            "title": "월든 (또 한 번!)",
            "author": "헨리 데이비드 소로",
            "vibe": "자연 · 고독 · 라이프스타일",
            "why": "조용히 자신만의 삶을 꾸미고 싶은 ISFP에게 ‘어떻게 나답게 살 것인가’를 고민하게 해 줌.",
            "career": ["프리랜서", "아티스트", "공예 · 디자인"],
        },
    ],
    "ESTP": [
        {
            "title": "돈키호테",
            "author": "세르반테스",
            "vibe": "모험 · 행동 · 유머",
            "why": "행동파 ESTP에게 현실과 이상 사이를 넘나드는 허술하지만 사랑스러운 모험가의 모습을 통해 자신을 비춰 볼 기회를 줌.",
            "career": ["세일즈", "사업", "스포츠 관련 직무", "이벤트 기획"],
        },
        {
            "title": "열하일기",
            "author": "박지원",
            "vibe": "여행 · 관찰 · 통찰",
            "why": "직접 보고 경험하며 배우는 것을 좋아하는 ESTP에게 여행기 속 생생한 관찰과 통찰을 전해 줌.",
            "career": ["무역", "여행 · 관광", "현장 중심 직무"],
        },
    ],
    "ESFP": [
        {
            "title": "로미오와 줄리엣",
            "author": "셰익스피어",
            "vibe": "감정 · 극적 상황",
            "why": "감정 표현이 풍부한 ESFP에게 사랑과 선택, 관계의 드라마를 강렬하게 느끼게 하는 연극 작품.",
            "career": ["공연예술", "연예 · 방송", "행사 · 이벤트"],
        },
        {
            "title": "삼국지 (이야기판, 청소년판 등)",
            "author": "나관중",
            "vibe": "캐릭터 · 드라마 · 의리",
            "why": "다양한 인물과 드라마가 가득한 삼국지는 사람 중심의 이야기를 좋아하는 ESFP에게 딱 맞는 서사.",
            "career": ["MC·진행", "마케터", "콘텐츠 크리에이터"],
        },
    ],
}

# ----------------- 사이드바 -----------------
with st.sidebar:
    st.markdown("### 🎯 MBTI 고전 추천 설정")
    st.write("학생의 MBTI를 선택하면 그 유형에 맞는 고전과 진로 아이디어를 추천해 줍니다.")

    name = st.text_input("학생 이름 (선택)", placeholder="예: 김OO")
    grade = st.selectbox("학년 (선택)", ["선택 안 함", "1학년", "2학년", "3학년"], index=0)
    mbti = st.selectbox(
        "MBTI 유형 선택",
        options=list(MBTI_ICONS.keys()),
        index=0,
        help="학생이 알고 있는 MBTI 유형을 선택하세요."
    )

    focus = st.multiselect(
        "관심 진로 키워드 (선택)",
        ["인문·사회", "경영·경제", "과학·기술", "예술·디자인", "교육·상담", "공공·행정"],
        default=[]
    )

    detail_level = st.radio(
        "설명 스타일",
        ["간단하게 요약", "조금 자세히"],
        index=1,
        horizontal=True
    )

    st.markdown("---")
    st.caption("💡 *수업시간에 학생들에게 링크를 공유하면\n간단한 진로·독서 상담 도구로 활용할 수 있어요.*")

# ----------------- 메인 화면 -----------------
col_left, col_right = st.columns([2, 1])

with col_left:
    icon = MBTI_ICONS.get(mbti, "📚")
    display_name = f" {name}" if name else ""
    display_grade = f" ({grade})" if grade != "선택 안 함" else ""

    st.markdown(
        f"""
        <div class="big-title">{icon} MBTI 고전 추천 진로 상담실</div>
        <div class="subtitle">
            {display_name}{display_grade} 학생에게 어울리는 고전 책과 진로 방향을 한눈에 볼 수 있는 작은 상담실입니다.
        </div>
        """,
        unsafe_allow_html=True,
    )

    # 선택한 MBTI 요약 배지
    st.markdown("#### 현재 상담 대상")
    cols_info = st.columns(3)
    with cols_info[0]:
        st.markdown(
            f"""<div class="pill">MBTI {icon} <b>{mbti}</b></div>""",
            unsafe_allow_html=True,
        )
    with cols_info[1]:
        if grade != "선택 안 함":
            st.markdown(
                f"""<div class="pill">🎓 {grade}</div>""",
                unsafe_allow_html=True,
            )
    with cols_info[2]:
        if focus:
            tags = " · ".join(focus)
            st.markdown(
                f"""<div class="pill">🚀 관심 분야: {tags}</div>""",
                unsafe_allow_html=True,
            )

    st.markdown("---")

    # ----------------- 추천 도서 출력 -----------------
    st.markdown(
        f"""<div class="section-title">📚 {mbti} 유형에게 어울리는 고전 책</div>""",
        unsafe_allow_html=True,
    )

    books = RECOMMENDATIONS.get(mbti, [])

    for book in books:
        with st.container():
            st.markdown('<div class="book-card">', unsafe_allow_html=True)
            st.markdown(
                f"""
                <div class="book-title">📖 {book['title']}</div>
                <div class="book-meta">
                    ✍️ {book['author']} · <span style="color:#6366f1;">{book['vibe']}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )

            if detail_level == "조금 자세히":
                st.write(book["why"])
            else:
                st.write("👉 이 MBTI의 성향과 잘 맞는 고전으로, 사고의 깊이와 시야를 넓혀 줄 수 있는 책입니다.")

            # 진로 태그
            tags_html = "".join(
                [f'<span class="tag">🎯 {c}</span>' for c in book["career"]]
            )
            st.markdown(tags_html, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

    # ----------------- 진로 코멘트 -----------------
    st.markdown(
        """<div class="section-title">🧭 MBTI + 고전 기반 진로 코멘트</div>""",
        unsafe_allow_html=True,
    )

    # MBTI 성향에 따른 짧은 진로 코멘트
    if mbti.startswith("I"):
        intro_extro = "내향(I) 성향이라 혼자 깊이 생각하고 정리하는 시간이 중요해요."
    else:
        intro_extro = "외향(E) 성향이라 사람들과의 상호작용 속에서 에너지를 얻어요."

    if "N" in mbti:
        sensing_intuition = "직관(N) 성향으로, 구체적인 사실보다 아이디어와 가능성을 보는 힘이 커요."
    else:
        sensing_intuition = "감각(S) 성향으로, 실제 경험과 현실적인 정보에 강점을 지니고 있어요."

    if "T" in mbti:
        thinking_feeling = "사고(T) 성향이라, 상황을 논리와 원칙 중심으로 판단하는 경향이 나타나요."
    else:
        thinking_feeling = "감정(F) 성향이라, 사람의 마음과 관계를 고려해 결정을 내리려는 경향이 있어요."

    if "J" in mbti:
        judging_perceiving = "계획형(J)이라, 일정과 목표를 세우고 차근차근 실행하는 스타일이에요."
    else:
        judging_perceiving = "인식형(P)이라, 여지를 두고 유연하게 움직이며 새로운 선택지를 탐색하는 타입이에요."

    st.write(f"✅ {intro_extro}")
    st.write(f"✅ {sensing_intuition}")
    st.write(f"✅ {thinking_feeling}")
    st.write(f"✅ {judging_perceiving}")

    if focus:
        st.info(
            "🎓 선택한 관심 분야와 오늘 읽은/읽을 고전에서 인상 깊었던 문장을 연결해서 "
            "‘나의 가치관·관심사·강점’을 한 문장으로 정리해 보면 자기소개서나 면접에 큰 도움이 됩니다."
        )
    else:
        st.info(
            "🎓 관심 진로 키워드를 선택하면, 상담 방향을 조금 더 구체적으로 잡아 줄 수 있어요."
        )

with col_right:
    st.markdown("### ✍️ 상담 메모 공간")
    st.write("학생과의 상담 내용을 간단히 기록해 두는 영역입니다.")
    memo = st.text_area(
        "오늘 상담 메모",
        height=220,
        placeholder="예) 책 중 가장 끌린 작품, 인상 깊었던 문장, 떠오르는 진로 아이디어 등을 적어 보세요.",
    )

    st.markdown("### 🧩 한 줄 정리 생성기")
    st.write("학생에게 보여 줄 ‘한 줄 요약’을 미리 정리해 두면 좋아요.")
    if st.button("한 줄 요약 템플릿 만들기 ✨"):
        line = f"{name or '이 학생'}은(는) {mbti} 유형의 강점을 살려 "
        if focus:
            line += f"{', '.join(focus)} 분야에서 "
        line += "고전을 통해 자기 생각을 깊이 있게 확장해 나갈 수 있는 가능성이 큰 학생임."
        st.success(line)

    st.markdown("---")
    st.caption(
        "📌 *Tip: Streamlit Cloud에 이 앱을 올려 두고, "
        "상담 시간마다 학생 MBTI만 바꿔 가며 간단한 독서·진로 상담 도구로 활용해 보세요.*"
    )
