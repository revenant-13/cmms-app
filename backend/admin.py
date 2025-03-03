from django.contrib import admin
from .models import Vendor, Equipment, Part, Task, Schedule
from django.utils import timezone

@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')
    list_filter = ('is_active',)

@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'model', 'serial', 'location_status', 'manufacturer', 'is_active')
    list_filter = ('location_status', 'is_active', 'manufacturer')

@admin.register(Part)
class PartAdmin(admin.ModelAdmin):
    list_display = ('part_number', 'part_name', 'status', 'get_equipment', 'get_suppliers', 'is_active')
    list_filter = ('is_active', 'status')

    def get_equipment(self, obj):
        return ', '.join(equip.name for equip in obj.equipment.all()) if obj.equipment.exists() else 'None'
    get_equipment.short_description = 'Equipment'

    def get_suppliers(self, obj):
        return ', '.join(vendor.name for vendor in obj.suppliers.all()) if obj.suppliers.exists() else 'None'
    get_suppliers.short_description = 'Suppliers'

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('description', 'frequency', 'equipment', 'task_type', 'priority', 'assigned_to')
    list_filter = ('frequency', 'task_type', 'priority')

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('task', 'due_date', 'status', 'is_overdue')
    list_filter = ('status',)

    def save_model(self, request, obj, form, change):
        print(f"Saving schedule ID={obj.pk}, status={obj.status}, due_date={obj.due_date}, completion_date={obj.completion_date}")
        if obj.status == 'completed' and not obj.completion_date:
            print("Setting completion date and checking for next schedule...")
            obj.completion_date = timezone.now().date()
            next_due_date = obj.task.calculate_next_due_date(obj.due_date)
            print(f"Next due date: {next_due_date}")
            if next_due_date:
                print("Creating new schedule...")
                Schedule.objects.create(
                    task=obj.task,
                    due_date=next_due_date,
                    status='pending'
                )
            else:
                print("No next due date, skipping new schedule.")
        obj.save()