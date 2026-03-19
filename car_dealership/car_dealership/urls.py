from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('car/', include('cars.urls')),
    path('user/', include('profiles.urls')),
    path('seller/', include('seller.urls', namespace='seller')),
    path('customer/', include('customer.urls')),
    path("reviews/", include('reviews.urls')),
    path('shops/', include('shops.urls')),
    path('category/<slug:category_slug>/', home, name='category_wise_car'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)