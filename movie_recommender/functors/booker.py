from .singleton import Singleton
from booking_system.models import *

class Booker(Singleton):
    def retrieve(show):
        bookings = Booking.objects.filter(show=show).exclude(invoice__status__name="Failure")
        return show.screen.seat_set.exclude(booking_in=bookings)

    def select(seats, show, user):
        booking = Booking.objects.create(show=show, user=user)
        booking.seats.set(seats)
        booking.save()
        #TODO pricing
        Invoice.objects.create(booking=booking, 
                status=StatusType.objects.get(name="In Progress")).save()
        return booking

    def book(booking):
        booking.invoice.status = StatusType.objects.get(name="Success")
        return booking.save()

    def cancel(booking):
        booking.invoice.status = StatusType.objects.get(name="Failure")
        return booking.save()

