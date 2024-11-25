# Job Application Portal

An interactive web application built with Streamlit that streamlines the job application and hiring process. This application allows HR personnel to post job offers and manage applicants, while job seekers can apply to specific job offers by uploading their resumes. A matching score will be associated between resumes and job offers. The goal of this application is to provide a matching score between resumes and job offers enhanced using sentiment analysis.

The sentiment analysis is done using the [GPT2 model](https://paperswithcode.com/paper/language-models-are-unsupervised-multitask) trained on the [Stanford Sentiment Treebank](https://paperswithcode.com/dataset/sst).

## Installation and Setup

Follow these steps to set up and run the project locally.

### 1. Clone the Repository

First, clone this repository to your local machine:

```bash
git clone https://github.com/Rickil/JobApplicationPortal
cd JobApplicationPortal
```

### 2. Install the minGPT Package

```bash
pip install -e .
```

### 3. Install Other Required Packages

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### 4. Initialize the Database

Set up the initial database by running only the first time:

```bash
python initialize_database.py
```

### 5. Run the Application

Finally, start the Streamlit application:

```bash
streamlit run app.py
```

## Usage

Once the app is running, open your browser and go to `http://localhost:8501` to interact with the application.
