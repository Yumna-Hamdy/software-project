from django.db import models
from composite_field import base
from composite_field.base import CompositeField
from djongo import models
from djongo.models.fields import forms
from accounts.models import Account
# Create your models here.


class role_field(CompositeField):
    member = models.TextField(default="Member", blank=True)
    admin = models.TextField(default="Admin", blank=True)


class blast_field(CompositeField):
    content = models.TextField(blank=True)
    date_blast_added = models.TextField(blank=True)
    user_id = models.CharField(max_length=100, blank=True)


class throttle_field(CompositeField):
    count = models.IntegerField(blank=True, default=0)
    mode = models.TextField(blank=True)
    remaining = models.TextField(blank=True)


class restrictions_field(CompositeField):
    photos_ok = models.BooleanField(blank=True, default=True)
    videos_ok = models.BooleanField(blank=True, default=True)
    images_ok = models.BooleanField(blank=True, default=True)
    # screens_ok = models.BooleanField(blank=True, default=True)
    art_ok = models.BooleanField(blank=True, default=True)
    safe_ok = models.BooleanField(blank=True, default=True)
    # moderate_ok = models.BooleanField(blank=True, default=False)
    restricted_ok = models.BooleanField(blank=True, default=False)
    has_geo = models.BooleanField(blank=True, default=False)


PRIVACY_GROUP_CHOICES = [
    (1, 'private'),
    (2, 'invitation_only'),
    (3, 'public'),
]

'''
# class role_field(models.Model):
#     member = models.TextField(default="Member", blank=True)
#     admin = models.TextField(default="Admin", blank=True)

#     class Meta:
#         abstract = True


# class role_form(forms.ModelForm):

#     class Meta:
#         model = role_field
#         fields = ['member', 'admin']
'''


class group (models.Model):
    path_alias = models.TextField(blank=True)
    iconserver = models.IntegerField(blank=True, default=0)
    iconfarm = models.IntegerField(blank=True, default=0)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    rules = models.TextField(blank=True)
    members = models.IntegerField(default=1, blank=True)
    pool_count = models.IntegerField(default=0, blank=True)
    topic_count = models.IntegerField(default=0, blank=True)
    privacy = models.IntegerField(choices=PRIVACY_GROUP_CHOICES)
    lang = models.TextField(blank=True)
    #   ispoolmoderated = models.BooleanField(default=False)
    # roles = models.EmbeddedField(model_container=role_field,
    # model_form_class=role_form)
    # objects = models.DjongoManager()
    roles = role_field()
    limit_photo_opt_out = models.IntegerField(default=0, blank=True)
    datecreate = models.DateTimeField(auto_now_add=True, blank=True)
    dateactivity = models.IntegerField(default=0, blank=True)
    eighteenplus = models.BooleanField()
    invitation_only = models.BooleanField(default=False)
    is_member = models.BooleanField(blank=True, default=False)
    is_admin = models.BooleanField(blank=True, default=False)
    is_founder = models.BooleanField(blank=True, default=False)
    user_group_prefs = models.TextField(blank=True)
    blast = blast_field()
    throttle = throttle_field()
    restrictions = restrictions_field()

    def __str__(self):
        return self.name


class topic(models.Model):
    group = models.ForeignKey(group, related_name='group_topic',
                              on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    message = models.TextField()
    owner = models.ForeignKey(Account, on_delete=models.CASCADE,
                              related_name='topic_owner')
    role = models.CharField(max_length=100, blank=True)
    count_replies = models.IntegerField(default=0, blank=True)
    datecreate = models.DateTimeField(auto_now=True, blank=True)
    datelastpost = models.DateTimeField(blank=True)
    last_reply = models.DateTimeField(blank=True)
    lastedit = models.DateTimeField(auto_now_add=True, blank=True)
    
    # author_id = models.IntegerField(blank=True)   # dlwa2ty bas
    # authorname = models.CharField(max_length=100, blank=True)  # dlwa2ty bas
    # author_path_alias = models.TextField(blank=True)
    # author_is_deleted = models.BooleanField(blank=True, default=False)
    # is_pro = models.BooleanField(blank=True, default=False)
    # iconserver = models.IntegerField(blank=True, default=0)
    # iconfarm = models.IntegerField(blank=True, default=0)
    # can_edit = models.BooleanField(blank=True, default=False)
    # can_delete = models.BooleanField(blank=True, default=False)
    # can_reply = models.BooleanField(blank=True, default=False)
    # is_sticky = models.BooleanField(blank=True, default=False)
    # is_locked = models.BooleanField(blank=True, default=False)

    def __str__(self):
        return self.subject


class reply(models.Model):
    topic = models.ForeignKey(topic, related_name='group_topic_reply',
                              on_delete=models.CASCADE)
    message = models.TextField()
    owner = models.ForeignKey(Account, on_delete=models.CASCADE,
                              related_name='reply_owner')
    role = models.CharField(max_length=100, blank=True)
    datecreate = models.DateTimeField(auto_now=True, blank=True)
    lastedit = models.DateTimeField(auto_now_add=True, blank=True)
    
    # author_id = models.IntegerField(blank=True)  
    # authorname = models.CharField(max_length=100, blank=True)
    # author_path_alias = models.TextField(blank=True)
    # author_is_deleted = models.BooleanField(blank=True, default=False)
    # is_pro = models.BooleanField(blank=True, default=False)
    # iconserver = models.IntegerField(blank=True, default=0)
    # iconfarm = models.IntegerField(blank=True, default=0)
    # can_edit = models.BooleanField(blank=True, default=False)
    # can_delete = models.BooleanField(blank=True, default=False)

    def __str__(self):
        return self.message
