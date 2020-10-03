from django.urls import path
from .views import *

app_name = "promoApplication"

urlpatterns = [
    path('', PromoListView.as_view(), name='list-promo'),
    path('create', PromoCreateView.as_view(), name='create-promo'),
    path('<int:pk>/', PromoRetrieveUpdateDestroyView.as_view(), name='get-update-delete-promo'),
    path('<int:pk>/promo_points/', PromoGetUsePointsView.as_view(), name='get-use-promo-points'),
]
