import streamlit as st
from riskValue import risk_manager

########## Questionnaire ##########
# QuestionNode class to represent each question node
class QuestionNode:
    def __init__(self, question, weight=0, category=None):
        self.question = question
        self.weight = weight
        self.yes_node = None
        self.no_node = None
        self.category = category

def get_custom_message(risk_percentage, scam_categories):
    messages = {
        #General categories
        "identity_theft": "Protect your personal information. Don't share sensitive details like passwords or social security numbers over the phone.",
        "urgency_scam": "Be skeptical of high-pressure tactics, urgent demands, or pressure to make quick decisions. Legitimate organizations give you time to consider offers and make decisions.",
        "secrecy": "Be wary of requests for secrecy. Legitimate callers don't ask you to keep conversations secret.",
        "unusual_payment": "Be extremely cautious of requests for payment through unusual methods like gift cards or wire transfers. These are often signs of a scam and are difficult to trace or reverse.",

        #Impersonation Scam categories
        "unexpected_contact": "Be cautious of unexpected contacts, especially those claiming to be someone you know. Verify their identity through independent means before sharing any information.",
        "authority_impersonation": "Be wary of unsolicited contacts from people claiming to be in positions of authority. Legitimate organizations usually have official channels for communication.",
        "personal_impersonation": "If someone claims to be a friend or family member in an unusual situation, verify their identity by contacting them through a known, trusted method before taking any action.",
        "financial": "Be cautious of any requests for financial transactions. Legitimate organizations typically don't ask for immediate transfers.",
        "vague_communication": "Be skeptical of vague or inconsistent information. Legitimate contacts should be able to provide clear, verifiable details.",
        "manipulation": "Be aware of emotional manipulation tactics. Scammers often try to provoke fear, excitement, or sympathy.",

        #Job Scam categories
        "unsolicited_offer": "Be cautious of unsolicited job offers. Legitimate employers typically don't send out job offers to people who haven't applied.",
        "unrealistic_offer": "If a job offer seems too good to be true, it probably is. Be skeptical of offers promising high pay for little work or experience.",
        "vague_details": "Legitimate job postings usually provide clear details about the role and company. Be wary of vague or overly general job descriptions.",
        "advance_fee_fraud": "Legitimate employers will never ask you to pay money upfront to get a job. Any request for payment is a major red flag.",
        "unprofessional_conduct": "Professional companies maintain professional communication. Be wary of poorly written emails, unprofessional language, or lack of proper business etiquette.",
        "suspicious_process": "Be cautious of unusual interview processes, such as job offers without proper interviews or interviews conducted only via text messages.",
        "financial_info_theft": "Never provide bank account information before you've been officially hired and have verified the legitimacy of the company.",
        "remote_work_scam": "While many legitimate remote work opportunities exist, be extra cautious with unsolicited work-from-home offers, as they're often used in scams.",
        "fake_company": "Always research the company offering the job. If you can't find verifiable information about the company, it might not be legitimate.",
        "money_laundering_scheme": "Legitimate jobs won't ask you to transfer money or handle financial transactions using your personal accounts. This is often a sign of a money laundering scheme.",
        "false_promises_job": "Be skeptical of jobs that promise easy money or guaranteed income. Legitimate jobs typically don't make such guarantees.",
        "lack_of_professionalism": "Legitimate companies usually use corporate email addresses. Be cautious if the employer is using a personal email address for official communication.",

        # Romance Scam categories
        "online_meeting": "Be cautious with online relationships. Scammers often use dating sites and social media to find victims. Always verify the person's identity and be wary of those who can't or won't meet in person.",
        "rapid_romance": "Be skeptical of someone who expresses intense feelings very quickly. Scammers often use this tactic to manipulate victims emotionally. True love takes time to develop.",
        "avoiding_meeting": "If someone always has excuses for why they can't meet in person, video chat, or voice call, this is a major red flag. Scammers avoid face-to-face interactions to hide their true identity.",
        "financial_romance": "Never send money to someone you haven't met in person, no matter how compelling their story. Legitimate romantic interests won't ask you for financial assistance, especially early in a relationship.",
        "identity_concealment": "If someone refuses to video chat or always has excuses for why their camera doesn't work, they may be hiding their true identity. Insist on seeing the person in real-time before the relationship progresses.",
        "fake_profile": "If the person's social media presence seems limited or recent, it could be a fake profile. Look for inconsistencies and be skeptical of profiles with few friends or posts.",
        "false_information": "Pay attention to inconsistencies in the information they provide about themselves. Scammers often struggle to keep their stories straight over time.",
        "false_promises_romance": "Be cautious of repeated promises to meet that always fall through due to last-minute emergencies. This is a common tactic to string victims along without ever meeting in person.",
        "status_claim": "Claims of high-status jobs, especially those that explain why they can't meet (like military deployment or international business), should be verified. Scammers often use these to seem impressive and explain their absence.",
        "blackmail": "Never send compromising photos or information, no matter how much you trust the person. Scammers can use these for blackmail, threatening to release them unless you pay.",
        "isolation_tactic": "Be cautious if someone insists on moving communication away from the dating site to email or text. While this can be normal as relationships progress, it's also a tactic scammers use to avoid detection by the dating site."
    }

    custom_message = "Based on your answers, here are some specific recommendations:\n\n"
    for category in scam_categories:
        if category in messages:
            custom_message += f"- {messages[category]}\n"
    return custom_message.strip()

# # Construct the trees with structured questions and weights
# Tree for impersonation scam scenario
impersonation_root = QuestionNode("Did you receive an unexpected contact claiming to be someone you know?", 10,
                                  "unexpected_contact")

# Level 1 questions
claim_authority = QuestionNode("Did they claim to be from a position of authority (e.g., government, bank, executive)?",
                               20, "authority_impersonation")
impersonation_root.yes_node = claim_authority

claim_personal = QuestionNode("Did they claim to be a friend, family member, or colleague in an unusual situation?", 20,
                              "personal_impersonation")
impersonation_root.no_node = claim_personal

# Level 2 questions for authority claim
request_sensitive_info = QuestionNode("Did they ask for sensitive personal or financial information?", 30,
                                      "identity_theft")
claim_authority.yes_node = request_sensitive_info

create_urgency = QuestionNode("Did they create a sense of urgency or emergency?", 20, "urgency_scam")
claim_authority.no_node = create_urgency

# Level 2 questions for personal claim
request_money = QuestionNode("Did they ask for money or financial assistance?", 30, "financial")
claim_personal.yes_node = request_money

avoid_direct_contact = QuestionNode("Did they provide reasons why they can't be contacted directly?", 20, "secrecy")
claim_personal.no_node = avoid_direct_contact

# Level 3 questions
unusual_payment = QuestionNode("Did they request payment through unusual methods (e.g., gift cards, wire transfers)?",
                               30, "unusual_payment")
request_sensitive_info.yes_node = unusual_payment

threaten_consequences = QuestionNode("Did they threaten negative consequences if you don't comply quickly?", 20,
                                     "urgency_scam")
request_sensitive_info.no_node = threaten_consequences

request_secrecy = QuestionNode("Did they ask you to keep the interaction secret?", 20, "secrecy")
create_urgency.yes_node = request_secrecy

provide_vague_info = QuestionNode("Did they provide vague or inconsistent information when asked for details?", 20,
                                  "vague_communication")
create_urgency.no_node = provide_vague_info

pressure_quick_decision = QuestionNode("Did they pressure you to make a quick decision without time to think?", 20,
                                       "urgency_scam")
request_money.yes_node = pressure_quick_decision

emotional_manipulation = QuestionNode("Did they use emotional manipulation (e.g., guilt, flattery)?", 20,
                                      "manipulation")
request_money.no_node = emotional_manipulation

# Level 4 questions
request_personal_details = QuestionNode("Did they ask for additional personal details to 'verify your identity'?", 20,
                                        "identity_theft")
unusual_payment.yes_node = request_personal_details

claim_exclusive_offer = QuestionNode("Did they claim you're receiving an exclusive offer or special treatment?", 20,
                                     "manipulation")
unusual_payment.no_node = claim_exclusive_offer

insist_immediate_action = QuestionNode("Did they insist that you take immediate action?", 20, "urgency_scam")
threaten_consequences.yes_node = insist_immediate_action

mention_legal_action = QuestionNode("Did they mention potential legal action or consequences?", 20, "manipulation")
threaten_consequences.no_node = mention_legal_action

# Tree for Job Scam scenario
job_scam_root = QuestionNode("Did you receive an unsolicited job offer or opportunity?", 10, "unsolicited_offer")

# Level 1 questions
too_good_to_be_true = QuestionNode("Does the job offer seem too good to be true? (e.g. high salary, low effort etc)",
                                   20, "unrealistic_offer")
job_scam_root.yes_node = too_good_to_be_true

vague_job_description = QuestionNode("Is the job description vague or unclear?", 10, "vague_details")
job_scam_root.no_node = vague_job_description

# Level 2 questions for 'too good to be true'
request_personal_info = QuestionNode(
    "Did they ask for personal information (e.g., SSN, bank details) before an interview?", 30, "identity_theft")
too_good_to_be_true.yes_node = request_personal_info

pressure_to_accept = QuestionNode("Are they pressuring you to accept the offer quickly?", 20, "urgency_scam")
too_good_to_be_true.no_node = pressure_to_accept

# Level 2 questions for 'vague job description'
upfront_payment = QuestionNode("Did they ask for any upfront payments or fees?", 30, "advance_fee_fraud")
vague_job_description.yes_node = upfront_payment

unprofessional_communication = QuestionNode("Is the communication unprofessional or filled with errors?", 10,
                                            "unprofessional_conduct")
vague_job_description.no_node = unprofessional_communication

# Level 3 questions
unusual_interview_process = QuestionNode("Is the interview process unusual (e.g., text-only, immediate job offer)?", 20,
                                         "suspicious_process")
request_personal_info.yes_node = unusual_interview_process

request_financial_info = QuestionNode("Did they ask for your bank account information for direct deposit?", 20,
                                      "financial_info_theft")
request_personal_info.no_node = request_financial_info

work_from_home = QuestionNode("Is it an unsolicited work-from-home opportunity?", 10, "remote_work_scam")
pressure_to_accept.yes_node = work_from_home

no_company_info = QuestionNode("Is there a lack of verifiable information about the company?", 20, "fake_company")
pressure_to_accept.no_node = no_company_info

request_money_transfer = QuestionNode("Did they ask you to transfer money or handle financial transactions?", 30,
                                      "money_laundering_scheme")
upfront_payment.yes_node = request_money_transfer

promise_easy_money = QuestionNode("Do they promise easy money or guaranteed income?", 20, "false_promises_job")
upfront_payment.no_node = promise_easy_money

# Level 4 questions
request_confidentiality = QuestionNode("Did they ask you to keep the job offer confidential?", 20, "secrecy")
unusual_interview_process.yes_node = request_confidentiality

use_personal_email = QuestionNode("Are they using a personal email instead of a company email?", 10,
                                  "lack_of_professionalism")
unusual_interview_process.no_node = use_personal_email

# Tree for Romance Scam scenario
romance_scam_root = QuestionNode("Did you meet this person online or through social media?", 10, "online_meeting")

# Level 1 questions
quick_romantic = QuestionNode("Did the person express strong feelings or propose a serious relationship very quickly?", 30, "rapid_romance")
romance_scam_root.yes_node = quick_romantic

in_person_meeting = QuestionNode("Does this person avoid attempts to meet face-to-face?", 20, "avoiding_meeting")
romance_scam_root.no_node = in_person_meeting

# Level 2 questions for 'quick romantic'
financial_help = QuestionNode("Has the person asked for any kind of financial assistance?", 30, "financial_romance")
quick_romantic.yes_node = financial_help

personal_info = QuestionNode("Have they asked for sensitive personal information?", 30, "identity_theft")
quick_romantic.no_node = personal_info

# Level 2 questions for 'in_person_meeting'
excuses_no_meeting = QuestionNode("Do they always have excuses for why they can't meet in person?", 30, "avoiding_meeting")
in_person_meeting.yes_node = excuses_no_meeting

webcam_refusal = QuestionNode("Do they refuse to video chat or always have excuses for why their camera doesn't work?", 20, "identity_concealment")
in_person_meeting.no_node = webcam_refusal

# Level 3 questions
urgent_money = QuestionNode("Have they claimed to have an urgent need for money (e.g., medical emergency, travel expenses)?", 30, "urgency_scam")
financial_help.yes_node = urgent_money

gift_cards = QuestionNode("Have they specifically asked for money via gift cards or wire transfers?", 30, "unusual_payment")
financial_help.no_node = gift_cards

social_media_limited = QuestionNode("Does their social media presence seem limited or recent?", 10, "fake_profile")
personal_info.yes_node = social_media_limited

inconsistent_info = QuestionNode("Have you noticed any inconsistencies in the information they've given about themselves?", 20, "false_information")
personal_info.no_node = inconsistent_info

# Level 4 questions
overseas_travel = QuestionNode("Have they mentioned plans to visit you but then canceled due to emergencies?", 20, "false_promises_romance")
excuses_no_meeting.yes_node = overseas_travel

professional_status = QuestionNode("Do they claim to have a high-status job (e.g., military, doctor, businessman abroad)?", 10, "status_claim")
excuses_no_meeting.no_node = professional_status

private_photos = QuestionNode("Have they asked you to send private or compromising photos?", 30, "blackmail")
webcam_refusal.yes_node = private_photos

separate_communication = QuestionNode("Do they insist on moving communication away from the dating site to email or text?", 10, "isolation_tactic")
webcam_refusal.no_node = separate_communication

# Recursive function to traverse the tree and calculate total weight
# Depth-first traversal algorithm on a binary tree structure
def traverse_tree(node, key_prefix=""):
    answers = {}
    current_node = node
    while current_node:
        unique_key = key_prefix + current_node.question
        response = st.radio(current_node.question, ["Yes", "No"], index=1, key=unique_key)
        answers[unique_key] = {"response": response, "node": current_node}

        if response == "Yes":
            current_node = current_node.yes_node
        else:
            current_node = current_node.no_node

    return answers

def calculate_score(answers):
    total_weight = 0
    scam_categories = set()
    for key, value in answers.items():
        if value["response"] == "Yes":
            total_weight += value["node"].weight
            scam_categories.add(value["node"].category)

    # Cap the total weight at 100 (which will be scaled to 50%)
    total_weight = min(total_weight, 100)
    
    # Scale the total_weight to be out of 50%
    scaled_weight = int((total_weight / 100) * 50)
    
    return scaled_weight, scam_categories

def run_questionnaire():
    st.subheader('Questionnaire')
    st.markdown("Select the scenario to begin identifying if the call is vishing:")

    scenario = st.selectbox("Select Scenario", ["Impersonation Scam", "Job Scam", "Romance Scam"])

    if scenario == "Impersonation Scam":
        answers = traverse_tree(impersonation_root, key_prefix="impersonation")
    elif scenario == "Job Scam":
        answers = traverse_tree(job_scam_root, key_prefix="job")
    elif scenario == "Romance Scam":
        answers = traverse_tree(romance_scam_root, key_prefix="romance")

    if st.button("Submit"):
        # Reset only the questionnaire risk value before processing new submission
        risk_manager.reset_risk('questionnaire')

        total_weight, scam_categories = calculate_score(answers)

        st.write("Likelihood of Vishing Scam (Questionnaire):")
        st.write(f"Score: {total_weight}% (out of 50%)")

        if total_weight > 0:
            # Risk categorization
            if total_weight >= 35:
                st.write(
                    "\nHigh risk of vishing. The call you received shows strong indicators of being a scam. We strongly advise you to terminate contact and report this to the relevant authorities.")
                questionnaire_risk = total_weight
            elif total_weight >= 20:
                st.write(
                    "\nModerate risk of vishing. The call you received shows some concerning signs. We recommend verifying any claims independently before taking any action.")
                questionnaire_risk = total_weight
            else:
                st.write(
                    "\nLow risk of vishing. While the risk seems low, always remain vigilant. If you have any doubts, verify the caller's identity through official channels.")
                questionnaire_risk = total_weight
            custom_message = get_custom_message(total_weight, scam_categories)
            st.write(custom_message)
        else:  # if user answered No to all questions
            st.write(
                "\nBased on your responses, no specific risk factors were identified. However, always remain vigilant and cautious when receiving unexpected calls or requests for personal information.")
            questionnaire_risk = 0

        # Update only the questionnaire risk
        risk_manager.update_risk(questionnaire_risk, source='questionnaire')



