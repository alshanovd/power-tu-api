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
                SELECT DATE_FORMAT(ao.timestamp, '%b %y') AS month, ao.user_country,ROUND(SUM(aoi.count * ap.price), 2) AS total_revenue 
                FROM analysis_orders ao 
                JOIN analysis_ordereditems aoi ON ao.order_id = aoi.order_id_id 
                JOIN analysis_products ap ON aoi.product_id_id = ap.product_id 
                WHERE ao.timestamp >= DATE_SUB(CURDATE(), INTERVAL 1 YEAR) 
                GROUP BY DATE_FORMAT(ao.timestamp, '%b %Y'), YEAR(ao.timestamp), MONTH(ao.timestamp), ao.user_country
                ORDER BY YEAR(ao.timestamp) ASC, MONTH(ao.timestamp) ASC, ao.user_country;
            """)
            rows = cursor.fetchall()

        # Convert the results to a list of dictionaries
        revenue = []
        for row in rows:
            revenue.append({
                "month": row[0],
                "user_country": row[1],
                "revenue": row[2]
            })

        return JsonResponse(revenue, safe=False)
    else:
        return JsonResponse("Failed to Retrieve", safe=False)
    
def annualRevenueByGenderApi(request):
    if request.method == 'GET':
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT DATE_FORMAT(ao.timestamp, '%b %y') AS month, ao.user_country, ao.user_gender, ROUND(SUM(aoi.count * ap.price), 2) AS total_revenue 
                FROM analysis_orders ao 
                JOIN analysis_ordereditems aoi ON ao.order_id = aoi.order_id_id 
                JOIN analysis_products ap ON aoi.product_id_id = ap.product_id 
                WHERE ao.timestamp >= DATE_SUB(CURDATE(), INTERVAL 1 YEAR) 
                GROUP BY DATE_FORMAT(ao.timestamp, '%b %Y'), ao.user_gender, YEAR(ao.timestamp), MONTH(ao.timestamp) 
                ORDER BY YEAR(ao.timestamp) ASC, MONTH(ao.timestamp) ASC, ao.user_country, ao.user_gender ASC;
            """)
            rows = cursor.fetchall()
        
        # Convert the results to a list of dictionaries
        revenue = []
        for row in rows:
            revenue.append({
                "month": row[0],
                "user_country": row[1],
                "gender": row[2],
                "revenue": row[3]
            })

        return JsonResponse(revenue, safe=False)
    else:
        return JsonResponse("Failed to Retrieve", safe=False)
    
def orderStatusCountApi(request):
    if request.method == 'GET':
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT user_country, status, COUNT(*) AS order_count
                FROM analysis_orders
                GROUP BY user_country, status
                ORDER BY user_country, order_count DESC;
            """)
            rows = cursor.fetchall()
        
        # Convert the results to a list of dictionaries
        status_counts = []
        for row in rows:
            status_counts.append({
                "user_country": row[0],
                "status": row[1],
                "count": row[2]
            })

        return JsonResponse(status_counts, safe=False)
    else:
        return JsonResponse("Failed to Retrieve", safe=False)

def totalItemsSoldApi(request):
    if request.method == 'GET':
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT ao.user_country, ap.product_id, ap.name AS product_name, SUM(aoi.count) AS total_items_sold
                FROM analysis_ordereditems aoi
                JOIN analysis_products ap ON aoi.product_id_id = ap.product_id
                JOIN analysis_orders ao on ao.order_id = aoi.order_id_id
                GROUP BY ao.user_country, ap.product_id, ap.name
                ORDER BY ao.user_country, total_items_sold DESC;
            """)
            rows = cursor.fetchall()
        
        # Convert the results to a list of dictionaries
        total_sold = []
        for row in rows:
            total_sold.append({
                "user_country": row[0],
                "id": row[1],
                "product_name": row[2],
                "total_sold": row[3]
            })

        return JsonResponse(total_sold, safe=False)
    else:
        return JsonResponse("Failed to Retrieve", safe=False)

def statusesByMonths(request, country):
    if request.method == 'GET':
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT DATE_FORMAT(ao.timestamp, '%%b %%y') AS month, ao.status, COUNT(*) AS order_count
                FROM analysis_orders ao
                WHERE ao.user_country = %s AND ao.timestamp >= DATE_SUB(CURDATE(), INTERVAL 1 YEAR)
                GROUP BY YEAR(ao.timestamp), MONTH(ao.timestamp), ao.status
                ORDER BY YEAR(ao.timestamp) ASC, MONTH(ao.timestamp) ASC, order_count DESC, ao.status ASC;
            """, [country])
            rows = cursor.fetchall()

        statuses = []
        for row in rows:
            statuses.append({
                "month": row[0],
                "status": row[1],
                "count": row[2]
            })

        return JsonResponse(statuses, safe=False)
    else:
        return JsonResponse("Failed to Retrieve", safe=False)

# def statusesByMonths(request):
#     if request.method == 'GET':
#         with connection.cursor() as cursor:
#             cursor.execute("""
#                 SELECT ao.user_country, DATE_FORMAT(ao.timestamp, '%b %y') AS month, ao.status, COUNT(*) AS order_count
#                 FROM analysis_orders ao
#                 WHERE ao.timestamp >= DATE_SUB(CURDATE(), INTERVAL 1 YEAR)
#                 GROUP BY ao.user_country, YEAR(ao.timestamp), MONTH(ao.timestamp), ao.status
#                 ORDER BY ao.user_country, YEAR(ao.timestamp) ASC, MONTH(ao.timestamp) ASC, order_count DESC, ao.status ASC;
#             """)
#             rows = cursor.fetchall()
        
#         # Convert the results to a list of dictionaries
#         statuses = []
#         for row in rows:
#             statuses.append({
#                 "user_country": row[0],
#                 "month": row[1],
#                 "status": row[2],
#                 "count": row[3]
#             })

#         return JsonResponse(statuses, safe=False)
#     else:
#         return JsonResponse("Failed to Retrieve", safe=False)