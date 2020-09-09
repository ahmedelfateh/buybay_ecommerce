from django.conf import settings
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, DetailView, View
from django.utils import timezone

from .forms import CheckoutForm, PromoCodeForm
from .models import Item, OrderItem, Order, PromoCode, Payment
from app.users.models import BillingAddress

import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

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
            return redirect("orders:ordersummary")
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
            order_item.delete()
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


class CheckoutView(View):
    def get(self, *args, **kwargs):

        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            form = CheckoutForm()
            context = {
                "form": form,
                "order": order,
                "promocodeform": PromoCodeForm(),
            }
            return render(self.request, "checkout.html", context)
        except ObjectDoesNotExist:
            messages.info(self.request, "You do not have an active order")
            return redirect("orders:checkout")

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():
                street_address = form.cleaned_data.get("street_address")
                apartment_address = form.cleaned_data.get("apartment_address")
                country = form.cleaned_data.get("country")
                zip = form.cleaned_data.get("zip")
                payment_option = form.cleaned_data.get("payment_option")
                billing_address = BillingAddress(
                    user=self.request.user,
                    street_address=street_address,
                    apartment_address=apartment_address,
                    country=country,
                    zip=zip,
                )
                billing_address.save()
                order.billing_address = billing_address
                order.save()

                # this will work to redirect to payments
                if payment_option == "S":
                    return redirect("orders:PaymentView", option="stripe")
                # elif payment_option == 'P':
                #     return redirect('orders:payment', payment_option='paypal')
                else:
                    messages.warning(self.request, "Invalid payment option selected")
                    return redirect("orders:checkout")

                return redirect("orders:checkout")
            messages.warning(self.request, "Failed checkout")
            return redirect("orders:checkout")

        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an active order")
            return redirect("orders:ordersummary")


def check_promocode(request, code):
    try:
        promocode = PromoCode.objects.get(code=code)
        if promocode.is_expired:
            messages.info(request, "This promo code is expired")
        else:
            return promocode
    except ObjectDoesNotExist:
        messages.info(request, "This promo code does not exist")


class PromoCodeView(View):
    def post(self, *args, **kwargs):
        form = PromoCodeForm(self.request.POST or None)
        if form.is_valid():
            code = form.cleaned_data.get("code")  # promocode
            order = Order.objects.get(user=self.request.user, ordered=False)  # order
            check_code = check_promocode(self.request, code)
            if str(check_code) == str(code):
                order.promo_code = check_code
                order.save()
                messages.success(self.request, "Successfully added coupon")
                return redirect("orders:checkout")
            else:
                messages.info(self.request, check_code)
                return redirect("orders:ordersummary")


# https://stripe.com/docs/api/charges/create?lang=python
class PaymentView(View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
        except:
            messages.info(self.request, "You have no orders yet, Go Shopping!")
            return redirect("/")

        if order.billing_address:
            context = {"order": order}
            return render(self.request, "payment.html", context)
        else:
            messages.info(self.request, "Complete your Data First!")
            return redirect("orders:checkout")

    def post(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        try:
            amount = int(order.get_total_promocode() * 100)
        except:
            amount = int(order.get_total() * 100)

        try:
            charge = stripe.Charge.create(
                amount=amount,
                currency="usd",
                source="tok_visa",
                description="My First Test Charge (created for API docs)",
            )

            # create the payment
            payment = Payment()
            payment.stripe_charge_id = charge["id"]
            payment.user = self.request.user
            payment.amount = order.get_total()
            payment.save()

            # assign the payment to the order

            order.ordered = True
            order.payment = payment
            order.save()

            messages.success(self.request, "Order has created, time to Buy again!")
            return redirect("/")

        # https://stripe.com/docs/api/errors/handling
        except stripe.error.CardError as e:
            body = e.json_body
            err = body.get("error", {})
            messages.error(self.request, f"{err.get('message')}")
            return redirect("/")

        except stripe.error.RateLimitError as e:
            # Too many requests made to the API too quickly
            messages.error(self.request, "Rate limit error")
            return redirect("/")

        except stripe.error.InvalidRequestError as e:
            # Invalid parameters were supplied to Stripe's API
            messages.error(self.request, "Invalid parameters")
            return redirect("/")

        except stripe.error.AuthenticationError as e:
            # Authentication with Stripe's API failed
            # (maybe you changed API keys recently)
            messages.error(self.request, "Not authenticated")
            return redirect("/")

        except stripe.error.APIConnectionError as e:
            # Network communication with Stripe failed
            messages.error(self.request, "Network error")
            return redirect("/")

        except stripe.error.StripeError as e:
            # Some thing else happend, completely unrelated to Stripe
            # TODO: log with Sentry
            messages.error(
                self.request,
                "Something went wrong. You were not charged. Please try again.",
            )
            return redirect("/")

        except Exception as e:
            # send an email to ourselves
            messages.error(
                self.request, "A serious error occurred. We have been notifed."
            )
            return redirect("/")
