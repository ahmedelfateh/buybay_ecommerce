from django.db import models
from django.shortcuts import reverse
import datetime

# Create your models here.


class Item(models.Model):
    class ItemCategory(models.TextChoices):  # A subclass of Enum
        SHIRT = "SH", "Shirt"
        SPORTWEAR = "SW", "Sport Wear"
        OUTWEAR = "OW", "Out Wear"

    class ItemLabel(models.TextChoices):  # A subclass of Enum
        PRIMARY = "PR", "primary"
        SECONDARY = "SE", "secondary"
        DANGER = "DA", "danger"

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


class Order(models.Model):
    user = models.ForeignKey(
        "users.User", on_delete=models.PROTECT, related_name="items"
    )
    items = models.ManyToManyField(OrderItem)
    ordered_date = models.DateField("Ordered Date")
    ordered = models.BooleanField("Ordered", default=False)
    start_data = models.DateField("Start Date", auto_now_add=True)

    def __str__(self):
        return self.user.name

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_total_item_price()
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