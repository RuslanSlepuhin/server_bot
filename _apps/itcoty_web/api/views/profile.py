from django.db.models import QuerySet
from rest_framework import mixins, permissions, viewsets

from api.models import User
from api.permissions import IsUserProfileOrReadOnly
from api.serializers import ProfileSerializer


class ProfileViewSet(
    mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet
):
    """
    A viewset that provides `retrieve`, `update` actions
    """

    permission_classes = [IsUserProfileOrReadOnly]
    serializer_class = ProfileSerializer
    http_method_names = ["get", "put"]

    def get_queryset(self) -> QuerySet[User]:
        return User.objects.all()
