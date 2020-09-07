from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, DetailView, View
from .models import Item, OrderItem, Order
from django.utils import timezone

# Create your views here.
class ItemListView(ListView):
    model = Item
    paginate_by = 12
    template_name = "home.html"


class ItemDetailView(DetailView):
    model = Item
    template_name = "product.html"


def checkout(request):
    context = {"items": Item.objects.all()}
    return render(request, "checkout.html", context=context)


@login_required
def add_item_cart(request, pk):
    item = get_object_or_404(Item, pk=pk)
    order_item, created = OrderItem.objects.get_or_create(
        item=item, user=request.user, ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__id=item.id).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This Item has updated")
            return redirect("orders:product", pk=pk)
        else:
            order.items.add(order_item)
            messages.info(request, "This Item has added to your cart")
            return redirect("orders:product", pk=pk)
    else:
        order_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=order_date)
        order.items.add(order_item)
        messages.info(request, "This Item has added to your cart")
        return redirect("orders:product", pk=pk)


@login_required
def remove_item_cart(request, pk):
    item = get_object_or_404(Item, pk=pk)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]

        if order.items.filter(item__id=item.id).exists():
            order_item = OrderItem.objects.filter(
                item=item, user=request.user, ordered=False
            )[0]
            order.items.remove(order_item)
            messages.info(request, "This item was removed from your cart.")
            return redirect("orders:product", pk=pk)
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("orders:product", pk=pk)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("orders:product", pk=pk)


@login_required
def remove_one_item_cart(request, pk):
    item = get_object_or_404(Item, pk=pk)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__id=item.id).exists():
            order_item = OrderItem.objects.filter(
                item=item, user=request.user, ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request, "You just removed one item")
            return redirect("orders:ordersummary")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("orders:product", pk=pk)


class orderSummaryDetailView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {"object": order}
            return render(
                self.request,
                "order_summary.html",
                context,
            )
        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an active order")
            return redirect("/")