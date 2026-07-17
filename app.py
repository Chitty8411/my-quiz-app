import streamlit as st
import pandas as pd
import random
import time
import streamlit.components.v1 as components

st.set_page_config(
    page_title="泰圣奇知识刷题系统", 
    page_icon="📱", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.markdown("""
    <style>
    /* ========================================================
       【终极硬核浅色模式锁定】彻底解除微信/iOS内置浏览器深色反色滤镜
       ======================================================== */
    :root {
        --primary-color: #1a52a5 !important;
        --background-color: #f8fafc !important;
        --secondary-background-color: #ffffff !important;
        --text-color: #1e293b !important;
        color-scheme: light !important;
    }
    
    /* 强力锁定渲染上下文为浅色模式，禁用系统/浏览器级别的反色和色彩调节 */
    html, body, [data-testid="stAppViewContainer"], .stApp, 
    div[data-testid="stRadio"], div[data-testid="stCheckbox"], 
    div[data-baseweb="checkbox"], div[data-baseweb="radio"],
    div[data-baseweb="checkbox"] *, div[data-baseweb="radio"] * {
        color-scheme: light !important;
        supported-color-schemes: light !important;
        filter: none !important;
        -webkit-filter: none !important;
    }
    
    /* 彻底隐藏 Streamlit 默认头部工具栏，回收顶端高度 */
    header[data-testid="stHeader"] {
        display: none !important;
        height: 0px !important;
        visibility: hidden !important;
    }
    
    /* 极窄贴顶：隐藏顶部白边，高度自适应 */
    .block-container {
        padding-top: 0px !important;
        padding-bottom: 0.5rem !important;
        padding-left: 0.75rem !important;
        padding-right: 0.75rem !important;
    }
    
    /* 强力压缩 Streamlit 容器内部小部件的纵向默认间距，确保一屏展示 */
    [data-testid="stVerticalBlock"] > div {
        gap: 0.4rem !important;
    }
    
    /* ========================================================
       【精准暗黑模式覆盖】拒绝任何系统或媒体查询将卡片或复选框反色
       ======================================================== */
    @media (prefers-color-scheme: dark) {
        html, body, [data-testid="stAppViewContainer"], .stApp {
            background-color: #f8fafc !important;
            color: #1e293b !important;
        }
        
        /* 1. 题干与错题回顾卡片：拒绝反色，强制浅色背景与高对比度文字 */
        .question-card, .wrong-question-card {
            background-color: #ffffff !important;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.02) !important;
        }
        .question-title {
            color: #1e293b !important;
        }
        
        /* 2. 选项卡片：拒绝变黑，锁死白底灰框 */
        div[data-testid="stRadio"] label, div[data-testid="stCheckbox"] label {
            background-color: #ffffff !important;
            border-color: #e2e8f0 !important;
        }
        div[data-testid="stRadio"] label p, div[data-testid="stCheckbox"] label p {
            color: #334155 !important;
        }
        
        /* 3. 进度卡片：拒绝变暗，锁死纯白字体 */
        .dashboard-card, .dashboard-card * {
            color: #ffffff !important;
        }
        .dashboard-title {
            color: rgba(255, 255, 255, 0.8) !important;
        }
        .dashboard-value {
            color: #ffffff !important;
        }
        
        /* 4. 主副按钮：确保高亮文字始终保持清晰白色 */
        .stButton > button, .stButton > button * {
            color: #ffffff !important;
        }
    }
    
    /* ========================================================
       【重装复选框/单选框防黑化规则】彻底解决图一中的黑色块
       ======================================================== */
    /* 针对未选中状态：使用轻微的非纯白色以绕过部分浏览器的智能反色，同时锁定边框 */
    div[data-baseweb="checkbox"] > div:first-child,
    div[data-baseweb="radio"] > div:first-child {
        background-color: #f8fafc !important;
        border: 2px solid #cbd5e1 !important;
        border-radius: 4px !important;
        box-shadow: none !important;
        filter: none !important;
        -webkit-filter: none !important;
    }
    
    /* 针对单选框（Radio）的圆形外观复原 */
    div[data-baseweb="radio"] > div:first-child {
        border-radius: 50% !important;
    }
    
    /* 被选中状态：强制保持高辨识度的活力宝蓝，防止在深色模式下变成灰黑色 */
    div[data-baseweb="checkbox"] input:checked + div,
    div[data-baseweb="radio"] input:checked + div,
    div[data-baseweb="checkbox"] input:checked ~ div,
    div[data-baseweb="radio"] input:checked ~ div {
        background-color: #1a52a5 !important;
        border-color: #1a52a5 !important;
        filter: none !important;
        -webkit-filter: none !important;
    }

    /* 全局网页背景色调 */
    .stApp {
        background-color: #f8fafc !important;
    }
    
    /* ========================================================
       【卡片与模块排版精细化】
       ======================================================== */
    /* 顶部渐变状态卡片 - 极佳高度与紧凑感 */
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
        color: #ffffff;
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
    
    /* 调整单选框与复选框文字的字号及颜色 */
    div[data-testid="stRadio"] label p, div[data-testid="stCheckbox"] label p {
        font-size: 14px !important;
        color: #334155 !important;
        font-weight: 500 !important;
    }
    
    /* ========================================================
       【按钮极致加高美化：舒适大拇指点按体验】
       ======================================================== */
    /* 提交答案和重置进度核心按钮 - 高度设定为 52px，渐变蓝 */
    .stButton>button[kind="primary"] {
        width: 100% !important;
        height: 52px !important;
        background: linear-gradient(90deg, #1a52a5 0%, #2563eb 100%) !important;
        color: white !important;
        font-size: 16px !important;
        font-weight: 700 !important;
        border-radius: 12px !important;
        border: none !important;
        box-shadow: 0 4px 14px rgba(37, 99, 235, 0.25) !important;
        transition: all 0.2s ease !important;
    }
    
    .stButton>button[kind="primary"]:active {
        transform: scale(0.97) !important;
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
    
    /* ========================================================
       【重构原生双列并排机制：锁定两端无缝齐平】
       ======================================================== */
    /* 彻底解禁 Flex 行换行，确保手机端两个列永远在一条横线上并列摆放 */
    .stHorizontalBlock,
    .stHorizontalBlock > div {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        gap: 8px !important; /* 对齐上方卡片的两端 */
        width: 100% !important;
    }
    
    /* 强制解除 250px 限制，完美50/50对半分 */
    .stColumn {
        width: calc(50% - 4px) !important;
        flex: 1 1 0% !important;
        min-width: 0 !important;
        max-width: calc(50% - 4px) !important;
    }
    
    /* 深度穿透列内的多重嵌套 React 包装元素，全部设为自适应 */
    .stColumn div,
    .stColumn * {
        min-width: 0 !important;
        max-width: 100% !important;
        width: 100% !important;
    }

    /* 优化内边距使 14px 字体两行能完美塞入 */
    .stColumn button {
        padding-left: 2px !important;
        padding-right: 2px !important;
    }

    .stColumn button p,
    .stColumn button span {
        font-size: 14px !important; /* 完美恢复为与主按钮一致的标准字号 */
        white-space: normal !important; /* 在超窄屏幕上优雅折行，绝不向两边挤爆出屏外 */
        line-height: 1.15 !important;
        letter-spacing: -0.5px !important;
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

# 新增计时器状态控制
if 'start_time' not in st.session_state:
    st.session_state.start_time = None
if 'elapsed_time' not in st.session_state:
    st.session_state.elapsed_time = 0

# 用于选项打乱的高级状态缓存机制
if 'shuffle_options' not in st.session_state:
    st.session_state.shuffle_options = False
if 'shuffled_options_cache' not in st.session_state:
    st.session_state.shuffled_options_cache = {}

current_num = st.session_state.current_index + 1
accuracy = int((st.session_state.score / st.session_state.total_answered * 100)) if st.session_state.total_answered > 0 else 0

if st.session_state.current_index < len(st.session_state.order):
    # 使用原生 Flexbox 高级排版机制，完美对齐下方并排按钮
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
                # 记录开始计时（用户提交第一题时正式开始）
                if st.session_state.start_time is None:
                    st.session_state.start_time = time.time()

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
                
                # 如果是最后一题被确认提交，立即结算最终用时
                if st.session_state.current_index + 1 >= len(st.session_state.order):
                    if st.session_state.start_time is not None:
                        st.session_state.elapsed_time = time.time() - st.session_state.start_time
                    else:
                        st.session_state.elapsed_time = 0
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
    
    # 完美双子星紫色打乱按钮并列布局
    col_shuffle1, col_shuffle2 = st.columns(2)
    with col_shuffle1:
        if st.button("🔀 打乱题库顺序", type="secondary", use_container_width=True):
            random.shuffle(st.session_state.order)
            st.session_state.current_index = 0
            st.session_state.submitted = False
            st.session_state.wrong_questions = [] 
            st.session_state.shuffle_options = False
            st.session_state.shuffled_options_cache = {}
            st.session_state.start_time = None # 重置计时
            st.session_state.elapsed_time = 0
            st.rerun()
    with col_shuffle2:
        if st.button("🔥 打乱题库和选项", type="secondary", use_container_width=True):
            random.shuffle(st.session_state.order)
            st.session_state.current_index = 0
            st.session_state.submitted = False
            st.session_state.wrong_questions = [] 
            st.session_state.shuffle_options = True
            st.session_state.shuffled_options_cache = {}
            st.session_state.start_time = None # 重置计时
            st.session_state.elapsed_time = 0
            st.rerun()
        
    # 重置进度按钮（高档蓝色渐变，与确认提交按钮风格统一）
    if st.button("🔄 重置进度从头开始", type="primary", use_container_width=True):
        st.session_state.current_index = 0
        st.session_state.submitted = False
        st.session_state.score = 0
        st.session_state.total_answered = 0
        st.session_state.wrong_questions = [] 
        st.session_state.shuffle_options = False
        st.session_state.shuffled_options_cache = {}
        st.session_state.start_time = None # 重置计时
        st.session_state.elapsed_time = 0
        st.rerun()

else:
    st.balloons()
    
    # 注入强制回到顶部 JavaScript，保证一进入结束页面直接从顶部（战报）展示
    components.html("""
        <script>
            if (window.parent) {
                window.parent.scrollTo({
                    top: 0,
                    behavior: 'smooth'
                });
            }
        </script>
    """, height=0, width=0)
    
    # 格式化用时：分、秒展示
    total_seconds = int(st.session_state.elapsed_time)
    if total_seconds < 60:
        time_display_str = f"{total_seconds} 秒"
    else:
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        time_display_str = f"{minutes} 分 {seconds} 秒"
        
    final_accuracy = int((st.session_state.score / len(st.session_state.order) * 100)) if len(st.session_state.order) > 0 else 0
    
    # 智能等级评价
    if final_accuracy == 100:
        grade_comment = "🌟 超凡大师！神级表现，完全无懈可击！"
    elif final_accuracy >= 90:
        grade_comment = "🔥 荣耀学霸！底子极其扎实，傲视群雄！"
    elif final_accuracy >= 80:
        grade_comment = "⚡ 渐入佳境！实力在线，稍加复习即臻完美！"
    elif final_accuracy >= 60:
        grade_comment = "📈 稳步前行！多看错题总结，加油突击！"
    else:
        grade_comment = "💪 再接再厉！坚持不懈，错题集是你的通关秘籍！"

    # 精美渐变结业战报 HTML 卡片展示在最上方 - 极致贴顶并拉高上下高度(padding: 45px 16px)
    st.markdown(f"""
        <div style="background: linear-gradient(135deg, #0f2b5c 0%, #1a52a5 100%); color: white !important; padding: 45px 16px; border-radius: 16px; box-shadow: 0 10px 25px rgba(26, 82, 165, 0.15); margin-top: 8px; margin-bottom: 16px; text-align: center;">
            <div style="font-size: 22px; font-weight: 800; margin-bottom: 10px; letter-spacing: 0.5px; color: #ffffff !important;">🏆 泰圣奇刷题结业战报</div>
            <div style="font-size: 13px; opacity: 0.8; margin-bottom: 24px; color: #ffffff !important;">恭喜您完成了本次的全部挑战！</div>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 24px;">
                <div style="background: rgba(255, 255, 255, 0.1); padding: 12px; border-radius: 12px; text-align: center; border: 1px solid rgba(255,255,255,0.05);">
                    <div style="font-size: 11px; opacity: 0.8; margin-bottom: 3px; color: rgba(255,255,255,0.8) !important;">⏱️ 刷题用时</div>
                    <div style="font-size: 16px; font-weight: 700; color: #ffffff !important;">{time_display_str}</div>
                </div>
                <div style="background: rgba(255, 255, 255, 0.1); padding: 12px; border-radius: 12px; text-align: center; border: 1px solid rgba(255,255,255,0.05);">
                    <div style="font-size: 11px; opacity: 0.8; margin-bottom: 3px; color: rgba(255,255,255,0.8) !important;">🎯 本次胜率</div>
                    <div style="font-size: 16px; font-weight: 700; color: #10b981 !important;">{final_accuracy}%</div>
                </div>
                <div style="background: rgba(255, 255, 255, 0.1); padding: 12px; border-radius: 12px; text-align: center; border: 1px solid rgba(255,255,255,0.05);">
                    <div style="font-size: 11px; opacity: 0.8; margin-bottom: 3px; color: rgba(255,255,255,0.8) !important;">✅ 答对题数</div>
                    <div style="font-size: 16px; font-weight: 700; color: #34d399 !important;">{st.session_state.score} 题</div>
                </div>
                <div style="background: rgba(255, 255, 255, 0.1); padding: 12px; border-radius: 12px; text-align: center; border: 1px solid rgba(255,255,255,0.05);">
                    <div style="font-size: 11px; opacity: 0.8; margin-bottom: 3px; color: rgba(255,255,255,0.8) !important;">❌ 答错题数</div>
                    <div style="font-size: 16px; font-weight: 700; color: #f87171 !important;">{len(st.session_state.wrong_questions)} 题</div>
                </div>
            </div>
            <div style="border-top: 1px solid rgba(255, 255, 255, 0.15); padding-top: 16px; font-size: 13px; font-weight: 700; color: #f3f4f6 !important; letter-spacing: 0.5px;">
                {grade_comment}
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.wrong_questions:
        # 错题回顾上方的完美并排重新挑战按钮（现在挪到战报下方，错题上方，并高对比度的经典耀眼蓝展现）
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
                st.session_state.start_time = None
                st.session_state.elapsed_time = 0
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
                st.session_state.start_time = None
                st.session_state.elapsed_time = 0
                st.rerun()

        st.markdown("<hr style='border-top:1px solid #e2e8f0; margin: 12px 0;'/ >", unsafe_allow_html=True)

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
            st.session_state.start_time = None
            st.session_state.elapsed_time = 0
            st.rerun()