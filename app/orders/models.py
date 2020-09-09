import datetime
from os import path
from django.db import models
from django.shortcuts import reverse
from app.users.models import BillingAddress
from django.utils import timezone


# Create your models here.


def get_file_path(prefix: str, filename: str):
    if not prefix.endswith("/"):
        prefix += "/"
    timestamp = timezone.now().strftime("%Y-%m-%d-%H-%M-%S-%f")
    ext = path.splitext(filename)[1]
    return prefix + timestamp + ext


class Item(models.Model):
    class ItemCategory(models.TextChoices):  # A subclass of Enum
        SHIRT = "SH", "Shirt"
        SPORTWEAR = "SW", "Sport Wear"
        OUTWEAR = "OW", "Out Wear"

    class ItemLabel(models.TextChoices):  # A subclass of Enum
        PRIMARY = "PR", "primary"
        SECONDARY = "SE", "secondary"
        DANGER = "DA", "danger"

    def product_image_path(self, filename):  # pylint: disable=no-self-use
        return get_file_path("product_image/", filename)

    title = models.CharField("Title", max_length=100)
    price = models.FloatField("Price")
    category = models.CharField(
        "Category",
        max_length=2,
        choices=ItemCategory.choices,
        default=ItemCategory.SHIRT,
    )
    label = models.CharField(
        "Label",
        max_length=2,
        choices=ItemLabel.choices,
        default=ItemLabel.PRIMARY,
    )
    description = models.CharField("Description", max_length=300, blank=True, null=True)
    amount = models.IntegerField("Amount")
    image = models.ImageField(
        "Product Image",
        max_length=256,
        upload_to=product_image_path,
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("orders:product", kwargs={"pk": self.id})

    def get_add_cart_url(self):
        return reverse("orders:addcart", kwargs={"pk": self.id})

    def get_remove_cart_url(self):
        return reverse("orders:removecart", kwargs={"pk": self.id})


class OrderItem(models.Model):
    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, null=True, blank=True
    )
    ordered = models.BooleanField("Ordered", default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField("Quantity", blank=True, null=True, default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    def get_total_item_price(self):
        return self.quantity * self.item.price


class OrderStates(models.TextChoices):  # A subclass of Enum
    INITIATED = "IN", "initiated"
    DELIVERED = "DE", "delivered"
    RECEIVED = "RE", "received"
    REFUNDREQUEST = "RR", "Refund Request"
    REFUNDGRANTED = "RG", "Refund Granted"


class Order(models.Model):

    user = models.ForeignKey(
        "users.User", on_delete=models.PROTECT, related_name="items"
    )
    items = models.ManyToManyField(OrderItem)
    ordered_date = models.DateField("Ordered Date")
    ordered = models.BooleanField("Ordered", default=False)
    start_data = models.DateField("Start Date", auto_now_add=True)
    payment = models.ForeignKey(
        "Payment", on_delete=models.SET_NULL, blank=True, null=True
    )
    promo_code = models.ForeignKey(
        "PromoCode", on_delete=models.SET_NULL, blank=True, null=True
    )
    billing_address = models.ForeignKey(
        "users.BillingAddress", on_delete=models.SET_NULL, blank=True, null=True
    )
    refund_code = models.CharField("Refund Code", max_length=20, blank=True, null=True)
    state = models.CharField(
        "Order State",
        max_length=2,
        choices=OrderStates.choices,
        default=OrderStates.INITIATED,
    )

    def __str__(self):
        return self.user.name

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_total_item_price()
        return total

    def get_total_promocode(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_total_item_price()
        total -= self.promo_code.amount
        return total


class PromoCode(models.Model):
    code = models.CharField("code", max_length=15)
    amount = models.FloatField("Amount")
    expiry_date = models.DateField("Expiry Date", blank=False)

    def __str__(self):
        return self.code

    @property
    def is_expired(self):
        return self.expiry_date < datetime.date.today()


class Payment(models.Model):
    stripe_charge_id = models.CharField(max_length=255)
    user = models.ForeignKey(
        "users.User", on_delete=models.SET_NULL, blank=True, null=True
    )
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}, {self.stripe_charge_id}"


class Refund(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    reason = models.TextField()
    accepted = models.BooleanField(default=False)
    email = models.EmailField()

    def __str__(self):
        return f"{self.reason}"