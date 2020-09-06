# https://docs.djangoproject.com/en/3.1/howto/custom-template-tags/

from django import template
from app.orders.models import Order

register = template.Library()


@register.filter
def cart_count(user):
    qs = Order.objects.filter(user=user, ordered=False)
    if qs.exists():
        return qs[0].items.count()