import streamlit as st
from PIL import Image  # ee line kothaga add chey

st.set_page_config(page_title="VERIFACT", page_icon="📰", layout="centered")
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
