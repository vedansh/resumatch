from django.test import TestCase
from django.urls import reverse

from .engine import analyze_match
from .models import MatchResult


class EngineTest(TestCase):
    def test_strong_match(self):
        jd = "We need a Python Django developer with PostgreSQL and AWS experience."
        resume = "I am a Python developer with 5 years experience in Django and PostgreSQL. I have deployed to AWS EC2 and S3."
        result = analyze_match(jd, resume)
        self.assertGreaterEqual(result["score"], 70)
        self.assertIn("matched_skills", result)
        self.assertIn("missing_skills", result)

    def test_weak_match(self):
        jd = "Looking for a Java Spring developer with Kubernetes and GCP."
        resume = "I am a Python developer with Django and PostgreSQL."
        result = analyze_match(jd, resume)
        self.assertLess(result["score"], 50)

    def test_empty_skills_fallback(self):
        jd = "We want a motivated team player who loves building products."
        resume = "I am a creative problem solver who loves collaborating on teams."
        result = analyze_match(jd, resume)
        self.assertIsInstance(result["score"], float)


class APITest(TestCase):
    def test_health(self):
        res = self.client.get("/health")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()["status"], "ok")

    def test_match_create_sync(self):
        payload = {
            "job_title": "Backend Engineer",
            "job_description": "Python Django PostgreSQL Redis AWS Docker",
            "resume_text": "I work with Python, Django, and PostgreSQL daily. I use Docker and AWS.",
        }
        res = self.client.post(
            "/api/match/",
            data=payload,
            content_type="application/json",
        )
        self.assertEqual(res.status_code, 201)
        data = res.json()
        self.assertEqual(data["status"], "done")
        self.assertIsNotNone(data["score"])
        self.assertGreater(data["score"], 0)

    def test_match_create_validation(self):
        res = self.client.post(
            "/api/match/",
            data={"job_description": "some JD"},
            content_type="application/json",
        )
        self.assertEqual(res.status_code, 400)

    def test_match_detail(self):
        m = MatchResult.objects.create(
            job_title="Test",
            job_description="python django",
            resume_text="python developer",
            status=MatchResult.STATUS_DONE,
            score=75.0,
            matched_skills=[],
            missing_skills=[],
        )
        res = self.client.get(f"/api/match/{m.id}/")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()["id"], m.id)

    def test_match_list(self):
        res = self.client.get("/api/matches/")
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.json(), list)

    def test_index(self):
        res = self.client.get("/")
        self.assertEqual(res.status_code, 200)
