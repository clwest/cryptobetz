from django.db import models


class Coindesk(models.Model):
    category = models.CharField(max_length=100, null=True)
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    date = models.DateTimeField(null=True)
    content = models.TextField()
    sentiment = models.CharField(max_length=15, blank=True, null=True)

    class Meta:
        unique_together = ('title', 'author', 'date')
        ordering = ['category']