from django.db import models
from accounts.models import Account
# Create your models here.


class Profile(models.Model):
    owner = models.OneToOneField(Account, on_delete=models.CASCADE)
    Occupation = models.CharField(max_length=50, blank=True)
    Hometown = models.CharField(max_length=50, blank=True)
    Current_City = models.CharField(max_length=50, blank=True)
    Country = models.CharField(max_length=50, blank=True)
    website = models.URLField(blank=True, null=True)
    facebook = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)
    pintrest = models.URLField(blank=True, null=True)
    tumblr = models.URLField(blank=True, null=True)
    total_views = models.IntegerField(default=0)
    fav_count = models.IntegerField(default=0)
    group_count = models.IntegerField(default=0)
    tag_count = models.IntegerField(default=0)
    galleries_count = models.IntegerField(default=0)
    #photoset count

    def __str__(self):
        return self.owner.email
