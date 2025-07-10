from django.db import models

class Hero(models.Model):
    title = models.CharField(max_length=150, blank=True, null=True, default="Hero title")
    video_url = models.URLField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Hero'
        verbose_name_plural = 'Heroes'
        ordering = ['title']


class Script(models.Model):
    product_title = models.CharField(max_length=150)
    product_category = models.CharField(max_length=100)
    key_benifits = models.CharField(max_length=150)
    target_audience = models.CharField(max_length=150)
    scripts_ton = models.CharField(max_length=100)
    script_title = models.CharField(max_length=150, blank=True, null=True)
    script = models.TextField(blank=True, null=True)
    rating = models.FloatField(default=0.0)

    def __str__(self):
        return self.script_title

    class Meta:
        verbose_name = 'Script'
        verbose_name_plural = 'Scripts'
        ordering = ['script_title']
