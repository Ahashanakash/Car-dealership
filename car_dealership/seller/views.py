from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from cars.models import Car, CarVideo
from .forms import CarForm, CarVideoForm
from django.views.generic import TemplateView
# from .forms import PasswordResetForm
from django.contrib.auth.mixins import LoginRequiredMixin

from profiles.mixins import IsSellerMixin

# Create your views here.

class SellerDashBoardView(LoginRequiredMixin, IsSellerMixin, TemplateView):
    template_name = 'seller_dashboard.html'
    # def get(self, request, *args, **kwargs):
    #     return render(request, 'profiles/login.html')
    
    # # def post(self, request, *args, **kwargs):
        
@login_required
def add_car_htmx(request):
    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES)
        if form.is_valid():
            car = form.save(commit=False)
            car.seller = request.user
            car.save()
            return render(request, 'your-cars')
    else:
        form = CarForm()
    return render(request, 'partials/add_car_form.html', {'form': form})

# HTMX: Your Cars list
@login_required
def your_cars_htmx(request):
    cars = Car.objects.filter(seller=request.user)
    return render(request, 'partials/your_cars_list.html', {'cars': cars})

# HTMX: Update Car
@login_required
def update_car_htmx(request, pk):
    car = get_object_or_404(Car, pk=pk, seller=request.user)
    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES, instance=car)
        if form.is_valid():
            form.save()
            return render(request, 'partials/car_updated.html', {'car': car})
    else:
        form = CarForm(instance=car)
    return render(request, 'partials/add_car_form.html', {'form': form, 'car': car})

# HTMX: Delete Car
@login_required
def delete_car_htmx(request, pk):
    car = get_object_or_404(Car, pk=pk, seller=request.user)
    car.delete()
    return HttpResponse('')  # HTMX can remove the row

# HTMX: Add Video
@login_required
def add_video_htmx(request, pk):
    car = get_object_or_404(Car, pk=pk, seller=request.user)
    if request.method == 'POST':
        form = CarVideoForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save(commit=False)
            video.model = car
            video.save()
            return render(request, 'partials/video_added.html', {'video': video})
    else:
        form = CarVideoForm()
    return render(request, 'partials/add_video_form.html', {'form': form, 'car': car})