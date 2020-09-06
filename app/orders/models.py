from django.db import models

# Create your models here.


class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField()
    amount = models.IntegerField()

    def __str__(self):
        return self.title


class OrderItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)

    def __str__(self):
        return Item


class Order(models.Model):
    user = models.ForeignKey(
        "users.User", on_delete=models.PROTECT, related_name="items"
    )
    items = models.ManyToManyField(OrderItem)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    start_data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username