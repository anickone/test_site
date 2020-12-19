from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Product


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Product
        fields = [
            'url',
            'id',
            'owner',
            'name',
            'description',
            'created',
            'updated',
            'logo',
            'rotate_duration',
            'modified']


class UserSerializer(serializers.HyperlinkedModelSerializer):
    products = serializers.HyperlinkedRelatedField(
        many=True, view_name='product-detail', read_only=True)

    class Meta:
        model = User
        fields = ['url', 'id', 'username', 'products']
