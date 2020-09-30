from rest_framework import generics

from promoApplication.models import Promo, User
from .serializers import PromoSerializer
from .permissions import IsAdmin


class PromoCreateView(generics.CreateAPIView):
    lookup_field = 'pk'
    serializer_class = PromoSerializer
    permission_classes = [IsAdmin]


class PromoUpdateView(generics.UpdateAPIView):
    lookup_field = 'pk'
    serializer_class = PromoSerializer
    permission_classes = [IsAdmin]


class PromoDeleteView(generics.DestroyAPIView):
    lookup_field = 'pk'
    serializer_class = PromoSerializer
    permission_classes = [IsAdmin]


class PromoListView(generics.ListAPIView):
    lookup_field = 'pk'
    serializer_class = PromoSerializer

    def get_queryset(self):
        current_user = User.objects.get(username=self.request.user)
        if current_user.is_admin:
            qs = Promo.objects.all()
            return qs
        else:
            qs = Promo.objects.filter(user=self.request.user)
            return qs


class PromoGetPointsView(generics.RetrieveAPIView):
    pass


class PromoUsePointsView(generics.UpdateAPIView):
    pass
