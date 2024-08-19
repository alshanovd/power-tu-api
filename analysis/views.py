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
    else:
        return JsonResponse("Failed to Retrieve", safe=False)

def countriesApi(request):
    if request.method == 'GET':
        with connection.cursor() as cursor:
            cursor.execute("SELECT DISTINCT user_country FROM analysis_orders")
            countries = cursor.fetchall()
            countries = [country[0] for country in countries]
        return JsonResponse(countries, safe=False)
    else:
        return JsonResponse("Failed to Retrieve", safe=False)

def ordersApi(request, id=0):
    if request.method == 'GET':
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT ao.order_id, ao.timestamp, ao.user_gender, ao.user_country, ao.user_name, ao.status, 
                       ROUND(SUM(aoi.count * ap.price), 2) AS total_price 
                FROM analysis_orders ao 
                JOIN analysis_ordereditems aoi ON ao.order_id = aoi.order_id_id 
                JOIN analysis_products ap ON aoi.product_id_id = ap.product_id 
                GROUP BY ao.order_id, ao.timestamp, ao.user_gender, ao.user_country, ao.user_name, ao.status 
                ORDER BY ao.timestamp DESC 
            """)
            rows = cursor.fetchall()

        # Convert the results to a list of dictionaries
        orders = []
        for row in rows:
            orders.append({
                "order_id": row[0],
                "timestamp": row[1],
                "user_gender": row[2],
                "user_country": row[3],
                "user_name": row[4],
                "status": row[5],
                "total_price": row[6]
            })

        return JsonResponse(orders, safe=False)
    else:
        return JsonResponse("Failed to Retrieve", safe=False)


def annualRevenueApi(request):
    if request.method == 'GET':
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT DATE_FORMAT(ao.timestamp, '%b %Y') AS month, ROUND(SUM(aoi.count * ap.price), 2) AS total_revenue 
                FROM analysis_orders ao 
                JOIN analysis_ordereditems aoi ON ao.order_id = aoi.order_id_id 
                JOIN analysis_products ap ON aoi.product_id_id = ap.product_id 
                WHERE ao.timestamp >= DATE_SUB(CURDATE(), INTERVAL 1 YEAR) 
                GROUP BY DATE_FORMAT(ao.timestamp, '%b %Y'), YEAR(ao.timestamp), MONTH(ao.timestamp) 
                ORDER BY YEAR(ao.timestamp) ASC, MONTH(ao.timestamp) ASC;
            """)
            rows = cursor.fetchall()

        # Convert the results to a list of dictionaries
        revenue = []
        for row in rows:
            revenue.append({
                "month": row[0],
                "revenue": row[1]
            })

        return JsonResponse(revenue, safe=False)
    else:
        return JsonResponse("Failed to Retrieve", safe=False)
    
def annualRevenueByGenderApi(request):
    if request.method == 'GET':
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT DATE_FORMAT(ao.timestamp, '%b %Y') AS month, ao.user_gender, ROUND(SUM(aoi.count * ap.price), 2) AS total_revenue 
                FROM analysis_orders ao 
                JOIN analysis_ordereditems aoi ON ao.order_id = aoi.order_id_id 
                JOIN analysis_products ap ON aoi.product_id_id = ap.product_id 
                WHERE ao.timestamp >= DATE_SUB(CURDATE(), INTERVAL 1 YEAR) 
                GROUP BY DATE_FORMAT(ao.timestamp, '%b %Y'), ao.user_gender, YEAR(ao.timestamp), MONTH(ao.timestamp) 
                ORDER BY YEAR(ao.timestamp) ASC, MONTH(ao.timestamp) ASC, ao.user_gender ASC;
            """)
            rows = cursor.fetchall()
        
        # Convert the results to a list of dictionaries
        revenue = []
        for row in rows:
            revenue.append({
                "month": row[0],
                "gender": row[1],
                "revenue": row[2]
            })

        return JsonResponse(revenue, safe=False)
    else:
        return JsonResponse("Failed to Retrieve", safe=False)
    

