
import re

SKILL_KEYWORDS = [
    "Python",
    "FastAPI",
    "Django",
    "Flask",
    "Java",
    "JavaScript",
    "TypeScript",
    "React",
    "React.js",
    "Node.js",
    "Express.js",
    "Spring Boot",
    "Spring MVC",
    "Hibernate",
    "JPA",
    "SQL",
    "PostgreSQL",
    "MySQL",
    "MongoDB",
    "Redis",
    "SQLAlchemy",
    "Sequelize",
    "Docker",
    "Git",
    "GitHub",
    "REST API",
    "RESTful API",
    "AWS",
    "Apache Kafka",
    "Kafka",
    "JWT",
    "OAuth2",
    "Microservices",
    "Machine Learning",
    "RAG",
    "OpenAI",
    "Claude",
    "Embeddings",
    "Tailwind CSS",
    "HTML5",
    "CSS3",
    "Redux",
    "CI/CD",
    "SOAP",
    "Postman",
    "Stripe",
    "Razorpay",
]


def extract_skills(text: str) -> list[str]:
    """Find known skills mentioned in resume text."""

    found_skills = []

    for skill in SKILL_KEYWORDS:
        pattern = r"(?<!\w)" + re.escape(skill) + r"(?!\w)"

        if re.search(pattern, text, re.IGNORECASE):
            found_skills.append(skill)

    return found_skills
