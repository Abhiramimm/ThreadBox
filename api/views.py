from django.shortcuts import render

from store.models import Product,BasketItem,Size,Order

from api.serializers import ProductSerializer,UserSerializer,BasketItemSerializer,OrderSerializer

from rest_framework.views import APIView

from rest_framework.response import Response

from rest_framework import authentication,permissions

# Create your views here.

class UserCreationView(APIView):

    def post(self,request,*args,**kwargs):
 
        serializer_instance=UserSerializer(data=request.data)  #deserialization

        if serializer_instance.is_valid():

            # data=serializer_instance.validated_data

            # User.objects.create_super(**data)

            serializer_instance.save()

            return Response(data=serializer_instance.data)
        
        else:

            return Response(data=serializer_instance.errors)

class ProductListView(APIView):

    authentication_classes=[authentication.TokenAuthentication]

    permission_classes=[permissions.IsAuthenticated]


    def get(self,request,*args,**kwargs):

        qs=Product.objects.all()

        serializer_instance=ProductSerializer(qs,many=True)

        return Response(data=serializer_instance.data)

class ProductDetailView(APIView):

    authentication_classes=[authentication.TokenAuthentication]

    permission_classes=[permissions.IsAuthenticated]


    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        product_obj=Product.objects.get(id=id)   

        serializer_instance=ProductSerializer(product_obj,many=False)

        return Response(data=serializer_instance.data)
    
class AddToCartView(APIView):

    authentication_classes=[authentication.TokenAuthentication]

    permission_classes=[permissions.IsAuthenticated]


    def post(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        basket_obj=request.user.cart

        product_obj=Product.objects.get(id=id)

        size_name=request.POST.get("size_object")

        size_obj=Size.objects.get(name=size_name)

        qty=request.POST.get("qty")

        basket_item_obj=BasketItem.objects.filter(basket_object=basket_obj,product_object=product_obj,size_object=size_obj,is_order_placed=False)
        
        print(basket_item_obj)

        if basket_item_obj:

            basket_item_obj[0].quantity+=int(qty)

            basket_item_obj[0].save()

        else:

            BasketItem.objects.create(

            basket_object=basket_obj,

            product_object=product_obj,

            size_object=size_obj,

            quantity=qty

           )
        return Response(data={"meassage":"item added to cart"})    

class CartSummaryView(APIView):

    authentication_classes=[authentication.TokenAuthentication]

    permission_classes=[permissions.IsAuthenticated]

    def get(self,request,*args,**kwargs):

        qs=request.user.cart.cartitems.filter(is_order_placed=False)

        serializer_instance=BasketItemSerializer(qs,many=True)

        return Response(data=serializer_instance.data)     

class CartitemDestroyView(APIView):

    authentication_classes=[authentication.TokenAuthentication]

    permission_classes=[permissions.IsAuthenticated]


    def delete(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        BasketItem.objects.get(id=id).delete()

        return Response(data={"message":"deleted successfully"})

class CartQuantityUpdateView(APIView):

    authentication_classes=[authentication.TokenAuthentication]

    permission_classes=[permissions.IsAuthenticated]


    def put(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        basket_item_object=BasketItem.objects.get(id=id)

        action=request.POST.get("action")

        print(action)

        if action=="increment":

            basket_item_object.quantity+=1

        else:

            basket_item_object.quantity-=1
        
        basket_item_object.save()

        return Response(data={"message":"quantity updated !!"})

class PlaceOrderView(APIView):

    authentication_classes=[authentication.TokenAuthentication]

    permission_classes=[permissions.IsAuthenticated]
    
    def post(self,request,*args,**kwargs):

        email=request.POST.get("email")

        phone=request.POST.get("phone")

        address=request.POST.get("address")

        pin=request.POST.get("pin")

        payment_mode=request.POST.get("payment_mode")

        user_obj=request.user

        cart_item_objects=request.user.cart.cartitems.filter(is_order_placed=False)

        if payment_mode=="cod":

            order_obj=Order.objects.create(

                user_object=user_obj,

                delivery_address=address,

                phone=phone,

                pin=pin,

                email=email,

                payment_mode=payment_mode

            )

            for bi in cart_item_objects:
                
                order_obj.basket_item_objects.add(bi)

                bi.is_order_placed=True

                bi.save()

            order_obj.save()


        print(email,phone,address,pin,payment_mode,)

        return Response({"meassge":"order successfully!!"})

class OrderSummaryView(APIView):

    authentication_classes=[authentication.TokenAuthentication]

    permission_classes=[permissions.IsAuthenticated]

    def get(self,request,*args,**kwargs):

        qs=Order.objects.filter(user_object=request.user).order_by("-created_date")

        serializer_instance=OrderSerializer(qs,many=True)

        return Response(data=serializer_instance.data)


