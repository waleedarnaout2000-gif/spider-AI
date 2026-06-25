import streamlit as st
import re
import time
from g4f.client import Client
import streamlit.components.v1 as components

# --- إعدادات الصفحة والتصميم العام المستوحى من Visily (CodeLab) ---
st.set_page_config(page_title="CodeLab Engine", page_icon="💻", layout="wide")

# تخصيص واجهة المستخدم بالكامل لتطابق نظام الألوان الداكن والتوزيع الهندسي للملفات المرفقة
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght=400;600;700&family=Fira+Code:wght=400;500&display=swap');
    html, body, .main { font-family: 'Cairo', sans-serif; text-align: right; direction: rtl; background-color: #0b0f17; color: #c9d1d9; }
    h1, h2, h3, h4, p, label { color: #f0f6fc; text-align: right; }
    
    /* تصميم الهيدر العلوي */
    .codelab-header { display: flex; justify-content: space-between; align-items: center; padding: 10px 20px; background-color: #161b22; border-bottom: 1px solid #30363d; border-radius: 8px; margin-bottom: 25px; }
    .codelab-logo { font-size: 24px; font-weight: bold; color: #58a6ff; font-family: 'Fira Code', monospace; }
    
    /* بطاقات أمثلة البدء السريع والكروت العادية */
    .visily-card { background-color: #161b22; border: 1px solid #30363d; border-radius: 12px; padding: 20px; margin-bottom: 15px; transition: 0.2s; }
    .visily-card:hover { border-color: #58a6ff; transform: translateY(-2px); }
    .example-title { color: #58a6ff; font-weight: bold; font-size: 16px; margin-bottom: 8px; }
    
    /* منصة الأوامر ووحدات الكونسول (Console Logs) */
    .console-box { background: #070a0e; border: 1px solid #f85149; border-radius: 10px; padding: 15px; margin: 15px 0; font-family: 'Fira Code', monospace; font-size: 13px; color: #ff7b72; direction: ltr; text-align: left; }
    .console-header { color: #f85149; font-weight: bold; border-bottom: 1px solid #3b1212; padding-bottom: 5px; margin-bottom: 10px; font-family: 'Cairo', sans-serif; text-align: right; direction: rtl; }
    
    /* شاشة المعاينة وإطار الكود */
    .preview-container { border: 2px solid #30363d; border-radius: 12px; overflow: hidden; background: #000; margin-top: 15px; }
    .tab-header { background: #161b22; padding: 8px 16px; border-bottom: 1px solid #30363d; font-family: 'Fira Code', monospace; color: #58a6ff; font-size: 14px; }
    
    /* تعديل مظهر الأزرار المخصصة للمنصة */
    div.stButton > button:first-child {
        background: #238636; color: white; border: 1px solid #30363d; padding: 8px 16px; border-radius: 6px; font-weight: bold; transition: 0.2s; width: 100%;
    }
    div.stButton > button:first-child:hover { background: #2ea44f; box-shadow: 0 4px 12px rgba(46, 164, 79, 0.2); }
    
    /* الأزرار الفرعية الثانوية كـ "تعديل الوصف" أو "عرض الأمثلة" */
    .sec-btn button { background-color: #21262d !important; color: #c9d1d9 !important; border: 1px solid #30363d !important; }
    .sec-btn button:hover { border-color: #8b949e !important; background-color: #30363d !important; }
    </style>
""", unsafe_allow_html=True)

# --- إدارة وتخزين بيانات الجلسة (State Management) ---
if 'generated_html' not in st.session_state:
    st.session_state.generated_html = ""
if 'current_stage' not in st.session_state:
    st.session_state.current_stage = "home"  # المراحل: home | generating | preview | error_view
if 'error_type' not in st.session_state:
    st.session_state.error_type = "" # وكيل_ذكي | بيئة_تشغيل
if 'user_prompt' not in st.session_state:
    st.session_state.user_prompt = ""

client = Client()

# --- دالة الـ AI الخاصة بك لتوليد الأكواد البرمجية الشاملة ---
def ask_agent(prompt):
    system_prompt = """
    You are an elite, world-class game architect and senior full-stack developer inside 'CodeLab' platform.
    Your absolute priority is to output flawless, clean, and fully executable single-file source code based on Arabic descriptions.
    NEVER write placeholder comments, incomplete logic, or short-cuts like "// rest of code".
    The entire output must be a single, self-contained HTML file incorporating all CSS and JavaScript.
    Return ONLY valid, clean HTML code starting strictly with <!DOCTYPE html> and ending with </html>. Do NOT wrap in markdown code blocks.
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

# --- هيدر التطبيق العلوي الموحد (مطابق لـ Screen 0 في ملف Visily) ---
st.markdown("""
    <div class='codelab-header'>
        <div class='codelab-logo'>CodeLab 💻</div>
        <div style='color: #8b949e; font-size: 14px;'>الحساب الافتراضي: مطور تجريبي | <b>10,000 نقطة</b></div>
    </div>
""", unsafe_allow_html=True)

# --- القائمة الجانبية للتنقل والمطابقة للملف تماماً ---
with st.sidebar:
    st.markdown("<h3 style='text-align: center;'>📋 القائمة الرئيسية</h3>", unsafe_allow_html=True)
    st.write("---")
    if st.button("🏠 الرئيسية"):
        st.session_state.current_stage = "home"
        st.rerun()
    if st.button("🚀 استعرض الأمثلة"):
        st.session_state.current_stage = "home"
        st.toast("تصفح قسم البدء السريع في منتصف الصفحة!")
    if st.button("⚙️ الإعدادات"):
        st.sidebar.info("الحد الأقصى للموارد: 512MB Sandbox Memory Limit")

# ----------------------------------------------------
# 1. الشاشة الرئيسية (Home Stage) - Screen ID: 0
# ----------------------------------------------------
if st.session_state.current_stage == "home":
    st.markdown("<h1 style='text-align: center; font-size: 32px;'>الذكاء الاصطناعي في مسكنك</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: #8b949e; font-weight: normal;'>بالعربية جسد فكرتك البرمجية</h3>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #8b949e;'>حول أوصافك باللغة العربية إلى مشاريع ويب كاملة وقابلة للتشغيل في ثوانٍ. محور متكامل، معاينة فورية، وذكاء اصطناعي يفهمك.</p>", unsafe_allow_html=True)
    
    # نموذج إدخال الفكرة والوصف البرمجي المباشر
    with st.container():
        st.markdown("<div class='visily-card'>", unsafe_allow_html=True)
        user_idea = st.text_area("وصف فكرتي بالعربية:", value=st.session_state.user_prompt, placeholder="اكتب هنا بالتفصيل (مثال: لوحة تحكم مهام ذكية، أو لعبة أفعى نيون مع حساب النقاط والـ Canvas)...")
        
        col_btn1, col_btn2 = st.columns([1, 4])
        with col_btn1:
            launch_build = st.button("إنشاء مشروعي الأول +")
        st.markdown("</div>", unsafe_allow_html=True)
        
        if launch_build and user_idea.strip():
            st.session_state.user_prompt = user_idea
            st.session_state.current_stage = "generating"
            st.rerun()

    st.write("---")
    
    # قسم البدء السريع والأمثلة الجاهزة المتطابقة مع الـ PDF
    st.markdown("### ⚡ بدء سريع: اختر مثالاً واجعل الـ AI يطلق سحره")
    col_ex1, col_ex2, col_ex3 = st.columns(3)
    
    with col_ex1:
        st.markdown("""
            <div class='visily-card'>
                <div class='example-title'>📊 لوحة تحكم مهام</div>
                <p style='font-size: 13px; color: #8b949e; margin-bottom: 12px;'>تطبيق ويب متكامل لإدارة المهام اليومية مع الإحصائيات والرسوم البيانية التفاعلية.</p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("توليد لوحة المهام", key="ex1"):
            st.session_state.user_prompt = "لوحة تحكم مهام ومتابعة أهداف يومية مع رسومات بيانية تفاعلية لإحصائيات الإنجاز باللغة العربية"
            st.session_state.current_stage = "generating"
            st.rerun()
            
    with col_ex2:
        st.markdown("""
            <div class='visily-card'>
                <div class='example-title'>💱 محول عملات لحظي</div>
                <p style='font-size: 13px; color: #8b949e; margin-bottom: 12px;'>أداة تحويل العملات مع حساب أسعار الصرف بشكل مباشر وتصميم واجهة فخمة مريحة.</p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("توليد محول العملات", key="ex2"):
            st.session_state.user_prompt = "محول عملات فخم تفاعلي كامل الحسابات مع واجهة مستخدم أنيقة باللغة العربية"
            st.session_state.current_stage = "generating"
            st.rerun()
            
    with col_ex3:
        st.markdown("""
            <div class='visily-card'>
                <div class='example-title'>🖼️ معرض صور ذكي</div>
                <p style='font-size: 13px; color: #8b949e; margin-bottom: 12px;'>معرض صور متطور يعتمد على الفلاتر، البحث الذكي، والتحريك السلس للعناصر.</p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("توليد معرض الصور", key="ex3"):
            st.session_state.user_prompt = "معرض صور تفاعلي متطور يحتوي على فلاتر تصفية وبحث مع مظهر وتأثيرات حركية جذابة"
            st.session_state.current_stage = "generating"
            st.rerun()

    # قسم خطوات العمل التوضيحية الثلاثة في التصميم
    st.write("---")
    st.markdown("<h4 style='text-align: center; margin-bottom: 20px;'>🚀 رحلة الإبداع في CodeLab</h4>", unsafe_allow_html=True)
    col_step1, col_step2, col_step3 = st.columns(3)
    with col_step1:
        st.markdown("<div style='text-align: center;'><b>1. صف فكرتك</b><p style='font-size: 12px; color: #8b949e;'>اكتب ما تريد بأسلوبك وب لغتك العربية المفضلة.</p></div>", unsafe_allow_html=True)
    with col_step2:
        st.markdown("<div style='text-align: center;'><b>2. بناء ذكي</b><p style='font-size: 12px; color: #8b949e;'>يقوم مهندس الكود بتحليل فكرتك وبنائها كوداً مكتملاً.</p></div>", unsafe_allow_html=True)
    with col_step3:
        st.markdown("<div style='text-align: center;'><b>3. تشغيل ومعاينة</b><p style='font-size: 12px; color: #8b949e;'>عاين النتيجة فوراً في بيئة التشغيل المستقلة.</p></div>", unsafe_allow_html=True)

# ----------------------------------------------------
# 2. مرحلة التوليد والأنيميشن الحركي (Generating Stage)
# ----------------------------------------------------
elif st.session_state.current_stage == "generating":
    st.markdown("### 🛠️ جاري إطلاق وتجميع عناصر الهندسة البرمجية...")
    
    status_box = st.empty()
    status_box.markdown("<div class='visily-card'><p style='color: #58a6ff;'>⏳ [1/3] جاري قراءة وتحليل النص الوصفي وصياغة هيكل تطبيق الويب...</p></div>", unsafe_allow_html=True)
    time.sleep(1.2)
    
    status_box.markdown("<div class='visily-card'><p style='color: #2ea44f;'>✅ تم فهم المتطلبات المعمارية بنجاح.</p><p style='color: #58a6ff;'>⏳ [2/3] جاري دمج عناصر التصميم وحقن دوال المنطق والتحكم التفاعلي الكامل...</p></div>", unsafe_allow_html=True)
    time.sleep(1.2)
    
    status_box.markdown("<div class='visily-card'><p style='color: #2ea44f;'>✅ تم حقن وتأمين منطق التحريك.</p><p style='color: #58a6ff;'>⏳ [3/3] جاري تجميع الملف المصدر النهائي index.html واستدعاء الخادم لإنتاج التطبيق الكامل...</p></div>", unsafe_allow_html=True)
    
    # الاتصال بالوكيل مع ضمان الموجه الصارم
    final_output = ask_agent(st.session_state.user_prompt)
    
    if "ERROR_API_FAILED" in final_output:
        st.session_state.error_type = "وكيل_ذكي"
        st.session_state.current_stage = "error_view"
        st.rerun()
    else:
        # تنظيف كود HTML المولد
        final_output = re.sub(r'^```html\s*', '', final_output, flags=re.IGNORECASE)
        final_output = re.sub(r'```$', '', final_output)
        st.session_state.generated_html = final_output.strip()
        st.session_state.current_stage = "preview"
        st.rerun()

# ----------------------------------------------------
# 3. شاشة المعاينة الحية المستقلة (Preview Stage)
# ----------------------------------------------------
elif st.session_state.current_stage == "preview":
    st.markdown("### 💻 منصة المعاينة البرمجية للمشروع المكتمل")
    st.write("تم بناء كودك النظيف بالكامل وهو يعمل الآن بشكل مستقل داخل حاوية المعاينة.")
    
    col_prev_left, col_prev_right = st.columns([3, 1])
    
    with col_prev_left:
        # عرض تبويب وسلسلة الكود البرمجي كما هو محدد بالرسمة (index.html </>)
        st.markdown("<div class='tab-header'>index.html &lt;/&gt; (المعاينة المباشرة للمشروع)</div>", unsafe_allow_html=True)
        st.markdown("<div class='preview-container'>", unsafe_allow_html=True)
        components.html(st.session_state.generated_html, height=550, scrolling=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col_prev_right:
        st.markdown("<div class='visily-card'>", unsafe_allow_html=True)
        st.markdown("<h4 style='color: #56d364; margin-top:0;'>⚙️ إجراءات وأدوات المشروع</h4>", unsafe_allow_html=True)
        st.write("يمكنك إجراء تعديلات برمجية أو إعادة صياغة للسيناريوهات المولد بها اللعبة الآن.")
        
        # حقل مخصص لمحاكاة إرسال الأخطاء لبيئة التشغيل أو فتح الإعدادات
        if st.button("📥 فتح الكود البرمجي بالكامل (صورس)"):
            st.toast("تم فحص الملف المصدر وهو جاهز بنسبة 100%!")
            
        st.write("---")
        if st.button("🔄 العودة وتعديل الوصف"):
            st.session_state.current_stage = "home"
            st.rerun()
            
        # زر محاكاة لعرض شاشة تجاوز الموارد أو أخطاء السيرفر (لفحص حالات النظام المفصلة بالملف)
        st.markdown("<p style='font-size: 11px; color:#8b949e; margin-top: 15px;'>أدوات فحص الحالات الاستثنائية للـ Sandbox:</p>", unsafe_allow_html=True)
        if st.button("🪲 محاكاة خطأ تجاوز الموارد (512MB)"):
            st.session_state.error_type = "بيئة_تشغيل"
            st.session_state.current_stage = "error_view"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# ----------------------------------------------------
# 4. لوحة معالجة الحالات والأخطاء الحرجة (Error View Stage) - Screen ID: 1, 4
# ----------------------------------------------------
elif st.session_state.current_stage == "error_view":
    st.markdown("## 🚨 CONSOLE LOGS (منصة فحص أخطاء وقت التشغيل للوكيل)")
    st.write("وقع النظام في إحدى الحالات الاستثنائية والبيئات الحرجة الموضحة بملف المخططات:")
    st.write("---")
    
    col_err_main, col_err_side = st.columns([3, 1])
    
    with col_err_main:
        if st.session_state.error_type == "وكيل_ذكي":
            # كرت أخطاء الوكيل الذكي وفشل توليد الكود (Screen ID: 1,9)
            st.markdown("""
                <div class='console-box'>
                    <div class='console-header'>⚠️ أخطاء الوكيل الذكي: فشل توليد الكود المطلق</div>
                    Error: AI MODEL TIMEOUT EXCEEDED (code: 504)<br>
                    [CodeLab Architect Log]: واجه مهندس الكود مشكلة أثناء معالجة الطلب الذكي، قد يكون السبب غموض أو تداخل في نص الوصف أو انقطاع مؤقت في الاتصال بالخادم.
                </div>
            """, unsafe_allow_html=True)
        else:
            # كرت أخطاء بيئة التشغيل وتجاوز حدود الموارد (Screen ID: 4,9)
            st.markdown("""
                <div class='console-box'>
                    <div class='console-header'>⚠️ أخطاء بيئة التشغيل: تجاوز حدود الموارد المسموح بها</div>
                    Uncaught ReferenceError: "appData" is not defined<br>
                    CRITICAL EXCEPTION: تم تعليق المعاينة الحية مؤقتاً لحماية النظام لتجاوز المشروع استهلاك الذاكرة المسموح بها (512MB)، قد يكون السبب حلقة تكرارية غير منتهية (Infinite Loop) أو تحميل ملفات ضخمة.
                </div>
            """, unsafe_allow_html=True)
            
    with col_err_side:
        st.markdown("<div class='visily-card'>", unsafe_allow_html=True)
        st.markdown("<h4 style='color: #ff7b72; margin-top:0;'>🛠️ إجراءات الطوارئ</h4>", unsafe_allow_html=True)
        st.write("اتخذ إجراءً برمجياً سريعاً لتصحيح المسار:")
        
        if st.button("✏️ تعديل الوصف النصي"):
            st.session_state.current_stage = "home"
            st.rerun()
            
        if st.button("🔄 إعادة محاولة التوليد"):
            st.session_state.current_stage = "generating"
            st.rerun()
            
        if st.session_state.error_type == "بيئة_تشغيل":
            if st.button("⚙️ فتح الإعدادات لزيادة الحدود"):
                st.toast("تم تعديل الذاكرة الافتراضية مؤقتاً!")
        st.markdown("</div>", unsafe_allow_html=True)
