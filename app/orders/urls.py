from django.urls import path
from .views import item_list, checkout, item_detail

app_name = "orders"

urlpatterns = [
    path("items/", item_list, name="item_list"),
    path("checkout/", checkout, name="checkout"),
    path("product/", item_detail, name="product"),
]
