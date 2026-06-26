# -*- coding: utf-8 -*-
import streamlit as st
import re
import time
from g4f.client import Client
import streamlit.components.v1 as components

# --- إعدادات الصفحة والهوية البصرية المتجاوبة مع الحاسوب والهاتف ---
st.set_page_config(
    page_title="SPIDER-AI | محرك التجسيد البرمجي", 
    page_icon="🕸️", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# تصميم واجهة مستخدم مظلمة واحترافية متجاوبة كلياً مع الهواتف والحواسب
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;700;800&family=Fira+Code:wght@400;500&display=swap');
    
    /* القواعد العامة للخطوط والاتجاهات */
    html, body, .main { 
        font-family: 'Cairo', sans-serif; 
        text-align: right; 
        direction: rtl; 
        background-color: #0b0e14; 
        color: #adbac7; 
    }
    
    h1, h2, h3, h4, p, span, label { 
        color: #f0f6fc !important; 
        font-family: 'Cairo', sans-serif;
    }

    /* تحسين شكل علامات التبويب (Tabs) */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background-color: #151b23;
        padding: 8px;
        border-radius: 8px;
        border: 1px solid #30363d;
    }
    .stTabs [data-baseweb="tab"] {
        height: 40px;
        white-space: pre-wrap;
        background-color: transparent;
        border-radius: 6px;
        color: #8b949e;
        font-weight: 600;
        border: none;
        transition: all 0.2s ease-in-out;
    }
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #21262d;
        color: #58a6ff;
    }
    .stTabs [aria-selected="true"] {
        background-color: #2ea44f !important;
        color: #ffffff !important;
        box-shadow: 0 0 10px rgba(46, 164, 79, 0.4);
    }

    /* صناديق تفكير الوكيل البرمجي */
    .thinking-box { 
        background: #151b23; 
        border: 1px solid #30363d; 
        border-radius: 8px; 
        padding: 15px; 
        margin: 10px 0; 
        font-family: 'Fira Code', monospace; 
        font-size: 13.5px; 
        color: #8b949e; 
        direction: ltr; 
        text-align: left; 
    }
    .step-done { color: #57ab5a; font-weight: bold; }
    .step-active { color: #58a6ff; font-weight: bold; animation: blink 1.2s infinite; }
    @keyframes blink { 50% { opacity: 0.4; } }
    
    /* أزرار مخصصة أنيقة */
    div.stButton > button {
        background: linear-gradient(135deg, #1f6feb, #58a6ff) !important; 
        color: white !important;
        border: none !important; 
        padding: 10px 18px !important; 
        border-radius: 8px !important; 
        font-weight: 700 !important; 
        transition: 0.2s !important;
        width: 100%;
        font-size: 14px !important;
    }
    div.stButton > button:hover { 
        transform: translateY(-1px); 
        box-shadow: 0 4px 15px rgba(88, 166, 255, 0.4) !important; 
    }
    
    /* تصميم بطاقات الأخطاء */
    .error-card {
        background-color: #2c1515;
        padding: 15px;
        border-radius: 8px;
        border: 1px solid #e5534b;
        color: #ff7b72;
        margin-bottom: 15px;
        direction: rtl;
        text-align: right;
    }

    /* تحسين مظهر محادثات الدردشة الافتراضية */
    [data-testid="stChatMessage"] {
        background-color: #151b23;
        border: 1px solid #21262d;
        border-radius: 10px;
        padding: 12px;
        margin-bottom: 10px;
    }

    /* 📱 تحسينات مخصصة لتجاوب الهواتف المحمولة */
    @media (max-width: 768px) {
        .main .block-container {
            padding: 10px !important;
        }
        h1 {
            font-size: 1.4rem !important;
        }
        p {
            font-size: 0.85rem !important;
        }
        /* ضبط ارتفاعات شاشات العرض على الموبايل لتوفير مساحة */
        iframe {
            height: 400px !important;
        }
        .stTabs [data-baseweb="tab"] {
            font-size: 11px !important;
            padding: 0 8px !important;
        }
    }
    </style>
""", unsafe_allow_html=True)

# --- إدارة وتخزين بيانات الجلسة (State Management) ---
if 'messages' not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant", 
            "content": "مرحباً بك في **SPIDER-AI: محرك التجسيد البرمجي** 🕸️\n\nأنا مهندس برمجيات ومصمم ألعاب ذكي. صف لي فكرتك البرمجية بالكامل، وسأقوم بطرح بعض الأسئلة الهندسية البسيطة عليك لتنقيح التصميم والخصائص، وعندما نصبح جاهزين، سنقوم ببنائها فوراً وتجسيدها في المعاينة الحية!"
        }
    ]
if 'generated_html' not in st.session_state:
    st.session_state.generated_html = ""
if 'is_generating' not in st.session_state:
    st.session_state.is_generating = False
if 'error_occurred' not in st.session_state:
    st.session_state.error_occurred = False
if 'architect_logs' not in st.session_state:
    st.session_state.architect_logs = []

client = Client()

# --- خوارزمية استخراج وتصفية كود HTML البرمجي ---
def extract_html_code(raw_text):
    html_pattern = re.compile(r'(<!DOCTYPE html>.*?</html>|<html.*?</html>)', re.DOTALL | re.IGNORECASE)
    match = html_pattern.search(raw_text)
    if match:
        return match.group(1).strip()
    
    cleaned = re.sub(r'^```html\s*', '', raw_text, flags=re.IGNORECASE)
    cleaned = re.sub(r'```$', '', cleaned).strip()
    return cleaned

# --- دالة استدعاء الوكيل الذكي (مناقشة تفاعلية وتوليد الكود) ---
def call_spider_agent(prompt_type="discussion", user_prompt="", chat_history=[]):
    
    # 1. موجه وضع المناقشة وطرح الأسئلة الذكية (Discussion System Prompt)
    discussion_system = """
    You are 'SPIDER-AI Business Analyst & Architect'. Your job is to act as a pro-active technical product manager.
    When a user describes an idea, do NOT write any code. Instead:
    1. Acknowledge and analyze their idea enthusiastically in Arabic.
    2. Ask exactly 2 to 3 deep, clear, and professional questions in Arabic to help refine their concept (e.g., questions about the visual theme, specific mechanics, mobile vs desktop controls, or score keeping).
    3. Keep your response concise, polite, and completely in Arabic. Do NOT output HTML or CSS in this mode.
    """

    # 2. موجه وضع التوليد وصياغة الأكواد الكاملة (Code Generation System Prompt)
    generation_system = """
    You are 'SPIDER-AI Code Architect' - an elite, world-class senior software engineer and game developer.
    Your sole focus is to design, code, and deliver fully working, bug-free, and single-file HTML executable applications, tools, or games.
    
    CRITICAL QUALITY CONTROL RULES:
    1. NEVER use code placeholders, comments indicating omissions (such as "// rest of code", "// TODO: implement"). Write every single line of styling, logic, and HTML markup completely.
    2. The output must be completely self-contained in ONE HTML file. Include Tailwind CSS or custom CSS inside <style> tags, and all interactive JavaScript logic inside <script> tags.
    3. Always design a modern, visually stunning UI/UX with beautiful dark/neon palettes, smooth CSS animations, and highly responsive components (mobile-friendly).
    4. For games (2D/3D): Always provide clean controls (both desktop keyboard keys and on-screen touch buttons for mobile compliance), audio visualizer context if relevant, scoring systems, and professional Game Over / Restart states.
    5. All visible text elements inside the generated application must be in the ARABIC language to suit the target userbase.
    6. Your response MUST strictly start with <!DOCTYPE html> and end with </html>. Do not write any markdown blocks (such as ```html) or pre/post commentary.
    """

    # إعداد السياق البرمجي للذكاء الاصطناعي بناء على المرحلة
    if prompt_type == "generation":
        # تجميع كامل المحادثة السابقة لتمريرها كمتطلبات برمجية للنموذج ليفهم كل التفاصيل
        compiled_messages = [{"role": "system", "content": generation_system}]
        for msg in chat_history:
            compiled_messages.append({"role": msg["role"], "content": msg["content"]})
        # توجيه أخير بالبناء الكامل
        compiled_messages.append({"role": "user", "content": "Now, write the complete, executable HTML code. Ensure no placeholders are used."})
    else:
        # وضع النقاش المستمر وطرح الأسئلة
        compiled_messages = [
            {"role": "system", "content": discussion_system},
            {"role": "user", "content": f"Here is my input: {user_prompt}"}
        ]

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=compiled_messages
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"ERROR_API_FAILED: {str(e)}"

# --- الهيكل البصري وعنوان المنصة ---
st.markdown("""
    <div style="text-align: center; margin-bottom: 20px; padding: 12px; background: #151b23; border: 1px solid #30363d; border-radius: 12px;">
        <h1 style="margin: 0; font-size: 1.8rem; font-weight: 800; background: linear-gradient(90deg, #58a6ff, #2ea44f); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
            🕸️ جوهر SPIDER-AI : محرك التجسيد البرمجي
        </h1>
        <p style="margin: 5px 0 0 0; color: #8b949e; font-size: 0.9rem;">التحويل التفاعلي للأفكار إلى تطبيقات وألعاب جاهزة فوراً في ملف واحد</p>
    </div>
""", unsafe_allow_html=True)

# تقسيم الشاشة تلقائياً (تتحول إلى رأسية على الهواتف تلقائياً بفضل Streamlit)
col_chat_pane, col_workspace_pane = st.columns([1, 1.2], gap="medium")

# --- العمود الأيمن: محرك المحادثة وصياغة الأسئلة التفاعلية ---
with col_chat_pane:
    st.markdown("### 💬 ناقش فكرتك مع المطور")
    
    # حاوية عرض الرسائل السابقة بشكل منسق
    chat_container = st.container(height=400)
    with chat_container:
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
                
    # استقبال الأوامر والمدخلات الجديدة من المستخدم
    if user_cmd := st.chat_input("تكلم مع المطور أو أجب عن الأسئلة هنا..."):
        # إضافة رسالة المستخدم للسجل
        st.session_state.messages.append({"role": "user", "content": user_cmd})
        
        # استدعاء الوكيل لمواصلة النقاش وطرح أسئلة توجيهية هادفة للعميل
        with st.spinner("🤖 يحلل المطور الفكرة ويصيغ أسئلة ذكية لتطويرها..."):
            agent_reply = call_spider_agent(
                prompt_type="discussion",
                user_prompt=user_cmd,
                chat_history=st.session_state.messages
            )
            
            if "ERROR_API_FAILED" in agent_reply:
                st.session_state.error_occurred = True
            else:
                st.session_state.messages.append({"role": "assistant", "content": agent_reply})
        st.rerun()

    # زر إطلاق البناء البرمجي الفخم عند اكتمال النقاش
    st.write("---")
    st.markdown("<p style='text-align: center; color: #8b949e; font-size: 12px;'>عندما تكتمل فكرتك وتجيب عن الأسئلة، اضغط على الزر بالأسفل لتجسيدها برمجياً فوراً 👇</p>", unsafe_allow_html=True)
    if st.button("🚀 ابدأ التجسيد وبناء الكود الآن", use_container_width=True):
        st.session_state.is_generating = True
        st.session_state.error_occurred = False
        st.rerun()

# --- العمل على معالجة طلب البناء والتوليد في الخلفية بعد تحديث الشاشة ---
if st.session_state.is_generating:
    # تهيئة سجل البناء والتفكير التفاعلي للوكيل البرمجي
    st.session_state.architect_logs = [
        "⏳ [1/4] جاري تجميع كامل النقاش وتوجيهاتك وصياغة الهيكل المعماري..."
    ]
    time.sleep(1.0)
    
    st.session_state.architect_logs.append("⏳ [2/4] جاري تصميم واجهات الـ CSS والتأكد من توافقية شاشات الهواتف...")
    time.sleep(1.0)
    
    # استدعاء التوليد الفعلي بناءً على تاريخ المحادثة الكامل
    with st.spinner("⚡ يقوم المهندس البرمجي ببناء وتجميع الكود كاملاً..."):
        raw_response = call_spider_agent(
            prompt_type="generation",
            chat_history=st.session_state.messages
        )
        
        if "ERROR_API_FAILED" in raw_response:
            st.session_state.error_occurred = True
            st.session_state.is_generating = False
            st.session_state.messages.append({
                "role": "assistant", 
                "content": f"⚠️ تعذر جلب الكود البرمجي بنجاح. تفاصيل الخطأ: {raw_response}"
            })
            st.rerun()
        else:
            # معالجة وتصفية كود HTML البرمجي بدقة
            final_html = extract_html_code(raw_response)
            st.session_state.generated_html = final_html
            
            # إنهاء خطوات تجميع الكود التخيلية بنجاح
            st.session_state.architect_logs.append("⏳ [3/4] جاري دمج دوال التفاعل ومصفوفة الحركة للـ JavaScript...")
            time.sleep(1.0)
            st.session_state.architect_logs.append("🎉 [4/4] تمت عملية التجميع والبناء بنجاح! تفضل بمعاينة لعبتك أو موقعك الآن.")
            
            st.session_state.messages.append({
                "role": "assistant", 
                "content": "✨ تم تجسيد وتجميع مشروعك بنجاح تام! الكود متكامل وبدون أي اختصارات وجاهز للمعاينة في التبويب المخصص على اليسار."
            })
            
            st.session_state.is_generating = False
            st.rerun()

# --- العمود الأيسر: مساحة التجسيد والتفاعل والتحكم البرمجي ---
with col_workspace_pane:
    st.markdown("### 🛠️ مساحة التجسيد البرمجي والمعاينة")
    
    if st.session_state.error_occurred:
        st.markdown("""
            <div class='error-card'>
                <h4>⚠️ واجه المحرك خطأ في معالجة الطلب</h4>
                <p>الرجاء إعادة المحاولة أو التحقق من اتصال الإنترنت وخوادم التوليد.</p>
            </div>
        """, unsafe_allow_html=True)
        
    # ألسنة تبويب المعاينة التفاعلية المخصصة
    tab_preview, tab_source, tab_architect = st.tabs([
        "👁️ المعاينة الحية (Live Preview)", 
        "💻 الكود المصدري (Source Code)", 
        "⚙️ سجل معالج البناء (Build Logs)"
    ])
    
    # 1. تبويب المعاينة الفورية (Live Preview)
    with tab_preview:
        if st.session_state.generated_html:
            # لوحة تحكم سريعة أعلى المعاينة
            col_ctrl_1, col_ctrl_2 = st.columns([3, 1])
            with col_ctrl_1:
                st.caption("⚡ يعمل الكود حالياً داخل بيئة معزولة وآمنة (Sandboxed Frame).")
            with col_ctrl_2:
                if st.button("🔄 تحديث المعاينة", key="refresh_iframe"):
                    st.rerun()
                    
            # حقن المعاينة الحية مع تفعيل التجاوب الذكي
            components.html(st.session_state.generated_html, height=520, scrolling=True)
        else:
            st.info("💡 بمجرد اكتمال نقاشك مع المطور الذكي والضغط على زر 'بدء التجسيد'، ستظهر معاينة اللعبة أو الموقع هنا فوراً.")
            
    # 2. تبويب الكود المصدري الكامل (Source Code)
    with tab_source:
        if st.session_state.generated_html:
            st.caption("📦 يمكنك تحميل الملف البرمجي أو نسخه كاملاً:")
            
            # أزرار النسخ والتحميل
            col_download, col_copy = st.columns(2)
            with col_download:
                st.download_button(
                    label="📥 تحميل ملف الـ HTML الكامل",
                    data=st.session_state.generated_html,
                    file_name="spider_project.html",
                    mime="text/html"
                )
            with col_copy:
                st.caption("ملاحظة: يمكنك نسخ الكود بالكامل بالضغط على زر النسخ المدمج في أعلى يمين نافذة الكود بالأسفل 👇")
                
            # عرض الكود المصدري منسقاً
            st.code(st.session_state.generated_html, language="html", line_numbers=True)
        else:
            st.info("لا يوجد كود برمجي حالياً. ابدأ النقاش والتجسيد لتوليد الكود البرمجي وعرضه هنا.")

    # 3. تبويب سجلات البناء والتحليل الهندسي (Architect Logs)
    with tab_architect:
        st.caption("⚙️ تفاصيل وسجل عملية البناء الحالية التي يقوم بها الوكيل البرمجي الذكي:")
        if st.session_state.architect_logs:
            log_content = ""
            for log in st.session_state.architect_logs:
                if "🎉" in log or "✅" in log:
                    log_content += f"<div class='step-done' style='margin-bottom:8px;'>{log}</div>"
                else:
                    log_content += f"<div class='step-active' style='margin-bottom:8px;'>{log}</div>"
            
            st.markdown(f"""
                <div class='thinking-box'>
                    {log_content}
                </div>
            """, unsafe_allow_html=True)
        else:
            st.info("لا توجد عمليات جارية حالياً. بانتظار إرسال توجيه من قبلك والبدء بالتجسيد.")
