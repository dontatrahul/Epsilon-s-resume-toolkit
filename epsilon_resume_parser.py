import openai
import streamlit as st
from PyPDF2 import PdfReader




#creating a pdf reader object
def text_extracter( resume):
    reader = PdfReader(resume)

    no_of_pages = len(reader.pages)
    text = ""

    for i in range(no_of_pages):
        page = reader.pages[i]
        text = text + page.extract_text()
    return text



def json_object(text):
    prompt = "Given a resume text, generate a JSON object with the following details: name, email, phone number, education, skills, and experience. Ensure that the JSON object includes only these key fields with their corresponding values. Exclude any additional information.if particular feilds mentioned previously are missing kindly avoid adding the to the jason."
    openai.api_key = "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"
    chatOutput = openai.ChatCompletion.create(model="gpt-3.5-turbo-16k",
                                              messages=[{"role": "system",
                                                         "content": "You are a helpful assistant designed to output JSON"},
                                                        {"role": "user", "content": (prompt + text)}
                                                        ],
                                              temperature=0
                                              )
    reply = chatOutput.choices[0].message.content
    return reply

def interview_ques(data,no_of_ques,job_title):
    prompt = f'''Generate interview questions for a candidate applying for the job interview based on the given resume extract.
    Generate {no_of_ques} interview questions for a candidate applying for {job_title}.Mke sure that the questions are tailor made for the given resume. delve into his work experience and skillset keeping in mind the job title and its requirement. Produce questions that human like. Do not trail the generated questions with unwanted texts.
    '''
    
    chatOutput = openai.ChatCompletion.create(model="gpt-3.5-turbo-16k",
                                              messages=[{"role": "system",
                                                         "content": "You are an expert interviewer skilled at producing questions from a json object of a resume"},
                                                        {"role": "user", "content": (prompt + data)}
                                                        ],
                                              temperature=0
                                              )
    r= chatOutput.choices[0].message.content
    return r





st.set_page_config(initial_sidebar_state="expanded")
st.title("Epsilon's Resume Parser")

st.sidebar.markdown("Drag and drop a Resume.")
pdf_file = st.sidebar.file_uploader("Upload a PDF file", type=["pdf"])
job_title = st.sidebar.text_input("Enter Job Title", "Eg:ML Engineer")
no_of_ques= st.sidebar.text_input("Enter the number of questions", "Eg:5")


if st.sidebar.button("Upload"):
    data = text_extracter(pdf_file)
    json1 = json_object(data)
    st.subheader("Required Json Object: ")
    st.write(json1)

    questions=interview_ques(data,no_of_ques,job_title)
    st.subheader("Interview Questionnaire")
    st.write(questions)





