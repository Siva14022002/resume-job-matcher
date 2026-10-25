
import os
import tempfile

from fastapi import FastAPI, File, HTTPException, UploadFile
from pydantic import BaseModel

from app.services.matcher import match_skills
from app.services.parser import extract_text_from_pdf
from app.services.skills import extract_skills


app = FastAPI(
    title="Resume Job Matcher",
    description="AI-powered resume and job matching API",
    version="1.0.0",
)


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "message": "Resume Job Matcher API is running!"
    }


@app.post("/parse")
def parse_resume(file: UploadFile = File(...)):
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Please upload a PDF resume."
        )

    temp_path = None

    try:
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".pdf"
        ) as temp_file:
            temp_path = temp_file.name

            while chunk := file.file.read(1024 * 1024):
                temp_file.write(chunk)

        extracted_text = extract_text_from_pdf(temp_path)

        if not extracted_text:
            raise HTTPException(
                status_code=422,
                detail="No text found. The PDF may be scanned or empty."
            )

        skills = extract_skills(extracted_text)

        return {
            "filename": file.filename,
            "text": extracted_text,
            "characters": len(extracted_text),
            "skills": skills,
            "skills_count": len(skills)
        }

    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Unable to read this PDF. Please upload a valid PDF."
        )
    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)
        file.file.close()




class JobMatchRequest(BaseModel):
    resume_text: str
    job_description: str


@app.post("/match")
def match_resume_to_job(request: JobMatchRequest):
    return match_skills(
        request.resume_text,
        request.job_description,
    )
