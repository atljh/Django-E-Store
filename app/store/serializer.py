from rest_framework import serializers


class SearchSerializer(serializers.Serializer):
    search_word = serializers.CharField(max_length=50)
    min_price = serializers.IntegerField(min_value=0, max_value=999999999)
    max_price = serializers.IntegerField(min_value=0, max_value=999999999)
    category = serializers.ListField(child=serializers.CharField(max_length=15))