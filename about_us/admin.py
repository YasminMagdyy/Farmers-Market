from django.contrib import admin
from django.utils import timezone
from .models import ProductPrices, Products


# to extend the admin functionality
from django.contrib import admin
# customize pages inside of the admin app
from django.urls import path
# send data back and forth and ajax calls
from django.http import JsonResponse
# to render html pages
from django.shortcuts import render
from .models import ProductPrices, Products
# creates groups for new keys --> useful for adding data
from collections import defaultdict

class PriceTrendsAdmin(admin.ModelAdmin):
    change_list_template = "admin/price_trends.html"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path("price-data/", self.admin_site.admin_view(self.price_data), name="price-data"),
        ]
        return custom_urls + urls

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context["products"] = Products.objects.all()
        return super().changelist_view(request, extra_context=extra_context)

    def price_data(self, request):
        product_ids = request.GET.getlist("products[]", [])
        data = defaultdict(list)

        for pid in product_ids:
            prices = ProductPrices.objects.filter(product_id=pid).order_by("editDeadlineDateTime")
            for p in prices:
                data[Products.objects.get(id=pid).productName].append({
                    "date": p.editDeadlineDateTime.strftime("%Y-%m-%d"),
                    "price": p.productPrice
                })
        return JsonResponse(data)


# admin.site.register(Products)

admin.site.register(Products)
admin.site.register(ProductPrices, PriceTrendsAdmin)

