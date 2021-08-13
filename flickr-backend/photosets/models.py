from django.db import models
from django.utils import timezone
from accounts.models import Account


class sets(models.Model):
    owner = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='user_photoset')
    primary = models.PositiveIntegerField(max_length=30, blank=True)
    secret = models.PositiveIntegerField(max_length=15, blank=True)
    server = models.PositiveIntegerField(max_length=15, blank=True)
    farm = models.PositiveIntegerField(max_length=15, blank=True)
    photos = models.PositiveIntegerField(default=1)
    count_views = models.PositiveIntegerField(default=0)
    count_comments = models.PositiveIntegerField(default=0)
    count_videos = models.PositiveIntegerField(default=0)
    can_comment = models. BooleanField(default=True)
    date_create = models. DateTimeField(default=timezone.now)
    date_update = models. DateTimeField(default=timezone.now)
    visibility_can_see_set = models.PositiveIntegerField(default=1)
    title = models.CharField(max_length=15, unique=True)
    description = models. TextField(max_length=1000)
    
    def __str__(self):
        return self.title


class commentss(models.Model):
    owner = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='user_photoset_comments')
    contents = models.CharField(max_length=15)
    date_create = models. DateTimeField(default=timezone.now)
    sets = models.ForeignKey(sets, related_name='comment', 
                             on_delete=models.CASCADE)
    
    