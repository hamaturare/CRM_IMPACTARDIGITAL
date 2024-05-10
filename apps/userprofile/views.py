from django.shortcuts import render

# Create your views here.

def preview_template(request):
    return render(request, 'index.html')
