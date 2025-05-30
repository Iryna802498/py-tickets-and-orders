from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet
from db.models import Ticket, Order


from datetime import datetime


User = get_user_model()


def create_order(
        tickets: list[dict],
        username: str,
        date: str = None
) -> None:
    user = User.objects.get(username=username)
    order_date = datetime.fromisoformat(date) if date else datetime.now()
    with transaction.atomic():
        order = Order.objects.create(user=user, created_at=order_date)
        for ticket in tickets:
            new_ticket = Ticket(
                movie_session_id=ticket["movie_session"],
                order=order,
                row=ticket["row"],
                seat=ticket["seat"]
            )
            new_ticket.full_clean()
            new_ticket.save()


def get_orders(username: str = None) -> QuerySet:
    if username is not None:
        user = User.objects.get(username=username)
        orders = Order.objects.filter(user=user)
        return orders
    else:
        return Order.objects.all()
