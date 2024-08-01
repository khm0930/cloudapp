
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('upload/', views.upload_file, name='upload_file'),
    path('delete/<int:id>/', views.delete_file, name='delete_file'),
    path('', views.file_list, name='file_list'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),  # 로그인 URL 패턴 추가
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),  # 로그아웃 URL 패턴 추가
]
