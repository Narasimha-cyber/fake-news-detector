from flask import Flask, render_template, request
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

app = Flask(__name__)

print("AI Model train avthondi...")
fake = pd.read_csv('Fake.csv')
real = pd.read_csv('real.csv')
fake['label'] = 0
real['label'] = 1
df = pd.concat([fake, real])
df = df.sample(frac=1).reset_index(drop=True)

X = df['title']
y = df['label']
vectorizer = TfidfVectorizer(stop_words='english', max_df=0.7)
X_tfidf = vectorizer.fit_transform(X)
model = LogisticRegression(max_iter=1000)
model.fit(X_tfidf, y)
print("AI Model ready!")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    news = request.form['news']
    news_tfidf = vectorizer.transform([news]) # [news] important
    prediction = model.predict(news_tfidf)[0]
    result = "✅ REAL NEWS" if prediction == 1 else "❌ FAKE NEWS"
    return render_template('index.html', prediction_text=result, news=news)

if __name__ == '__main__':
    app.run(debug=True)