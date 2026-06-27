import streamlit as st
import re
import time
from g4f.client import Client
import streamlit.components.v1 as components

# ═══════════════════════════════════════════════════════════════
# إعدادات الصفحة
# ═══════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="SPIDER-AI",
    page_icon="🕸️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ═══════════════════════════════════════════════════════════════
# الهوية البصرية الجديدة — VOID TERMINAL AESTHETIC
# لوحة ألوان: أسود عميق + ذهبي نيون + أبيض ثلجي
# ═══════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;700&display=swap');

/* ──────────── Reset & Base ──────────── */
*, *::before, *::after { box-sizing: border-box; }

html, body, [data-testid="stAppViewContainer"], .main {
    background-color: #080808 !important;
    font-family: 'Space Grotesk', sans-serif;
    direction: rtl;
    text-align: right;
    color: #e8e8e8;
}

/* Hide Streamlit chrome */
#MainMenu, footer, header, [data-testid="stToolbar"],
[data-testid="stDecoration"], [data-testid="stStatusWidget"] { display: none !important; }

[data-testid="stAppViewContainer"] > section:first-child { padding-top: 0 !important; }
.block-container { padding: 0 !important; max-width: 100% !important; }

/* ──────────── HERO HEADER ──────────── */
.hero-header {
    background: #080808;
    border-bottom: 1px solid #1a1a1a;
    padding: 18px 32px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    position: sticky;
    top: 0;
    z-index: 100;
}

.logo-mark {
    font-family: 'JetBrains Mono', monospace;
    font-size: 1.1rem;
    font-weight: 700;
    color: #e8c84a;
    letter-spacing: 0.15em;
    display: flex;
    align-items: center;
    gap: 10px;
}

.logo-mark .web-icon {
    width: 28px;
    height: 28px;
    border: 2px solid #e8c84a;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.75rem;
}

.header-tagline {
    font-size: 0.72rem;
    color: #555;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    font-family: 'JetBrains Mono', monospace;
}

.status-pill {
    background: #0f1a0f;
    border: 1px solid #1e3a1e;
    border-radius: 20px;
    padding: 4px 12px;
    font-size: 0.68rem;
    color: #4caf50;
    font-family: 'JetBrains Mono', monospace;
    letter-spacing: 0.05em;
    display: flex;
    align-items: center;
    gap: 6px;
}

.status-dot {
    width: 6px; height: 6px;
    background: #4caf50;
    border-radius: 50%;
    animation: pulse-green 2s infinite;
}

@keyframes pulse-green {
    0%, 100% { opacity: 1; box-shadow: 0 0 0 0 rgba(76,175,80,0.4); }
    50% { opacity: 0.7; box-shadow: 0 0 0 4px rgba(76,175,80,0); }
}

/* ──────────── TWO-COLUMN LAYOUT ──────────── */
.app-shell {
    display: grid;
    grid-template-columns: 380px 1fr;
    height: calc(100vh - 65px);
    overflow: hidden;
}

/* ──────────── LEFT PANEL — CHAT ──────────── */
.chat-panel {
    background: #0c0c0c;
    border-left: 1px solid #1a1a1a;
    display: flex;
    flex-direction: column;
    overflow: hidden;
}

.panel-label {
    padding: 14px 20px 10px;
    font-size: 0.65rem;
    color: #444;
    font-family: 'JetBrains Mono', monospace;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    border-bottom: 1px solid #111;
    flex-shrink: 0;
}

/* ──────────── WORKSPACE ──────────── */
.workspace-panel {
    background: #080808;
    display: flex;
    flex-direction: column;
    overflow: hidden;
}

/* ──────────── STREAMLIT OVERRIDES ──────────── */

/* Columns */
[data-testid="column"] { padding: 0 !important; }

/* Chat messages */
[data-testid="stChatMessage"] {
    background: transparent !important;
    border: none !important;
    padding: 8px 0 !important;
    margin: 0 !important;
}

[data-testid="stChatMessage"][data-testid*="user"] .stMarkdown {
    background: #141414;
    border: 1px solid #222;
    border-radius: 12px 12px 4px 12px;
    padding: 10px 14px;
    font-size: 0.88rem;
    color: #e8e8e8;
    max-width: 90%;
    margin-right: auto;
}

[data-testid="stChatMessage"][data-testid*="assistant"] .stMarkdown {
    background: #0f150f;
    border: 1px solid #1a2a1a;
    border-radius: 12px 12px 12px 4px;
    padding: 10px 14px;
    font-size: 0.88rem;
    color: #b8e8b8;
    max-width: 93%;
}

/* Chat avatar */
[data-testid="stChatMessage"] [data-testid="chatAvatarIcon-user"] {
    background: #1a1a1a !important;
    color: #e8c84a !important;
    border: 1px solid #2a2a2a !important;
    border-radius: 8px !important;
}

[data-testid="stChatMessage"] [data-testid="chatAvatarIcon-assistant"] {
    background: #0f150f !important;
    color: #4caf50 !important;
    border: 1px solid #1a2a1a !important;
    border-radius: 8px !important;
}

/* Chat input */
[data-testid="stChatInput"] {
    background: #0c0c0c !important;
    border-top: 1px solid #1a1a1a !important;
    padding: 12px 16px !important;
}

[data-testid="stChatInput"] textarea {
    background: #111 !important;
    border: 1px solid #222 !important;
    border-radius: 8px !important;
    color: #e8e8e8 !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 0.88rem !important;
    padding: 10px 14px !important;
    resize: none !important;
    caret-color: #e8c84a !important;
}

[data-testid="stChatInput"] textarea:focus {
    border-color: #333 !important;
    box-shadow: 0 0 0 2px rgba(232, 200, 74, 0.1) !important;
    outline: none !important;
}

[data-testid="stChatInput"] button {
    background: #e8c84a !important;
    border: none !important;
    border-radius: 6px !important;
    color: #080808 !important;
}

/* Tabs */
[data-baseweb="tab-list"] {
    background: transparent !important;
    border-bottom: 1px solid #1a1a1a !important;
    gap: 0 !important;
    padding: 0 20px !important;
}

[data-baseweb="tab"] {
    background: transparent !important;
    border: none !important;
    border-bottom: 2px solid transparent !important;
    border-radius: 0 !important;
    color: #444 !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.72rem !important;
    font-weight: 500 !important;
    padding: 12px 16px !important;
    margin: 0 !important;
    letter-spacing: 0.06em !important;
    transition: color 0.15s !important;
}

[data-baseweb="tab"]:hover { color: #888 !important; }

[aria-selected="true"] {
    color: #e8c84a !important;
    border-bottom-color: #e8c84a !important;
    background: transparent !important;
    font-weight: 700 !important;
}

[data-testid="stTabsContent"] { padding: 0 !important; }

/* Buttons */
div.stButton > button {
    background: #111 !important;
    border: 1px solid #222 !important;
    color: #888 !important;
    border-radius: 6px !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.72rem !important;
    font-weight: 500 !important;
    padding: 6px 14px !important;
    letter-spacing: 0.05em !important;
    transition: all 0.15s !important;
    width: auto !important;
}

div.stButton > button:hover {
    border-color: #e8c84a !important;
    color: #e8c84a !important;
    background: #0f0e06 !important;
    transform: none !important;
    box-shadow: none !important;
}

/* Download button */
[data-testid="stDownloadButton"] > button {
    background: #080e08 !important;
    border: 1px solid #1a3a1a !important;
    color: #4caf50 !important;
    border-radius: 6px !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.72rem !important;
    width: 100% !important;
    padding: 8px 14px !important;
}

/* Code block */
[data-testid="stCode"] {
    background: #0a0a0a !important;
    border: 1px solid #1a1a1a !important;
    border-radius: 8px !important;
}

pre { background: #0a0a0a !important; }

/* Scrollbar */
::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: #080808; }
::-webkit-scrollbar-thumb { background: #222; border-radius: 2px; }
::-webkit-scrollbar-thumb:hover { background: #333; }

/* Info / alerts */
[data-testid="stInfo"] {
    background: #0d0d0d !important;
    border: 1px solid #1a1a1a !important;
    border-radius: 8px !important;
    color: #555 !important;
    font-size: 0.85rem !important;
    font-family: 'JetBrains Mono', monospace !important;
}

/* Caption */
[data-testid="stCaption"] {
    color: #383838 !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.68rem !important;
}

/* Spinner */
[data-testid="stSpinner"] { color: #e8c84a !important; }

/* Container scrollable */
[data-testid="stVerticalBlockBorderWrapper"] { border: none !important; background: transparent !important; }

/* ──────────── CUSTOM COMPONENTS ──────────── */

/* Thinking terminal */
.terminal-log {
    background: #0a0a0a;
    border: 1px solid #1a1a1a;
    border-radius: 8px;
    padding: 16px 20px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.78rem;
    color: #555;
    margin: 16px;
}

.terminal-log .log-header {
    color: #2a2a2a;
    font-size: 0.65rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-bottom: 12px;
    padding-bottom: 8px;
    border-bottom: 1px solid #111;
}

.log-line { margin: 6px 0; display: flex; align-items: center; gap: 10px; }
.log-done { color: #4caf50; }
.log-active {
    color: #e8c84a;
    animation: flicker 1.5s ease-in-out infinite;
}
.log-wait { color: #2a2a2a; }

@keyframes flicker {
    0%, 100% { opacity: 1; }
    45% { opacity: 0.3; }
    55% { opacity: 0.3; }
}

.log-prefix { color: #2a2a2a; user-select: none; }
.log-active .log-prefix { color: #555; }
.log-done .log-prefix { color: #2a5f2a; }

/* Error card */
.error-terminal {
    background: #0d0505;
    border: 1px solid #3a1515;
    border-radius: 8px;
    padding: 14px 18px;
    margin: 16px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.78rem;
    color: #8b3a3a;
    direction: rtl;
    text-align: right;
}

.error-terminal .err-header { color: #c0392b; margin-bottom: 6px; font-weight: 700; }

/* Empty state */
.empty-workspace {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100%;
    gap: 16px;
    padding: 40px;
    text-align: center;
}

.empty-grid {
    width: 120px;
    height: 120px;
    position: relative;
    margin-bottom: 8px;
}

.empty-grid::before {
    content: '';
    position: absolute;
    inset: 0;
    background-image:
        linear-gradient(#111 1px, transparent 1px),
        linear-gradient(90deg, #111 1px, transparent 1px);
    background-size: 20px 20px;
    border-radius: 8px;
}

.empty-grid .center-dot {
    position: absolute;
    top: 50%; left: 50%;
    transform: translate(-50%, -50%);
    width: 12px; height: 12px;
    background: #e8c84a;
    border-radius: 50%;
    box-shadow: 0 0 20px rgba(232, 200, 74, 0.4);
}

.empty-title {
    font-size: 0.9rem;
    color: #333;
    font-family: 'JetBrains Mono', monospace;
    letter-spacing: 0.08em;
}

.empty-sub {
    font-size: 0.75rem;
    color: #222;
    max-width: 260px;
    line-height: 1.6;
}

/* iframe wrapper */
.preview-shell {
    padding: 0;
    height: calc(100vh - 130px);
    overflow: hidden;
}

/* Panel sections */
.section-padding { padding: 16px 20px; }
.workspace-actions {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 10px 20px;
    border-bottom: 1px solid #111;
}

/* Heading overrides */
h1, h2, h3, h4, h5, h6 {
    color: #e8e8e8 !important;
    font-family: 'Space Grotesk', sans-serif !important;
    margin: 0 !important;
}

p, span, label, div { color: inherit; }

/* Remove stMarkdown top margin */
.stMarkdown { margin: 0 !important; }

/* Columns gap fix */
[data-testid="stHorizontalBlock"] { gap: 0 !important; }

</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# State Management
# ═══════════════════════════════════════════════════════════════
defaults = {
    'messages': [
        {
            "role": "assistant",
            "content": "مرحباً — أنا **SPIDER-AI**.\n\nصِف فكرتك البرمجية: موقع، أداة، لوحة تحكم، أو لعبة. سأبنيها في ملف HTML واحد قابل للتشغيل الفوري."
        }
    ],
    'generated_html': "",
    'is_generating': False,
    'error_occurred': False,
    'architect_logs': [],
    'generation_count': 0,
}

for key, val in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = val

client = Client()

# ═══════════════════════════════════════════════════════════════
# Core Functions
# ═══════════════════════════════════════════════════════════════
def extract_html_code(raw_text: str) -> str:
    pattern = re.compile(
        r'(<!DOCTYPE html>.*?</html>|<html.*?</html>)',
        re.DOTALL | re.IGNORECASE
    )
    match = pattern.search(raw_text)
    if match:
        return match.group(1).strip()
    cleaned = re.sub(r'^```html\s*', '', raw_text, flags=re.IGNORECASE)
    cleaned = re.sub(r'```$', '', cleaned).strip()
    return cleaned


def call_spider_agent(prompt_type: str = "generation", user_prompt: str = "", existing_code: str = "") -> str:
    system_prompt = """
You are SPIDER-AI Code Architect — an elite senior software engineer and game developer.
Your only job: deliver fully working, bug-free, single-file HTML web applications and games.

ABSOLUTE RULES:
1. NEVER use placeholders, "// TODO", "// rest of code", or any omission comments. Write every line.
2. Output is a single self-contained HTML file. All CSS in <style>, all JS in <script>.
3. UI must be visually exceptional: dark/neon palette, smooth animations, fully responsive.
4. For games: keyboard + on-screen touch controls, scoring system, Game Over / Restart states.
5. ALL visible text in the generated app must be in ARABIC.
6. Response MUST start with <!DOCTYPE html> and end with </html>. No markdown fences. No commentary.
"""

    if prompt_type == "edit":
        compiled_prompt = f"""
Current code:
---
{existing_code}
---
Apply this modification precisely: "{user_prompt}"
Keep all existing features intact.
Output the FULL modified file starting with <!DOCTYPE html> ending with </html>.
"""
    else:
        compiled_prompt = (
            f"Build a complete, production-quality single-file HTML solution for: {user_prompt}"
        )

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

# ═══════════════════════════════════════════════════════════════
# HEADER
# ═══════════════════════════════════════════════════════════════
st.markdown("""
<div class="hero-header">
    <div class="header-tagline">محرك التجسيد البرمجي / Code Embodiment Engine</div>
    <div class="logo-mark">
        <div class="web-icon">🕸</div>
        SPIDER&ndash;AI
    </div>
    <div class="status-pill">
        <span class="status-dot"></span>
        ONLINE
    </div>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# LAYOUT: Chat (right) | Workspace (left)
# ═══════════════════════════════════════════════════════════════
col_workspace, col_chat = st.columns([1.4, 1], gap="small")

# ───────────────────────────────────────────
# CHAT PANEL
# ───────────────────────────────────────────
with col_chat:
    st.markdown('<div class="panel-label">◈ غرفة الأوامر / Command Room</div>', unsafe_allow_html=True)

    chat_container = st.container(height=int(
        # approximate height: full viewport minus header + input
        520
    ))
    with chat_container:
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

    if user_cmd := st.chat_input("اكتب فكرتك أو طلب التعديل..."):
        st.session_state.messages.append({"role": "user", "content": user_cmd})
        st.session_state.is_generating = True
        st.session_state.error_occurred = False
        st.rerun()

# ───────────────────────────────────────────
# GENERATION PROCESSING
# ───────────────────────────────────────────
if st.session_state.is_generating:
    last_user_msg = st.session_state.messages[-1]["content"]

    is_edit = bool(st.session_state.generated_html)
    prompt_type = "edit" if is_edit else "generation"
    existing_code = st.session_state.generated_html if is_edit else ""

    st.session_state.architect_logs = [
        ("active", "تحليل المتطلبات وهيكلة المشروع"),
        ("wait",   "بناء الواجهات البصرية وطبقات CSS" if not is_edit else "دمج التعديلات مع الكود الحالي"),
        ("wait",   "حقن منطق JavaScript والتفاعلية"),
        ("wait",   "مراجعة الكود وضمان الاكتمال"),
    ]

    with st.spinner(""):
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
            "content": f"⚠️ فشل الاتصال بمحرك التوليد. حاول مرة أخرى.\n\n`{raw_response.replace('ERROR_API_FAILED:', '').strip()}`"
        })
    else:
        final_html = extract_html_code(raw_response)
        st.session_state.generated_html = final_html
        st.session_state.generation_count += 1
        st.session_state.architect_logs = [
            ("done", "تحليل المتطلبات وهيكلة المشروع"),
            ("done", "بناء الواجهات البصرية وطبقات CSS" if not is_edit else "دمج التعديلات مع الكود الحالي"),
            ("done", "حقن منطق JavaScript والتفاعلية"),
            ("done", "اكتمل التجسيد — الكود جاهز للتشغيل"),
        ]
        st.session_state.messages.append({
            "role": "assistant",
            "content": "✓ تم. الكود جاهز في تبويب **المعاينة الحية** →"
        })
        st.session_state.is_generating = False

    st.rerun()

# ───────────────────────────────────────────
# WORKSPACE PANEL
# ───────────────────────────────────────────
with col_workspace:
    st.markdown('<div class="panel-label">◈ مساحة التجسيد / Build Workspace</div>', unsafe_allow_html=True)

    # Error banner
    if st.session_state.error_occurred:
        st.markdown("""
        <div class="error-terminal">
            <div class="err-header">✕ خطأ في الاتصال</div>
            <div>تعذر الوصول إلى محرك التوليد. الخوادم قد تكون مشغولة. أعد المحاولة.</div>
        </div>
        """, unsafe_allow_html=True)

    # Tabs
    tab_preview, tab_source, tab_logs = st.tabs([
        "PREVIEW",
        "SOURCE",
        "LOGS",
    ])

    # ── Preview Tab ──
    with tab_preview:
        if st.session_state.generated_html:
            c1, c2 = st.columns([5, 1])
            with c1:
                st.caption(f"build #{st.session_state.generation_count} · sandboxed iframe · read-only")
            with c2:
                if st.button("↺ reload"):
                    st.rerun()
            components.html(
                st.session_state.generated_html,
                height=580,
                scrolling=True
            )
        else:
            st.markdown("""
            <div class="empty-workspace" style="height:560px; display:flex; flex-direction:column; align-items:center; justify-content:center; gap:14px;">
                <div class="empty-grid" style="width:80px; height:80px; position:relative;">
                    <svg width="80" height="80" viewBox="0 0 80 80" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <rect x="0.5" y="0.5" width="79" height="79" rx="7.5" stroke="#1a1a1a"/>
                        <line x1="0" y1="20" x2="80" y2="20" stroke="#111" stroke-width="1"/>
                        <line x1="0" y1="40" x2="80" y2="40" stroke="#111" stroke-width="1"/>
                        <line x1="0" y1="60" x2="80" y2="60" stroke="#111" stroke-width="1"/>
                        <line x1="20" y1="0" x2="20" y2="80" stroke="#111" stroke-width="1"/>
                        <line x1="40" y1="0" x2="40" y2="80" stroke="#111" stroke-width="1"/>
                        <line x1="60" y1="0" x2="60" y2="80" stroke="#111" stroke-width="1"/>
                        <circle cx="40" cy="40" r="5" fill="#e8c84a" opacity="0.8"/>
                        <circle cx="40" cy="40" r="10" stroke="#e8c84a" stroke-width="0.5" opacity="0.3"/>
                        <circle cx="40" cy="40" r="18" stroke="#e8c84a" stroke-width="0.5" opacity="0.12"/>
                    </svg>
                </div>
                <div style="font-family:'JetBrains Mono',monospace; font-size:0.72rem; color:#2a2a2a; letter-spacing:0.1em;">AWAITING INPUT</div>
                <div style="font-size:0.78rem; color:#1e1e1e; max-width:240px; text-align:center; line-height:1.7;">
                    اكتب فكرتك البرمجية في غرفة الأوامر لتجسيدها هنا
                </div>
            </div>
            """, unsafe_allow_html=True)

    # ── Source Tab ──
    with tab_source:
        if st.session_state.generated_html:
            dl_col, _ = st.columns([1, 2])
            with dl_col:
                st.download_button(
                    label="↓ تحميل HTML",
                    data=st.session_state.generated_html,
                    file_name="spider_project.html",
                    mime="text/html"
                )
            st.caption("انسخ الكود من زر النسخ أعلى يسار الحقل ↓")
            st.code(st.session_state.generated_html, language="html", line_numbers=True)
        else:
            st.markdown("""
            <div style="padding:40px 20px; text-align:center; font-family:'JetBrains Mono',monospace; font-size:0.75rem; color:#1e1e1e;">
                // no code generated yet
            </div>
            """, unsafe_allow_html=True)

    # ── Logs Tab ──
    with tab_logs:
        if st.session_state.architect_logs:
            lines_html = ""
            for state, text in st.session_state.architect_logs:
                if state == "done":
                    lines_html += f'<div class="log-line log-done"><span class="log-prefix">✓</span> {text}</div>'
                elif state == "active":
                    lines_html += f'<div class="log-line log-active"><span class="log-prefix">›</span> {text}</div>'
                else:
                    lines_html += f'<div class="log-line log-wait"><span class="log-prefix">·</span> {text}</div>'

            st.markdown(f"""
            <div class="terminal-log">
                <div class="log-header">SPIDER-AI / BUILD LOG</div>
                {lines_html}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="padding:40px 20px; text-align:center; font-family:'JetBrains Mono',monospace; font-size:0.75rem; color:#1e1e1e;">
                // no active build process
            </div>
            """, unsafe_allow_html=True)
