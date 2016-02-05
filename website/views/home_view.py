from django.shortcuts import render


def home(request):
    """
    Homepage
    """
    # render page
    return render(request, 'home.html')
