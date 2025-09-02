import streamlit as st
from datetime import datetime
import os

# Left Leaning Red Black Tree implementation for educational quiz. Node class represents each node in the LLRBT
class Node:
    RED = True
    BLACK = False

    def __init__(self, key, val, color, size):
        self.key = key
        self.val = val
        self.color = color
        self.size = size
        self.left = None
        self.right = None

class LLRBT:
    def __init__(self):
        self.root = None

    def is_red(self, x): # Check if a node is red
        if x is None:
            return False
        return x.color == Node.RED

    def size(self, x): # Get the size of subtree rooted at node x
        if x is None:
            return 0
        return x.size

    def put(self, key, val): # Insert a new key-value pair into the LLRBT
        self.root = self._put(self.root, key, val)
        self.root.color = Node.BLACK # Ensure root is black

    def _put(self, h, key, val): # Recursive helper function for put() to maintain LLRBT properties
        if h is None: # Base case: insert new red node if current node is None
            return Node(key, val, Node.RED, 1)

        if key < h.key: # Recursively insert into left subtree
            h.left = self._put(h.left, key, val)
        elif key > h.key: # Recursively insert into right subtree
            h.right = self._put(h.right, key, val)
        else: # Update value if key already exists
            h.val = val

        # Rotations and color flips to maintain LLRBT properties
        if self.is_red(h.right) and not self.is_red(h.left):
            h = self.rotate_left(h)
        if self.is_red(h.left) and self.is_red(h.left.left):
            h = self.rotate_right(h)
        if self.is_red(h.left) and self.is_red(h.right):
            self.flip_colors(h)

        h.size = self.size(h.left) + self.size(h.right) + 1 # Update size of subtree rooted at h
        return h

    def rotate_left(self, h): # Left rotation to fix right-leaning red links
        x = h.right
        h.right = x.left
        x.left = h
        x.color = h.color
        h.color = Node.RED
        x.size = h.size
        h.size = self.size(h.left) + self.size(h.right) + 1
        return x

    def rotate_right(self, h): # Right rotation to fix two consecutive left red links
        x = h.left
        h.left = x.right
        x.right = h
        x.color = h.color
        h.color = Node.RED
        x.size = h.size
        h.size = self.size(h.left) + self.size(h.right) + 1
        return x

    def flip_colors(self, h): # Color flip to split a 4-node
        h.color = not h.color
        h.left.color = not h.left.color
        h.right.color = not h.right.color

    def get(self, key): # Get the value associated with a key
        return self._get(self.root, key)

    def _get(self, x, key): # Recursive helper function for get()
        if x is None:
            return None
        if key < x.key:
            return self._get(x.left, key)
        elif key > x.key:
            return self._get(x.right, key)
        else:
            return x.val

# Initialize the LLRBT with quiz questions
def init_quiz():
    quiz = LLRBT()
    quiz.put(1, {
        "question": "Is it safe to give out your bank details over the phone if the caller claims to be from your bank?",
        "options": ["Yes", "No"],
        "correct": "No",
        "explanation": "Always verify the caller's identity independently."
    })
    quiz.put(2, {
        "question": "What information should you never share over the phone?",
        "options": ["Your favorite color", "Your bank account details and passwords", "Your pet's name"],
        "correct": "Your bank account details and passwords",
        "explanation": "Never share sensitive information like bank account details and passwords over the phone."
    })
    quiz.put(3, {
        "question": "If you receive a suspicious call, what's the best immediate action to take?",
        "options": ["Keep the caller on the line to gather information", "Hang up immediately", "Provide false information to confuse the caller"],
        "correct": "Hang up immediately",
        "explanation": "The safest action is to end the call immediately."
    })
    quiz.put(4, {
        "question": "If a caller creates a sense of urgency, it's best to act quickly to resolve the issue.",
        "options": ["True", "False"],
        "correct": "False",
        "explanation": "Urgency is a common tactic used by scammers. Always take time to verify the situation."
    })
    quiz.put(5, {
        "question": "Why should you avoid clicking on links sent to you by unknown callers?",
        "options": ["The link might be broken", "The link could lead to a phishing site",
                    "It might take too much time"],
        "correct": "The link could lead to a phishing site",
        "explanation": "Links sent by unknown callers could direct you to phishing websites designed to steal your personal information."
    })
    quiz.put(6, {
        "question": "What should you do if you accidentally provide personal information to a scammer?",
        "options": ["Report the incident to your bank and change your passwords", "Ignore it and hope nothing happens",
                    "Call the scammer back and ask them to delete the information"],
        "correct": "Report the incident to your bank and change your passwords",
        "explanation": "If you accidentally share personal information with a scammer, report the incident immediately to your bank and change your passwords to protect your accounts."
    })
    return quiz

# Dataset for user tips submission
TIPS_FILE = "Datasets/community_tips.txt"

def save_tip(tip):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(TIPS_FILE, "a") as file:
        file.write(f"{timestamp} - {tip}\n")

def get_tips():
    if os.path.exists(TIPS_FILE):
        with open(TIPS_FILE, "r") as file:
            return file.readlines()
    return []
def displayEducation():
    # Header
    col1, col2 = st.columns([1, 3])
    with col1:
        st.image("Images/icon.png", width=150)  # Replace with your logo
    with col2:
        st.title("Vishing Education Page")
        st.info("""
        Contrary to popular beliefs, not only the older demographics are susceptible to Vishing. \n
        Millennials and Gen Z are increasingly targeted due to their high engagement with digital platforms, 
        where threat actors can extract personal information and initiate a sophisticated vishing attack.
        """)

    # Main Content
    st.write("---")
    st.markdown("""
                
                
                
                """)


    # Two-column layout for main content
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("How to identify a vishing scam?")
        st.markdown("""
        1. **Urgency and fear tactics**: \n
        Scammers will utilize threats to induce a feeling of urgency in order to push you into taking quick action. 
        If you receive a call like this, stay composed and do not provide any payment or personal details.
    
        2. **Background noise or poor audio quality**: \n
        Loud ambient sounds or inferior audio clarity.

        Be alert for unusual background noise or low-quality audio during phone conversations. 
        Additionally, pay attention to voices that sound unnatural or robotic, as they may indicate a robocall.
                    
        3. **Immediate Payment**: \n
        A telltale sign is if the caller warns of consequences if money is not transfered immediately.
                    
        4. **Personal Information Inquiry**: \n
        You should start to be suspicious if the caller claims to be a government official or from a legitimate source and
        requests for your bank details and personal information such as NRIC. 
                    
        5. **Keep it to yourself**: \n
                    
        You are advised not to share the call with anyone.
        This is done to discourage you from finding help and identify the call as a vishing scam.
                    
        6. **Caller number with the "+" prefix**: \n
        When you see a number that appears to be local but has a "+" at the beginning, it is probably

        Fake phone call. The prefix "+" sign is only used for incoming international calls.

        Local calls will not include a "+" prefix in the display.       
        """)




    with col2:
        st.subheader("How to Protect Yourself?")
        st.info("""
        🔒 Use our Vishing Defender to protect yourself from vishing 
        """)
        st.info("""
        1. **Verify the identity of the caller**: \n
        When requested for sensitive information, always verify the identity of the caller by
        calling the phone number found on the official website of the company the caller claims to work for.\n
        **DO NOT call back using the number provided by the caller.**
        """)

        st.info("""
        2. **Ignore calls from unknown numbers**: \n
        It may be tempting to pick up every call, but there is no obligation to do so.
        If the call is legitamate or important, the caller will call back again or leave a voicemail.
        """)

        st.info("""
        3. **Use call-blocking features**: \n
        Activate call-blocking functions on your phone in order to screen for possible vishing scams. 
        Many smartphones include this feature in order to assist you in dodging deceptive phone calls.
        """)

        st.info("""
        4. **Use two-factor authentication**: \n
        Add an extra layer of security to your mobile device and accounts by enabling two-factor authentication.
        """)

        st.info("""
        5. **Have faith in your gut feelings and end the call**: \n
        Lastly, if you feel like you are receiving a vishing call, you are not obligated to speak politely. 
        Just end the call and add the number to your block list.
        """)

    # Interactive Quiz
    st.write("---")
    st.subheader("Test Your Vishing Knowledge")

    if 'quiz_submitted' not in st.session_state:
        st.session_state.quiz_submitted = False
    if 'user_answers' not in st.session_state:
        st.session_state.user_answers = {}
    if 'quiz_score' not in st.session_state:
        st.session_state.quiz_score = 0

    def submit_quiz():
        st.session_state.quiz_submitted = True
        score = 0
        for i in range(1, num_questions + 1):
            if st.session_state.user_answers.get(i) == quiz.get(i)['correct']:
                score += 1
        st.session_state.quiz_score = score

    with st.expander("Take a Quick Quiz"):
        quiz = init_quiz()
        num_questions = 6

        for i in range(1, num_questions + 1):
            q = quiz.get(i)
            user_answer = st.radio(f"{i}. {q['question']}", q['options'], index=None, key=f"q{i}")
            st.session_state.user_answers[i] = user_answer

            if st.session_state.quiz_submitted:
                if st.session_state.user_answers[i] == q['correct']:
                    st.success("Correct!")
                else:
                    st.error(f"Incorrect. The correct answer is '{q['correct']}'.")
                st.info(q['explanation'])

        if not st.session_state.quiz_submitted:
            if st.button("Submit Quiz", on_click=submit_quiz):
                pass
        else:
            st.write(f"Your score: {st.session_state.quiz_score}/{num_questions}")
            if st.session_state.quiz_score == num_questions:
                st.success("Great job! You're well-prepared to identify vishing attempts.")
            elif st.session_state.quiz_score >= num_questions // 2:
                st.success("Good effort! Keep learning to better protect yourself.")
            else:
                st.info("Keep reviewing the information above to improve your vishing awareness.")

            if st.button("Retake Quiz"):
                st.session_state.quiz_submitted = False
                st.session_state.user_answers = {}
                st.session_state.quiz_score = 0
                st.experimental_rerun()

    # Community Tips Section
    st.write("---")
    st.subheader("Community Tips")

    with st.expander("Click to view community tips"):
        tips = get_tips()
        if tips:
            for tip in tips:
                st.info(tip.strip())
        else:
            st.write("No tips have been submitted yet. Be the first to share your advice!")

    st.write("---")
    st.subheader("Share Your Tips")
    user_tip = st.text_area("Do you have a tip for avoiding vishing scams? Share it here:")
    if st.button("Submit Tip"):
        if user_tip:
            save_tip(user_tip)
            st.success("Thank you for sharing your tip! It has been added to our community tips section.")
        else:
            st.error("Please enter a tip before submitting.")

    # Call-to-Action
    st.write("---")
    st.subheader("Ready to Protect Yourself?")
    if st.button("Launch Vishing Defender", key="launch_button"):
        st.session_state.app_mode = "Vishing Defender"
        st.experimental_rerun()

    # Footer
    st.write("---")
    st.write("© 2024 Vishing Defender. All rights reserved.")