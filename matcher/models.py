from django.db import models


class MatchResult(models.Model):
    STATUS_PENDING = "pending"
    STATUS_DONE = "done"
    STATUS_FAILED = "failed"
    STATUS_CHOICES = [
        (STATUS_PENDING, "Pending"),
        (STATUS_DONE, "Done"),
        (STATUS_FAILED, "Failed"),
    ]

    job_title = models.CharField(max_length=200, blank=True)
    job_description = models.TextField()
    resume_text = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)

    score = models.FloatField(null=True, blank=True)
    matched_skills = models.JSONField(default=list)
    missing_skills = models.JSONField(default=list)
    extra_skills = models.JSONField(default=list)
    summary = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        title = self.job_title or "Untitled"
        score = f"{self.score:.0f}%" if self.score is not None else "pending"
        return f"Match #{self.id} — {title} ({score})"
