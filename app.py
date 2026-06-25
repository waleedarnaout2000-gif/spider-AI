import streamlit as st
import re
import time
from g4f.client import Client
import streamlit.components.v1 as components

# --- إعدادات الصفحة والتصميم العام للمنصة ---
st.set_page_config(page_title="SPIDER-AI Engine", page_icon="🕷️", layout="wide")

# حقن تصاميم CSS مخصصة ومطابقة تماماً لرسوماتك اليدوية وأبعاد القوالب الاحترافية
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&family=Fira+Code:wght=400;500&display=swap');
    
    /* الخلفية العامة وتنسيق النصوص */
    html, body, .main { 
        font-family: 'Cairo', sans-serif; 
        text-align: right; 
        direction: rtl; 
        background-color: #0d1117; 
        color: #c9d1d9; 
    }
    h1, h2, h3, p, label { text-align: right; color: #f0f6fc; }

    /* كروت الواجهة المستوحاة من الرسومات اليدوية (Rounded Cards) */
    .custom-card {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    
    /* صندوق النقاط والرصيد العلوي المميز */
    .points-badge {
        background: linear-gradient(135deg, #1f293d, #0d1117);
        border: 2px solid #58a6ff;
        border-radius: 12px;
        padding: 15px;
        text-align: center;
        margin-bottom: 20px;
    }

    /* صناديق المحادثة ووصف الأفكار السينمائية */
    .chat-card { padding: 15px; border-radius: 10px; margin-bottom: 15px; line-height: 1.6; }
    .user-msg { background-color: #21262d; border-right: 4px solid #58a6ff; }
    .agent-msg { background-color: #111418; border-right: 4px solid #2ea44f; }
    
    /* مؤشرات تفكير الوكيل البرمجي (Console) */
    .thinking-box { 
        background: #070a0e; 
        border: 1px solid #21262d; 
        border-radius: 10px; 
        padding: 15px; 
        margin: 10px 0; 
        font-family: 'Fira Code', monospace; 
        font-size: 13px; 
        color: #8b949e; 
        direction: ltr; 
        text-align: left; 
    }
    .step-done { color: #56d364; font-weight: bold; }
    .step-active { color: #58a6ff; font-weight: bold; animation: blink 1s infinite; }
    @keyframes blink { 50% { opacity: 0.5; } }
    
    /* تصميم أزرار التوليد الرئيسية الأخري */
    div.stButton > button:first-child {
        background: linear-gradient(135deg, #238636, #2ea44f); 
        color: white;
        border: none; 
        padding: 12px 20px; 
        border-radius: 8px; 
        font-weight: bold; 
        font-size: 16px;
        width: 100%; 
        transition: 0.2s;
    }
    div.stButton > button:first-child:hover { 
        transform: translateY(-2px); 
        box-shadow: 0 6px 16px rgba(46, 164, 79, 0.4); 
    }
    
    /* تصميم بطاقات الأخطاء و التنبيهات */
    .error-card {
        background-color: #2d1313;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #f85149;
        color: #ff7b72;
        margin-bottom: 20px;
    }
    
    /* إطار محاكاة الشاشات للألعاب والمعاينة */
    .preview-frame-container {
        border: 4px solid #30363d;
        border-radius: 16px;
        overflow: hidden;
        background: #000;
        box-shadow: 0 12px 24px rgba(0,0,0,0.5);
    }
    </style>
""", unsafe_allow_html=True)

# --- إدارة وتخزين بيانات الجلسة (State Management) ---
if 'messages' not in st.session_state:
    st.session_state.messages = [{"role": "agent", "content": "مرحباً بك في SPIDER-AI! أنا مهندس البرمجيات الذكي الخاص بك. ضع هنا فكرتك البرمجية (موقع، تطبيق، لعبة 2D تفاعلية، أو لعبة 3D متطورة)، وسأقوم بمناقشتها معك وبنائها فوراً."}]
if 'generated_html' not in st.session_state:
    st.session_state.generated_html = ""
if 'current_stage' not in st.session_state:
    st.session_state.current_stage = "discussion" 
if 'code_blocks' not in st.session_state:
    st.session_state.code_blocks = {}
if 'error_occurred' not in st.session_state:
    st.session_state.error_occurred = False
if 'sidebar_page' not in st.session_state:
    st.session_state.sidebar_page = "dashboard"
if 'is_logged_in' not in st.session_state:
    st.session_state.is_logged_in = False # نظام التحقق المضاف من الرسمة الأولى

client = Client()

# --- دالة الذكاء الاصطناعي للمحادثة والتوليد الذكي ---
def ask_agent(prompt):
    system_prompt = """
    You are an elite, world-class game architect and senior full-stack developer.
    Your absolute priority is to output flawless, clean, and fully executable single-file source code.
    CRITICAL INSTRUCTIONS FOR CODE COMPLETENESS:
    1. NEVER write placeholder comments or short-cuts like "// rest of code". Every single line of styling, HTML, and JavaScript MUST be written out in full.
    2. The entire output must be a single, self-contained HTML file incorporating all CSS and JavaScript.
    3. All interface text inside the generated application MUST be written in the Arabic language.
    4. Return ONLY valid, clean HTML code starting strictly with <!DOCTYPE html> and ending with </html>. Do NOT wrap the code in markdown code blocks.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"ERROR_API_FAILED: {str(e)}"


# --- شاشة تسجيل الدخول الأولى (صورة رقم 1 في الرسمة اليدوية) ---
if not st.session_state.is_logged_in:
    st.markdown("<h1 style='text-align: center; color: #58a6ff; margin-top: 50px;'>🕷️ SPIDER.AI</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #8b949e;'>معلومات عن الموقع: أداة ثورية لإنشاء وتوليد الألعاب والبرمجيات التفاعلية بذكاء اصطناعي فائق</p>", unsafe_allow_html=True)
    
    col_auth_left, col_auth_mid, col_auth_right = st.columns([1, 1.5, 1])
    with col_auth_mid:
        st.markdown("""
            <div class='custom-card' style='text-align: center;'>
                <h3 style='text-align: center; color: #56d364;'>تسجيل الدخول / إنشاء حساب</h3>
                <p style='text-align: center; font-size: 13px; color: #8b949e;'>اختر طريقة الدخول المفضلة لديك للوصول إلى لوحة التحكم</p>
            </div>
        """, unsafe_allow_html=True)
        
        # أزرار الدخول المطابقة للرسمة الأولى
        if st.button("🔑 تسجيل الدخول بواسطة حساب Google"):
            st.session_state.is_logged_in = True
            st.rerun()
            
        if st.button("📧 الدخول بالبريد الإلكتروني وكلمة السر"):
            st.session_state.is_logged_in = True
            st.rerun()
            
        st.markdown("<p style='text-align: center; font-size: 12px; color: #8b949e; margin-top: 15px;'>بالتسجيل أنت توافق على شروط الخدمة وسياسة الاستخدام الخاصة بـ SPIDER-AI</p>", unsafe_allow_html=True)

# --- شاشات النظام الرئيسية بعد تسجيل الدخول (الرسومات 2 و 3 و 4) ---
else:
    # القائمة الجانبية الثابتة والمنظمة هندسياً
    with st.sidebar:
        st.markdown("<h2 style='text-align: center; color: #58a6ff;'>🕷️ SPIDER-AI</h2>", unsafe_allow_html=True)
        st.write("---")
        if st.button("🏠 لوحة التحكم الرئيسية"):
            st.session_state.sidebar_page = "dashboard"
            st.rerun()
        if st.button("🎮 ألعابي وتطبيقاتي"):
            st.session_state.sidebar_page = "projects"
            st.rerun()
        if st.button("⚙️ الإعدادات وتوطين اللغة"):
            st.session_state.sidebar_page = "settings"
            st.rerun()
        st.write("---")
        if st.button("🚪 تسجيل الخروج"):
            st.session_state.is_logged_in = False
            st.rerun()

    # 1. صفحة المشاريع والألعاب الفارغة
    if st.session_state.sidebar_page == "projects":
        st.markdown("## 🎮 معرض مشاريعك المكتملة")
        st.write("---")
        st.markdown("""
            <div style='text-align: center; padding: 50px; background-color: #161b22; border-radius: 16px; border: 2px dashed #30363d;'>
                <h3 style='color: #8b949e;'>📭 قائمة المشاريع فارغة</h3>
                <p style='color: #8b949e;'>يبدو أنك لم تقم بإنشاء أي مشروع برمجى تفاعلي حتى الآن. عد للوحة القيادة وقم بكتابة فكرتك الأولى!</p>
            </div>
        """, unsafe_allow_html=True)

    # 2. صفحة الإعدادات وتخصيص بيئة المحاكاة
    elif st.session_page == "settings" if 'sidebar_page' in st.session_state and st.session_state.sidebar_page == "settings" else False:
        st.markdown("## ⚙️ إعدادات المنصة وبيئة التشغيل")
        st.write("---")
        st.selectbox("لغة واجهة الوكيل البرمجي الذكي:", ["العربية (المحلية)", "English"])
        st.slider("الحد الأقصى لاستهلاك الذاكرة الافتراضية (Sandbox Memory Limit):", 256, 1024, 512, fmt="%d MB")
        st.checkbox("تفعيل نظام التصحيح التلقائي للأخطاء (Auto Code Healing)", value=True)
        st.success("تم تأمين وحفظ الإعدادات بنجاح!")

    # 3. لوحة القيادة التفاعلية الكبرى (Dashboard)
    else:
        # تقسيم الشاشة للحصول على الهيكل المتوازن في رسمتك الثانية والثالثة
        col_main_panel, col_info_panel = st.columns([1.3, 0.7])
        
        with col_info_panel:
            # كرت رصيد النقاط المستقل والمطابق للرسمة رقم 2
            st.markdown("""
                <div class='points-badge'>
                    <p style='margin: 0; font-size: 14px; color: #8b949e;'>📊 رصيد النقاط المتاح</p>
                    <h2 style='margin: 5px 0; color: #58a6ff; text-align: center;'>10,000 نقطة</h2>
                </div>
            """, unsafe_allow_html=True)
            if st.button("💳 شراء نقاط إضافية"):
                st.toast("سيتم تحويلك إلى بوابة الدفع الآمنة قريباً!", icon="💳")
            
            # كرت إضافي لعرض تفاصيل النظام والمراقبة الحية للـ Sandbox
            st.markdown("""
                <div class='custom-card'>
                    <h4 style='color: #58a6ff; margin-top:0;'>🖥️ بيئة التشغيل المعزولة</h4>
                    <p style='font-size: 13px; color: #8b949e; margin-bottom: 5px;'>الحالة: <span style='color: #56d364;'>متصل ونشط</span></p>
                    <p style='font-size: 13px; color: #8b949e; margin-bottom: 5px;'>الذاكرة: 245MB / 512MB</p>
                    <p style='font-size: 13px; color: #8b949e; margin-bottom: 0;'>المعالج: CPU 12%</p>
                </div>
            """, unsafe_allow_html=True)

        with col_main_panel:
            # حالة الانتهاء وعرض المعاينة الحية المستقلة (الرسومات 3 و 4)
            if st.session_state.current_stage == "finished":
                st.markdown("### 🎮 بيئة التشغيل والمعاينة الحية المستقلة")
                
                # إطار فخم ومحاكي للشاشات والألعاب لعزل النتيجة بشكل رائع ومطابق لطلبك
                st.markdown("<div class='preview-frame-container'>", unsafe_allow_html=True)
                components.html(st.session_state.generated_html, height=500, scrolling=True)
                st.markdown("</div>", unsafe_allow_html=True)
                
                # كرت الملاحظات والتوصيات البرمجية المكتوبة في أسفل الرسمة الرابعة
                st.markdown("""
                    <div class='custom-card' style='margin-top: 20px;'>
                        <h4 style='color: #56d364; margin-top: 0;'>📋 ملاحظات وتوصيات بيئة SPIDER</h4>
                        <ul style='font-size: 13px; color: #c9d1d9; padding-right: 20px;'>
                            <li>التجربة والواجهة متكاملة بالكامل وتدعم اللمس على الهواتف الذكية والأجهزة اللوحية.</li>
                            <li>تم تفعيل الخطوط والأنماط البصرية الجذابة لضمان مظهر عصري ومريح للعين.</li>
                            <li>كود اللعبة نظيف وخالٍ من الاختصارات ومحمي بالكامل داخل ملف HTML مستقل.</li>
                        </ul>
                    </div>
                """, unsafe_allow_html=True)
                
                if st.button("🔄 العودة إلى لوحة التحكم والوصف لتعديل اللعبة"):
                    st.session_state.current_stage = "discussion"
                    st.rerun()
            
            # حالة كتابة الفكرة ومناقشتها مع الوكيل البرمجي (الرسمة الثانية)
            elif st.session_state.current_stage in ["discussion", "generating"]:
                st.markdown("<h2 style='margin-top: 0;'>🤖 المهندس المعماري والبرمجي الذكي</h2>", unsafe_allow_html=True)
                st.write("اكتب سيناريو أو وصف اللعبة والتطبيق البرمجي الذي يدور في ذهنك بالتفصيل أدناه:")
                
                # صندوق المحادثة والوصف المستوحى من رسوماتك
                chat_placeholder = st.container(height=280)
                with chat_placeholder:
                    for msg in st.session_state.messages:
                        cls = "user-msg" if msg["role"] == "user" else "agent-msg"
                        st.markdown(f"<div class='chat-card {cls}'>{msg['content']}</div>", unsafe_allow_html=True)
                
                # حقل استقبال الأفكار وزر البناء والتعديل المباشر
                with st.form("chat_form", clear_on_submit=True):
                    user_input = st.text_input("اشرح مشروعك هنا (الألوان، التفاعلات، الوظائف البرمجية المطلوب بناؤها):", placeholder="مثال: أريد إنشاء لعبة أفعى نيون تفاعلية مع حساب النقاط وتدعم الهواتف...")
                    submit_chat = st.form_submit_button("إرسال فكرة المشروع وبدء البناء الذكي 🚀")
                    
                if submit_chat and user_input.strip():
                    st.session_state.messages.append({"role": "user", "content": user_input})
                    
                    if any(word in user_input for word in ["ابدا", "انشئ", "برمج", "بناء", "ابدأ", "أنشئ"]):
                        st.session_state.current_stage = "generating"
                        st.rerun()
                    else:
                        with st.spinner("🤖 يقوم المهندس البرمجي بتحليل الأبعاد وصياغة الهيكل..."):
                            prompt_query = f"User idea: {user_input}. Respond in Arabic. Ask 2-3 deep architectural or design questions."
                            agent_reply = ask_agent(prompt_query)
                            
                            if "ERROR_API_FAILED" in agent_reply:
                                st.session_state.error_occurred = True
                            else:
                                st.session_state.messages.append({"role": "agent", "content": agent_reply})
                        st.rerun()

                # منطقة تتبع الأوامر والأنيميشن الحركي (Console Logs) في الكرت الأيسر من الرسمة الثالثة
                if st.session_state.error_occurred:
                    st.markdown(f"""
                        <div class='error-card'>
                            <h3>⚠️ خطأ حرج: AI MODEL TIMEOUT EXCEEDED</h3>
                            <p>حدثت مشكلة أثناء معالجة الطلب، قد يكون السبب غموض في وصف الفكرة المعمارية أو مشكلة مؤقتة في الاتصال بالخادم الرئيسي.</p>
                            <p><b>الإجراء المقترح:</b> يرجى مراجعة وتعديل الوصف أو الضغط على زر إعادة المحاولة الآن.</p>
                        </div>
                    """, unsafe_allow_html=True)
                    if st.button("🔄 إعادة تفعيل المحاولة وتأسيس الاتصال"):
                        st.session_state.error_occurred = False
                        st.rerun()
                        
                elif st.session_state.current_stage == "generating":
                    status_box = st.empty()
                    
                    status_box.markdown("<div class='thinking-box'><div class='step-active'>⏳ [1/4] جاري تحليل المتطلبات وصياغة الهيكل الكامل للمشروع...</div></div>", unsafe_allow_html=True)
                    time.sleep(1.2)
                    
                    status_box.markdown("<div class='thinking-box'><div class='step-done'>✅ [1/4] تم الانتهاء من تحليل وفهم متطلبات اللعبة.</div><div class='step-active'>⏳ [2/4] جاري تجميع وحقن ملف الأنماط والتصميم البصري (CSS Styles)...</div></div>", unsafe_allow_html=True)
                    st.session_state.code_blocks["css"] = "/* واجهة مفعمة بالحيوية */"
                    time.sleep(1.2)
                    
                    status_box.markdown("<div class='thinking-box'><div class='step-done'>✅ [1/4] تم الانتهاء من تحليل متطلبات اللعبة.</div><div class='step-done'>✅ [2/4] تم تطبيق واجهات الـ CSS الفخمة والمظهر العصري.</div><div class='step-active'>⏳ [3/4] جاري بناء محرك الحركة والتحكم البرمجي بالكامل (JS Logic)...</div></div>", unsafe_allow_html=True)
                    st.session_state.code_blocks["js"] = "// محرك الحركة"
                    time.sleep(1.2)
                    
                    # استدعاء وإنتاج الملف الشامل والنظيف
                    full_prompt = f"Create a fully detailed, clean and complete executable single-file solution in Arabic based on: {str(st.session_state.messages)}."
                    final_generated = ask_agent(full_prompt)
                    
                    if "ERROR_API_FAILED" in final_generated:
                        st.session_state.error_occurred = True
                        st.session_state.current_stage = "discussion"
                        st.rerun()
                    else:
                        final_generated = re.sub(r'^```html\s*', '', final_generated, flags=re.IGNORECASE)
                        final_generated = re.sub(r'```$', '', final_generated)
                        st.session_state.generated_html = final_generated.strip()
                        st.session_state.current_stage = "finished"
                        st.rerun()
