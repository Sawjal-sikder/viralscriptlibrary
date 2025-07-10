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


class Package(models.Model):
    title = models.CharField(max_length=150)
    discount_price_per_month = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    regular_price_per_month = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    discount_price_per_year = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    regular_price_per_year = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    have_access_scripts_per_month = models.BooleanField(default=True)
    access_scripts_per_month = models.IntegerField(default=0)
    full_scripts_library_access = models.BooleanField(default=True)
    downloadable_template = models.BooleanField(default=False)
    ai_screept_generator = models.BooleanField(default=False)
    

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Package'
        verbose_name_plural = 'Packages'
        ordering = ['title']