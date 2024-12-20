from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import UserProfile

@login_required
def user_profile(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    return render(request, 'users/profile.html', {'profile': user_profile})

