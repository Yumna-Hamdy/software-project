from django.db import models
from accounts.models import *
from django_google_maps import fields as map_fields


# Can be removed until upload() is implemented
def media_upload(instance, file_name):
    media_name, extention = file_name.split(".")
    return "images_and_videos/%s.%s" % (instance.media_id, extention)


# Create your models here.
class Photo(models.Model):

    # Unique Identifier
    media_id = models.BigAutoField(primary_key=True)

    # Owner (relation)
    owner = models.ForeignKey(Account, on_delete=models.CASCADE,
                              related_name='user_photos')

    # Static URL Components
    secret = models.CharField(max_length=100, blank=True)
    original_secret = models.CharField(max_length=100, blank=True)
    server = models.PositiveSmallIntegerField(blank=True)
    farm = models.PositiveSmallIntegerField(blank=True)

    # Extention
    original_format = models.CharField(max_length=5, blank=True)

    # Meta Data
    title = models.CharField(max_length=300, blank=True)
    description = models.TextField(max_length=2000, blank=True)

    # Visibility & Privacy
    is_public = models.BooleanField(default=True)
    is_friend = models.BooleanField(default=False)
    is_family = models.BooleanField(default=False)

    # If photo is favourited by calling user
    is_favourite = models.BooleanField(default=False)

    # Permissions
    can_comment = models.PositiveSmallIntegerField(default=3)
    can_addmeta = models.PositiveSmallIntegerField(default=3)

    # Location
    #   address = map_fields.AddressField(max_length=200, blank=True)
    #   geolocation = map_fields.GeoLocationField(max_length=100, blank=True)

    # Dates
    date_posted = models.DateTimeField(blank=True)
    date_taken = models.DateTimeField(blank=True)
    last_update = models.DateTimeField(auto_now=True)

    # Stats
    views = models.PositiveIntegerField(default=0) #big
    comments = models.PositiveIntegerField(default=0) #big 
    favourites = models.PositiveIntegerField(default=0) #big

    # Tags & People Tagged Info
    count_tags = models.PositiveIntegerField(default=0)
    has_people = models.BooleanField(default=False)
    count_people_tagged = models.PositiveIntegerField(default=0)

    # People Tagged (relation)
    people_tagged = models.ManyToManyField(Account, through='Tagging',
                                           through_fields=('photo',
                                                           'person_tagged'),
                                           related_name="photos_tagged_in")

    # URLS
    #   photo_url = models.URLField(blank = True)
    #   thumb = models.URLField(blank = True)

    # Media
    MEDIA_TYPE = (
     ('Photo', 'Photo'),
     ('Video', 'Video'),
    )
    media = models.CharField(max_length=10, choices=MEDIA_TYPE)
    media_file = models.FileField(upload_to=media_upload)
    file_size = models.PositiveIntegerField(blank=True)

    # Photo Size
    photo_height = models.PositiveSmallIntegerField(blank=True)
    photo_width = models.PositiveSmallIntegerField(blank=True)
    photo_displaypx = models.PositiveSmallIntegerField()

    # Video Duration
    video_duration = models.PositiveSmallIntegerField()


class Tagging(models.Model):

    # Foreign Keys
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE)
    person_tagged = models.ForeignKey(Account, on_delete=models.CASCADE)

    # Added By
    added_by = models.ForeignKey(Account, on_delete=models.CASCADE,
                                 related_name="tagging_people_actions")

    # Tagged Person Relationship
    is_contact = models.BooleanField(default=False)
    is_friend = models.BooleanField(default=False)
    is_family = models.BooleanField(default=False)


class Comment(models.Model):

    # Unique Identifier
    comment_id = models.BigAutoField(primary_key=True)

    # Author (relation)
    author = models.ForeignKey(Account, on_delete=models.CASCADE,
                               related_name='user_comments')

    # Date
    date_created = models.DateTimeField(auto_now=True)

    # Body: required
    comment_text = models.TextField(max_length=1000)

    # URL
    #   link = models.URLField(blank=True)

    # Photo Data (relation)
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE,
                              related_name='photo_comments')


class Note(models.Model):

    # Unique Identifier
    note_id = models.BigAutoField(primary_key=True)

    # Author (relation)
    author = models.ForeignKey(Account, on_delete=models.CASCADE,
                               related_name='user_notes')

    # Dimensions: required
    left_coord = models.PositiveSmallIntegerField()
    top_coord = models.PositiveSmallIntegerField()
    note_width = models.PositiveSmallIntegerField()
    note_height = models.PositiveSmallIntegerField()

    # Body: required
    note_text = models.TextField(max_length=1000)

    # Photo Data (relation)
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE,
                              related_name='photo_notes')


class View(models.Model):

    # Unique Identifier
    view_id = models.BigAutoField(primary_key=True)

    # Photo Data (relation)
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE,
                              related_name='photo_views')

    # User (relation)
    user = models.ForeignKey(Account, on_delete=models.CASCADE,
                             related_name='user_views')

    # Date
    view_date = models.DateTimeField(auto_now_add=True)
