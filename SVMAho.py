import csv
import string
import pandas as pd
import streamlit as st
import time
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import numpy as np
from sklearn.svm import SVC #ML model
from analyzeWav import load_speech_to_text_model, wav_to_text
from linkanalysis import detect_url
from riskValue import risk_manager
import re

class TrieNode:
    def __init__(self):
        self.children = {}
        self.fail = None
        self.output = []

class AhoCorasick:
    def __init__(self):
        self.root = TrieNode()

    def add_word(self, word, category):
        current_node = self.root
        for char in word:
            if char not in current_node.children:
                current_node.children[char] = TrieNode()
            current_node = current_node.children[char]
        current_node.output.append((word, category))

    def build_automaton(self):
        queue = []
        for char, node in self.root.children.items():
            node.fail = self.root
            queue.append(node)

        while queue:
            current_node = queue.pop(0)
            for char, next_node in current_node.children.items():
                queue.append(next_node)
                fail_node = current_node.fail
                while fail_node is not None and char not in fail_node.children:
                    fail_node = fail_node.fail
                next_node.fail = fail_node.children[char] if fail_node else self.root
                next_node.output += next_node.fail.output if next_node.fail else []

    def search(self, text):
        current_node = self.root
        results = []

        for index, char in enumerate(text):
            while current_node is not None and char not in current_node.children:
                current_node = current_node.fail
            if current_node is None:
                current_node = self.root
                continue
            current_node = current_node.children[char]
            if current_node.output:
                for pattern, category in current_node.output:
                    results.append((pattern, category, index - len(pattern) + 1, index))
        
        return results

def load_patterns(file_path):
    patterns = []
    with open(file_path, 'r') as file:
        for line in file:
            patterns.append(line.strip().lower())
    return patterns

def preprocess_text(text):
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))  # Remove punctuation
    return text

def get_ngrams(text, n):
    words = text.split()
    return [' '.join(words[i:i+n]) for i in range(len(words)-n+1)]

def get_ac_features(text, automaton):
    ac_text = preprocess_text(text)
    matches = automaton.search(ac_text)
    
    keyword_score = sum(2 for pattern, category, start, end in matches if category == 'keyword')
    phrase_score = sum(3 for pattern, category, start, end in matches if category == 'phrase')
    
    bigrams = get_ngrams(ac_text, 2)
    trigrams = get_ngrams(ac_text, 3)
    bigram_score = sum(1 for bg in bigrams if any(keyword in bg for keyword, _, _, _ in matches if _ == 'keyword'))
    trigram_score = sum(2 for tg in trigrams if any(phrase in tg for phrase, _, _, _ in matches if _ == 'phrase'))
    
    return {
        'keyword_score': keyword_score,
        'phrase_score': phrase_score,
        'bigram_score': bigram_score,
        'trigram_score': trigram_score,
        'total_ac_score': keyword_score + phrase_score + bigram_score + trigram_score
    }

def extract_features(text, automaton, vectorizer):
    ac_features = get_ac_features(text, automaton)
    tfidf_features = vectorizer.transform([text])
    return ac_features, tfidf_features

def train_ml_model(X, y, automaton):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    vectorizer = TfidfVectorizer(max_features=5000, ngram_range=(1, 3))
    X_train_tfidf = vectorizer.fit_transform(X_train)
    X_test_tfidf = vectorizer.transform(X_test)
    
    # Extract Aho-Corasick features
    X_train_ac = pd.DataFrame([get_ac_features(text, automaton) for text in X_train])
    X_test_ac = pd.DataFrame([get_ac_features(text, automaton) for text in X_test])
    
    # Combine TF-IDF and Aho-Corasick features
    X_train_combined = np.hstack((X_train_tfidf.toarray(), X_train_ac))
    X_test_combined = np.hstack((X_test_tfidf.toarray(), X_test_ac))

    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train_combined)
    X_test_scaled = scaler.transform(X_test_combined)

    # Create SVM model with best parameters
    model = SVC(C=0.1, kernel='linear', gamma='scale', probability=True, random_state=42)
    
    # Fit the model
    model.fit(X_train_scaled, y_train)

    # Evaluate the model
    accuracy = model.score(X_test_scaled, y_test)
    print(f"Model accuracy: {accuracy:.2f}")
    
    return vectorizer, model, scaler

def interpret_vishing_probability(prob):
    score = int(prob * 35)  # Convert probability to a percentage out of 35%
    if score < 9:
        return score, "Very likely not vishing. However, remember to remain vigilant and cautious when receiving unknown phone calls."
    elif score < 18:
        return score, "Probably not vishing, but exercise caution"
    elif score < 27:
        return score, "Possibly vishing, treat with high suspicion"
    else:
        return score, "Very likely vishing"
    
def update_database(user_input, result):
    try:
        with open("./Datasets/Vishing_Data.csv", 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if user_input == row[0]:
                    return

        with open("./Datasets/Vishing_Data.csv",'a',newline='') as file:
            csvwriter = csv.writer(file)
            if result == "Very likely not vishing. However, remember to remain vigilant and cautious when receiving unknown phone calls.":
                label = 0
                csvwriter.writerow([user_input, label])
            elif result == "Probably not vishing, but exercise caution":
                label = 0
                csvwriter.writerow([user_input, label])
            elif result == "Possibly vishing, treat with high suspicion":
                label = 1
                csvwriter.writerow([user_input, label])
            else:
                label = 1
                csvwriter.writerow([user_input, label])
    except Exception as e:
        print(f"An error occurred while saving feedback: {str(e)}")

def calculate_risk(score):
    return score  # The score is already out of 35, so we return it as is

def detect_vishing(text, automaton, vectorizer, ml_model, scaler):
    ac_features, tfidf_features = extract_features(text, automaton, vectorizer)
    
    # Combine features
    combined_features = np.hstack((tfidf_features.toarray(), pd.DataFrame([ac_features])))
    
    # Scale features
    scaled_features = scaler.transform(combined_features)
    
    # Predict using the ML model
    ml_prob = ml_model.predict_proba(scaled_features)[0][1]  # Probability of being vishing
    
    score, interpretation = interpret_vishing_probability(ml_prob)
    return interpretation, score, score  # We return the score as the risk value directly

def Initialize_Automaton():
    vishing_keywords = load_patterns('./Datasets/Vishing_Keyword.txt')
    vishing_phrases = load_patterns('./Datasets/Vishing_Phrases.txt')

    automaton = AhoCorasick()

    # Add keywords and phrases to automaton
    for keyword in vishing_keywords:
        automaton.add_word(keyword, 'keyword')
    for phrase in vishing_phrases:
        automaton.add_word(phrase, 'phrase')

    automaton.build_automaton()

    # Load the dataset
    df = pd.read_csv('./Datasets/Vishing_Data.csv')

    # Prepare dataset
    X = df['text'].tolist()
    y = df['label'].tolist()

    # Train the model
    vectorizer, ml_model, scaler = train_ml_model(X, y, automaton)
    return automaton, vectorizer, ml_model, scaler

def contains_url(text, file_path='./Datasets/URL_keyword.csv'):
    text_lower = text.lower()
    with open(file_path, 'r') as file:
        for line in file:
            keyword = line.strip().lower()
            if keyword in text_lower:
                return True
    return False

def extract_urls(text):
    # Define a regex pattern to match URLs with and without protocols
    url_pattern = re.compile(
        r'\b(?:https?://|www\.)[^\s/$.?#].[^\s]*|'  # Matches http:// and https:// URLs, and www. URLs
        r'\b(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}(?:[^\s]*)?'  # Matches domains like example.com and example.com/path
        r'|(?:[a-zA-Z0-9-]+\.[a-zA-Z]{2,})(?:[^\s]*)?',  # Matches domains without protocol like example.com
        re.IGNORECASE
    )
    
    # Find all matches in the text
    urls = url_pattern.findall(text)
    
    # Clean up URLs by removing any trailing punctuation or special characters
    cleaned_urls = [url.strip('.,;()[]') for url in urls]
    
    return cleaned_urls

def run_text_analysis():
    st.subheader('Text Analysis')
    
    analysis_type = st.radio("Choose input type:", ("Text", "WAV File"))
    
    user_input = ""
    
    if analysis_type == "Text":
        user_input = st.text_area("Enter the text to analyze:")
    else:
        uploaded_file = st.file_uploader("Upload a WAV file", type=["wav"])
        
    if st.button('Analyze'):
        if analysis_type == "Text" and not user_input:
            st.error("Please enter some text to analyze.")
            return
        
        if analysis_type == "WAV File" and uploaded_file is None:
            st.error("Please upload a WAV file before analyzing.")
            return
        
        start_time = time.time()

        # Ensure the models and automaton are initialized only once
        if 'automaton' not in st.session_state:
            st.session_state.automaton, st.session_state.vectorizer, st.session_state.ml_model, st.session_state.scaler = Initialize_Automaton()
        
        if analysis_type == "WAV File":
            # Initialize speech-to-text model
            if 'speech_to_text_model' not in st.session_state:
                st.session_state.processor, st.session_state.speech_model, st.session_state.decoder = load_speech_to_text_model()
            
            # Convert WAV to text
            file_bytes = uploaded_file.read()
            user_input = wav_to_text(file_bytes, st.session_state.processor, st.session_state.speech_model, st.session_state.decoder)
            st.write("Transcribed text:")
            st.write(user_input)
        
        # Text Analysis
        if user_input:  
            result, score, risk_score = detect_vishing(user_input, st.session_state.automaton, st.session_state.vectorizer, 
                                                    st.session_state.ml_model, st.session_state.scaler)
                
            st.write(f"Likelihood of Vishing Scam (Text Analysis): {result}")
            st.write(f"Score: {score}% (out of 35%)")
                
            # Update the risk manager with the calculated risk score
            risk_manager.update_risk(risk_score, source='text_analysis')
                
            update_database(user_input, result)
                    
            # Check for URLs in the text
            urls = extract_urls(user_input)
            if urls:
                st.write("\nURLs detected in the text:")
                for url in urls:
                    st.write(f"Detected URL: {url}")
                    url_status, url_message = detect_url(url)
                    st.write(f"Analysis: {url_status} - {url_message}")
            else:
                st.write("No URLs detected in the text.")
        else:
            st.error("No input to analyze. Please enter text or upload a WAV file.")
        
        end_time = time.time()
        runtime = end_time - start_time
        st.write(f"\nRuntime: {runtime:.10f} seconds")
