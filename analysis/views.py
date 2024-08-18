from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse

from analysis.models import Products, Orders, OrderedItems
from analysis.serializers import ProductsSerializer, OrdersSerializer, OrderedItemsSerializer

from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import OrderedItems
from django.db.models import F

@csrf_exempt
def productsApi(request, id=0):
    if request.method == 'GET':
        products = Products.objects.all()
        products_serializer = ProductsSerializer(products, many=True)
        return JsonResponse(products_serializer.data, safe=False)
    elif request.method == 'POST':
        product_data = JSONParser().parse(request)
        products_serializer = ProductsSerializer(data=product_data)
        if products_serializer.is_valid():
            products_serializer.save()
            return JsonResponse(products_serializer.data, safe=False)
        return JsonResponse("Failed to Add", safe=False)
    elif request.method == 'PUT':
        product_data = JSONParser().parse(request)
        product = Products.objects.get(product_id=product_data['product_id'])
        products_serializer = ProductsSerializer(product, data=product_data)
        if products_serializer.is_valid():
            products_serializer.save()
            return JsonResponse(products_serializer.data, safe=False)
        return JsonResponse("Failed to Update", safe=False)
    elif request.method == 'DELETE':
        product = Products.objects.get(product_id=id)
        product.delete()
        return JsonResponse("Deleted Successfully", safe=False)

# Create your views here.

class OrderItemsPagination(PageNumberPagination):
    page_size = 10  # Number of items per page
    page_size_query_param = 'page_size'
    max_page_size = 100

class OrderItemsListView(APIView):
    permission_classes = [AllowAny]
    pagination_class = OrderItemsPagination
    
    def get(self, request):
        order_items = OrderedItems.objects.select_related('order', 'product') \
            .annotate(
                order_id=F('order__id'),
                product_name=F('product__name'),
                price=F('product__price'),
                count=F('count'),
                date=F('order__date'),
                time=F('order__time'),
                total_price=F('product__price') * F('count'),
                total_item=F('product__price') * F('count')
            ).values(
                'order_id', 'product_name', 'price', 'count', 'date', 'time', 'total_price', 'total_item'
            )

        paginator = self.pagination_class()
        paginated_order_items = paginator.paginate_queryset(order_items, request)
        return paginator.get_paginated_response(paginated_order_items)
