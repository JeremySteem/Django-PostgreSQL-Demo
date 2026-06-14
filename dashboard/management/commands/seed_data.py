from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from dashboard.models import Asset, Task


class Command(BaseCommand):
    help = 'Seed the database with sample Assets and Tasks'

    def handle(self, *args, **options):
        admin_user = User.objects.filter(is_superuser=True).first()
        if not admin_user:
            self.stdout.write(self.style.ERROR('No superuser found. Create one first.'))
            return

        assets = [
            ('Forklift #1', 'active', 'Warehouse A', 'Routine inspection complete.'),
            ('Forklift #2', 'maintenance', 'Warehouse A', 'Hydraulic leak reported, scheduled for repair.'),
            ('Generator #1', 'active', 'Yard 1', ''),
            ('Compressor #3', 'inactive', 'Workshop', 'Awaiting replacement part.'),
            ('Pickup Truck #5', 'active', 'Yard 2', 'Oil change due next month.'),
        ]
        for name, status, location, notes in assets:
            Asset.objects.get_or_create(
                name=name,
                defaults={'status': status, 'location': location, 'notes': notes},
            )

        tasks = [
            ('Repair Forklift #2 hydraulics', 'Hydraulic fluid leaking from main lift cylinder.', 'in_progress'),
            ('Order replacement compressor part', 'Part number CMP-3300 needed for Compressor #3.', 'open'),
            ('Schedule oil change for Pickup Truck #5', 'Due within 30 days.', 'open'),
            ('Quarterly safety inspection - Warehouse A', 'Completed all checks, no issues found.', 'done'),
        ]
        for title, description, status in tasks:
            Task.objects.get_or_create(
                title=title,
                defaults={'description': description, 'status': status, 'created_by': admin_user},
            )

        self.stdout.write(self.style.SUCCESS('Seed data created successfully.'))
