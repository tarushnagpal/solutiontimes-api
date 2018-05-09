from django.db import models

# Create your models here.
class FAQ(models.Model):
    pub_date = models.DateTimeField(auto_now_add=True, blank=True)

    question = models.CharField(max_length=200)
    answer = models.TextField()

    class Meta:
        ordering = ('pub_date',)
