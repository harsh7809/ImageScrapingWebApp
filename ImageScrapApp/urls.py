from django.urls import path 
from . import views



urlpatterns = [
    path('',views.scrape_images_dow, name='scrape_images_dow')
    
]