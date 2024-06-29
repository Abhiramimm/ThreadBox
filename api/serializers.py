from rest_framework import serializers

from store.models import Product,Size,Category,Brand,Tag,BasketItem,Order

from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):

    class Meta:

        model=User

        fields=["username","email","password"]

        read_only_fields=["id"]
    
    def create(self,validated_data):

        return User.objects.create_user(**validated_data)

class ProductSerializer(serializers.ModelSerializer):
      
    category_object=serializers.StringRelatedField(read_only=True)

    brand_object=serializers.StringRelatedField(read_only=True)

    size_object=serializers.StringRelatedField(read_only=True,many=True)

    tag_object=serializers.StringRelatedField(read_only=True,many=True)


    class Meta:

        model=Product

        fields="__all__"

        # read_only_fields=["id","size_object","category_object","brand_object","tag_object","created_date","updated_date","is_active"]

class BasketItemSerializer(serializers.ModelSerializer):

    product_object=serializers.StringRelatedField(read_only=True)

    size_object=serializers.StringRelatedField(read_only=True)

    class Meta:

        model=BasketItem

        fields="__all__"

class OrderSerializer(serializers.ModelSerializer):

    user_object=serializers.StringRelatedField(read_only=True)
    
    class Meta:

        model=Order

        fields="__all__"