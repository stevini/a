# app1/management/commands/import_products.py

import json
from django.core.management.base import BaseCommand
from web.models import Products

class Command(BaseCommand):
    help = "Import products from a JSON fixture with selected fields (name, price, cost)."

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str, help="Path to the JSON fixture file.")

    def handle(self, *args, **kwargs):
        json_file = kwargs['json_file']
        try:
            with open(json_file, 'r') as f:
                # If your file is a JSON array, load it directly:
                data = json.load(f)
        except Exception as e:
            self.stderr.write(f"Error loading JSON file: {e}")
            return

        for entry in data:
            fields = entry.get("fields", {})
            name = fields.get("name")
            price = fields.get("price")
            cost = fields.get("cost")
            if not name or price is None or cost is None:
                self.stdout.write(f"Skipping incomplete entry: {entry}")
                continue

            # Create or update the product in App1.
            product, created = Products.objects.update_or_create(
                name=name,
                defaults={
                    'sellp': price,
                    'buyp': cost,
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created product: {name}"))
            else:
                self.stdout.write(f"Updated product: {name}")

        self.stdout.write(self.style.SUCCESS("Product import complete."))
