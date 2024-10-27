import streamlit as st
from applicant_interface import applicant_interface
from hr_interface import hr_interface
import os

def main():
    #create directories for storing resumes and job offers
    if not os.path.exists("data"):
        os.makedirs("data")
    if not os.path.exists("data/resumes"):
        os.makedirs("data/resumes")
    if not os.path.exists("data/job_offers"):
        os.makedirs("data/job_offers")
        
    st.set_page_config(page_title="Job Application Portal", layout="wide")
    st.sidebar.title("Navigation")
    app_mode = st.sidebar.selectbox("Choose the mode", ["Applicant", "HR"])

    if app_mode == "Applicant":
        applicant_interface()
    elif app_mode == "HR":
        hr_interface()

if __name__ == "__main__":
    main()
