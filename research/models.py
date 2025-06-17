from django.db import models

class ResearchResult(models.Model):
    keyword = models.CharField(max_length=255)
    scope = models.TextField(null=True, blank=True)
    design = models.TextField(null=True, blank=True)
    literature = models.TextField(null=True, blank=True)
    analysis = models.TextField(null=True, blank=True)
    discussion = models.TextField(null=True, blank=True)
    ethics = models.TextField(null=True, blank=True)
    references = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.keyword
