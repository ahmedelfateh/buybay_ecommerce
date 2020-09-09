from django.urls import path
from .views import (
    ItemDetailView,
    ItemListView,
    add_item_cart,
    remove_item_cart,
    orderSummaryDetailView,
    remove_one_item_cart,
    CheckoutView,
    PromoCodeView,
    PaymentView,
    RequestRefundView,
)

app_name = "orders"

urlpatterns = [
    path("", ItemListView.as_view(), name="home"),
    path("product/<pk>", ItemDetailView.as_view(), name="product"),
    path("ordersum/", orderSummaryDetailView.as_view(), name="ordersummary"),
    path("checkout/", CheckoutView.as_view(), name="checkout"),
    path("promo/", PromoCodeView.as_view(), name="promo"),
    path("payment/<option>/", PaymentView.as_view(), name="PaymentView"),
    path("refund/", RequestRefundView.as_view(), name="refund"),
    path("addcart/<pk>/", add_item_cart, name="addcart"),
    path("removecart/<pk>/", remove_item_cart, name="removecart"),
    path("removeitem/<pk>/", remove_one_item_cart, name="removeitem"),
]
