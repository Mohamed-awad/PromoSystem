from rest_framework import generics
from rest_framework import serializers
from rest_framework import status
from rest_framework.response import Response

from promoApplication.models import Promo, User
from .serializers import PromoSerializer, PromoPointsSerializer, UserSerializer
from .permissions import IsAdmin, IsOwner


class UserCreateView(generics.CreateAPIView):
    """
    View to create User.
    * Only normal users are able to access this view.
    """
    lookup_field = 'pk'
    serializer_class = UserSerializer
    permission_classes = []


class PromoCreateView(generics.CreateAPIView):
    """
    View to create promo.
    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    lookup_field = 'pk'
    serializer_class = PromoSerializer
    permission_classes = [IsAdmin]

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}


class PromoRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
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

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response("promo code deleted successfully", status=status.HTTP_200_OK)

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}


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

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}


class PromoGetUsePointsView(generics.RetrieveUpdateAPIView):
    """
    View to get promo remaining points and user promo points.
    * Requires token authentication.
    """
    lookup_field = 'pk'
    serializer_class = PromoPointsSerializer
    permission_classes = [IsOwner]
    queryset = Promo.objects.all()

    def put(self, request, *args, **kwargs):
        pk = self.kwargs.get("pk")
        promo = Promo.objects.filter(pk=pk)[0]
        if request.data['deducted_points'] > promo.promo_amount:
            raise serializers.ValidationError("Error deducted points should be lower than or equal remaining points")
        request.data['promo_amount'] = promo.promo_amount - request.data['deducted_points']
        request.data.pop('deducted_points')
        return self.partial_update(request, *args, **kwargs)

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}
