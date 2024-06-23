from ..models import UserRequests
from ..serializers import UserRequestsSerializer
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response


class UserRequestsViewSet(viewsets.ModelViewSet):
    """ViewSet для UserRequests используемой в индивидуальном тг боте"""

    queryset = UserRequests.objects.all()
    serializer_class = UserRequestsSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        """Получение последних 3х записей по created_at если в запросе присутствует user_id,
        либо получение 1 записи при наличии data_id"""
        user_id = self.request.query_params.get("user_id")
        data_id = self.request.query_params.get("data_id")
        selected_notification = self.request.query_params.get("selected_notification")
        if user_id:
            queryset = self.queryset.filter(user_id=user_id).order_by("-created_at")[:3]
        elif data_id:
            queryset = self.queryset.filter(id=data_id)
        elif selected_notification:
            queryset = self.queryset.filter(selected_notification=selected_notification)
        else:
            queryset = self.queryset
        return queryset

    def create(self, request, *args, **kwargs):
        """Создание новой записи их полученных данных от тг бота"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            UserRequests.objects.create(
                user_id=request.data.get("user_id"),
                direction=request.data.get("direction"),
                specialization=request.data.get("specialization", []),
                level=request.data.get("level", []),
                location=request.data.get("location", []),
                work_format=request.data.get("work_format", []),
                keywords=request.data.get("keywords", ""),
                selected_notification=request.data.get("selected_notification", []),
            )
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
