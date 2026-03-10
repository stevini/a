from django.core.management.base import BaseCommand
from web.models import Products


class Command(BaseCommand):
    help = 'Populate products with stock quantity of 5 if stock is 0 or less'

    def handle(self, *args, **options):
        products = Products.objects.all()
        count = 0
        for item in products:
            if item.quantity_in_stock <= 0:
                item.quantity_in_stock = 5
                item.save()
                count += 1
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully populated stock for {count} products'
            )
        )
