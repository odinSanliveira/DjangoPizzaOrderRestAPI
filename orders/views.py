from django.shortcuts import render, get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response

from . import serializers
from . models import Order

from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser, AllowAny
from rest_framework.pagination import PageNumberPagination

User = get_user_model()

class HelloOrderView(generics.GenericAPIView):
    def get(self, request):
        return Response(data={"message":"Hello Orders"}, status=status.HTTP_200_OK)

# json of orders
class OrderCreateListView(generics.GenericAPIView):
    
    permission_classes = [IsAuthenticatedOrReadOnly, AllowAny]

    
    serializer_class = serializers.OrderCreationSerializer
    queryset = Order.objects.all()

    def get(self, request):
        paginator = PageNumberPagination()
        query_set = Order.objects.all()
        context = paginator.paginate_queryset(query_set, request)
        serializer = self.serializer_class(context, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)


        if serializer.is_valid():
            serializer.save(customer = request.user)
            return Response(data = serializer.data, status= status.HTTP_200_OK)
        
        return Response(data = serializer.errors, status = status.HTTP_400_BAD_REQUEST)
   

class OrderDetailView(generics.GenericAPIView):

    serializer_class = serializers.OrderDetailSerializer
    permission_classes = [IsAdminUser]
    
    def get(self, request, order_id):
        order = get_object_or_404(Order, pk = order_id)
        serializer = self.serializer_class(instance=order)

        return Response(data = serializer.data, status = status.HTTP_200_OK)

    #update orders
    def put(self, request, order_id):
        
        data = request.data
        
        order =get_object_or_404(Order, pk = order_id)
        serializer = self.serializer_class(data=data, instance=order)

        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        
        return Response(data=serializer.data, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, order_id):
        order =get_object_or_404(Order, pk = order_id)
        order.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)


class UpdateOrderStatus(generics.GenericAPIView):
    serializer_class= serializers.OrderStatusUpdateSerializer

    
    def put(self, request, order_id):
        order =get_object_or_404(Order, pk = order_id)

        data=request.data
        serializer = self.serializer_class(data=data, instance=order)

        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        
        return Response(data=serializer.data, status=status.HTTP_400_BAD_REQUEST)
    

class UserOrdersView(generics.GenericAPIView):
    serializer_class = serializers.OrderDetailSerializer

    def get(self,request,user_id):
        user=User.objects.get(pk=user_id)

        orders=Order.objects.all().filter(customer=user)

        serializer=self.serializer_class(instance=orders,many=True)

        return Response(data=serializer.data,status=status.HTTP_200_OK)


class UserOrderDetailView(generics.GenericAPIView):
    serializer_class=serializers.OrderDetailSerializer
    def get(self,request,user_id,order_id):
        
        user=User.objects.get(pk=user_id)
        order=Order.objects.all().filter(customer=user).get(pk=order_id)
        serializer=self.serializer_class(instance=order)
        return Response(data=serializer.data,status=status.HTTP_200_OK)
