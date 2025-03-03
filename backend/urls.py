from django.urls import path
from .views import (
    VendorListCreateView, VendorDetailView,
    EquipmentListCreateView, EquipmentDetailView,
    PartListCreateView, PartDetailView,
    TaskListCreateView, TaskDetailView,
    ScheduleListCreateView, ScheduleDetailView,
    UserListView
)

urlpatterns = [
    path('vendors/', VendorListCreateView.as_view(), name='vendor-list'),
    path('vendors/<int:pk>/', VendorDetailView.as_view(), name='vendor-detail'),
    path('equipment/', EquipmentListCreateView.as_view(), name='equipment-list'),
    path('equipment/<int:pk>/', EquipmentDetailView.as_view(), name='equipment-detail'),
    path('parts/', PartListCreateView.as_view(), name='part-list'),
    path('parts/<int:pk>/', PartDetailView.as_view(), name='part-detail'),
    path('tasks/', TaskListCreateView.as_view(), name='task-list'),
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
    path('schedules/', ScheduleListCreateView.as_view(), name='schedule-list'),
    path('schedules/<int:pk>/', ScheduleDetailView.as_view(), name='schedule-detail'),
    path('users/', UserListView.as_view(), name='user-list'),
]