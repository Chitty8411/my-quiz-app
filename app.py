import streamlit as st
import pandas as pd
import random

# 针对手机屏幕进行终极美化配置，强制折叠侧边栏
st.set_page_config(
    page_title="泰圣奇知识刷题系统", 
    page_icon="📱", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.markdown("""
    <style>
    /* 全局背景色调 */
    .stApp {
        background-color: #f8fafc;
    }
    
    /* 强力压缩 Streamlit 容器内部小部件的纵向默认间距，确保一屏展示 */
    [data-testid="stVerticalBlock"] > div {
        gap: 0.4rem !important;
    }
    
    /* 隐藏顶部白边，降低内边距，挤压出首屏空间 */
    .block-container {
        padding-top: 0.5rem !important;
        padding-bottom: 0.5rem !important;
        padding-left: 0.75rem !important;
        padding-right: 0.75rem !important;
    }
    
    /* 顶部渐变状态卡片 - 缩减内边距与高度 */
    .dashboard-card {
        background: linear-gradient(135deg, #0f2b5c 0%, #1a52a5 100%);
        color: white;
        padding: 10px 14px;
        border-radius: 12px;
        box-shadow: 0 5px 10px rgba(26, 82, 165, 0.1);
        margin-bottom: 6px;
    }
    
    .dashboard-title {
        font-size: 11px !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        opacity: 0.8;
        font-weight: 500;
        margin-bottom: 2px;
    }
    
    .dashboard-value {
        font-size: 20px !important;
        font-weight: 700 !important;
        color: #ffffff !important;
    }
    
    /* 题目核心容器卡片 - 紧凑型内边距 */
    .question-card {
        background-color: #ffffff;
        border-left: 5px solid #1a52a5;
        padding: 12px 14px;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.02);
        margin-bottom: 10px;
    }
    
    /* 错题回顾专用卡片 */
    .wrong-question-card {
        background-color: #ffffff;
        border-left: 5px solid #ef4444;
        padding: 12px;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.02);
        margin-bottom: 10px;
    }
    
    .question-tag {
        display: inline-block;
        background-color: #eff6ff;
        color: #1e40af;
        padding: 3px 8px;
        font-size: 11px;
        font-weight: 700;
        border-radius: 20px;
        margin-bottom: 6px;
    }
    
    .question-title {
        font-size: 15px !important;
        color: #1e293b !important;
        line-height: 1.4 !important;
        font-weight: 700 !important;
    }
    
    /* 选项卡片包装 - 显著缩减高度与间距，防止多选超出一屏幕 */
    div[data-testid="stRadio"] label, div[data-testid="stCheckbox"] label {
        display: flex;
        align-items: center;
        background-color: #ffffff !important;
        border: 1px solid #e2e8f0 !important;
        padding: 10px 14px !important;
        border-radius: 10px !important;
        margin-bottom: 6px !important;
        transition: all 0.2s ease-in-out !important;
        cursor: pointer !important;
        box-shadow: 0 1px 2px rgba(0,0,0,0.01) !important;
    }
    
    /* 鼠标悬浮及点按选项的高亮动效 */
    div[data-testid="stRadio"] label:hover, div[data-testid="stCheckbox"] label:hover {
        border-color: #1a52a5 !important;
        background-color: #f8fafc !important;
        transform: translateY(-0.5px);
        box-shadow: 0 3px 8px rgba(26, 82, 165, 0.06) !important;
    }
    
    /* 调整原生选择圈/方框的间距 */
    div[data-testid="stRadio"] label p, div[data-testid="stCheckbox"] label p {
        font-size: 14px !important;
        color: #334155 !important;
        font-weight: 500 !important;
    }
    
    /* 提交答案和重置进度核心按钮 - 高度压缩至 44px 更适合拇指点击，蓝色渐变 */
    .stButton>button[kind="primary"] {
        width: 100% !important;
        height: 44px !important;
        background: linear-gradient(90deg, #1a52a5 0%, #2563eb 100%) !important;
        color: white !important;
        font-size: 15px !important;
        font-weight: 600 !important;
        border-radius: 10px !important;
        border: none !important;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.2) !important;
        transition: all 0.2s ease !important;
    }
    
    .stButton>button[kind="primary"]:active {
        transform: scale(0.98) !important;
        box-shadow: 0 2px 6px rgba(37, 99, 235, 0.15) !important;
    }
    
    /* 底部辅助小按钮 (打乱题库等按钮) - 设定精美高档的“罗兰紫”配色 */
    .stButton>button[kind="secondary"] {
        background: linear-gradient(90deg, #7c3aed 0%, #8b5cf6 100%) !important;
        color: white !important;
        font-size: 14px !important;
        font-weight: 600 !important;
        border-radius: 10px !important;
        border: none !important;
        box-shadow: 0 4px 10px rgba(124, 58, 246, 0.15) !important;
        height: 44px !important;
        width: 100% !important;
        transition: all 0.2s ease !important;
    }
    
    .stButton>button[kind="secondary"]:hover {
        background: linear-gradient(90deg, #6d28d9 0%, #7c3aed 100%) !important;
        box-shadow: 0 6px 12px rgba(124, 58, 246, 0.25) !important;
    }
    
    .stButton>button[kind="secondary"]:active {
        transform: scale(0.97) !important;
    }
    
    /* 【神级修复】彻底摒弃属性选择器，直接使用原生底层类对横向列布局执行绝对锁定 */
    .stHorizontalBlock,
    .stHorizontalBlock > div {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        gap: 8px !important; /* 精准对齐上方 flex-gap 的 8px */
        width: 100% !important;
    }
    
    /* 对所有列宽度进行强效对半分，强力挤出屏幕内空间 */
    .stColumn {
        width: calc(50% - 4px) !important; /* 精准分摊，50% 减去 4px 间距 */
        flex: 1 1 0% !important; /* 强制平分，不允许任何溢出 */
        min-width: 0 !important;  /* 击碎任何原生 250px 限制 */
        max-width: calc(50% - 4px) !important;
    }
    
    /* 深度递归级联：锁定列内部任何深层包裹 div 和元素，彻底消除撑开宽度的可能 */
    .stColumn div,
    .stColumn * {
        min-width: 0 !important;
        max-width: 100% !important;
        width: 100% !important;
    }

    /* 针对并行小按钮内部的 padding 和文字换行进行深度控制，打碎 white-space: nowrap */
    .stColumn button {
        padding-left: 2px !important;
        padding-right: 2px !important;
    }

    .stColumn button p,
    .stColumn button span {
        font-size: 11px !important; /* 降低字号，确保在超窄屏下也能塞得进 */
        white-space: normal !important; /* 允许在极窄屏幕下进行优雅换行，绝不允许挤压容器宽度 */
        line-height: 1.1 !important;
        letter-spacing: -0.6px !important; /* 稍微压缩字间距 */
        text-align: center !important;
        display: block !important;
    }
    
    /* 进度条精细化 */
    .stProgress > div > div > div > div {
        background-color: #2563eb !important;
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
    st.error("⚠️ 未找到题库文件，请确保 '题库(1).xlsx' 在 GitHub 仓库的主目录下。")
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
if 'wrong_questions' not in st.session_state:
    st.session_state.wrong_questions = []

# 用于选项打乱的高级状态缓存机制，避免刷新时选项排序乱跳
if 'shuffle_options' not in st.session_state:
    st.session_state.shuffle_options = False
if 'shuffled_options_cache' not in st.session_state:
    st.session_state.shuffled_options_cache = {}

current_num = st.session_state.current_index + 1
accuracy = int((st.session_state.score / st.session_state.total_answered * 100)) if st.session_state.total_answered > 0 else 0

if st.session_state.current_index < len(st.session_state.order):
    # 使用原生 Flexbox 高级排版机制，完美对齐下方即将重修的并排按钮
    st.markdown(f"""
        <div style="display: flex; gap: 8px; margin-bottom: 6px; width: 100%;">
            <div class="dashboard-card" style="flex: 1; margin-bottom: 0;">
                <div class="dashboard-title">📈 刷题进度</div>
                <div class="dashboard-value" style="font-size: 18px !important;">{current_num} <span style="font-size:11px; opacity:0.8;">/ {len(st.session_state.order)} 题</span></div>
            </div>
            <div class="dashboard-card" style="flex: 1; margin-bottom: 0; background: linear-gradient(135deg, #10b981 0%, #059669 100%); box-shadow: 0 5px 10px rgba(16, 185, 129, 0.1);">
                <div class="dashboard-title">🎯 当前胜率</div>
                <div class="dashboard-value" style="font-size: 18px !important;">{accuracy}% <span style="font-size:10px; opacity:0.8;">({st.session_state.score}对/{st.session_state.total_answered}做)</span></div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # 紧凑型进度条
    st.progress((st.session_state.current_index) / len(st.session_state.order) if len(st.session_state.order) > 0 else 0)

if st.session_state.current_index < len(st.session_state.order):
    real_idx = st.session_state.order[st.session_state.current_index]
    row = df.iloc[real_idx]
    
    st.markdown(f"""
        <div class="question-card">
            <span class="question-tag">🏷️ {row['产品']} · {row['题型']}</span>
            <div class="question-title">{row['问题']}</div>
        </div>
    """, unsafe_allow_html=True)
    
    # 获取并解析原本的所有有效非空选项
    orig_options_list = []
    for letter in ['A', 'B', 'C', 'D', 'E']:
        opt_text = row.get(f'选项{letter}', '')
        if pd.notna(opt_text) and str(opt_text).strip() != "":
            orig_options_list.append((letter, str(opt_text).strip()))
            
    # 如果开启了选项乱序，且还未建立当前题目的缓存，则执行洗牌
    if real_idx not in st.session_state.shuffled_options_cache:
        if st.session_state.shuffle_options:
            shuffled_list = list(orig_options_list)
            attempts = 0
            # 确保洗牌后确实打乱了选项
            while len(orig_options_list) > 1 and shuffled_list == orig_options_list and attempts < 10:
                random.shuffle(shuffled_list)
                attempts += 1
            st.session_state.shuffled_options_cache[real_idx] = shuffled_list
        else:
            st.session_state.shuffled_options_cache[real_idx] = orig_options_list

    # 从选项排序缓存中读取当前展示组合
    active_options = st.session_state.shuffled_options_cache[real_idx]
    
    # 建立展现的 A/B/C/D 字母与原始答案 A/B/C/D 字母之间的双向精确映射，防止错乱
    display_letters = ['A', 'B', 'C', 'D', 'E'][:len(active_options)]
    display_options = {}
    map_display_to_orig = {}
    map_orig_to_display = {}
    
    for i, (orig_letter, text) in enumerate(active_options):
        disp_letter = display_letters[i]
        display_options[disp_letter] = f"{disp_letter}. {text}"
        map_display_to_orig[disp_letter] = orig_letter
        map_orig_to_display[orig_letter] = disp_letter

    # 计算映射后的正确答案
    correct_answer = str(row['正确答案']).strip().upper()
    correct_answer_disp_letters = [map_orig_to_display[l] for l in correct_answer if l in map_orig_to_display]
    correct_answer_disp_str = "".join(sorted(correct_answer_disp_letters))
    
    user_answer_orig = None
    user_answer_disp_str = None
    
    if row['题型'] == "单选题":
        choice = st.radio("请点按选择正确答案：", options=list(display_options.values()), index=None, key=f"q_{real_idx}", label_visibility="collapsed")
        if choice:
            user_answer_disp_str = choice[0]
            user_answer_orig = map_display_to_orig[user_answer_disp_str]
            
    elif row['题型'] == "多选题":
        st.caption("👈 请勾选所有正确答案：")
        selected_disp_opts = []
        for disp_letter, text in display_options.items():
            if st.checkbox(text, key=f"q_{real_idx}_{disp_letter}"):
                selected_disp_opts.append(disp_letter)
        if selected_disp_opts:
            user_answer_disp_str = "".join(sorted(selected_disp_opts))
            selected_orig_opts = [map_display_to_orig[l] for l in selected_disp_opts]
            user_answer_orig = "".join(sorted(selected_orig_opts))

    if not st.session_state.submitted:
        if st.button("📥 确认提交此题", type="primary", use_container_width=True):
            if not user_answer_orig:
                st.warning("⚠️ 请先勾选或选择您的答案！")
            else:
                st.session_state.submitted = True
                st.session_state.total_answered += 1
                if user_answer_orig == correct_answer:
                    st.session_state.score += 1
                else:
                    if not any(item['index'] == real_idx for item in st.session_state.wrong_questions):
                        st.session_state.wrong_questions.append({
                            'index': real_idx,
                            'user_answer': user_answer_orig,
                            'correct_answer': correct_answer
                        })
                st.rerun()
    else:
        if user_answer_orig == correct_answer:
            st.success(f"🎉 答对啦！您的答案是: {user_answer_disp_str}")
        else:
            st.error(f"❌ 答错啦！您的答案是: {user_answer_disp_str}，正确答案是: **{correct_answer_disp_str}**")
            
        st.markdown(f"""
            <div style="background-color: #f0fdf4; border: 1px solid #bbf7d0; padding: 12px; border-radius: 10px; margin-top:5px; margin-bottom:5px;">
                <span style="color:#15803d; font-weight:700; font-size:13px;">💡 正确答案详情：</span><br/>
                <span style="color:#1e293b; font-size:13px; line-height:1.4;">
                    {"<br/>".join([display_options[l] for l in sorted(correct_answer_disp_letters) if l in display_options])}
                </span>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("➡️ 开启下一题", type="primary", use_container_width=True):
            st.session_state.current_index += 1
            st.session_state.submitted = False
            st.rerun()

    st.markdown("<hr style='border-top:1px solid #e2e8f0; margin: 8px 0;'/ >", unsafe_allow_html=True)
    
    # 调用原生 st.columns(2) 模块，由我们重构的 CSS 直接强制接管并 50/50 锁死对齐
    col_shuffle1, col_shuffle2 = st.columns(2)
    with col_shuffle1:
        if st.button("🔀 打乱题库顺序", type="secondary", use_container_width=True):
            random.shuffle(st.session_state.order)
            st.session_state.current_index = 0
            st.session_state.submitted = False
            st.session_state.wrong_questions = [] 
            st.session_state.shuffle_options = False
            st.session_state.shuffled_options_cache = {}
            st.rerun()
    with col_shuffle2:
        if st.button("🔥 打乱题库和选项", type="secondary", use_container_width=True):
            random.shuffle(st.session_state.order)
            st.session_state.current_index = 0
            st.session_state.submitted = False
            st.session_state.wrong_questions = [] 
            st.session_state.shuffle_options = True
            st.session_state.shuffled_options_cache = {}
            st.rerun()
        
    # 重置进度按钮（高档蓝色渐变，与提交按钮高度统一）
    if st.button("🔄 重置进度从头开始", type="primary", use_container_width=True):
        st.session_state.current_index = 0
        st.session_state.submitted = False
        st.session_state.score = 0
        st.session_state.total_answered = 0
        st.session_state.wrong_questions = [] 
        st.session_state.shuffle_options = False
        st.session_state.shuffled_options_cache = {}
        st.rerun()

else:
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
            if st.button("🔥 针对错题重新挑战", type="primary", use_container_width=True):
                st.session_state.order = [item['index'] for item in st.session_state.wrong_questions]
                st.session_state.current_index = 0
                st.session_state.submitted = False
                st.session_state.score = 0
                st.session_state.total_answered = 0
                st.session_state.wrong_questions = [] 
                st.session_state.shuffled_options_cache = {}
                st.rerun()
        with col_w2:
            if st.button("🔄 重新挑战完整题库", type="primary", use_container_width=True):
                st.session_state.order = list(range(len(df)))
                st.session_state.current_index = 0
                st.session_state.submitted = False
                st.session_state.score = 0
                st.session_state.total_answered = 0
                st.session_state.wrong_questions = []
                st.session_state.shuffled_options_cache = {}
                st.rerun()
    else:
        st.markdown("""
            <div style="background-color: #f0fdf4; border: 1px solid #bbf7d0; padding: 25px; border-radius: 16px; text-align: center; margin-top: 20px; box-shadow: 0 4px 12px rgba(16, 185, 129, 0.08);">
                <span style="font-size: 48px;">💯</span>
                <h3 style="color: #16a34a; margin-top: 10px; font-weight:700;">完美的答题记录！</h3>
                <p style="color: #475569; font-size:15px; margin-bottom:0;">您本次没有答错任何题目，满分通过！</p>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔄 再次挑战完整题库", type="primary", use_container_width=True):
            st.session_state.order = list(range(len(df)))
            st.session_state.current_index = 0
            st.session_state.submitted = False
            st.session_state.score = 0
            st.session_state.total_answered = 0
            st.session_state.wrong_questions = []
            st.session_state.shuffled_options_cache = {}
            st.rerun()