from django.urls import path

from . import views

app_name = 'profiles'
urlpatterns = [
    path('', views.ProfileList.as_view(), name='profilelist'),
    path('<int:id>', views.ProfileDetailList.as_view(), name='profiledetail'),
]
