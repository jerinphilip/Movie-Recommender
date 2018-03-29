from .singleton import Singleton
from ..booking_system.models import *

class Booker(Singleton):
    def retrieve(show):
        all_seats = show.screen.seat_set.all()
        booked_setas = Booking.objects.filter()
        - Booking.objects.get(invoice.status != "Failed", show=Show)
        pass

    def select(seat, show, user):
        pass

    def book(seat, show, user):
        pass

    def cancel(seat, show, user):
        pass

