import time

from celery import shared_task
from django.utils import timezone


@shared_task(bind=True, max_retries=3)
def run_match_analysis(self, result_id: int):
    from .engine import analyze_match
    from .models import MatchResult

    try:
        result = MatchResult.objects.get(id=result_id)
        # Simulate a slightly heavier analysis pass (e.g. expanded NLP in production)
        time.sleep(1)
        analysis = analyze_match(result.job_description, result.resume_text)
        result.score = analysis["score"]
        result.matched_skills = analysis["matched_skills"]
        result.missing_skills = analysis["missing_skills"]
        result.extra_skills = analysis["extra_skills"]
        result.summary = analysis["summary"]
        result.status = MatchResult.STATUS_DONE
        result.completed_at = timezone.now()
        result.save()
    except MatchResult.DoesNotExist:
        pass
    except Exception as exc:
        try:
            result.status = MatchResult.STATUS_FAILED
            result.summary = str(exc)
            result.save()
        except Exception:
            pass
        raise self.retry(exc=exc, countdown=5)
