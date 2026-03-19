from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import BrandViewSet, CarViewSet, CarVideoViewSet
# from django.views.generic import TemplateView
from .views import *

router = DefaultRouter()

router.register('brands', BrandViewSet)
router.register('cars', CarViewSet)
router.register('videos', CarVideoViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('', CarList.as_view(), name='cars'),
    path('details/<int:pk>/', CarDetails.as_view(), name='car_details'),
    path('car/<int:pk>/like/', toggle_like, name='toggle_like'),
    path('add-to-cart/<int:pk>/', add_to_cart, name="add_to_cart"),
    path('cart/', cart_page, name="cart"),
    path('cart/qty/<int:pk>/<str:action>/', update_quantity, name="cart_qty"),
    path('cart/remove/<int:pk>/', remove_item, name="remove_item"),
]
