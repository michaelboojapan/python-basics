from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404

from .models import Product

from .forms import ProductForm, RawProductForm

from django.http import HttpResponse

# Create your views here.
def product_detail_view(request, *args, **kwargs):

    obj = Product.objects.get(id=1)
    context = {
        'object': obj
    }
    return render(request, 'products/product_detail.html', context)


def product_create_view(request, *args, **kwargs):
    form = ProductForm(request.POST or None)
    if form.is_valid():
        form.save()
        form = ProductForm()

    context = {
        'form': form
    }
    return render(request, 'products/product_create.html', context)

# def product_create_view(request, *args, **kwargs):
#     my_form = RawProductForm()
#     if request.method == 'POST':
#         my_form = RawProductForm(request.POST)
#         if my_form.is_valid():
#             print(my_form.cleaned_data)
#             Product.objects.create(**my_form.cleaned_data)
#
#     context = {
#         'form': my_form
#     }
#     return render(request, 'products/product_create.html', context)

# def product_create_view(request, *args, **kwargs):
#     print("#"*36)
#     if request.method == 'POST':
#         my_new_title = request.POST.get('title')
#         print(my_new_title)
#         # Product.objects.get(id=1)
#
#     context = {
#     }
#     return render(request, 'products/product_create.html', context)


def product_search_view(request, *args, **kwargs):
    context = {
    }
    return render(request, 'products/product_search.html', context)

def render_initial_data_view(request):
    initial_data = {
        'title': 'my this awesome title',
        'description': 'my owen description',

    }
    # my_form = RawProductForm(request.POST or None, initial=initial_data)
    obj = Product.objects.get(id=1)

    my_form = ProductForm(request.POST or None, initial=initial_data, instance=obj)
    if my_form.is_valid():
        print("it is valid")
        my_form.save()



    context = {
        'form': my_form
    }
    return render(request, 'products/product_create.html', context)


def render_lookup_view(request, my_id):

    # obj = get_object_or_404(Product, id=my_id)
    try:
        obj = Product.objects.get(id=my_id)
    except Product.DoesNotExist:
        raise Http404

    context = {
        'object': obj
    }
    return render(request, 'products/product_detail.html', context)


def product_delete_view(request, my_id):
    print(request.method)

    obj = get_object_or_404(Product, id=my_id)
    if request.method == 'POST':
        obj.delete()
        return redirect('../../')

    context = {
        'object': obj
    }
    return render(request, 'products/product_delete.html', context)


def product_list_view(request):
    queryset = Product.objects.all()
    context = {
        'object_list': queryset
    }
    return render(request, 'products/product_list.html', context)



