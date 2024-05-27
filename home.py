import streamlit as st
import streamlit_survey as ss
from datetime import datetime

st.set_page_config(page_icon="🔬", page_title="TLC genAI Risk Assessment")

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

survey = ss.StreamlitSurvey()

if '__streamlit-survey-data_Risk Assessment_Pages__btn_submit' not in st.session_state:
    st.session_state['__streamlit-survey-data_Risk Assessment_Pages__btn_submit'] = False

st.title("🔬 TLC genAI Risk Assessment")
st.sidebar.title("🔬 TLC genAI Risk Assessment")
st.sidebar.info("""
                The **TLC genAI Risk Assessment** application is maintained by the TLC-FMG AI Team at the University of Amsterdam. Please reach out to [tlc-fmg@uva.nl](mailto:tlc-fmg@uva.nl) with feedback and/or questions.
                \n\n
                We do not save any identifiable information. Our code base is public [here](https://github.com/saurabh-khanna/tlc-ai-risk).
                """)

st.write("&nbsp;")

questions = {
    "q1": "Is the final course grade determined by unsupervised written assignments?",
    "q2": "What percentage of the final grade is determined by unsupervised assignments?",
    "q3": "Do the assignments allow you to monitor students' progression towards a learning objective?",
    "q4": "Do the assignments require course-specific knowledge or skills?",
    "q5": "Can Generative AI produce passing results for the assignments?",
    "q6": "Is there a clear policy on student use of Generative AI in the course?"
}

def calculate_score(responses):
    score_mapping = {
        "q1": {"Yes, entirely": 3, "Mostly": 2, "Partially": 1, "Not at all": 0},
        "q2": {"More than 75%": 3, "50% to 75%": 2, "25% to 50%": 1, "Less than 25%": 0},
        "q3": {"No, not at all": 3, "Rarely": 2, "Sometimes": 1, "Yes, always": 0},
        "q4": {"No, generic knowledge is sufficient": 3, "Somewhat": 2, "Mostly": 1, "Yes, completely": 0},
        "q5": {"Yes, very easily": 3, "Possibly, with effort": 2, "Unlikely": 1, "No, not possible": 0},
        "q6": {"No policy at all": 3, "Vague or informal policy": 2, "Clear but not applied": 1, "Clear and applied policy": 0}
    }
    total_score = sum(score_mapping[q][responses[q]['value']] for q in score_mapping if q in responses)
    return total_score

def get_feedback(responses):
    feedback = ""
    if responses["q1"]["value"] in ["Yes, entirely", "Mostly"]:
        feedback += "- Consider incorporating more supervised assessments or in-person exams to mitigate risks associated with unsupervised assignments.\n\n"
    if responses["q2"]["value"] in ["More than 75%", "50% to 75%"]:
        feedback += "- Diversify assessment methods to include a mix of supervised and unsupervised components.\n\n"
    if responses["q3"]["value"] in ["No, not at all", "Rarely"]:
        feedback += "- Implement regular checkpoints or progress submissions to monitor student progress more closely.\n\n"
    if responses["q4"]["value"] in ["No, generic knowledge is sufficient", "Somewhat"]:
        feedback += "- Design assignments that require specific knowledge or skills unique to the course, making it harder for AI to generate satisfactory responses.\n\n"
    if responses["q5"]["value"] in ["Yes, very easily", "Possibly, with effort"]:
        feedback += "- Revise assignments to include more analytical, critical thinking, or creative tasks that are less susceptible to AI generation.\n\n"
    if responses["q6"]["value"] in ["No policy at all", "Vague or informal policy"]:
        feedback += "- Establish a clear and applied policy on the use of generative AI in coursework to set expectations and consequences for misuse.\n\n"
    return feedback

with st.expander("TLC genAI Risk Assessment", expanded=True):
    st.write("&nbsp;")
    survey = ss.StreamlitSurvey("Risk Assessment")
    pages = survey.pages(10, on_submit=lambda: st.info("Thank you for your responses!"))
    with pages:
        if pages.current == 0:
            st.write("Hello! Do you wish to start the risk assessment?")
            consent = survey.radio(
                "consent", options=["Yes", "No"], index=0, label_visibility="collapsed", horizontal=True
            )
            if consent == "No":
                st.success("Thank you for your time! Please reach out to [tlc-fmg@uva.nl](mailto:tlc-fmg@uva.nl) if you have any questions.")
                st.stop()
        elif pages.current == 1:
            st.write("Which course are we discussing today?")
            survey.text_input("Which course are we discussing today?", id="course", label_visibility="collapsed")
        elif pages.current == 2:
            if st.session_state["__streamlit-survey-data_Risk Assessment"]["course"]["value"].strip().title() is not None and st.session_state["__streamlit-survey-data_Risk Assessment"]["course"]["value"].strip().title() != "":
                templabel = "How many students are enrolled in " + st.session_state["__streamlit-survey-data_Risk Assessment"]["course"]["value"].strip().title() +"?"
            else:
                templabel = "How many students are enrolled in this course?"
            st.write(templabel)
            survey.number_input(templabel, id="enrolled", value = None, min_value=0, label_visibility="collapsed")
        elif pages.current == 3:
            st.write(questions["q1"])
            survey.radio(questions["q1"], options=["Yes, entirely", "Mostly", "Partially", "Not at all"], label_visibility="collapsed", id="q1")
        elif pages.current == 4:
            st.write(questions["q2"])
            survey.radio(questions["q2"], options=["More than 75%", "50% to 75%", "25% to 50%", "Less than 25%"], label_visibility="collapsed", id="q2")
        elif pages.current == 5:
            st.write(questions["q3"])
            survey.radio(questions["q3"], options=["No, not at all", "Rarely", "Sometimes", "Yes, always"], label_visibility="collapsed", id="q3")
        elif pages.current == 6:
            st.write(questions["q4"])
            survey.radio(questions["q4"], options=["No, generic knowledge is sufficient", "Somewhat", "Mostly", "Yes, completely"], label_visibility="collapsed", id="q4")
        elif pages.current == 7:
            st.write(questions["q5"])
            survey.radio(questions["q5"], options=["Yes, very easily", "Possibly, with effort", "Unlikely", "No, not possible"], label_visibility="collapsed", id="q5")
        elif pages.current == 8:
            st.write(questions["q6"])
            survey.radio(questions["q6"], options=["No policy at all", "Vague or informal policy", "Clear but not applied", "Clear and applied policy"], label_visibility="collapsed", id="q6")
        elif pages.current == 9:
            st.write("Please provide any additional comments or suggestions on how to minimize unauthorized GenAI use in assessments.")
            survey.text_area("Please provide any additional comments or suggestions on how to minimize unauthorized GenAI use in assessments.", value="", label_visibility="collapsed", id="q7")

if st.session_state["__streamlit-survey-data_Risk Assessment_Pages__btn_submit"]:
    responses = survey.data
    total_score = calculate_score(responses)
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    response_text = f"### Your genAI Risk Assessment Report\n\n"
    response_text += f"**Generated at**: {timestamp}\n\n"
    response_text += f"**Course**: {st.session_state['__streamlit-survey-data_Risk Assessment']['course']['value'].strip().title()}\n\n"    
    
    for key, value in responses.items():
        if key in questions:
            response_text += f"**{questions[key]}**: {value['value']} (Risk Score: {calculate_score({key: value})}/3)\n\n"

    response_text += f"### Total Risk Score: {total_score}/18\n\n"
    
    # Interpretation of the total score
    if total_score >= 15:
        response_text += "**Interpretation: High vulnerability to unauthorized Generative AI use.**\n"
    elif 10 <= total_score < 15:
        response_text += "**Interpretation: Moderate vulnerability to unauthorized Generative AI use.**\n"
    elif 5 <= total_score < 10:
        response_text += "**Interpretation: Low vulnerability to unauthorized Generative AI use.**\n"
    else:
        response_text += "**Interpretation: Minimal vulnerability to unauthorized Generative AI use.**\n"
    
    # Scorecard interpretation
    response_text += """
    **Scorecard Interpretation**
    
    - 0-4: Minimal vulnerability to unauthorized Generative AI use.
    - 5-9: Low vulnerability to unauthorized Generative AI use.
    - 10-14: Moderate vulnerability to unauthorized Generative AI use.
    - 15-18: High vulnerability to unauthorized Generative AI use.
    """

    # Adding tailored feedback
    response_text += f"\n### Tailored Feedback\n\n{get_feedback(responses)}"

    st.info(response_text)
    st.download_button("Download your report", data=response_text, file_name="TLC_genAI_Risk_Assessment_Report.txt")
