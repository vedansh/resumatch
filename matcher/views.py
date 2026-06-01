from django.shortcuts import render
from django.utils import timezone
from django.views import View
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .engine import analyze_match
from .models import MatchResult
from .tasks import run_match_analysis


class IndexView(View):
    def get(self, request):
        recent = MatchResult.objects.filter(status=MatchResult.STATUS_DONE)[:8]
        return render(request, "matcher/index.html", {"recent_matches": recent})


class MatchCreateView(APIView):
    def post(self, request):
        job_title = request.data.get("job_title", "").strip()
        job_description = request.data.get("job_description", "").strip()
        resume_text = request.data.get("resume_text", "").strip()
        async_mode = bool(request.data.get("async", False))

        if not job_description or not resume_text:
            return Response(
                {"error": "job_description and resume_text are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        result = MatchResult.objects.create(
            job_title=job_title,
            job_description=job_description,
            resume_text=resume_text,
        )

        if async_mode:
            run_match_analysis.delay(result.id)
            return Response(
                {"id": result.id, "status": "pending"},
                status=status.HTTP_202_ACCEPTED,
            )

        # Synchronous path — run inline and return immediately
        analysis = analyze_match(job_description, resume_text)
        result.score = analysis["score"]
        result.matched_skills = analysis["matched_skills"]
        result.missing_skills = analysis["missing_skills"]
        result.extra_skills = analysis["extra_skills"]
        result.summary = analysis["summary"]
        result.status = MatchResult.STATUS_DONE
        result.completed_at = timezone.now()
        result.save()

        return Response(_serialize(result), status=status.HTTP_201_CREATED)


class MatchDetailView(APIView):
    def get(self, request, pk):
        try:
            result = MatchResult.objects.get(pk=pk)
        except MatchResult.DoesNotExist:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(_serialize(result))


class MatchListView(APIView):
    def get(self, request):
        results = MatchResult.objects.all()[:20]
        return Response([_serialize_summary(r) for r in results])


def _serialize(result: MatchResult) -> dict:
    return {
        "id": result.id,
        "job_title": result.job_title,
        "status": result.status,
        "score": result.score,
        "matched_skills": result.matched_skills,
        "missing_skills": result.missing_skills,
        "extra_skills": result.extra_skills,
        "summary": result.summary,
        "created_at": result.created_at,
        "completed_at": result.completed_at,
    }


def _serialize_summary(result: MatchResult) -> dict:
    return {
        "id": result.id,
        "job_title": result.job_title or "Untitled",
        "status": result.status,
        "score": result.score,
        "summary": result.summary,
        "created_at": result.created_at,
    }
