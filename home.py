import streamlit as st

def display_home():
    # Header
    col1, col2 = st.columns([1, 3])
    with col1:
        st.image("Images/icon.png", width=150)  # Replace with your logo
    with col2:
        st.title("Welcome to Vishing Defender")
        st.subheader("Your Personal Guardian Against Voice Phishing Scams")

    # Main Content
    st.write("---")
    st.header("Protect Yourself from Voice Phishing Scams")

    # Two-column layout for main content
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("What is Vishing?")
        st.write("""
        Vishing, short for "voice phishing," is a sophisticated scam where 
        fraudsters use phone calls to trick individuals into revealing sensitive 
        information or transferring money. Our app helps you stay one step ahead 
        of these scammers.
        """)

        st.subheader("Why Use Vishing Defender?")
        st.markdown("""
        - 🔒 Comprehensive analysis of potential vishing threats
        - 🔄 Up-to-date database of scam indicators
        - 🛠️ Multi-faceted approach to scam detection
        - 👤 Personalized safety recommendations
        - 📚 Increase your awareness and protect your information
        """)

    with col2:
        st.subheader("How Vishing Defender Works")
        st.markdown("""
        1. **Phone Number Analysis**: Check if a number is associated with known vishing attempts.
        2. **Text Analysis**: Determine the likelihood of a given text being a scam.
        3. **Audio Analysis**: Identify potential vishing attempts in voice recordings.
        4. **URL Risk Assessment**: Evaluate the risk level of suspicious websites.
        5. **Interactive Risk Assessment**: Answer questions about a suspicious call to gauge the risk level.
        6. **Educational Resources**: Learn about common vishing tactics and protection strategies.
        """)

        st.info("Don't become a victim of vishing. Use Vishing Defender to stay safe!")

    # Call-to-Action
    st.write("---")
    st.subheader("Ready to Protect Yourself?")
    if st.button("Launch Vishing Defender", key="launch_button"):
        st.session_state.app_mode = "Vishing Defender"
        st.experimental_rerun()

    # Footer
    st.write("---")
    st.write("© 2024 Vishing Defender. All rights reserved.")

if __name__ == "__main__":
    display_home()