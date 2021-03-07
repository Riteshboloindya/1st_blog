from django.db import models
from django.conf import settings

def get_upload_path(instance,filename):
    return '/'.join([settings.MEDIA_ROOT ,'images', str(instance.id),filename])
    # return settings.UPLOAD_ROOT + '/'.join(["pickups",str(instance.id),filename])

# Create your models here.
class Post (models.Model):
    title =models.CharField(max_length=150)
    desc=models.TextField()
    post_img = models.ImageField(default=None,null=True,blank=True,upload_to=get_upload_path) 