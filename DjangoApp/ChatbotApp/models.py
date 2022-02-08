from django.db import models

# Create your models here.

class corona_xray(models.Model):
    corona_id=models.AutoField(primary_key=True)
    image = models.ImageField()
    def __str__(self):
        return f"{self.corona_id}"
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
        	url = ''
        return url