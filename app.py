import streamlit as st
import pandas as pd
import random

# 针对手机屏幕进行优化配置
st.set_page_config(page_title="移动知识刷题", page_icon="📱", layout="centered")

# 强制手机端隐藏不必要的组件，加大字号和按钮尺寸，防止手指误触
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        height: 50px;
        font-size: 18px !important;
        margin-top: 10px;
        border-radius: 10px;
    }
    div[data-testid="stMarkdownContainer"] p {
        font-size: 18px !important;
    }
    label {
        font-size: 16px !important;
    }
    </style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    df = pd.read_excel("题库(1).xlsx")
    return df.fillna("")

try:
    df = load_data()
except Exception as e:
    st.error("未找到题库文件，请确保 '题库(1).xlsx' 与本程序在同一目录下。")
    st.stop()

if 'current_index' not in st.session_state:
    st.session_state.current_index = 0
if 'submitted' not in st.session_state:
    st.session_state.submitted = False
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'total_answered' not in st.session_state:
    st.session_state.total_answered = 0
if 'order' not in st.session_state:
    st.session_state.order = list(range(len(df)))

st.title("📱 手机专项刷题系统")

# 手机端紧凑型进度与正确率看板
col1, col2 = st.columns(2)
with col1:
    st.caption(f"进度: {st.session_state.current_index + 1} / {len(df)}")
with col2:
    st.caption(f"正确率: {st.session_state.score}/{st.session_state.total_answered}")

st.progress((st.session_state.current_index) / len(df) if len(df) > 0 else 0)

if st.session_state.current_index < len(st.session_state.order):
    real_idx = st.session_state.order[st.session_state.current_index]
    row = df.iloc[real_idx]
    
    st.markdown(f"**【{row['题型']}】**")
    st.markdown(f"### {row['问题']}")
    
    options = {}
    for letter in ['A', 'B', 'C', 'D', 'E']:
        opt_text = row.get(f'选项{letter}', '')
        if opt_text:
            options[letter] = f"{letter}. {opt_text}"
            
    correct_answer = str(row['正确答案']).strip().upper()
    user_answer = None
    
    if row['题型'] == "单选题":
        choice = st.radio("选择答案：", options=list(options.values()), index=None, key=f"q_{real_idx}")
        if choice:
            user_answer = choice[0]
            
    elif row['题型'] == "多选题":
        st.write("选择答案（多选）：")
        selected_opts = []
        for letter, text in options.items():
            if st.checkbox(text, key=f"q_{real_idx}_{letter}"):
                selected_opts.append(letter)
        if selected_opts:
            user_answer = "".join(sorted(selected_opts))

    if not st.session_state.submitted:
        if st.button("📥 提交答案", type="primary"):
            if not user_answer:
                st.warning("请先选择答案！")
            else:
                st.session_state.submitted = True
                st.session_state.total_answered += 1
                if user_answer == correct_answer:
                    st.session_state.score += 1
                st.rerun()
    else:
        if user_answer == correct_answer:
            st.success(f"正解！ 你的答案: {user_answer}")
        else:
            st.error(f"答错啦！正确答案是: {correct_answer}")
            
        st.info("💡 **答案详情：**\n" + "\n".join([options[l] for l in correct_answer if l in options]))
        
        if st.button("➡️ 下一题"):
            st.session_state.current_index + 1
            st.session_state.current_index += 1
            st.session_state.submitted = False
            st.rerun()

    # 底部辅助功能按钮
    st.markdown("---")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🔀 打乱顺序"):
            random.shuffle(st.session_state.order)
            st.session_state.current_index = 0
            st.session_state.submitted = False
            st.rerun()
    with c2:
        if st.button("🔄 重新开始"):
            st.session_state.current_index = 0
            st.session_state.submitted = False
            st.session_state.score = 0
            st.session_state.total_answered = 0
            st.rerun()
else:
    st.balloons()
    st.success("🏆 恭喜你，全部题目都刷完啦！")