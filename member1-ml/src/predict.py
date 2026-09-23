import pandas as pd

from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

from preprocess import clean_text


df = pd.read_csv("../data/complaints.csv")

df["cleaned_complaint"] = df["complaint"].apply(clean_text)

X = df["cleaned_complaint"]
y = df["category"]

model = Pipeline([
    ("tfidf", TfidfVectorizer(ngram_range=(1, 2))),
    ("classifier", LogisticRegression(max_iter=1000))
])

model.fit(X, y)

complaint = input("Enter citizen complaint: ")

cleaned = clean_text(complaint)

prediction = model.predict([cleaned])[0]

print("\nPredicted Category:", prediction)
