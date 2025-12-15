from django.core.management import BaseCommand
from shopapp.models import Order
from django.contrib.auth.models import User

class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write('create order')
        user = User.objects.get(username='admin')
        order = Order.objects.get_or_create(
            delivery_address='ul pushkina 8',
            promocode='PRomOCODE123',
            user=user,
        )
        self.stdout.write(f'order is created {order}')
