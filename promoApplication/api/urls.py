from django.urls import path
from .views import *

app_name = "promoApplication"

urlpatterns = [
    path('', PromoListView.as_view(), name='list-promo'),
    path('', PromoCreateView.as_view(), name='create-promo'),
]
