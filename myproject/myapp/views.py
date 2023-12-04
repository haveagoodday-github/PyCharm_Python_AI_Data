from django.shortcuts import render
from .models import pageforimage
# Create your views here.

def home_view(request):
    new_pageforimage = pageforimage(title="中国")
    return render(request, 'index.html')