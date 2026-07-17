import streamlit as st
import pandas as pd
import random

# 针对手机屏幕进行终极美化配置
st.set_page_config(
    page_title="泰圣奇知识刷题系统", 
    page_icon="📱", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 注入精美的高级 CSS 样式表 (Roche蓝 & 极光绿配色)
st.markdown("""
    <style>
    /* 全局背景色调 */
    .stApp {
        background-color: #f8fafc;
    }
    
    /* 隐藏顶部白边，优化紧凑度 */
    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 2rem !important;
    }
    
    /* 顶部渐变状态卡片 */
    .dashboard-card {
        background: linear-gradient(135deg, #0f2b5c 0%, #1a52a5 100%);
        color: white;
        padding: 20px;
        border-radius: 16px;
        box-shadow: 0 10px 20px rgba(26, 82, 165, 0.15);
        margin-bottom: 20px;
    }
    
    .dashboard-title {
        font-size: 13px !important;
        text-transform: uppercase;
        letter-spacing: 1px;
        opacity: 0.8;
        font-weight: 500;
        margin-bottom: 4px;
    }
    
    .dashboard-value {
        font-size: 26px !important;
        font-weight: 700 !important;
        color: #ffffff !important;
    }
    
    /* 题目核心容器卡片 */
    .question-card {
        background-color: #ffffff;
        border-left: 6px solid #1a52a5;
        padding: 22px;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.03);
        margin-bottom: 25px;
    }
    
    /* 错题回顾专用卡片 */
    .wrong-question-card {
        background-color: #ffffff;
        border-left: 6px solid #ef4444;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.03);
        margin-bottom: 20px;
    }
    
    .question-tag {
        display: inline-block;
        background-color: #eff6ff;
        color: #1e40af;
        padding: 5px 12px;
        font-size: 12px;
        font-weight: 700;
        border-radius: 30px;
        margin-bottom: 12px;
    }
    
    .question-title {
        font-size: 20px !important;
        color: #1e293b !important;
        line-height: 1.5 !important;
        font-weight: 700 !important;
    }
    
    /* 选项框的完美卡片化包装 */
    div[data-testid="stRadio"] label, div[data-testid="stCheckbox"] label {
        display: flex;
        align-items: center;
        background-color: #ffffff !important;
        border: 1.5px solid #e2e8f0 !important;
        padding: 16px 20px !important;
        border-radius: 14px !important;
        margin-bottom: 12px !important;
        transition: all 0.2s ease-in-out !important;
        cursor: pointer !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.01) !important;
    }
    
    /* 鼠标悬浮及点按状态 */
    div[data-testid="stRadio"] label:hover, div[data-testid="stCheckbox"] label:hover {
        border-color: #1a52a5 !important;
        background-color: #f8fafc !important;
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(26, 82, 165, 0.08) !important;
    }
    
    /* 调整原生选择圈/方框的间距 */
    div[data-testid="stRadio"] label p, div[data-testid="stCheckbox"] label p {
        font-size: 16px !important;
        color: #334155 !important;
        font-weight: 500 !important;
    }
    
    /* 提交答案核心按钮 */
    .stButton>button {
        width: 100% !important;
        height: 52px !important;
        background: linear-gradient(90deg, #1a52a5 0%, #2563eb 100%) !important;
        color: white !important;
        font-size: 18px !important;
        font-weight: 600 !important;
        border-radius: 14px !important;
        border: none !important;
        box-shadow: 0 6px 20px rgba(37, 99, 235, 0.25) !important;
        transition: all 0.2s ease !important;
    }
    
    .stButton>button:active {
        transform: scale(0.98) !important;
        box-shadow: 0 3px 10px rgba(37, 99, 235, 0.2) !important;
    }
    
    /* 底部辅助小按钮 */
    div[data-testid="column"] button {
        background-color: #f1f5f9 !important;
        color: #475569 !important;
        font-size: 15px !important;
        border-radius: 12px !important;
        border: 1px solid #e2e8f0 !important;
        box-shadow: none !important;
        height: 44px !important;
    }
    
    div[data-testid="column"] button:hover {
        background-color: #e2e8f0 !important;
        color: #1e293b !important;
        border-color: #cbd5e1 !important;
    }
    
    /* 进度条精细化 */
    .stProgress > div > div > div > div {
        background-color: #2563eb !important;
    }
    </style>
""", unsafe_allow_html=True)

# 3. 加载题库数据
@st.cache_data
def load_data():
    df = pd.read_excel("题库(1).xlsx")
    return df.fillna("")

try:
    df = load_data()
except Exception as e:
    st.error("⚠️ 未找到题库文件，请确保 '题库(1).xlsx' 在 GitHub 仓库的主目录下。")
    st.stop()

# 4. 初始化和保持刷题状态
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
if 'wrong_questions' not in st.session_state:
    st.session_state.wrong_questions = [] # 用来存放错题

# 5. 顶栏：高级渐变卡片式仪表盘
current_num = st.session_state.current_index + 1
accuracy = int((st.session_state.score / st.session_state.total_answered * 100)) if st.session_state.total_answered > 0 else 0

# 只有没刷完时才显示顶栏状态卡
if st.session_state.current_index < len(st.session_state.order):
    col_dash1, col_dash2 = st.columns(2)
    with col_dash1:
        st.markdown(f"""
            <div class="dashboard-card">
                <div class="dashboard-title">📈 刷题进度</div>
                <div class="dashboard-value">{current_num} <span style="font-size:16px; opacity:0.8;">/ {len(st.session_state.order)} 题</span></div>
            </div>
        """, unsafe_allow_html=True)
    with col_dash2:
        st.markdown(f"""
            <div class="dashboard-card" style="background: linear-gradient(135deg, #10b981 0%, #059669 100%); box-shadow: 0 10px 20px rgba(16, 185, 129, 0.15);">
                <div class="dashboard-title">🎯 当前胜率</div>
                <div class="dashboard-value">{accuracy}% <span style="font-size:16px; opacity:0.8;">({st.session_state.score}对/{st.session_state.total_answered}做)</span></div>
            </div>
        """, unsafe_allow_html=True)

    # 进度条
    st.progress((st.session_state.current_index) / len(st.session_state.order) if len(st.session_state.order) > 0 else 0)
    st.write("") 

# 6. 核心刷题逻辑
if st.session_state.current_index < len(st.session_state.order):
    real_idx = st.session_state.order[st.session_state.current_index]
    row = df.iloc[real_idx]
    
    st.markdown(f"""
        <div class="question-card">
            <span class="question-tag">🏷️ {row['产品']} · {row['题型']}</span>
            <div class="question-title">{row['问题']}</div>
        </div>
    """, unsafe_allow_html=True)
    
    options = {}
    for letter in ['A', 'B', 'C', 'D', 'E']:
        opt_text = row.get(f'选项{letter}', '')
        if opt_text:
            options[letter] = f"{letter}. {opt_text}"
            
    correct_answer = str(row['正确答案']).strip().upper()
    user_answer = None
    
    if row['题型'] == "单选题":
        choice = st.radio("请点按选择正确答案：", options=list(options.values()), index=None, key=f"q_{real_idx}", label_visibility="collapsed")
        if choice:
            user_answer = choice[0]
            
    elif row['题型'] == "多选题":
        st.caption("👈 请勾选所有正确答案：")
        selected_opts = []
        for letter, text in options.items():
            if st.checkbox(text, key=f"q_{real_idx}_{letter}"):
                selected_opts.append(letter)
        if selected_opts:
            user_answer = "".join(sorted(selected_opts))

    # 7. 答题提交与即时反馈
    st.write("")
    if not st.session_state.submitted:
        if st.button("📥 确认提交此题"):
            if not user_answer:
                st.warning("⚠️ 请先勾选或选择您的答案！")
            else:
                st.session_state.submitted = True
                st.session_state.total_answered += 1
                if user_answer == correct_answer:
                    st.session_state.score += 1
                else:
                    if not any(item['index'] == real_idx for item in st.session_state.wrong_questions):
                        st.session_state.wrong_questions.append({
                            'index': real_idx,
                            'user_answer': user_answer,
                            'correct_answer': correct_answer
                        })
                st.rerun()
    else:
        if user_answer == correct_answer:
            st.success(f"🎉 答对啦！您的答案是: {user_answer}")
        else:
            st.error(f"❌ 答错啦！您的答案是: {user_answer}，正确答案是: **{correct_answer}**")
            
        st.markdown(f"""
            <div style="background-color: #f0fdf4; border: 1px solid #bbf7d0; padding: 16px; border-radius: 12px; margin-top:10px; margin-bottom:15px;">
                <span style="color:#15803d; font-weight:700; font-size:15px;">💡 正确答案详情：</span><br/>
                <span style="color:#1e293b; font-size:14px; line-height:1.6;">
                    {"<br/>".join([options[l] for l in correct_answer if l in options])}
                </span>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("➡️ 开启下一题"):
            st.session_state.current_index += 1
            st.session_state.submitted = False
            st.rerun()

    # 8. 辅助控制面板
    st.markdown("<br/><hr style='border-top:1px solid #e2e8f0;'/><br/>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🔀 打乱题库顺序"):
            random.shuffle(st.session_state.order)
            st.session_state.current_index = 0
            st.session_state.submitted = False
            st.session_state.wrong_questions = [] 
            st.rerun()
    with c2:
        if st.button("🔄 重置进度从头开始"):
            st.session_state.current_index = 0
            st.session_state.submitted = False
            st.session_state.score = 0
            st.session_state.total_answered = 0
            st.session_state.wrong_questions = [] 
            st.rerun()
else:
    # 9. 刷题结束画面 + 错题本生成
    st.balloons()
    st.success(f"🏆 太了不起了！您已经完成了本次全部 {len(st.session_state.order)} 道题目的挑战！")
    
    if st.session_state.wrong_questions:
        st.markdown(f"### ❌ 本轮错题集回顾 ({len(st.session_state.wrong_questions)} 题)")
        st.caption("以下是您刚刚答错的题目，请仔细看答案对比进行复习：")
        
        for i, item in enumerate(st.session_state.wrong_questions):
            w_idx = item['index']
            w_row = df.iloc[w_idx]
            
            w_options = {}
            for letter in ['A', 'B', 'C', 'D', 'E']:
                opt_text = w_row.get(f'选项{letter}', '')
                if opt_text:
                    w_options[letter] = f"{letter}. {opt_text}"
            
            st.markdown(f"""
                <div class="wrong-question-card">
                    <span class="question-tag" style="background-color: #fef2f2; color: #991b1b;">📌 错题 {i+1} · {w_row['产品']} · {w_row['题型']}</span>
                    <div class="question-title" style="font-size:17px !important; margin-bottom: 12px;">{w_row['问题']}</div>
                    <div style="font-size:14px; color:#475569; margin-bottom:12px; line-height:1.6;">
                        {"<br/>".join([w_options[l] for l in w_options])}
                    </div>
                    <div style="background-color: #fff5f5; border: 1px solid #fee2e2; padding: 12px; border-radius: 10px; font-size:14px; line-height:1.5;">
                        <span style="color:#dc2626; font-weight:700;">❌ 您的答案：</span> {item['user_answer']} &nbsp;&nbsp;|&nbsp;&nbsp; 
                        <span style="color:#16a34a; font-weight:700;">✅ 正确答案：</span> {item['correct_answer']}
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
        st.markdown("<br/>", unsafe_allow_html=True)
        col_w1, col_w2 = st.columns(2)
        with col_w1:
            if st.button("🔥 针对错题重新挑战"):
                st.session_state.order = [item['index'] for item in st.session_state.wrong_questions]
                st.session_state.current_index = 0
                st.session_state.submitted = False
                st.session_state.score = 0
                st.session_state.total_answered = 0
                st.session_state.wrong_questions = [] 
                st.rerun()
        with col_w2:
            if st.button("🔄 重新挑战完整题库"):
                st.session_state.order = list(range(len(df)))
                st.session_state.current_index = 0
                st.session_state.submitted = False
                st.session_state.score = 0
                st.session_state.total_answered = 0
                st.session_state.wrong_questions = []
                st.rerun()
    else:
        st.markdown("""
            <div style="background-color: #f0fdf4; border: 1px solid #bbf7d0; padding: 25px; border-radius: 16px; text-align: center; margin-top: 20px; box-shadow: 0 4px 12px rgba(16, 185, 129, 0.08);">
                <span style="font-size: 48px;">💯</span>
                <h3 style="color: #16a34a; margin-top: 10px; font-weight:700;">完美的答题记录！</h3>
                <p style="color: #475569; font-size:15px; margin-bottom:0;">您本次没有答错任何题目，满分通过！</p>
            </div>
        """, unsafe_allow_html=True)
        st.write("")
        if st.button("🔄 再次挑战完整题库"):
            st.session_state.order = list(range(len(df)))
            st.session_state.current_index = 0
            st.session_state.submitted = False
            st.session_state.score = 0
            st.session_state.total_answered = 0
            st.session_state.wrong_questions = []
            st.rerun()