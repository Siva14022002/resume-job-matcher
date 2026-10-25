
from sentence_transformers import SentenceTransformer, util

from app.services.skills import extract_skills


# Load the model once when this module is imported.
model = SentenceTransformer("all-MiniLM-L6-v2")


def match_skills(
    resume_text: str,
    job_description: str,
) -> dict:
    """Compare resume skills and semantic similarity."""

    resume_skills = set(extract_skills(resume_text))
    required_skills = set(extract_skills(job_description))

    matched_skills = sorted(resume_skills & required_skills)
    missing_skills = sorted(required_skills - resume_skills)

    if required_skills:
        skill_score = (
            len(matched_skills) / len(required_skills)
        ) * 100
    else:
        skill_score = 0.0

    resume_embedding = model.encode(
        resume_text,
        convert_to_tensor=True,
    )

    job_embedding = model.encode(
        job_description,
        convert_to_tensor=True,
    )

    similarity = util.cos_sim(
        resume_embedding,
        job_embedding,
    ).item()

    # Convert cosine similarity to a percentage from 0 to 100.
    semantic_score = max(0.0, min(1.0, similarity)) * 100

    final_score = (skill_score * 0.60) + (semantic_score * 0.40)

    return {
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "skill_match_score": round(skill_score, 2),
        "semantic_similarity_score": round(semantic_score, 2),
        "final_match_score": round(final_score, 2),
    }
