import streamlit as st
import os
import time
from dotenv import load_dotenv
from openai import OpenAI

# Load API
load_dotenv()

client = OpenAI(
    api_key=os.getenv("API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

# ---------------- THEME ---------------- #
dark_mode = st.toggle("🌗 Dark Mode", value=True)

if dark_mode:
    bg = "linear-gradient(135deg, #020617, #0f172a, #1e293b)"
    text = "#ffffff"
    subtext = "#cbd5f5"
    card = "rgba(255,255,255,0.06)"
    input_bg = "#020617"
    input_text = "#ffffff"
else:
    bg = "linear-gradient(135deg, #f8fafc, #e2e8f0)"
    text = "#000000"
    subtext = "#334155"
    card = "rgba(0,0,0,0.04)"
    input_bg = "#ffffff"
    input_text = "#000000"

st.markdown(f"""
<style>
.stApp {{ background: {bg}; color: {text}; }}

.title {{
    text-align: center;
    font-size: 3rem;
    font-weight: bold;
    background: linear-gradient(90deg, #38bdf8, #6366f1);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}}

.subtitle {{
    text-align: center;
    font-size: 1.2rem;
    color: {subtext};
}}

.card {{
    background: {card};
    padding: 20px;
    border-radius: 16px;
    backdrop-filter: blur(12px);
    margin-top: 20px;
}}

textarea {{
    background-color: {input_bg} !important;
    color: {input_text} !important;
}}

textarea::placeholder {{
    color: #94a3b8 !important;
}}

.stButton>button {{
    width: 100%;
    border-radius: 12px;
    background: linear-gradient(90deg, #6366f1, #3b82f6);
    color: white;
    height: 3em;
}}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ---------------- #
st.set_page_config(page_title="DECODR", layout="wide")

st.markdown("""
<h1 style='text-align:center; font-size:3rem;
background: linear-gradient(90deg, #38bdf8, #6366f1);
-webkit-background-clip: text;
-webkit-text-fill-color: transparent;'>
⚡ DECODR
</h1>
<p style='text-align:center; font-size:1.2rem; opacity:0.8;'>
Decode any code. Instantly.
</p>
""", unsafe_allow_html=True)

# ---------------- INPUT ---------------- #
st.markdown('<div class="card">', unsafe_allow_html=True)
code = st.text_area("📌 Paste your code here:", height=300)
st.markdown('</div>', unsafe_allow_html=True)

# ---------------- AI FUNCTIONS ---------------- #

def get_explanation(code):
    prompt = f"""
    Explain this code clearly in simple terms.

    Code:
    {code}
    """
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content


def get_complexity(code):
    prompt = f"""
    Analyze ONLY the time and space complexity of this code.
    Do NOT explain the code.
    Give a short answer.

    Code:
    {code}
    """
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content


def get_improvements(code):
    prompt = f"""
    Suggest improvements for this code.
    Do NOT explain the code.
    Give only improvements in bullet points.

    Code:
    {code}
    """
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# ---------------- TYPEWRITER ---------------- #
def typewriter(text):
    output = ""
    box = st.empty()
    for char in text:
        output += char
        box.markdown(output)
        time.sleep(0.002)

# ---------------- BUTTON ---------------- #
if st.button("🚀 Analyze Code"):
    if code:
        with st.spinner("Analyzing..."):
            explanation = get_explanation(code)
            complexity = get_complexity(code)
            improvements = get_improvements(code)

        # Tabs
        tab1, tab2, tab3 = st.tabs(["📘 Explanation", "📊 Complexity", "✨ Improvements"])

        with tab1:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            typewriter(explanation)
            st.markdown('</div>', unsafe_allow_html=True)

        with tab2:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            typewriter(complexity)
            st.markdown('</div>', unsafe_allow_html=True)

        with tab3:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            typewriter(improvements)
            st.markdown('</div>', unsafe_allow_html=True)

    else:
        st.warning("Please paste code.")

# ---------------- FOOTER ---------------- #
st.markdown("---")
st.caption("🚀 Built with AI • Advanced Developer Tool")