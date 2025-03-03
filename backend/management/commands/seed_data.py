from django.core.management.base import BaseCommand
from django.utils import timezone
from cmms.models import Vendor, Equipment, Part, Task, Schedule
import random
from faker import Faker

fake = Faker()

class Command(BaseCommand):
    help = 'Seeds the database with sample data'

    def handle(self, *args, **kwargs):
        # Clear existing data
        Schedule.objects.all().delete()
        Task.objects.all().delete()
        Part.objects.all().delete()
        Equipment.objects.all().delete()
        Vendor.objects.all().delete()

        # Seed Vendors (10)
        vendors = []
        for _ in range(10):
            vendor = Vendor(
                name=fake.company(),
                contact_info=fake.email(),
                address=fake.address(),
                is_active=True
            )
            vendor.save()
            vendors.append(vendor)
        self.stdout.write(self.style.SUCCESS('Created 10 Vendors'))

        # Seed Equipment (10, with nesting)
        equipment_list = []
        # 5 top-level equipment
        for i in range(5):
            equip = Equipment(
                name=f"Equipment {i+1}",
                model=f"Model-X{i+1}",
                serial=f"SN{i+1:03d}",
                description=fake.sentence(),
                location_status=random.choice(['in-house', 'off-site']),
                manufacturer=random.choice(vendors),
                is_active=True
            )
            equip.save()
            equipment_list.append(equip)

        # 5 nested equipment (children of top-level)
        for i in range(5):
            parent = random.choice(equipment_list[:5])  # Pick from top-level
            child = Equipment(
                name=f"Sub-Equipment {i+1}",
                model=f"Model-Y{i+1}",
                serial=f"SN{i+6:03d}",
                description=fake.sentence(),
                parent=parent,
                location_status=random.choice(['in-house', 'off-site']),
                manufacturer=random.choice(vendors),
                is_active=True
            )
            child.save()
            equipment_list.append(child)
        self.stdout.write(self.style.SUCCESS('Created 10 Equipment (5 top-level, 5 nested)'))

        # Seed Parts (10, connected to equipment)
        parts = []
        for i in range(10):
            part = Part(
                part_number=f"P{i+1:03d}",
                part_name=f"Part {i+1}",
                description=fake.sentence(),
                status=random.choice(['available', 'in-stock', 'on-order']),
                last_updated=timezone.now(),
                is_active=True,
                vendor=random.choice(vendors)
            )
            part.save()
            # Connect to 1-3 random equipment (fixed syntax)
            connected_equipment = random.sample(equipment_list, k=random.randint(1, 3))
            part.equipment.set(connected_equipment)
            parts.append(part)
        self.stdout.write(self.style.SUCCESS('Created 10 Parts with Equipment connections'))

        # Seed Tasks (10, tied to equipment)
        tasks = []
        for i in range(10):
            task = Task(
                description=f"Task {i+1}: {fake.sentence(nb_words=5)}",
                frequency=random.choice(['daily', 'weekly', 'monthly', 'yearly', None]),
                equipment=random.choice(equipment_list),
                start_date=timezone.now().date(),
                task_type=random.choice(['maintenance', 'calibration']),
                priority=random.choice(['low', 'medium', 'high'])
            )
            task.save()
            tasks.append(task)
        self.stdout.write(self.style.SUCCESS('Created 10 Tasks'))

        # Seed Schedules (10, linked to tasks)
        for i, task in enumerate(tasks):
            Schedule.objects.create(
                task=task,
                due_date=timezone.now().date() + timezone.timedelta(days=random.randint(1, 30)),
                status='pending',
                history_log=f"Schedule {i+1} created"
            )
        self.stdout.write(self.style.SUCCESS('Created 10 Schedules'))

        self.stdout.write(self.style.SUCCESS('Database seeded successfully with 10 of each!'))