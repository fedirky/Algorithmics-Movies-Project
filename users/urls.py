from django.urls import path
from django.contrib.auth.views import LoginView
from .views import user_profile, recommended_movies_render 


urlpatterns = [
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('profile/', user_profile, name='user_profile'),
    path('recommendations/', recommended_movies_render, name='recommendations'),
]
