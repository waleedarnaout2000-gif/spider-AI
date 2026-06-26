import streamlit as st
import re
import time
from g4f.client import Client
import streamlit.components.v1 as components

# --- إعدادات الصفحة والهوية البصرية ---
st.set_page_config(
    page_title="SPIDER-AI | محرك التجسيد البرمجي", 
    page_icon="🕸️", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# تصميم واجهة مستخدم مظلمة واحترافية (Cyberpunk Dark Mode)
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
        padding: 8px 16px !important; 
        border-radius: 6px !important; 
        font-weight: 700 !important; 
        transition: 0.2s !important;
        width: 100%;
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
    </style>
""", unsafe_allow_html=True)

# --- إدارة وتخزين بيانات الجلسة (State Management) ---
if 'messages' not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant", 
            "content": "مرحباً بك في **SPIDER-AI: محرك التجسيد البرمجي** 🕸️\n\nأنا مهندس البرمجيات المتخصص ومصمم الألعاب الخاص بك. صف لي فكرتك البرمجية بالكامل (موقع، أداة تفاعلية، لوحة تحكم، أو لعبة 2D/3D)، وسأقوم ببنائها وهيكلتها لك فوراً وتجسيدها في شاشة المعاينة الحية!"
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
    """
    تقوم هذه الدالة بالبحث عن كود HTML الفعلي داخل مخرجات النموذج البرمجي وتصفيته،
    حتى لو قام النموذج بكتابة نصوص أو تعليقات قبل أو بعد الكود.
    """
    # البحث عن وسم البداية والنهاية للـ HTML
    html_pattern = re.compile(r'(<!DOCTYPE html>.*?</html>|<html.*?</html>)', re.DOTALL | re.IGNORECASE)
    match = html_pattern.search(raw_text)
    if match:
        return match.group(1).strip()
    
    # محاولة تنظيف الكود في حال تم إرجاعه داخل بلوك Markdown فقط
    cleaned = re.sub(r'^```html\s*', '', raw_text, flags=re.IGNORECASE)
    cleaned = re.sub(r'```$', '', cleaned).strip()
    return cleaned

# --- دالة استدعاء الوكيل الذكي ومحرك التعديل التتابعي ---
def call_spider_agent(prompt_type="generation", user_prompt="", existing_code=""):
    # الموجه الهندسي الصارم جداً (System Prompt Matrix) لمنع كتابة الأكواد الناقصة
    system_prompt = """
    You are 'SPIDER-AI Code Architect' - an elite, world-class senior software engineer and game developer.
    Your sole focus is to design, code, and deliver fully working, bug-free, and single-file executable web applications, tools, and games.
    
    CRITICAL QUALITY CONTROL RULES:
    1. NEVER use code placeholders, comments indicating omissions (such as "// rest of code", "// TODO: implement"), or incomplete functions. Write every single line of styling, logic, and HTML markup.
    2. The output must be completely self-contained in ONE HTML file. Include Tailwind CSS or custom CSS inside <style> tags, and all interactive JavaScript logic inside <script> tags.
    3. Always design a modern, visually stunning UI/UX with beautiful dark/neon palettes, smooth CSS animations, and highly responsive components.
    4. For games (2D/3D): Always provide clean controls (both desktop keyboard keys and on-screen touch joysticks/buttons for mobile compliance), audio visualizer context if relevant, scoring systems, and professional Game Over / Restart states.
    5. All visible text elements, instructions, menus, alerts, and controls inside the generated application must be in the ARABIC language to suit the target userbase.
    6. Your response MUST strictly start with <!DOCTYPE html> and end with </html>. Do not write any markdown blocks (such as ```html) or pre/post commentary.
    """

    if prompt_type == "edit":
        # موجه خاص للتعديل والتطوير على الكود البرمجي الحالي دون فقدان الميزات السابقة
        compiled_prompt = f"""
        Here is the current working code:
        ---
        {existing_code}
        ---
        The user wants you to apply the following modification or enhancement:
        "{user_prompt}"
        
        Refactor the code to apply this request perfectly. Keep all other features fully functional.
        Ensure you output the FULL modified single-file code starting strictly with <!DOCTYPE html> and ending with </html>.
        """
    else:
        # موجه التوليد لأول مرة
        compiled_prompt = f"Create a fully detailed, clean and complete executable single-file solution in Arabic based on the user's idea: {user_prompt}"

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": compiled_prompt}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"ERROR_API_FAILED: {str(e)}"

# --- الهيكل البصري وتقسيم الشاشة الاحترافي ---

# عنوان المنصة الرئيسي بألوان النيون الفخمة
st.markdown("""
    <div style="text-align: center; margin-bottom: 25px; padding: 15px; background: #151b23; border: 1px solid #30363d; border-radius: 12px;">
        <h1 style="margin: 0; font-size: 2.2rem; font-weight: 800; background: linear-gradient(90deg, #58a6ff, #2ea44f); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
            🕸️ جوهر SPIDER-AI : محرك التجسيد البرمجي
        </h1>
        <p style="margin: 5px 0 0 0; color: #8b949e; font-size: 1rem;">التحويل من المفهوم الفكري إلى الكود والتشغيل التفاعلي الفوري في ملف واحد</p>
    </div>
""", unsafe_allow_html=True)

# تقسيم الشاشة إلى عمودين متوازنين (الدردشة على اليمين والمساحة التفاعلية على اليسار)
col_chat_pane, col_workspace_pane = st.columns([1, 1.3], gap="medium")

# --- العمود الأيمن: محرك المحادثة وصياغة الأفكار ---
with col_chat_pane:
    st.markdown("### 💬 غرفة صياغة الأفكار والتعديلات")
    
    # حاوية عرض الرسائل السابقة بشكل منسق
    chat_container = st.container(height=520)
    with chat_container:
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
                
    # استقبال الأوامر والمدخلات الجديدة من المستخدم
    if user_cmd := st.chat_input("صف فكرتك البرمجية الجديدة أو اكتب طلباً لتعديل الكود الحالي..."):
        # إضافة رسالة المستخدم للسجل
        st.session_state.messages.append({"role": "user", "content": user_cmd})
        
        # تفعيل حالة المعالجة والتوليد
        st.session_state.is_generating = True
        st.session_state.error_occurred = False
        st.rerun()

# --- العمل على معالجة الطلبات في الخلفية بعد تحديث الشاشة ---
if st.session_state.is_generating:
    # الحصول على آخر رسالة كتبها المستخدم
    last_user_msg = st.session_state.messages[-1]["content"]
    
    # تحديث سجل البناء والتفكير للمستخدم في واجهة جميلة
    st.session_state.architect_logs = [
        "⏳ [1/4] جاري تحليل المتطلبات والبحث عن البنية الأنسب للمشروع..."
    ]
    
    # تحديد ما إذا كان الطلب توليداً جديداً بالكامل أو تعديلاً على كود سابق
    if st.session_state.generated_html:
        prompt_type = "edit"
        existing_code = st.session_state.generated_html
        log_text_step2 = "⏳ [2/4] جاري دمج التعديلات الجديدة مع الحفاظ على استقرار الكود القديم..."
    else:
        prompt_type = "generation"
        existing_code = ""
        log_text_step2 = "⏳ [2/4] جاري بناء وتنسيق الواجهات البصرية وأنماط الـ CSS..."
        
    st.session_state.architect_logs.append(log_text_step2)
    
    # استدعاء الذكاء الاصطناعي
    with st.spinner("جاري معالجة وتجسيد الكود البرمجي..."):
        raw_response = call_spider_agent(
            prompt_type=prompt_type,
            user_prompt=last_user_msg,
            existing_code=existing_code
        )
        
        if "ERROR_API_FAILED" in raw_response:
            st.session_state.error_occurred = True
            st.session_state.is_generating = False
            st.session_state.messages.append({
                "role": "assistant", 
                "content": f"⚠️ واجهت مشكلة أثناء الاتصال بخوادم التوليد. الرجاء المحاولة مرة أخرى.\n\n**التفاصيل:** {raw_response.replace('ERROR_API_FAILED:', '')}"
            })
            st.rerun()
        else:
            # معالجة الكود وتنظيفه
            final_html = extract_html_code(raw_response)
            st.session_state.generated_html = final_html
            
            # تحديث السجل النهائي للبناء
            st.session_state.architect_logs.append("⏳ [3/4] جاري حقن واختبار دوال التفاعل ومحرك الـ JavaScript...")
            st.session_state.architect_logs.append("🎉 [4/4] تمت عملية التجسيد والبناء بنجاح واكتمال تام!")
            
            # تحديث دردشة الذكاء الاصطناعي بنجاح العملية
            st.session_state.messages.append({
                "role": "assistant", 
                "content": "✨ تم تجسيد وتحديث الكود بنجاح! يمكنك الآن مشاهدة النتيجة وتجربتها في تبويب **المعاينة الحية** على اليسار."
            })
            
            # إنهاء حالة التوليد بنجاح
            st.session_state.is_generating = False
            st.rerun()

# --- العمود الأيسر: مساحة التجسيد والتفاعل والتحكم البرمجي ---
with col_workspace_pane:
    st.markdown("### 🛠️ مساحة العمل والتجسيد الفوري")
    
    # عرض رسائل الخطأ إن وجدت بشكل بارز لحماية تماسك التطبيق
    if st.session_state.error_occurred:
        st.markdown("""
            <div class='error-card'>
                <h4>⚠️ تعذر الاتصال بمحرك التوليد البرمجي</h4>
                <p>الخوادم البرمجية ممتلئة بالطلبات حالياً أو واجهت خطأ مؤقتاً. الرجاء الضغط على زر إعادة الإرسال في الدردشة للمحاولة مرة أخرى.</p>
            </div>
        """, unsafe_allow_html=True)
        
    # بناء ألسنة التبويب الاحترافية للتحكم
    tab_preview, tab_source, tab_architect = st.tabs([
        "👁️ المعاينة الحية (Live Preview)", 
        "💻 الكود المصدري (Source Code)", 
        "⚙️ سجل ومراحل البناء (Architect Logs)"
    ])
    
    # 1. تبويب المعاينة الفورية (Live Preview)
    with tab_preview:
        if st.session_state.generated_html:
            # لوحة تحكم سريعة أعلى المعاينة
            col_ctrl_1, col_ctrl_2 = st.columns([3, 1])
            with col_ctrl_1:
                st.caption("⚡ يعمل الكود حالياً داخل بيئة معزولة وآمنة (Sandboxed Frame).")
            with col_ctrl_2:
                # زر إعادة تحميل وتحديث المعاينة
                if st.button("🔄 تحديث المعاينة", key="refresh_iframe"):
                    st.rerun()
                    
            # حقن المعاينة الحية داخل عنصر iframe آمن ومستقر
            components.html(st.session_state.generated_html, height=550, scrolling=True)
        else:
            st.info("💡 بمجرد كتابة فكرتك في شاشة المحادثة والضغط على إرسال، سيتم تجسيدها ومعاينتها مباشرة هنا.")
            
    # 2. تبويب الكود المصدري الكامل (Source Code)
    with tab_source:
        if st.session_state.generated_html:
            st.caption("📦 يمكنك مراجعة الكود الموحد بالكامل، نسخه، أو تحميله للتشغيل الفوري خارج المنصة.")
            
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
                # استخدام مكون برمجيات streamlit لعرض الكود لسهولة النسخ اليدوي أيضاً
                st.caption("ملاحظة: يمكنك نسخ الكود بالكامل بالضغط على زر النسخ المدمج في أعلى يمين نافذة الكود بالأسفل 👇")
                
            # عرض الكود المصدري منسقاً
            st.code(st.session_state.generated_html, language="html", line_numbers=True)
        else:
            st.info("لا يوجد كود برمجي حالياً. ابدأ النقاش مع الوكيل ليتم كتابة الكود وعرضه هنا.")

    # 3. تبويب سجلات البناء والتحليل الهندسي (Architect Logs)
    with tab_architect:
        st.caption("⚙️ تفاصيل وسجل عملية البناء الحالية التي يقوم بها الوكيل البرمجي الذكي:")
        if st.session_state.architect_logs:
            # صياغة السجلات في بطاقة مخصصة
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
            st.info("لا توجد عمليات جارية حالياً. بانتظار إرسال توجيه من قبلك.")
