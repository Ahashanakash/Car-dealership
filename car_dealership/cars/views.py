from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Car, CarVideo
from reviews.models import Review
from django.core.paginator import Paginator
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from .models import Car
from .cart import Cart

# Create your views here.

class CarList(ListView):
    model = Car
    ordering = ['id']
    paginate_by = 1
    # paginate_orphans = 1
    context_object_name = "cars"
    
    #handles invalid page number search
    def get_context_data(self, **kwargs):
        try:
            return super(CarList, self).get_context_data(**kwargs)
        except Http404:
            self.kwargs['page']=1
            return super(CarList,self).get_context_data(**kwargs)
    
    
class CarDetails(DetailView):
    model = Car
    context_object_name = "car"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["reviews"] = Review.objects.filter(car=self.get_object())
        
        # --- Added: Include video if exists ---
        try:
            context["car_video"] = self.get_object().carvideo.video
        except CarVideo.DoesNotExist:
            context["car_video"] = None
        
        return context
    
    

@login_required
def toggle_like(request, pk):
    car = get_object_or_404(Car, pk=pk)

    if request.user in car.likes.all():
        car.likes.remove(request.user)
    else:
        car.likes.add(request.user)

    html = render_to_string(
        "partials/like_section.html",
        {"car": car, "user": request.user},
        request=request
    )

    return HttpResponse(html)


def add_to_cart(request, pk):
    cart = Cart(request)
    car = get_object_or_404(Car, pk=pk)

    cart.add(car)

    return render(request, "partials/cart_badge.html", {
        "cart_count": cart.count()
    })


def cart_page(request):

    cart = Cart(request)

    return render(request, "cart.html", {
        "cart": cart.cart,
        "total": cart.total()
    })


def cart_page(request):

    cart = Cart(request)

    return render(request, "cart.html", {
        "cart": cart.cart,
        "total": cart.total(),
        "cart_count": cart.count()
    })


def update_quantity(request, pk, action):

    cart = Cart(request)
    car = get_object_or_404(Car, pk=pk)

    item = cart.cart[str(pk)]
    qty = item['quantity']

    if action == "inc":
        qty += 1
    elif action == "dec" and qty > 1:
        qty -= 1

    cart.update(car, qty)

    return render(request, "partials/cart_container.html", {
        "cart": cart.cart,
        "total": cart.total(),
        "cart_count": cart.count()
    })
    
    
def remove_item(request, pk):

    cart = Cart(request)
    car = get_object_or_404(Car, pk=pk)

    cart.remove(car)

    return render(request, "partials/cart_container.html", {
        "cart": cart.cart,
        "total": cart.total(),
        "cart_count": cart.count()
    })