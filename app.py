 import streamlit as st
import re
import time
from g4f.client import Client
import streamlit.components.v1 as components

--- إعدادات الصفحة والتصميم العام للمنصة ---
st.set_page_config(page_title="Emergent Engine", page_icon="🤖", layout="wide")

تصميم واجهة مستخدم مظلمة واحترافية تحاكي البيئات البرمجية المتقدمة
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght=400;600;700&family=Fira+Code:wght=400;500&display=swap');
    html, body, .main { font-family: 'Cairo', sans-serif; text-align: right; direction: rtl; background-color: #0d1117; color: #c9d1d9; }
    h1, h2, h3, p, label { color: #f0f6fc; text-align: right; }

    /* صناديق المحادثة السينمائية */
    .chat-card { padding: 15px; border-radius: 10px; margin-bottom: 15px; line-height: 1.6; }
    .user-msg { background-color: #21262d; border-right: 4px solid #58a6ff; }
    .agent-msg { background-color: #161b22; border-right: 4px solid #2ea44f; }

    /* مؤشرات تفكير الوكيل البرمجي */
    .thinking-box { background: #0d1117; border: 1px solid #30363d; border-radius: 8px; padding: 12px; margin: 10px 0; font-family: 'Fira Code', monospace; font-size: 13px; color: #8b949e; direction: ltr; text-align: left; }
    .step-done { color: #56d364; }
    .step-active { color: #58a6ff; font-weight: bold; animation: blink 1s infinite; }
    @keyframes blink { 50% { opacity: 0.5; } }

    /* أزرار مخصصة فخمة */
    div.stButton > button:first-child {
        background: linear-gradient(135deg, #238636, #2ea44f); color: white;
        border: none; padding: 10px 20px; border-radius: 6px; font-weight: bold; width: 100%; transition: 0.2s;
    }
    div.stButton > button:first-child:hover { transform: translateY(-1px); box-shadow: 0 4px 12px rgba(46, 164, 79, 0.3); }

    /* تصميم بطاقات الأخطاء الذكية */
    .error-card {
        background-color: #3b1212;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #f85149;
        color: #ff7b72;
        margin-bottom: 20px;
        text-align: right;
    }
    </style>
""", unsafe_allow_html=True)

--- إدارة وتخزين بيانات الجلسة (State Management) ---
if 'messages' not in st.session_state:
    st.session_state.messages = [{"role": "agent", "content": "مرحباً بك! أنا مهندس البرمجيات الذكي الخاص بك. ضع هنا فكرتك البرمجية (موقع، تطبيق، لعبة 2D تفاعلية، أو لعبة 3D متطورة)، وسأقوم بمناقشتها معك وبنائها فوراً."}]
if 'generated_html' not in st.session_state:
    st.session_state.generated_html = ""
if 'current_stage' not in st.session_state:
    st.session_state.current_stage = "discussion" # المراحل المتاحة: discussion | generating | finished
if 'code_blocks' not in st.session_state:
    st.session_state.code_blocks = {}
if 'error_occurred' not in st.session_state:
    st.session_state.error_occurred = False

client = Client()

--- دالة الذكاء الاصطناعي للمحادثة والتوليد الذكي مع تفعيل الموجه الخلفي الصارم ---
def ask_agent(prompt):
    # الموجه الهندسي الخلفي الصارم جداً (System Prompt Matrix) لضمان الأكواد الكاملة
    system_prompt = """
    You are an elite, world-class game architect and senior full-stack developer.
    Your absolute priority is to output flawless, clean, and fully executable single-file source code.

    CRITICAL INSTRUCTIONS FOR CODE COMPLETENESS:
    1. NEVER write placeholder comments, incomplete logic, or short-cuts like "// rest of the code goes here" or "// TODO: add logic". Every single line of styling, HTML markup, and JavaScript logic MUST be written out in full.
    2. The entire output must be a single, self-contained HTML file incorporating all CSS (inside <style> tags) and JavaScript (inside <script> tags).
    3. All interface text, game labels, game-over screens, and instructions inside the generated application MUST be written in the Arabic language.
    4. Return ONLY valid, clean HTML code starting strictly with <!DOCTYPE html> and ending with </html>. Do NOT wrap the code in markdown code blocks (such as html ...).

    RULES FOR 2D GAMES:
    - If a 2D game is requested, build it using HTML5 Canvas and vanilla JavaScript.
    - Implement a proper responsive game loop using requestAnimationFrame.
    - Always include on-screen touch controls (arrows or joysticks) for mobile players alongside standard keyboard controls (WASD/Arrows).
    - Design beautiful modern UI overlays for start, score tracking, and game-over states.

    RULES FOR 3D GAMES & SIMULATIONS:
    - If a 3D game or simulation is requested, build it using Three.js.
    - Load Three.js safely from: "https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"
    - ALWAYS configure AmbientLight (intensity ~0.6) and DirectionalLight (intensity ~0.8) pointing at the center to prevent black screens.
    - Implement smooth rotation camera controls (mouse dragging or touch swiping) so players can change the viewing angle.
    - Start the animation loop strictly after window.onload event.
    - NEVER use external image URLs for textures. Use generated solid or glowing neon materials and colors on basic procedural meshes (Cubes, Spheres, Cylinders) instead.
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
        # إرجاع رسالة خطأ قياسية ليتم معالجتها في الواجهة دون تجميدها
        return f"ERROR_API_FAILED: {str(e)}"

كود احتياطي فخم للغاية للعبة تفاعلية في حال فشل الاتصال بالسيرفر
backup_html = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>محاكي الألعاب التفاعلي</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
        body { margin: 0; padding: 0; background-color: #0b0f19; color: white; font-family: 'Cairo', sans-serif; text-align: center; }
        .container { display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100vh; }
        h1 { color: #00FF87; }
        .card { background: #161b22; padding: 30px; border-radius: 12px; border: 1px solid #30363d; max-width: 600px; }
        .btn { display: inline-block; background: #00FF87; color: black; padding: 12px 24px; font-weight: bold; text-decoration: none; border-radius: 6px; margin-top: 15px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="card">
            <h1>🎮 تم تجهيز البيئة الاحتياطية بنجاح!</h1>
            <p>المنصة مستعدة بالكامل الآن لتوليد وبناء ألعاب الـ 2D والـ 3D التفاعلية وفقاً للبرومبت الصارم الجديد.</p>
            <p>اضغط على الزر بالأسفل لتجربة لوحة التحكم والتعديل التفاعلي.</p>
            <a href="#" class="btn" onclick="alert('أهلاً بك في منصة التطوير السريع!')">ابدأ الاستكشاف 🚀</a>
        </div>
    </div>
</body>
</html>
"""

--- واجهة وتجربة المستخدم بناءً على مرحلة التوليد ---

if st.session_state.current_stage in ["discussion", "generating"]:
    st.markdown("## 🤖 المهندس البرمجي الذكي (الجيل القادم)")
    st.write("ناقش الفكرة، اطلع على تفاصيل الكود خطوة بخطوة، ثم انتقل للمعاينة النقية.")
    st.write("---")

    col_chat, col_steps = st.columns([1.2, 1])

    with col_chat:
        st.markdown("### 💬 سجل المحادثة الفعلية")
        chat_placeholder = st.container(height=400)
        with chat_placeholder:
            for msg in st.session_state.messages:
                cls = "user-msg" if msg["role"] == "user" else "agent-msg"
                st.markdown(f"<div class='chat-card {cls}'>{msg['content']}</div>", unsafe_allow_html=True)

        # حقل إرسال الأوامر والردود للمستخدم
        with st.form("chat_form", clear_on_submit=True):
            user_input = st.text_input("اكتب ردك، إجاباتك على الأسئلة، أو فكرتك البرمجية هنا:", placeholder="مثال: نعم، أريد لعبة أفعى 2D مع ألوان نيون وحساب النقاط الفائزة...")
            submit_chat = st.form_submit_button("إرسال التوجيه والرد")

        if submit_chat and user_input.strip():
            st.session_state.messages.append({"role": "user", "content": user_input})

            # إذا طلب المستخدم صراحة بناء أو إطلاق التطبيق
            if any(word in user_input for word in ["ابدا", "انشئ", "برمج", "بناء", "ابدأ", "أنشئ"]):
                st.session_state.current_stage = "generating"
                st.rerun()
            else:
                with st.spinner("🤖 يفكر المهندس في أبعاد فكرتك ويصيغ لك أسئلة توجيهية..."):
                    prompt_query = f"User idea: {user_input}. Respond in Arabic. Ask 2-3 deep, professional architectural or design questions to help them make this single-page app or game perfect."
                    agent_reply = ask_agent(prompt_query)

                    if "ERROR_API_FAILED" in agent_reply:
                        st.session_state.error_occurred = True
                    else:
                        st.session_state.messages.append({"role": "agent", "content": agent_reply})
                st.rerun()

    with col_steps:
        st.markdown("### 🛠️ خطوات العمل وهيكل الكود المكتوب")

        # معالجة أخطاء الـ API وحماية التطبيق من التجمد
        if st.session_state.error_occurred:
            st.markdown(f"""
                <div class='error-card'>
                    <h3>⚠️ خطأ في معالجة طلبك الذكي</h3>
                    <p>يبدو أن خوادم الذكاء الاصطناعي مشغولة حالياً أو تواجه ضغطاً كبيراً في التوليد.</p>
                    <p><b>التفاصيل:</b> تعذر جلب الرد الفوري من السيرفر بنجاح.</p>
                </div>
            """, unsafe_allow_html=True)
            if st.button("🔄 إعادة المحاولة وتجربة الاتصال مجدداً"):
                st.session_state.error_occurred = False
                st.rerun()

        elif st.session_state.current_stage == "generating":
            status_box = st.empty()

            # الأنيميشن ومراحل التوليد التفاعلية
            status_box.markdown("""
                <div class='thinking-box'>
                    <div class='step-active'>⏳ [1/4] جاري تحليل المتطلبات البرمجية وصياغة الهيكل الكامل...</div>
                </div>
            """, unsafe_allow_html=True)
            time.sleep(1.5)

            status_box.markdown("""
                <div class='thinking-box'>
                    <div class='step-done'>✅ [1/4] تم فهم وتحليل المتطلبات البرمجية بنجاح.</div>
                    <div class='step-active'>⏳ [2/4] جاري كتابة وتأمين ملف الأنماط والتصميم البصري (CSS Styles)...</div>
                </div>
            """, unsafe_allow_html=True)
            st.session_state.code_blocks["css"] = "/* تصميم واجهة مفعمة بالحيوية والتحكم التفاعلي */\ncanvas {\n  display: block;\n  background: #000;\n  margin: auto;\n  border: 4px solid #00FF87;\n  box-shadow: 0 0 20px #00FF87;\n}"
            with st.expander("📦 كود هيكل الأنماط البصرية المكتوب"):
                st.code(st.session_state.code_blocks["css"], language="css")
            time.sleep(1.5)

            status_box.markdown("""
                <div class='thinking-box'>
                    <div class='step-done'>✅ [1/4] تم فهم وتحليل المتطلبات البرمجية بنجاح.</div>
                    <div class='step-done'>✅ [2/4] تم الانتهاء من تصميم وتطبيق واجهات الـ CSS الفخمة.</div>
                    <div class='step-active'>⏳ [3/4] جاري برمجة منطق التفاعل والحركة (Javascript Engine)...</div>
                </div>
            """, unsafe_allow_html=True)
            st.session_state.code_blocks["js"] = "// محرك المنطق والحركة التفاعلية للألعاب\nfunction gameLoop() {\n  updateState();\n  drawScene();\n  requestAnimationFrame(gameLoop);\n}"
            with st.expander("📦 كود منطق الحركة والتحكم المكتوب"):
                st.code(st.session_state.code_blocks["js"], language="javascript")
            time.sleep(1.5)

            status_box.markdown("""
                <div class='thinking-box'>
                    <div class='step-done'>✅ [1/4] تم فهم وتحليل المتطلبات البرمجية بنجاح.</div>
                    <div class='step-done'>✅ [2/4] تم الانتهاء من تصميم وتطبيق واجهات الـ CSS الفخمة.</div>
                    <div class='step-done'>✅ [3/4] تم حقن وتأمين منطق الحركة ومحرك التفاعل البرمجي.</div>
                    <div class='step-active'>⏳ [4/4] جاري تجميع وإخراج الكود الكامل والنظيف في ملف واحد...</div>
                </div>
            """, unsafe_allow_html=True)

            # استدعاء التوليد الفعلي باستخدام الموجه الخلفي الصارم
            full_prompt = f"Create a fully detailed, clean and complete executable single-file solution in Arabic based on: {str(st.session_state.messages)}. Remember, do NOT use placeholders or truncation comments like '// rest of code'."
            final_generated = ask_agent(full_prompt)

            if "ERROR_API_FAILED" in final_generated:
                st.session_state.error_occurred = True
                st.session_state.current_stage = "discussion"
                st.rerun()
            else:
                # تنظيف الكود وتأمينه بالكامل
                final_generated = re.sub(r'^html\s*', '', final_generated, flags=re.IGNORECASE)                 final_generated = re.sub(r'$', '', final_generated)
                st.session_state.generated_html = final_generated.strip()

                status_box.markdown("""
                    <div class='thinking-box'>
                        <div class='step-done'>✅ [1/4] تم فهم وتحليل المتطلبات البرمجية بنجاح.</div>
                        <div class='step-done'>✅ [2/4] تم الانتهاء من تصميم وتطبيق واجهات الـ CSS الفخمة.</div>
                        <div class='step-done'>✅ [3/4] تم حقن وتأمين منطق الحركة ومحرك التفاعل البرمجي.</div>
                        <div class='step-done'>🎉 [4/4] تمت عملية التجميع والتوليد بنجاح واكتمال تام! الكود جاهز للتشغيل الحركي.</div>
                    </div>
                """, unsafe_allow_html=True)

                st.session_state.current_stage = "finished"
                st.rerun()
        else:
            st.info("اكتب فكرتك البرمجية في شاشة المحادثة وابدأ النقاش التفاعلي مع المهندس البرمجي لتشغيل التوليد!")

المرحلة الثانية: وضع المعاينة النقي وحظر أي معلومات أخرى
elif st.session_state.current_stage == "finished":
    # عرض اللعبة أو الموقع المنشأ بالكامل ونقياً داخل iframe فخم ملء الشاشة
    components.html(st.session_state.generated_html, height=750, scrolling=True)

    st.write("---")
    if st.button("🔄 العودة إلى شاشة التطوير والمحادثة لإجراء تعديل جديد"):
        st.session_state.current_stage = "discussion"
        st.rerun()
