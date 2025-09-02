import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score
from sklearn.metrics import make_scorer, precision_score

# Load the data
data = pd.read_csv('./Datasets/Vishing_Data.csv')

# Assuming 'text' is the column containing the text data and 'label' is the target variable
X = data['text']
y = data['label']

# Text vectorization
vectorizer = TfidfVectorizer(max_features=1000)
X_tfidf = vectorizer.fit_transform(X)

# If you have any numerical features, you can add them here
# For example, if you have a 'duration' column:
# X_numerical = data[['duration']]
# X_numerical_scaled = StandardScaler().fit_transform(X_numerical)
# X_combined = np.hstack((X_tfidf.toarray(), X_numerical_scaled))

# If you don't have additional numerical features, just use the TF-IDF features
X_combined = X_tfidf.toarray()

def compare_models(X, y):
    models = {
        'Logistic Regression': LogisticRegression(random_state=42),
        'Naive Bayes': MultinomialNB(),
        'Decision Tree': DecisionTreeClassifier(max_depth=3, random_state=42),
        'SVM': SVC(kernel='rbf', probability=True, random_state=42),
        'Random Forest': RandomForestClassifier(n_estimators=100, max_depth=3, random_state=42)
    }

    # Create a precision scorer
    precision_scorer = make_scorer(precision_score, zero_division=0)
    
    for name, model in models.items():
        accuracy_scores = cross_val_score(model, X, y, cv=5, scoring='accuracy')
        precision_scores = cross_val_score(model, X, y, cv=5, scoring=precision_scorer)
        
        print(f"{name}:")
        print(f"  Mean accuracy: {accuracy_scores.mean():.2f} (+/- {accuracy_scores.std() * 2:.2f})")
        print(f"  Mean precision: {precision_scores.mean():.2f} (+/- {precision_scores.std() * 2:.2f})")
        print()
        
# Run the comparison
compare_models(X_combined, y)