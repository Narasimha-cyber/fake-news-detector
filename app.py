import streamlit as st

st.set_page_config(page_title="VERIFACT", page_icon="logo.png", layout="centered")

# ===== VERIFACT THEME + WATERMARK CSS =====
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(180deg, #0B1120 0%, #111827 100%);
        color: #E5E7EB;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #00D4FF !important;
    }
    p, div, span, label {
        color: #E5E7EB;
    }
    .stButton>button {
        background-color: #1E3A8A;
        color: white;
        border-radius: 8px;
        border: 1px solid #00D4FF;
        font-weight: bold;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #00D4FF;
        color: #0B1120;
    }
    .stTextArea textarea {
        background-color: #1F2937;
        color: #E5E7EB;
        border: 1px solid #00D4FF;
        border-radius: 8px;
    }
    [data-testid="stAlert"] {
        background-color: #1F2937;
        border: 1px solid #00D4FF;
    }

    /* ===== WATERMARK LOGO BACKSIDE ===== */
    body {
        position: relative;
    }
    body::before {
        content: "";
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        width: 500px;
        height: 500px;
        background-image: url("logo.png");
        background-size: contain;
        background-repeat: no-repeat;
        opacity: 0.06; /* light watermark. 0.1 cheste konchem clear */
        z-index: -1;
        pointer-events: none;
    }
</style>
""", unsafe_allow_html=True)
# ===== CSS END =====


# Ikkada nunchi nee original VERIFACT code start avvali
# st.title("VERIFACT")
# st.write("Don't believe everything you read...")




st.components.v1.html('<meta name="google-site-verification" content="hO9BqD-mx6i5iv3UcL-7bVITxfSs_-NvheHkk0q7MIw" />')
# Iddi kothaga add chey - Logo show cheyyadaniki
logo = Image.open("logo.png")
st.image(logo, width=100)

st.title("📰 VERIFACT")
st.write("**Don't believe everything you read - Verify it with AI!**")
import pandas as pd
from io import StringIO
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

st.markdown("### AI-Powered Live Web Application for Fake News Detection")
st.markdown("### Made by: **Narasimha Rao Killi**")
st.markdown("#### **National Sanskrit University, Tirupati**")

# Dataset direct ga code lo ne undi
CSV_DATA = """title,text,label
"FAKE NEWS 1","This is fake news about politics",0
"REAL NEWS 1","The government announced new policy today",1
"FAKE NEWS 2","Aliens landed in Telangana yesterday",0
"REAL NEWS 2","India won the cricket match against Australia",1
"FAKE NEWS 3","Drink bleach to cure corona",0
"REAL NEWS 3","Scientists discovered new planet",1
"""

@st.cache_resource
def load_data():
    df = pd.read_csv(StringIO(CSV_DATA))
    
    vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
    X = vectorizer.fit_transform(df['text'])
    model = LogisticRegression().fit(X, df['label'])
    return model, vectorizer

model, vectorizer = load_data()
st.success("✅ Ready!")

news = st.text_area("News paste chey:")
if st.button("Check"):
    if news:
        vec = vectorizer.transform([news])
        pred = model.predict(vec)[0]
        if pred==1:
            st.success("✅ REAL news")
        else:
            st.error("❌ FAKE news")
