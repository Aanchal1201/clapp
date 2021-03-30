from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.utils.html import mark_safe

# Create your models here.
class UserPost(models.Model):
    authorUsername = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    label = models.CharField(max_length=200,default="no Label") #not use now
    category = models.CharField(max_length=200)
    image = models.ImageField(upload_to='images/userPost/')
    slug = models.CharField(max_length=255)
    dateUpdate = models.DateTimeField(auto_now=True,blank=True, null=True)
    timeStamp = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    timeRead = models.CharField(max_length=10)
    content = RichTextField(blank=True)
    userStatus = models.CharField(max_length=50)
    adminStatus = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def image_tag(self):
        if self.image:
            return mark_safe('<img src="/media/%s" width="80" height="50" />'% (self.image))
    image_tag.short_description = 'Blogimage'