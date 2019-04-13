from django.db import models
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.models import User
from django.utils.text import slugify
from model_utils.fields import StatusField
from model_utils import Choices
from django.urls import reverse
from taggit.managers import TaggableManager
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth import get_user_model
User = get_user_model()

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(blank=True,null=True,)
    class Meta:
          #enforcing that there can not be two
        verbose_name_plural = "categories"       #categories under a parent with same
                                                 #slug

    def __str__(self):                           # __str__ method elaborated later in
       return self.name



    def get_absolute_url(self):
        return reverse("category", args=[self.name])



class Article(models.Model):
    STATUS =Choices('DRAFTS','PUBLISHED',)
    title = models.CharField(max_length=100)
    slug = models.SlugField(blank=True,null=True,)
    body= RichTextUploadingField()
    category = models.ForeignKey('Category', null=True, blank=True,on_delete=models.CASCADE,)
    date =models.DateTimeField(auto_now_add= True,)
    thumb =models.ImageField(default='default.jpg', blank=True,null=True,)
    author=models.ForeignKey(User,models.SET_NULL,null=True,blank=True,)
    likes=models.ManyToManyField(User,blank=True,related_name='post_likes',)
    tags=TaggableManager()
    status=StatusField(default="DRAFTS")
    class Meta:
        ordering = ['-date']
    def __unicode__(self):
        return self.title
    def get_absolute_url(self):
        return reverse("articles:details", args=[self.slug])
    def total_likes(self):
        return self.likes.count()
    def __str__(self):
        return self.title


class Comment(models.Model):
    post=models.ForeignKey(Article,on_delete=models.CASCADE,null=True,)
    user=models.ForeignKey(User,models.SET_NULL,null=True,blank=True,)
    content=models.TextField()
    timestamp =models.DateTimeField(auto_now_add= True,)
    reply=models.ForeignKey('Comment',null=True ,on_delete=models.CASCADE,related_name="replies")

    def __str__(self):
        return '{}-{}' .format(self.post.title,str(self.user.username))

    class Meta:
        ordering = ['-id']
