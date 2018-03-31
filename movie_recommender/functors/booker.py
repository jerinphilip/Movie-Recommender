from .singleton import Singleton
from booking_system.models import *
from celery import Celery
from django.db import transaction

app = Celery('booking_system', broker="redis://locahost:6379/0")


class Booker(Singleton):
    def retrieve(show):
        bookings = Booking.objects.filter(show=show).exclude(
            invoice__status__name="Failure")
        return show.screen.seat_set.exclude(booking_in=bookings)

    @app.task
    def start_booking(show, user):
        booking = Booking.objects.create(show=Show, user=user)
        booking.save()
        invoice = Invoice.objects.create(booking=booking,
                                         status=StatusType.objects.
                                         get(name="In Progress")).save()
        return invoice.save()

    @app.task
    def select(booking_id, seat):
        with transaction.atomic():
            booking = Booking.objects.get(id=booking_id)
            booking.seats.add(seat)
            booking.save()
            return booking

    @app.task
    def deselect(booking_id, seat):
        with transaction.atomic():
            booking = Booking.objects.get(id=booking_id)
            booking.seats.remove(seat)
            booking.save()
            return booking

    def book(booking):
        booking.invoice.status = StatusType.objects.get(name="Success")
        return booking.save()

    def cancel(booking):
        booking.invoice.status = StatusType.objects.get(name="Failure")
        return booking.save()
