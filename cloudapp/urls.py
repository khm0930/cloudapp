from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_file, name='upload_file'),
    path('delete/<int:id>/', views.delete_file, name='delete_file'),
    path('', views.file_list, name='file_list'),
   path('signup/', views.signup, name='signup'),  # signup URL 패턴 추가
]
