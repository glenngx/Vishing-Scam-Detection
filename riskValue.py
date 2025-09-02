import streamlit as st

class RiskManager:
    def __init__(self):
        self.risk_types = ['total', 'questionnaire', 'phone_number', 'text_analysis']
        self._init_risk_values()

    def _init_risk_values(self):
        for risk_type in self.risk_types:
            if f'{risk_type}_risk_value' not in st.session_state:
                st.session_state[f'{risk_type}_risk_value'] = 0

    def update_risk(self, val, source='general'):
        if source in self.risk_types:
            st.session_state[f'{source}_risk_value'] = val
        else:
            st.session_state.total_risk_value += val
        return self.get_total_risk()

    def get_risk(self, risk_type):
        return st.session_state[f'{risk_type}_risk_value']

    def get_total_risk(self):
        total_risk = sum(self.get_risk(risk_type) for risk_type in self.risk_types if risk_type != 'total')
        return min(total_risk, 100)  # Cap the total risk at 100%

    def reset_risk(self, risk_type=None):
        if risk_type:
            st.session_state[f'{risk_type}_risk_value'] = 0
        else:
            for risk_type in self.risk_types:
                st.session_state[f'{risk_type}_risk_value'] = 0

    def display_main(self):
        st.sidebar.subheader('Current Risk Level')
        total_risk = self.get_total_risk()
        st.sidebar.write(f'Likelihood of scam: {total_risk:.2f}%')
        self.color_progress_bar(total_risk)

    def color_progress_bar(self, percentage):
        if percentage == 100:
            bar_color = "#FF0000"  # Red
        elif percentage > 50:
            bar_color = "#FFA500"  # Orange
        else:
            bar_color = "#FFD700"  # Gold

        bar_width = f"{percentage}%"

        bar_html = f"""
            <style>
            .progress-bar {{
                width: 100%;
                background-color: #f0f0f0;
                border-radius: 5px;
                padding: 3px;
            }}
            .progress {{
                width: {bar_width};
                height: 24px;
                background-color: {bar_color};
                border-radius: 3px;
                transition: width 0.5s ease-out;
            }}
            </style>
            <div class="progress-bar">
                <div class="progress"></div>
            </div>
            """
        st.sidebar.markdown(bar_html, unsafe_allow_html=True)

# Create a global instance of RiskManager
risk_manager = RiskManager()
