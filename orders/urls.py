from django.urls import path
from . import views

urlpatterns = [
    
     path('', views.OrderCreateListView.as_view(), name='orders'),
    path('<int:order_id>/', views.OrderDetailView.as_view(), name ='order_detail'),
    path('update-status/<int:order_id>/', views.UpdateOrderStatus.as_view(), name ='order_status_update'),
    path('user/<int:user_id>/orders/', views.UserOrdersView.as_view(), name ='user_orders_detail'),
    path('user/<int:user_id>/order/<int:order_id>/', views.UserOrderDetailView.as_view(), name = 'specific_user_detail'),    
]

