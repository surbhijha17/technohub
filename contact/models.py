from django.db import models
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.models import User




class Contact(models.Model):
    name=models.CharField(max_length=50)
    email=models.EmailField()
    content=models.TextField()


    class Meta:
        verbose_name_plural='contacts'

    def __str__(self):
        return self.content
