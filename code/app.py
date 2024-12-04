import streamlit as st

st.set_page_config(page_title="ETF 자동분석 보고서", page_icon="📊", layout="wide")

st.title("원자재 ETF 선택")

etf_categories = {
    "농산물": {"color": "#98FB98", "image": "🌾"},
    "금": {"color": "#FFD700", "image": "🪙"},
    "은": {"color": "#C0C0C0", "image": "🪞"},
    "기타 귀금속": {"color": "#DAA520", "image": "⚜️"},
    "탄소배출권": {"color": "#90EE90", "image": "🌍"},
    "원유": {"color": "#FF6347", "image": "🛢️"},
    "기타 금속": {"color": "#87CEEB", "image": "🔩"}
}

if "selected_category" not in st.session_state:
    st.session_state["selected_category"] = None

st.markdown(
    """
    <style>
    .etf-button {
        display: flex;
        align-items: center;
        justify-content: flex-start;
        border-radius: 20px;
        height: 200px;
        width: 90%;
        margin: 20px auto;
        padding: 20px;
        font-size: 28px;
        font-weight: bold;
        color: white;
        cursor: pointer;
        transition: transform 0.3s, background-color 0.3s;
        text-align: left;
    }
    .etf-button:hover {
        transform: scale(1.05);
        background-color: #ccc;
    }
    .action-container {
        display: flex;
        align-items: center;
        justify-content: center;
        margin-top: 50px;
        gap: 20px;
    }
    .selected-category {
        padding: 20px;
        background-color: #ADD8E6;
        border-radius: 20px;
        width: 40%;
        text-align: center;
        font-size: 24px;
        font-weight: bold;
    }
    .action-button {
        height: 80px;
        width: 200px;
        background-color: #32CD32;
        color: white;
        font-size: 24px;
        font-weight: bold;
        border-radius: 20px;
        text-align: center;
        line-height: 80px;
        cursor: pointer;
    }
    .action-button:hover {
        background-color: #2E8B57;
    }
    </style>
    """,
    unsafe_allow_html=True
)

cols = st.columns(2, gap="large")
for i, (category, props) in enumerate(etf_categories.items()):
    with cols[i % 2]:
        st.markdown(
            f"""
            <div class="etf-button" style="background-color: {props['color']};">
                {props['image']} {category}
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button(category, key=f"button_{category}"):
            st.session_state["selected_category"] = category

st.markdown(
    f"""
    <div class="action-container">
        <div class="selected-category">
            선택한 ETF 종류: {st.session_state['selected_category'] if st.session_state['selected_category'] else '선택되지 않음'}
        </div>
        <button class="action-button" onclick="window.location.reload()">선택</button>
    </div>
    """,
    unsafe_allow_html=True
)