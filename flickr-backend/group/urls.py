from django.urls import path, include
from group import views
app_name = 'group'

urlpatterns = [
    path('<int:id>', views.group_info, name='group_info'),
    path('', views.group_create, name='group_create'),
    path('<int:group_id>/topic', views.topic, name='topic'),
    path('<int:group_id>/topic/<int:topic_id>', views.topic_info,
         name='topic_info'),
    path('<int:group_id>/topic/<int:topic_id>/reply', views.reply,
         name='reply'),
    path('<int:group_id>/topic/<int:topic_id>/reply/<int:reply_id>',
         views.reply_info, name='reply_info'),
]
