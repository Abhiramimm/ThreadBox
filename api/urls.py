from django.urls import path

from api import views

from rest_framework.authtoken.views import ObtainAuthToken

urlpatterns=[

    path("register/",views.UserCreationView.as_view()),

    path("products/",views.ProductListView.as_view()),
   
    path("products/<int:pk>/",views.ProductDetailView.as_view()),

    path("products/<int:pk>/cart/",views.AddToCartView.as_view()),
    
    path("cart/all/",views.CartSummaryView.as_view()),

    path("basketitem/<int:pk>/delete/",views.CartitemDestroyView.as_view()),
    
    path("basketitem/quantity/<int:pk>/change/",views.CartQuantityUpdateView.as_view()),

    path("order/summary/",views.OrderSummaryView.as_view()),

    path("order/",views.PlaceOrderView.as_view()),

    path("order/summary/",views.OrderSummaryView.as_view()),

    path("token/",ObtainAuthToken.as_view()),

]