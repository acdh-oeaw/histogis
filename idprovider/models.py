from django.db import models

DATE_ACCURACY = (("Y", "Year"), ("YM", "Month"), ("DMY", "Day"))


class IdProvider(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
