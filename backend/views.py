from django.contrib.auth.models import User
from rest_framework import generics, permissions
from rest_framework.exceptions import ValidationError
from mptt.exceptions import InvalidMove
from .models import Vendor, Equipment, Part, Task, Schedule
from .serializers import (
    VendorSerializer, EquipmentSerializer, PartSerializer,
    TaskSerializer, ScheduleSerializer, UserSerializer
)

class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.DjangoModelPermissions]

class VendorListCreateView(generics.ListCreateAPIView):
    queryset = Vendor.objects.filter(is_active=True)
    serializer_class = VendorSerializer
    permission_classes = [permissions.DjangoModelPermissions]

class VendorDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    permission_classes = [permissions.DjangoModelPermissions]

class EquipmentListCreateView(generics.ListCreateAPIView):
    queryset = Equipment.objects.filter(parent__isnull=True)
    serializer_class = EquipmentSerializer
    permission_classes = [permissions.DjangoModelPermissions]

class EquipmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Equipment.objects.filter(is_active=True)
    serializer_class = EquipmentSerializer
    permission_classes = [permissions.DjangoModelPermissions]

    def update(self, request, *args, **kwargs):
        try:
            return super().update(request, *args, **kwargs)
        except InvalidMove:
            raise ValidationError({"detail": "Cannot set this equipment as a child of its own descendant."})

    def perform_update(self, serializer):
        instance = serializer.save()
        Equipment.objects.rebuild()  # Correctly rebuild the MPTT tree

class PartListCreateView(generics.ListCreateAPIView):
    queryset = Part.objects.filter(is_active=True)
    serializer_class = PartSerializer
    permission_classes = [permissions.DjangoModelPermissions]

class PartDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Part.objects.all()
    serializer_class = PartSerializer
    permission_classes = [permissions.DjangoModelPermissions]

class TaskListCreateView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.DjangoModelPermissions]

class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.DjangoModelPermissions]

class ScheduleListCreateView(generics.ListCreateAPIView):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
    permission_classes = [permissions.DjangoModelPermissions]

class ScheduleDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
    permission_classes = [permissions.DjangoModelPermissions]