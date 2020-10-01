from rest_framework import generics
from rest_framework import serializers

from promoApplication.models import Promo, User
from .serializers import PromoSerializer, PromoPointsSerializer
from .permissions import IsAdmin


class PromoCreateView(generics.CreateAPIView):
    """
    View to create promo.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    lookup_field = 'pk'
    serializer_class = PromoSerializer
    permission_classes = [IsAdmin]


class PromoUpdateView(generics.RetrieveUpdateDestroyAPIView):
    """
    View to get, update, delete promo.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    lookup_field = 'pk'
    serializer_class = PromoSerializer
    permission_classes = [IsAdmin]

    queryset = Promo.objects.all()

    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


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


class PromoGetUsePointsView(generics.RetrieveUpdateAPIView):
    """
    View to get promo remaining points and user promo points.

    * Requires token authentication.
    """
    lookup_field = 'pk'
    serializer_class = PromoPointsSerializer
    queryset = Promo.objects.all()

    def get_object(self):
        pk = self.kwargs.get("pk")
        return Promo.objects.filter(pk=pk)[0]

    def put(self, request, *args, **kwargs):
        pk = self.kwargs.get("pk")
        promo = Promo.objects.filter(pk=pk)[0]
        if request.data['deducted_points'] > promo.promo_amount:
            raise serializers.ValidationError("Error deducted points should be lower than or equal remaining points")
        request.data['promo_amount'] = promo.promo_amount - request.data['deducted_points']
        request.data.pop('deducted_points')
        print(request.data)
        return self.partial_update(request, *args, **kwargs)
