from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.contrib.auth.models import User
from .models import *

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User model.
    """
    class Meta:
        model = User
        fields = ["username", "password"]
        extra_kwargs = {"password": {"write_only": True}}

class ReferenceSerializer(serializers.ModelSerializer):
    """
    Serializer for Reference model.
    """
    availability = serializers.SerializerMethodField()

    class Meta:
        model = Reference
        fields = "__all__"
        read_only_fields = ["id"]

    def validate_ref(self, value):
        """
        Check if the ref exists in the database.
        """
        if Reference.objects.filter(ref=value).exists():
            raise serializers.ValidationError("This reference already exists.")
        return value

    def validate_name(self, value):
        """
        Validate the data for creating a new reference.
        """
        if not value.strip():
            raise serializers.ValidationError("Name field cannot be empty.")

        return value

    def get_availability(self, instance):
        stocks = Stock.objects.filter(reference=instance)

        if not stocks.exists():
            return "outofstock"

        for stock in stocks:
            if stock.stock > 0:
                return "available"
        return "outofstock"

class BarSerializer(serializers.ModelSerializer):
    """
    Serializer for Bar model.
    """
    class Meta:
        model = Bar
        fields = "__all__"
        read_only_fields = ["id"]

    def validate_name(self, value):
        """
        Check if the name field is not empty.
        """
        if not value.strip():
            raise serializers.ValidationError("Name field cannot be empty.")
        return value

    def validate_id(self, value):
        """
        Check if the provided stock exists in the database.
        """
        if self.instance:
            if not Bar.objects.filter(id=value).exists():
                raise serializers.ValidationError("Invalid bar id.")
        return value

class StockSerializer(serializers.ModelSerializer):
    """
    Serializer for Stock model.
    """
    class Meta:
        model = Stock
        fields = "__all__"
        read_only_fields = ["id"]

class StatisticsSerializer(serializers.Serializer):
    """
    Serializer for statistics data.
    """
    all_stocks = serializers.SerializerMethodField()
    miss_at_least_one = serializers.SerializerMethodField()

    def get_all_stocks(self):
        """
        Retrieve a list of bars that have all references in stock.

        Returns:
            dict: A dictionary containing the description and list of bars with all stocks.
        """
        bars_with_all_stocks = []
        bars = Bar.objects.all()

        for bar in bars:
            stocks = Stock.objects.filter(bar=bar).all()
            if all(stock.stock > 0 for stock in stocks):
                bars_with_all_stocks.append(bar.id)
        return {
            "description": "Liste des comptoirs qui ont toutes les références en stock",
            "bars": list(set(bars_with_all_stocks))
        }

    def get_miss_at_least_one(self):
        """
        Retrieve a list of bars that have at least one reference out of stock.

        Returns:
            dict: A dictionary containing the description and list of bars with missing stocks.
        """
        bars_with_missing_stocks = []
        bars = Bar.objects.all()

        for bar in bars:
            stocks = Stock.objects.filter(bar=bar).all()
            if any(stock.stock == 0 for stock in stocks):
                bars_with_missing_stocks.append(bar.id)
        return {
            "description": "Liste des comptoirs qui ont au moins une référence épuisée",
            "bars": list(set(bars_with_missing_stocks))
        }

class OrderItemSerializer(serializers.ModelSerializer):
    """
    Serializer for OrderItem model.
    """
    class Meta:
        model = OrderItem
        fields = ["reference", "count"]

class OrderSerializer(serializers.ModelSerializer):
    """
    Serializer for Order model.
    """
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ["id", "bar", "items"]

    def create(self, validated_data):
        items_data = validated_data.pop("items")
        order = Order.objects.create(**validated_data)

        for item_data in items_data:
            reference_id = item_data.get("reference")
            count = item_data.get("count")
            reference = item_data.get("reference")
            stock = Stock.objects.get(reference=reference, bar=validated_data.get("bar"))

            if count > stock.stock:
                raise serializers.ValidationError(
                    {"detail": f"Count for reference '{reference.name}' exceeds available stock."}
                )
            order_item = OrderItem.objects.create(order=order, reference=reference, count=count)
            order.items.add(order_item)

        return order
