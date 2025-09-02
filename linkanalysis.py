import pandas as pd
from collections import deque
import streamlit as st

# Defines the structure ofa node in the Trie data structure used for pattern matching.
class TrieNode:
    def __init__(self):
        self.children = {}
        self.end_of_word = False
        self.fail_link = None
        self.output = []

# This function adds a pattern (URL) to the Trie data structure and marks the end of the pattern.
def insert_trie(root, pattern, label):
    node = root
    for char in pattern:
        if char not in node.children:
            node.children[char] = TrieNode()
        node = node.children[char]
    node.end_of_word = True
    node.output.append(label)

# This builds the Aho-Corasick Automaton, which is built upon the Trie data structure, but with the set up of failure links for efficient pattern matching.
def build_aho_corasick(urls_and_patterns):
    root = TrieNode()
    
    # Insert URLs and patterns into the Trie
    for url, label in urls_and_patterns:
        insert_trie(root, url, label)
    
    # Build failure links using BFS
    queue = deque()
    for child in root.children.values():
        child.fail_link = root
        queue.append(child)

    # BFS to set failure links
    while queue:
        current_node = queue.popleft()
        for char, child in current_node.children.items():
            fail_node = current_node.fail_link
            while fail_node and char not in fail_node.children:
                fail_node = fail_node.fail_link
            child.fail_link = fail_node.children[char] if fail_node else root
            child.output += child.fail_link.output
            queue.append(child)
    
    return root

# Search function using Aho-Corasick automaton to find patterns in the given text.
def search_aho_corasick(root, text):
    node = root
    for char in text:
        while node and char not in node.children:
            node = node.fail_link
        if not node:
            node = root
            continue
        node = node.children[char]
        if node.output:
            return node.output
    return []

# Reads URL data from a CSV file using pandas.
@st.cache_data
def load_website_data(filepath='Datasets/url_dataset.csv'):
    return pd.read_csv(filepath)

# This function determines the category of a given URL by checking it against various patterns and domains.
def detect_url(input_url):
    if not input_url:
        return "info", "Please enter a URL to check."

    data = load_website_data()

    # Initialize an empty dictionary to store patterns by type
    patterns_by_type = {}

    # Iterate over unique types and extract URLs and types
    for url_type in data['type'].unique():
        patterns_by_type[url_type] = list(zip(data[data['type'] == url_type]['url'], data[data['type'] == url_type]['type']))
    
    # Build the Aho-Corasick automatons for each category
    automaton_roots = {url_type: build_aho_corasick(patterns) for url_type, patterns in patterns_by_type.items()}
    
    # Check if it's an official government or educational website based on domain suffix
    is_official_domain = any(suffix in input_url for suffix in ['.gov.sg', '.sg', '.edu.sg'])
    
    if is_official_domain:
        # Check against official URLs
        automaton_root = automaton_roots.get('official', TrieNode())
        matches_official = search_aho_corasick(automaton_root, input_url)
        if matches_official:
            return "Success", "The URL you entered is a verified official government or educational website in the database."
        else:
            return "Warning", "The URL you entered is under a government or educational domain, but it is not recognized as an official link in the current database. Please proceed with caution."
    
    else:
        # Check against all other categories
        found_match = False
        for url_type in ['phishing', 'benign', 'defacement', 'malware']:
            # Check if the URL matches any patterns in the automaton
            automaton_root = automaton_roots.get(url_type, TrieNode())
            # Search for matches in the automaton
            matches = search_aho_corasick(automaton_root, input_url)
            if matches:
                if url_type == 'phishing':
                    return "Error", "The URL you entered is potentially malicious (phishing)!"
                elif url_type == 'benign':
                    return "Success", "The URL you entered is a harmless website."
                elif url_type == 'defacement':
                    return "Warning", "The URL you entered is a defacement website where contents of the website have been possibly modified by attackers."
                elif url_type == 'malware':
                    return "Warning", "The URL you entered is a malware website where contents of the website might be malicious."
                found_match = True
                break
        
        if not found_match:
            return "warning", "The URL you entered is unknown but proceed with caution."

def stURL():
    input_url = st.text_input("Enter URL here:")

    if input_url:
        status, message = detect_url(input_url)
        if status == "Success":
            st.success(message)
        elif status == "Warning":
            st.warning(message)
        elif status == "Error":
            st.error(message)
    else:
        st.info("Please enter a URL to check.")