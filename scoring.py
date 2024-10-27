def calculate_matching_score(extracted_skills, validated_answers, job_description_skills):
    print(validated_answers)
    # add validated answers to extracted skills
    extracted_skills += [skill for skill, validated in validated_answers.items() if validated == 1]

    # Calculate the matching score using the jaccard similarity
    job_skills = set(job_description_skills)
    resume_skills = set(extracted_skills)
    intersection = job_skills.intersection(resume_skills)
    union = job_skills.union(resume_skills)
    score = len(intersection) / len(union)
    score = round(score * 100, 0)

    return score
