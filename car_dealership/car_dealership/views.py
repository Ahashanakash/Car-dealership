from django.shortcuts import render
from cars.models import Brand, Car

def home(request, category_slug=None):
    data = Car.objects.all()
    brands = Brand.objects.all()

    if category_slug:
        data = Car.objects.filter(category=category_slug)
    else:
        data = Car.objects.filter(category='sedan')
    categories = Car.objects.values_list('category', flat=True).distinct()

    return render(request, 'home.html', {
        'data': data,
        'categories': categories,
        'brands':brands
    })