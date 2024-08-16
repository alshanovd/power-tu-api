from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.http import HttpResponse

from analysis.models import Products, Orders, OrderedItems
from analysis.serializers import ProductsSerializer, OrdersSerializer, OrderedItemsSerializer


#@csrf_exempt
#@permission_classes([IsAuthenticated])

class Home(APIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    def get(self, request):
        if request.method == 'GET':
            products = Products.objects.all()
            products_serializer = ProductsSerializer(products, many=True)
            return HttpResponse(JsonResponse(products_serializer.data, safe=False))
        elif request.method == 'POST':
            product_data = JSONParser().parse(request)
            products_serializer = ProductsSerializer(data=product_data)
            if products_serializer.is_valid():
                products_serializer.save()
                return HttpResponse(JsonResponse(products_serializer.data, safe=False))
            return JsonResponse("Failed to Add", safe=False)
        elif request.method == 'PUT':
            product_data = JSONParser().parse(request)
            product = Products.objects.get(product_id=product_data['product_id'])
            products_serializer = ProductsSerializer(product, data=product_data)
            if products_serializer.is_valid():
                products_serializer.save()
                return HttpResponse(JsonResponse(products_serializer.data, safe=False))
            return JsonResponse("Failed to Update", safe=False)
        elif request.method == 'DELETE':
            product = Products.objects.get(product_id=id)
            product.delete()
            return HttpResponse(JsonResponse("Deleted Successfully", safe=False))

    # Create your views here.
