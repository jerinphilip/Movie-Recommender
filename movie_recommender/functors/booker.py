from .singleton import Singleton
from booking_system.models import *
from celery import Celery
from django.db import transaction

app = Celery('booking_system', broker="redis://locahost:6379/0")


class Booker(Singleton):
    def retrieve(self, show):
        bookings = Booking.objects.filter(show=show).exclude(
            invoice__status__name="Failure")
        return show.screen.seat_set.exclude(booking__in=bookings)

    def start_booking(self, show, user):
        booking = Booking.objects.create(show=show, user=user)
        booking.save()
        Invoice.objects.create(booking=booking,
                               status=StatusType.objects.
                               get(name="In Progress")).save()
        return booking

    @app.task
    def select(self, booking_id, seat_id, user_id):
        with transaction.atomic():
            booking = Booking.objects.get(id=booking_id)
            if booking.user.id != user_id or booking.invoice.status.name != "In Progress":
                return
            if Booking.objects.filter(show=booking.show, seats__id=seat_id).count():
                return booking.delete()
            booking.seats.add(Seat.objects.get(pk=seat_id))
            return booking.save()

    @app.task
    def deselect(self, booking_id, seat_id, user_id):
        with transaction.atomic():
            booking = Booking.objects.get(id=booking_id)
            if booking.user.id != user_id or booking.invoice.status.name != "In Progress":
                return
            booking.seats.remove(Seat.objects.get(pk=seat_id))
            return booking.save()

    def invoice_success(self, booking):
        booking.invoice.status = StatusType.objects.get(name="Success")
        return booking.save()

    def invoice_failure(self, booking):
        booking.invoice.status = StatusType.objects.get(name="Failure")
        return booking.save()

    def cancel(self, booking):
        booking.delete()
