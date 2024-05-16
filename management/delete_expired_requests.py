from django.core.management.base import BaseCommand
from django.utils import timezone
from librarian.models import BorrowRequest

class Command(BaseCommand):
    help = 'Delete expired borrow requests'

    def handle(self, *args, **kwargs):
        now = timezone.now()
        expired_requests = BorrowRequest.objects.filter(expires_at__lt=now)
        count = expired_requests.count()
        expired_requests.delete()
        self.stdout.write(self.style.SUCCESS(f'Successfully deleted {count} expired borrow requests'))