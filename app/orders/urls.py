from django.urls import path
from .views import (
    ItemDetailView,
    ItemListView,
    checkout,
    add_item_cart,
    remove_item_cart,
)

app_name = "orders"

urlpatterns = [
    path("", ItemListView.as_view(), name="home"),
    path("product/<pk>", ItemDetailView.as_view(), name="product"),
    path("addcart/<pk>", add_item_cart, name="addcart"),
    path("removecart/<pk>", remove_item_cart, name="removecart"),
    path("checkout/", checkout, name="checkout"),
]
