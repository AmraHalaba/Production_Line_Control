from django.shortcuts import render
from .models import *

def testview(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    
    context = {'user' : profile}
    return render(request, 'profiles/test.html', context)


