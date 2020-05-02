from django.urls import path
from . import views
urlpatterns = [
    path('test/<int:text>/<keyword>/', views.home, name='home'),
    path('about/',views.about, name='about')
]