```markdown
# Job Application Portal

An interactive web application built with Streamlit that streamlines the job application and hiring process. This application allows HR personnel to post job offers and manage applicants, while job seekers can apply to specific job offers by uploading their resumes. A matching score will be associated betwwen resumes and job offers. The goal of this application is to provide a matching score between resumes and job offers enhanced using sentiment analysis.

## Installation and Setup

Follow these steps to set up and run the project locally.

### 1. Clone the Repository

First, clone this repository to your local machine:

```bash
git clone https://github.com/Rickil/hrflow
cd hrflow
```

### 2. Install the minGPT Package

```bash
pip install -e .
```

### 3. Install Other Required Packages

```bash
pip install -r requirements.txt
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