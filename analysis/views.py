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


def annualRevenueApi(request, country):
    if request.method == 'GET':
        with connection.cursor() as cursor:
            if country == 'Global':
                query = """
                        SELECT DATE_FORMAT(ao.timestamp, '%b %y') AS month, ROUND(SUM(aoi.count * ap.price), 2) AS total_revenue 
                        FROM analysis_orders ao 
                        JOIN analysis_ordereditems aoi ON ao.order_id = aoi.order_id_id 
                        JOIN analysis_products ap ON aoi.product_id_id = ap.product_id 
                        WHERE ao.timestamp >= DATE_SUB(CURDATE(), INTERVAL 1 YEAR) 
                        GROUP BY DATE_FORMAT(ao.timestamp, '%b %Y'), YEAR(ao.timestamp), MONTH(ao.timestamp)
                        ORDER BY YEAR(ao.timestamp) ASC, MONTH(ao.timestamp) ASC;
                        """
                cursor.execute(query)
            else:
                query = """
                        SELECT DATE_FORMAT(ao.timestamp, '%%b %%y') AS month,ROUND(SUM(aoi.count * ap.price), 2) AS total_revenue 
                        FROM analysis_orders ao 
                        JOIN analysis_ordereditems aoi ON ao.order_id = aoi.order_id_id 
                        JOIN analysis_products ap ON aoi.product_id_id = ap.product_id 
                        WHERE ao.user_country = %s AND ao.timestamp >= DATE_SUB(CURDATE(), INTERVAL 1 YEAR) 
                        GROUP BY DATE_FORMAT(ao.timestamp, '%%b %%Y'), YEAR(ao.timestamp), MONTH(ao.timestamp)
                        ORDER BY YEAR(ao.timestamp) ASC, MONTH(ao.timestamp) ASC;
                        """
                cursor.execute(query,[country])
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
    
def annualRevenueByGenderApi(request, country):
    if request.method == 'GET':
        with connection.cursor() as cursor:
            if country == 'Global':
                query = """
                        SELECT DATE_FORMAT(ao.timestamp, '%b %y') AS month, ao.user_gender, ROUND(SUM(aoi.count * ap.price), 2) AS total_revenue 
                        FROM analysis_orders ao 
                        JOIN analysis_ordereditems aoi ON ao.order_id = aoi.order_id_id 
                        JOIN analysis_products ap ON aoi.product_id_id = ap.product_id 
                        WHERE ao.timestamp >= DATE_SUB(CURDATE(), INTERVAL 1 YEAR) 
                        GROUP BY DATE_FORMAT(ao.timestamp, '%b %Y'), ao.user_gender, YEAR(ao.timestamp), MONTH(ao.timestamp) 
                        ORDER BY YEAR(ao.timestamp) ASC, MONTH(ao.timestamp) ASC, ao.user_gender ASC;
                        """
                cursor.execute(query)
            else:
                query = """
                        SELECT DATE_FORMAT(ao.timestamp, '%%b %%y') AS month, ao.user_gender, ROUND(SUM(aoi.count * ap.price), 2) AS total_revenue 
                        FROM analysis_orders ao 
                        JOIN analysis_ordereditems aoi ON ao.order_id = aoi.order_id_id 
                        JOIN analysis_products ap ON aoi.product_id_id = ap.product_id 
                        WHERE ao.user_country = %s AND ao.timestamp >= DATE_SUB(CURDATE(), INTERVAL 1 YEAR) 
                        GROUP BY DATE_FORMAT(ao.timestamp, '%%b %%Y'), ao.user_gender, YEAR(ao.timestamp), MONTH(ao.timestamp) 
                        ORDER BY YEAR(ao.timestamp) ASC, MONTH(ao.timestamp) ASC, ao.user_gender ASC;
                        """
                cursor.execute(query,[country])
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
    
def orderStatusCountApi(request,country):
    if request.method == 'GET':
        with connection.cursor() as cursor:
            if country == 'Global':
                query = """
                        SELECT status, COUNT(*) AS order_count
                        FROM analysis_orders
                        GROUP BY status
                        ORDER BY order_count DESC;
                        """
                cursor.execute(query)
            else:
                query = """
                        SELECT status, COUNT(*) AS order_count
                        FROM analysis_orders
                        WHERE user_country = %s
                        GROUP BY status
                        ORDER BY order_count DESC;
                        """
                cursor.execute(query,[country])
            rows = cursor.fetchall()
        
        # Convert the results to a list of dictionaries
        status_counts = []
        for row in rows:
            status_counts.append({
                "status": row[0],
                "count": row[1]
            })

        return JsonResponse(status_counts, safe=False)
    else:
        return JsonResponse("Failed to Retrieve", safe=False)

def totalItemsSoldApi(request, country):
    if request.method == 'GET':
        with connection.cursor() as cursor:
            if country == 'Global':
                query = """
                        SELECT ap.product_id, ap.name AS product_name, SUM(aoi.count) AS total_items_sold
                        FROM analysis_ordereditems aoi
                        JOIN analysis_products ap ON aoi.product_id_id = ap.product_id
                        JOIN analysis_orders ao on ao.order_id = aoi.order_id_id
                        GROUP BY ap.product_id, ap.name
                        ORDER BY total_items_sold DESC;
                        """
                cursor.execute(query)
            else:
                query = """
                        SELECT ap.product_id, ap.name AS product_name, SUM(aoi.count) AS total_items_sold
                        FROM analysis_ordereditems aoi
                        JOIN analysis_products ap ON aoi.product_id_id = ap.product_id
                        JOIN analysis_orders ao on ao.order_id = aoi.order_id_id
                        WHERE ao.user_country = %s
                        GROUP BY ap.product_id, ap.name
                        ORDER BY total_items_sold DESC;
                        """
                cursor.execute(query,[country])
            rows = cursor.fetchall()
        
        # Convert the results to a list of dictionaries
        total_sold = []
        for row in rows:
            total_sold.append({
                "id": row[0],
                "product_name": row[1],
                "total_sold": row[2]
            })

        return JsonResponse(total_sold, safe=False)
    else:
        return JsonResponse("Failed to Retrieve", safe=False)

def statusesByMonths(request, country):
    if request.method == 'GET':
        with connection.cursor() as cursor:
            if country == 'Global':
                # SQL query for global data (all countries)
                query = """
                    SELECT DATE_FORMAT(ao.timestamp, '%b %y') AS month, ao.status, COUNT(*) AS order_count
                    FROM analysis_orders ao
                    WHERE ao.timestamp >= DATE_SUB(CURDATE(), INTERVAL 1 YEAR)
                    GROUP BY YEAR(ao.timestamp), MONTH(ao.timestamp), ao.status
                    ORDER BY YEAR(ao.timestamp) ASC, MONTH(ao.timestamp) ASC, order_count DESC, ao.status ASC;
                """
                cursor.execute(query)
            else:
                # SQL query for a specific country
                query = """
                    SELECT DATE_FORMAT(ao.timestamp, '%%b %%y') AS month, ao.status, COUNT(*) AS order_count
                    FROM analysis_orders ao
                    WHERE ao.user_country = %s AND ao.timestamp >= DATE_SUB(CURDATE(), INTERVAL 1 YEAR)
                    GROUP BY YEAR(ao.timestamp), MONTH(ao.timestamp), ao.status
                    ORDER BY YEAR(ao.timestamp) ASC, MONTH(ao.timestamp) ASC, order_count DESC, ao.status ASC;
                """
                cursor.execute(query, [country])

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


