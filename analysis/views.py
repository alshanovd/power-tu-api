from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from django.db import connection

from analysis.models import Products, Orders, OrderedItems
from analysis.serializers import ProductsSerializer, OrdersSerializer, OrderedItemsSerializer


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

def countriesApi(request):
    if request.method == 'GET':
        with connection.cursor() as cursor:
            cursor.execute("SELECT DISTINCT user_country FROM analysis_orders")
            countries = cursor.fetchall()
            countries = [country[0] for country in countries]
        return JsonResponse(countries, safe=False)
    else:
        return JsonResponse("Failed to Retrieve", safe=False)