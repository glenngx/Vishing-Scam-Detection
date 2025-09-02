import time
import string

# Boyer-Moore Implementation
def build_bad_char_heuristic(pattern):
    m = len(pattern)
    bad_char = {c: m for c in string.printable}
    for i in range(m - 1):
        bad_char[pattern[i]] = m - 1 - i
    return bad_char

def boyer_moore_search(text, pattern):
    m = len(pattern)
    n = len(text)
    
    if m == 0:
        return False

    bad_char = build_bad_char_heuristic(pattern)
    
    i = 0
    while i <= n - m:
        j = m - 1
        while j >= 0 and pattern[j] == text[i + j]:
            j -= 1
        if j < 0:
            return True
        else:
            i += max(1, j - bad_char.get(text[i + j], m))
    return False

# Aho-Corasick Implementation
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

# KMP with DFA Implementation
def build_dfa(pattern):
    m = len(pattern)
    alphabet = set(pattern)
    dfa = {char: [0] * m for char in alphabet}
    if m == 0:
        return dfa
    dfa[pattern[0]][0] = 1
    
    x = 0
    for j in range(1, m):
        for char in alphabet:
            dfa[char][j] = dfa[char][x]
        dfa[pattern[j]][j] = j + 1
        x = dfa[pattern[j]][x]
    
    return dfa

def kmp_search_with_dfa(dfa, pattern, text):
    m = len(pattern)
    n = len(text)
    i = 0  # index for text
    j = 0  # index for pattern (state in DFA)

    while i < n:
        if text[i] in dfa:
            j = dfa[text[i]][j]
        else:
            j = 0
        i += 1
        if j == m:
            return True
    return False

def preprocess_text(text):
    text = text.lower()  # Convert to lowercase
    text = text.translate(str.maketrans('', '', string.punctuation))  # Remove punctuation
    return text

# Load patterns from files
def load_patterns(file_path):
    with open(file_path, 'r') as file:
        patterns = [line.strip().lower() for line in file if line.strip()]
    return patterns

# Test Data
keywords = load_patterns('./Datasets/Vishing_Keyword.txt')
phrases = load_patterns('./Datasets/Vishing_Phrases.txt')
text = "Hi, I am John from Manuhealth Insurance. Your current plan has expired, do you want to renew the plan?"

# Measure Boyer-Moore setup and search time
bm_setup_time = 0
bm_search_time = 0
bm_results = []

for keyword in keywords:
    if keyword:
        start_time = time.time()
        bad_char = build_bad_char_heuristic(keyword)
        bm_setup_time += time.time() - start_time

        start_time = time.time()
        if boyer_moore_search(text, keyword):
            bm_results.append((keyword, "keyword"))
        bm_search_time += time.time() - start_time

for phrase in phrases:
    if phrase:
        start_time = time.time()
        bad_char = build_bad_char_heuristic(phrase)
        bm_setup_time += time.time() - start_time

        start_time = time.time()
        if boyer_moore_search(text, phrase):
            bm_results.append((phrase, "phrase"))
        bm_search_time += time.time() - start_time
    
print(f"Boyer-Moore setup time: {bm_setup_time:.10f} seconds")
print(f"Boyer-Moore search time: {bm_search_time:.10f} seconds")

# Add patterns to Aho-Corasick automaton
aho_automaton = AhoCorasick()
start_time = time.time()
for keyword in keywords:
    if keyword:
        aho_automaton.add_word(keyword, "keyword")
for phrase in phrases:
    if phrase:
        aho_automaton.add_word(phrase, "phrase")
aho_automaton.build_automaton()
setup_time_aho = time.time() - start_time

# Measure Aho-Corasick search time
start_time = time.time()
aho_results = aho_automaton.search(text)
search_time_aho = time.time() - start_time
print(f"Aho-Corasick setup time: {setup_time_aho:.10f} seconds")
print(f"Aho-Corasick search time: {search_time_aho:.10f} seconds")

# Measure KMP setup and search time
kmp_setup_time = 0
kmp_search_time = 0
kmp_results = []
for keyword in keywords:
    if keyword:
        start_time = time.time()
        dfa = build_dfa(keyword)
        kmp_setup_time += time.time() - start_time

        start_time = time.time()
        if kmp_search_with_dfa(dfa, keyword, text):
            kmp_results.append((keyword, "keyword"))
        kmp_search_time += time.time() - start_time

for phrase in phrases:
    if phrase:
        start_time = time.time()
        dfa = build_dfa(phrase)
        kmp_setup_time += time.time() - start_time

        start_time = time.time()
        if kmp_search_with_dfa(dfa, phrase, text):
            kmp_results.append((phrase, "phrase"))
        kmp_search_time += time.time() - start_time

print(f"KMP with DFA setup time: {kmp_setup_time:.10f} seconds")
print(f"KMP with DFA search time: {kmp_search_time:.10f} seconds")

# Print results
print(f"Aho-Corasick results: {aho_results}")
print(f"KMP with DFA results: {kmp_results}")
print(f"Boyer-Moore results: {bm_results}")
