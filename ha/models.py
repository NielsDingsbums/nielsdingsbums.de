from django.db import models
from django.utils.timezone import now
from .choices import subjects


# Create your models here.
class haItem (models.Model):

	subject = models.CharField (choices=subjects, max_length=100)
	exercise = models.TextField ()
	exercise_url = models.URLField(blank=True)
	information = models.TextField (blank=True)
	date_created_at = models.DateField (default=now, blank=True)
	date_until = models.DateField ()
	author = models.CharField (max_length=3)

	def __str__(self):
		return self.exercise

	class Meta:
		verbose_name_plural = "Hausaufgaben Einträge"
		verbose_name = "Hausaufgaben Eintrag"
