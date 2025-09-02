import streamlit as st
from riskValue import risk_manager
import checkphoneNumber
import questionnaire
import home
import SVMAho
import linkanalysis
import education

def home_page():
    home.display_home()
    # Reset risk value when returning to home page
    risk_manager.reset_risk()

    # Reset questionnaire_submitted state
    if 'questionnaire_submitted' in st.session_state:
        del st.session_state.questionnaire_submitted

def vishing_page():
    st.header('Vishing Page')
    st.markdown('We will help you determine whether a caller is a scammer or not.')
    checkphoneNumber.phonenumberChecker()
    questionnaire.run_questionnaire()
    SVMAho.run_text_analysis()
    risk_manager.display_main()

    total_risk = risk_manager.get_total_risk()
    if total_risk > 50:
        if 'phone_number_reported' not in st.session_state:
            st.session_state.phone_number_reported = False

        if not st.session_state.phone_number_reported:
            if st.button("Report Phone Number"):
                if checkphoneNumber.report_phone_number():
                    st.session_state.phone_number_reported = True
                    st.success("Phone number reported successfully!")
                    st.session_state.show_acknowledge = True
                    st.experimental_rerun()
        else:
            if st.session_state.get('show_acknowledge', False):
                st.success(st.session_state.get('report_message', "Phone number reported successfully!"))
                if st.button("Acknowledge"):
                    # Reset all relevant session state variables
                    st.session_state.phone_number_reported = False
                    st.session_state.show_acknowledge = False
                    if 'report_message' in st.session_state:
                        del st.session_state.report_message
                    # Set the app_mode to 'Home'
                    st.session_state.app_mode = 'Home'
                    st.experimental_rerun()
    else:
        st.warning("The total risk is below 50%. Reporting is not available for this number as it may not be a scam.")

def URL_page():
    st.header('URL Page')
    st.markdown('We will help you determine if the URL is a scam.')
    linkanalysis.stURL()

def education_page():
    education.displayEducation()


def main():
    risk_manager._init_risk_values()

    if 'app_mode' not in st.session_state:
        st.session_state.app_mode = 'Home'

    # Use the app_mode from session state for the selectbox
    st.session_state.app_mode = st.sidebar.selectbox('Select an Application',
                                                     ['Home', 'Vishing Defender', 'URL', 'Education'],
                                                     index=['Home', 'Vishing Defender', 'URL', 'Education'].index(
                                                         st.session_state.app_mode)
                                                     )

    if st.session_state.app_mode == 'Home':
        home_page()
    elif st.session_state.app_mode == 'Vishing Defender':
        vishing_page()
    elif st.session_state.app_mode == 'URL':
        URL_page()
    elif st.session_state.app_mode == 'Education':
        education_page()

if __name__ == '__main__':
    main()
