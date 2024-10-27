import streamlit as st
import sqlite3
import json
import os
import uuid
from pydparser import JdParser

def hr_interface():
    st.title("HR Dashboard")
    st.sidebar.title("HR Actions")
    action = st.sidebar.selectbox("Select an action", ["Post Job Offer", "View Applicants"])

    if action == "Post Job Offer":
        st.header("Post a New Job Offer")

        job_title = st.text_input("Job Title")
        job_description_file = st.file_uploader("Upload Job Description (PDF)", type="pdf")

        if st.button("Submit Job Offer"):
            if job_title and job_description_file:
                # Generate a unique ID for the job offer
                job_id = str(uuid.uuid4())
                job_description_path = f"data/job_offers/{job_id}.pdf"
                os.makedirs(os.path.dirname(job_description_path), exist_ok=True)

                # Save the uploaded job description
                with open(job_description_path, "wb") as f:
                    f.write(job_description_file.getbuffer())

                # Extract required skills from the job description
                required_skills = JdParser(job_description_path).get_extracted_data()['skills']

                # Save job offer to the database
                job_offer_data = {
                    'job_id': job_id,
                    'title': job_title,
                    'required_skills': json.dumps(required_skills)
                }

                # Connect to the database
                conn = sqlite3.connect('data/database.db')
                c = conn.cursor()

                c.execute('''INSERT INTO job_offers (job_id, title, required_skills) VALUES (?, ?, ?)''',
                            (job_id, job_title, job_offer_data['required_skills']))
                conn.commit()
                conn.close()

                st.success("Job offer posted successfully!")
            else:
                st.error("Please provide a job title and upload a job description.")
    elif action == "View Applicants":
        st.header("View Applicants for Job Offers")

        # Connect to the database
        conn = sqlite3.connect('data/database.db')
        c = conn.cursor()

        # Fetch job offers
        c.execute('''SELECT job_id, title FROM job_offers''')
        job_offers = c.fetchall()

        if job_offers:
            job_options = {job_id: title for job_id, title in job_offers}
            selected_job_id = st.selectbox("Select a job offer", options=list(job_options.keys()), format_func=lambda x: job_options[x])

            if selected_job_id:
                # Fetch applicants for the selected job offer
                c.execute('''SELECT applicant_id, data FROM applicants WHERE job_id = ?''', (selected_job_id,))
                applicants = c.fetchall()

                if applicants:
                    applicant_list = []
                    for applicant_id, data_json in applicants:
                        data = json.loads(data_json)
                        applicant_list.append({
                            'Applicant ID': applicant_id,
                            'Matching Score': data['matching_score'],
                            'Extracted Skills': data['extracted_skills'],
                            'Answers': data['answers'],
                            'Validated Answers': data['validated_answers']
                        })

                    selected_applicant_id = st.selectbox("Select an applicant", [a['Applicant ID'] for a in applicant_list])
                    applicant_data = next(a for a in applicant_list if a['Applicant ID'] == selected_applicant_id)

                    st.write(f"**Applicant ID:** {applicant_data['Applicant ID']}")
                    st.write(f"**Matching Score:** {applicant_data['Matching Score']}%")

                    st.write("**Extracted Skills from Resume:**")
                    st.write(", ".join(applicant_data['Extracted Skills']))

                    # Improved Section Name and Presentation
                    st.write("**Applicant's Additional Information on Missing Skills:**")
                    for skill, answer in applicant_data['Answers'].items():
                        validated = applicant_data['Validated Answers'][skill]
                        if validated == 1:
                            validation_text = "Validated: Yes"
                            validation_color = "green"
                        else:
                            validation_text = "Validated: No"
                            validation_color = "red"

                        st.markdown(f"""
                        <div style='border: 1px solid #ccc; padding: 10px; margin-bottom: 10px;'>
                            <p><strong>Skill:</strong> {skill}</p>
                            <p><strong>Answer:</strong> {answer}</p>
                            <p><strong style='color: {validation_color};'>{validation_text}</strong></p>
                        </div>
                        """, unsafe_allow_html=True)

                    # Optionally, provide a link to download the resume
                    resume_path = f"data/resumes/{applicant_data['Applicant ID']}.pdf"
                    try:
                        with open(resume_path, "rb") as f:
                            st.download_button(
                                label="Download Resume",
                                data=f,
                                file_name=f"{applicant_data['Applicant ID']}.pdf",
                                mime="application/pdf"
                            )
                    except FileNotFoundError:
                        st.error("Resume file not found.")
                else:
                    st.write("No applicants have applied for this job offer yet.")
            else:
                st.warning("No job offer selected.")
        else:
            st.write("No job offers found.")

        conn.close()
