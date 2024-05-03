from django.db import models


class ScrapedImage(models.Model):
    image = models.FileField(upload_to='scraped_images/')