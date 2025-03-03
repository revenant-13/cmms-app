from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.utils import timezone
from dateutil.relativedelta import relativedelta  # For monthly/yearly increments
from django.contrib.auth.models import User

# Choices for various fields
PRIORITY_CHOICES = [
    ('low', 'Low'),
    ('medium', 'Medium'),
    ('high', 'High'),
]

FREQUENCY_CHOICES = [
    ('daily', 'Daily'),
    ('weekly', 'Weekly'),
    ('monthly', 'Monthly'),
    ('yearly', 'Yearly'),
]

TASK_TYPE_CHOICES = [
    ('maintenance', 'Maintenance'),
    ('calibration', 'Calibration'),
]

EQUIPMENT_LOCATION_STATUS = [  # Simplified: Removed 'on-site'
    ('in-house', 'In-House'),
    ('off-site', 'Off-Site'),
]

SCHEDULE_STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('completed', 'Completed'),
]

class Vendor(models.Model):
    name = models.CharField(max_length=255)
    contact_info = models.TextField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Equipment(MPTTModel):
    name = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    serial = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)  # New optional field
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )
    location_status = models.CharField(
        max_length=50,
        choices=EQUIPMENT_LOCATION_STATUS,
        default='in-house'
    )
    expected_return_date = models.DateField(null=True, blank=True)
    vendor = models.ForeignKey(
        Vendor,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='equipment_serviced'
    )
    manufacturer = models.ForeignKey(  # New field, renamed from 'vendor' for clarity
        Vendor,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='equipment_manufactured'
    )
    is_active = models.BooleanField(default=True)

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return self.name

class Part(models.Model):
    part_number = models.CharField(max_length=255)
    part_name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=50)
    last_updated = models.DateTimeField(auto_now=True)
    equipment = models.ManyToManyField(
        Equipment,
        blank=True,  # Allow no equipment
        related_name='parts'
    )
    suppliers = models.ManyToManyField(  # New multi-select field
        Vendor,
        blank=True,
        related_name='supplied_parts'
    )
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.part_name
    
    vendor = models.ForeignKey(
        Vendor,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='parts'
    )
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.part_number

class Task(models.Model):
    description = models.TextField()
    frequency = models.CharField(
        max_length=50,
        choices=FREQUENCY_CHOICES,
        blank=True,
        null=True  # Allow one-time tasks
    )
    equipment = models.ForeignKey(
        Equipment,
        on_delete=models.CASCADE,
        related_name='tasks'
    )
    start_date = models.DateField()
    task_type = models.CharField(
        max_length=50,
        choices=TASK_TYPE_CHOICES
    )
    priority = models.CharField(
        max_length=50,
        choices=PRIORITY_CHOICES,
        default='medium'
    )
    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='tasks'
    )

    def __str__(self):
        return f"{self.task_type}: {self.description[:50]}"

    def calculate_next_due_date(self, last_date):
        """Calculate the next due date based on frequency."""
        if not self.frequency:  # One-time task, no next date
            return None
        if self.frequency == 'daily':
            return last_date + relativedelta(days=1)
        elif self.frequency == 'weekly':
            return last_date + relativedelta(weeks=1)
        elif self.frequency == 'monthly':
            return last_date + relativedelta(months=1)
        elif self.frequency == 'yearly':
            return last_date + relativedelta(years=1)
        return last_date  # Fallback

class Schedule(models.Model):
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name='schedules'
    )
    due_date = models.DateField()
    completion_date = models.DateField(null=True, blank=True)
    status = models.CharField(
        max_length=50,
        choices=SCHEDULE_STATUS_CHOICES,
        default='pending'
    )
    history_log = models.TextField(blank=True)

    def __str__(self):
        return f"Schedule for {self.task} due on {self.due_date}"

    @property
    def is_overdue(self):
        if self.status == 'pending' and self.due_date < timezone.now().date():
            return True
        return False

    def save(self, *args, **kwargs):
        """Override save to auto-generate next schedule on completion."""
        if self.pk and self.status == 'completed' and not self.completion_date:
            # If completing a schedule, set completion date and create next one
            self.completion_date = timezone.now().date()
            next_due_date = self.task.calculate_next_due_date(self.due_date)
            if next_due_date:
                Schedule.objects.create(
                    task=self.task,
                    due_date=next_due_date,
                    status='pending'
                )
        super().save(*args, **kwargs)