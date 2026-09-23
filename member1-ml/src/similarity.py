from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from preprocess import clean_text


complaint1 = input("Enter first complaint: ")
complaint2 = input("Enter second complaint: ")

complaint1 = clean_text(complaint1)
complaint2 = clean_text(complaint2)

vectorizer = TfidfVectorizer()

vectors = vectorizer.fit_transform([
    complaint1,
    complaint2
])

similarity = cosine_similarity(vectors[0], vectors[1])[0][0]

print("\nSimilarity Score:", round(similarity, 3))

if similarity >= 0.5:
    print("Potentially similar complaints")
else:
    print("Complaints appear different")
