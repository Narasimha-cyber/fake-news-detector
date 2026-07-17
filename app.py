import streamlit as st
import pandas as pd
import gdown
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

st.set_page_config(page_title="Fake News Detector", layout="centered")

FAKE_URL = "https://drive.google.com/uc?id=1QGrDaL88OVGrwTBRXfJcJzWGqDuYuB8D"
REAL_URL = "https://drive.google.com/uc?id=1RaLax4cnSZBsa2z2nwRj8SX69M6cWm3-"

@st.cache_data
def load_data():
    st.write("⏳ Downloading dataset from Google Drive...")
    gdown.download(FAKE_URL, "Fake.csv", quiet=False)
    gdown.download(REAL_URL, "real.csv", quiet=False)
    fake = pd.read_csv("Fake.csv")
    real = pd.read_csv("real.csv")
    fake["label"] = 0
    real["label"] = 1
    df = pd.concat([fake, real])
    df = df[["title", "text", "label"]].fillna("")
    df["content"] = df["title"] + " " + df["text"]
    return df

@st.cache_resource
def train_model(df):
    st.write("🧠 Training model...")
    X = df["content"]
    y = df["label"]
    vectorizer = TfidfVectorizer(stop_words="english", max_df=0.7)
    X_vec = vectorizer.fit_transform(X)
    X_train, X_test, y_train, y_test = train_test_split(X_vec, y, test_size=0.2)
    model = LogisticRegression(max_iter=200)
    model.fit(X_train, y_train)
    acc = accuracy_score(y_test, model.predict(X_test))
    return model, vectorizer, acc

st.title("📰 Fake News Detector")
df = load_data()
model, vectorizer, acc = train_model(df)
st.success(f"✅ Model Ready! Accuracy: {acc*100:.2f}%")

news_input = st.text_area("News text ikkada paste chey:")
if st.button("Check News"):
    if news_input:
        vec = vectorizer.transform([news_input])
        pred = model.predict(vec)[0]
        st.success("✅ REAL news") if pred == 1 else st.error("❌ FAKE news")
