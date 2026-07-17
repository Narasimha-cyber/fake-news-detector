import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

st.title("📰 Fake News Detector - LIVE")

@st.cache_resource
def load_data():
    # Public dataset direct ga net nunchi
    df = pd.read_csv("https://raw.githubusercontent.com/GeorgeMcIntire/fake_news/master/data/fake_or_real_news.csv")
    df.columns = ['title', 'text', 'label']
    df['label'] = df['label'].map({'FAKE': 0, 'REAL': 1})

    vectorizer = TfidfVectorizer(stop_words='english', max_features=3000)
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
        st.success("✅ REAL") if pred==1 else st.error("❌ FAKE")
