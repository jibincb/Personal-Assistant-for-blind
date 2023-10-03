from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('start/', views.start, name='start'),
    # path('stop/', views.stop, name='stop'),
    path('faceregn/',views.faceregn,name='faceregn'),
    path('upload/', views.image_upload, name='image_upload'),
]
