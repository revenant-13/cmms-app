from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Vendor, Equipment, Part, Task, Schedule

# Custom RecursiveField for self-referential serializers
class RecursiveField(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ['id', 'name', 'contact_info', 'address', 'is_active']

class EquipmentSerializer(serializers.ModelSerializer):
    vendor = VendorSerializer(read_only=True)
    parent = serializers.PrimaryKeyRelatedField(
        queryset=Equipment.objects.all(),
        allow_null=True,
        required=False
    )
    parent_details = RecursiveField(read_only=True)
    manufacturer = serializers.PrimaryKeyRelatedField(
        queryset=Vendor.objects.all(),
        allow_null=True,
        required=False
    )
    manufacturer_details = VendorSerializer(source='manufacturer', read_only=True)
    children = serializers.SerializerMethodField()
    parts = serializers.SerializerMethodField()

    class Meta:
        model = Equipment
        fields = [
            'id', 'name', 'model', 'serial', 'description', 'parent', 'parent_details',
            'location_status', 'expected_return_date', 'vendor', 'manufacturer',
            'manufacturer_details', 'is_active', 'children', 'parts'
        ]

    def get_children(self, obj):
        children = obj.get_children()
        return EquipmentSerializer(children, many=True).data

    def get_parts(self, obj):
        parts = obj.parts.all()
        from .serializers import PartSerializer
        return PartSerializer(parts, many=True).data

class PartSerializer(serializers.ModelSerializer):
    equipment = serializers.PrimaryKeyRelatedField(
        queryset=Equipment.objects.all(),
        many=True,
        allow_null=True,
        required=False
    )
    # Removed equipment_details to break recursion; use IDs instead
    suppliers = serializers.PrimaryKeyRelatedField(
        queryset=Vendor.objects.all(),
        many=True,
        allow_null=True,
        required=False
    )
    supplier_details = VendorSerializer(source='suppliers', many=True, read_only=True)

    class Meta:
        model = Part
        fields = [
            'id', 'part_number', 'part_name', 'description', 'status', 'last_updated',
            'equipment', 'suppliers', 'supplier_details', 'is_active'
        ]

class TaskSerializer(serializers.ModelSerializer):
    equipment = serializers.PrimaryKeyRelatedField(queryset=Equipment.objects.all())
    assigned_to = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        allow_null=True,
        required=False
    )

    class Meta:
        model = Task
        fields = [
            'id', 'description', 'frequency', 'equipment',
            'start_date', 'task_type', 'priority', 'assigned_to'
        ]

class ScheduleSerializer(serializers.ModelSerializer):
    task = TaskSerializer(read_only=True)
    is_overdue = serializers.ReadOnlyField()

    class Meta:
        model = Schedule
        fields = [
            'id', 'task', 'due_date', 'completion_date',
            'status', 'history_log', 'is_overdue'
        ]