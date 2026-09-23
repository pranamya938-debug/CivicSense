from src.preprocess import clean_text


print("===================================")
print("      CivicSense ML Demo")
print("===================================")

complaint = input("\nEnter a citizen complaint: ")

print("\nOriginal Complaint:")
print(complaint)

print("\nAfter Text Preprocessing:")
print(clean_text(complaint))

print("\nML modules available:")
print("1. Complaint preprocessing")
print("2. Complaint classification")
print("3. Complaint prediction")
print("4. Duplicate similarity detection")
