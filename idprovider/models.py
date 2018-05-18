from django.db import models

DATE_ACCURACY = (
    ('Y', 'Year'),
    ('YM', 'Month'),
    ('DMY', 'Day')
)


class IdProvider(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    start_date = models.DateField(
        verbose_name="Start Date.",
        help_text="Earliest date this entity captures"
    )
    end_date = models.DateField(
        verbose_name="End Date.",
        help_text="Latest date this entity captures"
    )
    date_accuracy = models.CharField(
        default="Y", max_length=3, choices=DATE_ACCURACY
    )
