from django.urls import path

from orders import views

app_name = 'orders'


urlpatterns = [
    path('', views.orders_list, name='list'),
    path('create/', views.create_order, name='create'),
    path('<int:order_id>/update_status/', views.update_order_status,
         name='update_status'),
    path('<int:order_id>/delete/', views.delete_order, name='delete'),
    path('sales_revenues', views.sales_revenues, name='sales_revenues')
]
