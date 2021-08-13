from django.urls import path, include
from . import views
from . import api
app_name = 'photosets'
urlpatterns = [
    
    
    path('<int:id>', views.set_list),
    #   apis
    path('list', api.set_lists, name='set_lists'),
    path('list/<int:id>', api.get_lists, name='get_lists'),
    path('create', api.create_set, name='create_lists'),
    path('delete/<int:id>', api.delete_set, name='delete_lists'),
    path('edit/<int:id>', api.edit_meta, name='edit_meta'),
    path('<int:id>/createcomment', api.create_comment,
         name='create_comment'),
    path('deletecomment/<int:id>', api.delete_comment,
         name='delete_comment'),
    path('editcomment/<int:id>', api.edit_comment, name='edit_comment'),
    path('<int:id>/getcomment', api.get_comments_list, name='get_comment')
]