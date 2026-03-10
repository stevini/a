from django.core.management.base import BaseCommand
from web.models import Products


class Command(BaseCommand):
    help = 'Disable all products that do not have an image'

    def handle(self, *args, **options):
        products = Products.objects.all()
        count = 0
        for item in products:
            if not item.image:
                item.active = False
                item.save()
                count += 1
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully disabled {count} products without images'
            )
        )
