from rest_framework import serializers
from analysis.models import Products, Orders, OrderedItems, Clients

class ClientsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clients
        fields = '__all__'

class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = '__all__'

class OrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = '__all__'

class OrderedItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderedItems
        fields = '__all__'

# Compare this snippet from analysis/views.py: