from django.shortcuts import render

from catalog.models import Product


def home(request):
    products = Product.objects.all()
    context = {
        'object_list': products
    }
    return render(request, 'home_page/home.html', context)


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        with open('catalog/data/users.txt', 'a') as file:
            file.write(f"Имя:{name}, телефон:{phone}, контактный телефон:{message}\n")
    return render(request, 'contact_page/contact.html')


def product(request, product_id):
    product = Product.objects.get(pk=product_id)
    context = {
        'object': product
    }
    return render(request, 'product_page/product.html', context)
