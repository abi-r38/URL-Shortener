# shortener/models.py
from django.db import models

class URL(models.Model):
    # This will be our primary key: a short, unique code (e.g., 'aB3xYz').
    short_code = models.CharField(max_length=8, primary_key=True)
    # The original, long URL that the user entered.
    long_url = models.URLField()
    # A timestamp automatically added when a new row is created.
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.short_code} -> {self.long_url[:50]}..."