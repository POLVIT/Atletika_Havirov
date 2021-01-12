from django.db import models
from ckeditor.fields import RichTextField
# Create your models here.

class PrispevekProMediatora(models.Model):
    text    = models.TextField(blank=True, null=True)



class PrispevekFiles(models.Model):
    def path(instance, filename):
        return f'prispevky/preispevek{instance.prispevek_id}/{filename}'

    prispevek   = models.ForeignKey(PrispevekProMediatora, on_delete=models.CASCADE)
    file = models.FileField(upload_to=path, default='default.txt' )


class createPost(models.Model):
    fb_post         = models.BooleanField(default=False)
    fb_time         = models.DateTimeField(blank=True,null=True, default=None)
    ig_post         = models.BooleanField(default=False)
    ig_time         = models.DateTimeField(blank=True,null=True, default=None)
    web_post        = models.BooleanField(default=False)
    web_post_succes = models.BooleanField(default=False)
    titulek         = models.CharField(max_length=255, blank=True, null=True)
    text            = RichTextField(blank=True, null=True)
    foto_urls       = models.TextField(blank=True, null=True)



