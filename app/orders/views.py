from django.shortcuts import render
from .models import Item

# Create your views here.
def item_list(request):
    context = {"items": Item.objects.all()}
    return render(request, "home.html", context=context)


def checkout(request):
    context = {"items": Item.objects.all()}
    return render(request, "checkout.html", context=context)


def item_detail(request):
    context = {"items": Item.objects.all()}
    return render(request, "products.html", context=context)