from django.urls import path
from Home import views

urlpatterns = [
    path('',views.index, name='home'),
    path('about/',views.about, name='about'),
]