from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home_view(request, *args, **kwargs):
    print(request.user)
    # return HttpResponse('<h1>Hello World!</h1>')
    return render(request, 'home.html', {})

def contact_view(request, *args, **kwargs):
    return render(request, 'contact.html', {})

def about_view(request, *args, **kwargs):
    about_context = {
        'my_text': 'this is about us',
        'my_number': 23,
        'my_list': [123, 45, 667, 'Abc'],

    }
    return render(request, 'product_detail.html', about_context)

def social_view(request, *args, **kwargs):
    return render(request, 'product_detail.html', {})
