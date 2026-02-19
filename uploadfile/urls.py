from django.urls import path
from . import views

app_name = 'uploadfile'

urlpatterns = [
    path('', views.home, name='home'),
    path('upload/', views.upload_page, name='upload_page'),
    path('api/save/', views.Savefile, name='save_file'),
    path('download/', views.download_page, name='download_page'),
    path('api/files/', views.Showlines, name='show_lines'),
    path('file/download/<int:pk>/', views.Downloadfile, name='download_file'),
    path('file/delete/<int:pk>/', views.Deletefile, name='delete_file'),
]
