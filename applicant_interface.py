# applicant_interface.py

import streamlit as st
import os
import uuid
from pydparser import ResumeParser
from sentiment_analysis import sentiment_analysis_model
from scoring import calculate_matching_score
import sqlite3
import json

def applicant_interface():
    st.title("Job Application Portal")

    # Connect to the database
    conn = sqlite3.connect('data/database.db')
    c = conn.cursor()

    # Fetch available job offers
    c.execute('''SELECT job_id, title FROM job_offers''')
    job_offers = c.fetchall()

    if job_offers:
        # Let applicant select a job offer
        job_options = {job_id: title for job_id, title in job_offers}
        selected_job_id = st.selectbox("Select a job offer to apply for", options=list(job_options.keys()), format_func=lambda x: job_options[x])

        if selected_job_id:
            # Retrieve the job description skills for the selected job offer
            c.execute('''SELECT required_skills FROM job_offers WHERE job_id = ?''', (selected_job_id,))
            job_offer = c.fetchone()
            job_description_skills = json.loads(job_offer[0])  # Assuming required_skills is stored as JSON

            # Resume upload
            uploaded_file = st.file_uploader("Upload your resume (PDF)", type="pdf")

            if uploaded_file is not None:
                # Generate a unique ID for the applicant
                applicant_id = str(uuid.uuid4())
                resume_path = f"data/resumes/{applicant_id}.pdf"
                os.makedirs(os.path.dirname(resume_path), exist_ok=True)

                # Save the uploaded resume
                with open(resume_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())

                # Extract text and skills from the resume
                extracted_skills = ResumeParser(resume_path).get_extracted_data()['skills']

                # Compare skills to find missing ones
                missing_skills = list(set(job_description_skills) - set(extracted_skills))

                # Generate questions for missing skills, store in session_state
                if 'questions' not in st.session_state:
                    import random
                    num_questions = min(3, len(missing_skills))
                    st.session_state['questions'] = random.sample(missing_skills, k=num_questions)
                    st.session_state['answers'] = {}  # Initialize answers dict

                st.write("Please answer the following questions:")

                # Display questions and collect answers
                for idx, skill in enumerate(st.session_state['questions']):
                    answer = st.text_area(
                        f"Do you have experience with {skill}? Please elaborate.",
                        key=f"answer_{idx}"
                    )
                    st.session_state['answers'][skill] = answer

                if st.button("Submit Application"):
                    # Validate answers using sentiment analysis
                    validated_answers = {}
                    for skill, answer in st.session_state['answers'].items():
                        validation = sentiment_analysis_model(answer)
                        validated_answers[skill] = validation

                    # Calculate the matching score
                    matching_score = calculate_matching_score(extracted_skills, validated_answers, job_description_skills)

                    # Save applicant data to the database
                    applicant_data = {
                        'applicant_id': applicant_id,
                        'job_id': selected_job_id,
                        'extracted_skills': extracted_skills,
                        'answers': st.session_state['answers'],
                        'validated_answers': validated_answers,
                        'matching_score': matching_score
                    }

                    c.execute('''INSERT INTO applicants (applicant_id, job_id, data) VALUES (?, ?, ?)''',
                              (applicant_id, selected_job_id, json.dumps(applicant_data)))
                    conn.commit()

                    # Clear session state
                    del st.session_state['questions']
                    del st.session_state['answers']

                    st.success("Your application has been submitted!")
        else:
            st.warning("No job offer selected.")
    else:
        st.write("No job offers available at the moment.")

    conn.close()