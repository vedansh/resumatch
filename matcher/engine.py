"""
Resume matching engine.

Approach:
  1. Skill taxonomy (~100 skills across 7 categories) is searched in both texts.
  2. JD skills not in resume → missing; JD skills in resume → matched.
  3. Base score = matched / required * 100, capped bonuses for extra skills.
  4. Keyword overlap fills the gap when the JD has no named skills.
  5. Experience-years mention earns a small bonus.
"""

import re
from collections import defaultdict

SKILL_TAXONOMY: dict[str, list[str]] = {
    "languages": [
        "python", "javascript", "typescript", "java", "golang", "go", "ruby",
        "rust", "c++", "c#", "php", "swift", "kotlin", "scala", "r", "sql",
        "bash", "shell", "elixir", "haskell",
    ],
    "frameworks": [
        "django", "fastapi", "flask", "rails", "spring", "laravel", "express",
        "react", "vue", "angular", "next.js", "nextjs", "svelte", "nuxt",
        "celery", "graphql", "grpc", "fastify", "gin", "echo",
    ],
    "cloud": [
        "aws", "gcp", "azure", "ec2", "s3", "rds", "lambda", "ecs", "eks",
        "cloudfront", "cloud run", "bigquery", "amplify", "sqs", "sns",
        "cloudwatch", "iam", "vpc",
    ],
    "devops": [
        "docker", "kubernetes", "k8s", "terraform", "ansible", "github actions",
        "gitlab ci", "ci/cd", "nginx", "linux", "git", "helm", "prometheus",
        "grafana", "datadog", "sentry",
    ],
    "databases": [
        "postgresql", "postgres", "mysql", "sqlite", "mongodb", "redis",
        "elasticsearch", "dynamodb", "cassandra", "neo4j", "cockroachdb",
        "kafka", "rabbitmq", "airflow",
    ],
    "practices": [
        "tdd", "bdd", "agile", "scrum", "kanban", "rest api", "microservices",
        "system design", "code review", "pair programming", "devops",
        "sre", "observability", "api design", "data modeling",
    ],
    "soft_skills": [
        "leadership", "communication", "mentoring", "cross-functional",
        "problem solving", "collaboration", "stakeholder management",
        "technical writing", "project management",
    ],
}

# flat map: skill → category
_ALL_SKILLS: dict[str, str] = {
    skill: category
    for category, skills in SKILL_TAXONOMY.items()
    for skill in skills
}

# category display weights (technical skills matter more for scoring)
_CATEGORY_WEIGHT: dict[str, float] = {
    "languages": 1.2,
    "frameworks": 1.2,
    "cloud": 1.1,
    "devops": 1.0,
    "databases": 1.0,
    "practices": 0.9,
    "soft_skills": 0.7,
}

_STOPWORDS = {
    "a", "an", "the", "and", "or", "but", "in", "on", "at", "to", "for",
    "of", "with", "by", "from", "as", "is", "was", "are", "were", "be",
    "been", "has", "have", "had", "do", "does", "did", "will", "would",
    "could", "should", "may", "might", "can", "that", "this", "these",
    "those", "we", "you", "our", "your", "their", "its", "it", "not",
    "no", "any", "all", "both", "each", "few", "more", "most", "other",
    "such", "own", "same", "so", "than", "too", "very", "just", "over",
    "under", "about", "up", "out", "into", "through", "during", "before",
    "after", "above", "below", "between", "must", "also", "if", "while",
    "new", "strong", "good", "work", "working", "experience", "ability",
    "skills", "knowledge", "including", "looking", "required", "preferred",
    "responsibilities", "qualifications", "minimum", "role", "team",
    "position", "candidate", "years", "year", "plus",
}


def _find_skills(text: str) -> dict[str, str]:
    text_lower = text.lower()
    found: dict[str, str] = {}
    for skill, category in _ALL_SKILLS.items():
        pattern = r"(?<![a-z])" + re.escape(skill) + r"(?![a-z])"
        if re.search(pattern, text_lower):
            found[skill] = category
    return found


def _extract_keywords(text: str, top_n: int = 40) -> set[str]:
    words = re.findall(r"\b[a-z][a-z0-9\-\.]{2,}\b", text.lower())
    freq: dict[str, int] = defaultdict(int)
    for w in words:
        if w not in _STOPWORDS and len(w) > 2:
            freq[w] += 1
    sorted_words = sorted(freq, key=lambda w: freq[w], reverse=True)
    return set(sorted_words[:top_n])


def _years_experience_bonus(resume_text: str) -> float:
    """Return a small bonus (0–5) if the resume shows senior experience."""
    matches = re.findall(r"(\d+)\+?\s*years?", resume_text.lower())
    if not matches:
        return 0.0
    max_years = max(int(m) for m in matches)
    if max_years >= 8:
        return 5.0
    elif max_years >= 5:
        return 3.0
    elif max_years >= 3:
        return 1.5
    return 0.0


def analyze_match(job_description: str, resume_text: str) -> dict:
    jd_skills = _find_skills(job_description)
    resume_skills = _find_skills(resume_text)

    matched = {s: c for s, c in jd_skills.items() if s in resume_skills}
    missing = {s: c for s, c in jd_skills.items() if s not in resume_skills}
    extra = {s: c for s, c in resume_skills.items() if s not in jd_skills}

    if jd_skills:
        # Weighted score: matched skills weighted by category importance
        matched_weight = sum(_CATEGORY_WEIGHT.get(c, 1.0) for c in matched.values())
        total_weight = sum(_CATEGORY_WEIGHT.get(c, 1.0) for c in jd_skills.values())
        base_score = (matched_weight / total_weight) * 100
    else:
        # Fallback: keyword overlap
        jd_kw = _extract_keywords(job_description)
        resume_kw = _extract_keywords(resume_text)
        overlap = jd_kw & resume_kw
        base_score = (len(overlap) / max(len(jd_kw), 1)) * 85

    extra_bonus = min(len(extra) * 1.5, 8.0)
    exp_bonus = _years_experience_bonus(resume_text)
    score = min(base_score + extra_bonus + exp_bonus, 100.0)

    # Group by category for the response
    def by_category(skill_dict: dict[str, str]) -> list[dict]:
        grouped: dict[str, list[str]] = defaultdict(list)
        for skill, cat in skill_dict.items():
            grouped[cat].append(skill)
        return [
            {"category": cat, "skills": sorted(skills)}
            for cat, skills in sorted(grouped.items())
        ]

    if score >= 80:
        verdict, color = "Strong match", "green"
    elif score >= 60:
        verdict, color = "Good match", "blue"
    elif score >= 40:
        verdict, color = "Partial match", "yellow"
    else:
        verdict, color = "Weak match", "red"

    summary_parts = [f"{verdict} — {score:.0f}% compatibility."]
    if matched:
        summary_parts.append(
            f"Covers {len(matched)} of {len(jd_skills)} required skills."
        )
    if missing:
        top_gaps = list(missing.keys())[:4]
        summary_parts.append(f"Key gaps: {', '.join(top_gaps)}.")
    if extra:
        summary_parts.append(
            f"Resume brings {len(extra)} additional skills not listed in the JD."
        )

    return {
        "score": round(score, 1),
        "verdict": verdict,
        "color": color,
        "matched_skills": by_category(matched),
        "missing_skills": by_category(missing),
        "extra_skills": by_category(extra),
        "summary": " ".join(summary_parts),
        "stats": {
            "jd_skills_total": len(jd_skills),
            "matched": len(matched),
            "missing": len(missing),
            "extra": len(extra),
        },
    }
